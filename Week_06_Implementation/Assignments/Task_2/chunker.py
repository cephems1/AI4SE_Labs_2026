"""Split the AI4SE_Playground repository into structure-aware chunks.

Usage:
    python chunker.py [REPO_ROOT] [OUTPUT_JSON]

Defaults: REPO_ROOT = ../Task_1/AI4SE_Playground, OUTPUT_JSON = ./chunks.json

Chunking strategy (see report.md):
  * one chunk per function / method (decorators included),
  * one "class" chunk per class: signature, docstring, class attributes and
    the signatures of its methods (a skeleton giving class-level context),
  * one "module" chunk per file: module docstring, imports, top-level code,
  * test methods of a TestCase are packed into "test_group" chunks (<= MAX_LINES),
  * functions longer than MAX_LINES are split into overlapping line windows.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

MAX_LINES = 60      # functions longer than this are split into windows
WINDOW_OVERLAP = 10  # lines shared by neighbouring windows

HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parent / "Task_1" / "AI4SE_Playground"
DEFAULT_OUT = HERE / "chunks.json"


def _start_line(node: ast.AST) -> int:
    """First line of a definition, including its decorators."""
    decos = getattr(node, "decorator_list", [])
    return min([d.lineno for d in decos] + [node.lineno])


def _is_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True when the body is only an optional docstring plus ``pass`` / ``...``.

    Abstract methods are intentionally empty, so they are not counted as stubs.
    """
    if any((isinstance(d, ast.Name) and d.id == "abstractmethod")
           or (isinstance(d, ast.Attribute) and d.attr == "abstractmethod")
           for d in node.decorator_list):
        return False
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    return all(
        isinstance(s, ast.Pass)
        or (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis)
        for s in body
    )


def _signature(lines: list[str], node: ast.AST) -> str:
    """Source of a def/class header up to (and including) the line ending with ':'."""
    first = node.lineno - 1
    body_start = node.body[0].lineno - 1
    header = lines[first:max(body_start, first + 1)]
    # trim anything after the colon line (e.g. a docstring that starts on the same line)
    out = []
    for ln in header:
        out.append(ln)
        if ln.rstrip().endswith(":"):
            break
    return "\n".join(out)


def _header(rel: str, cls: str | None, name: str | None, kind: str) -> str:
    """Context line prepended to every chunk so it is self-describing for embeddings."""
    parts = [f"# File: {rel}", f"Kind: {kind}"]
    if cls:
        parts.append(f"Class: {cls}")
    if name:
        parts.append(f"Name: {name}")
    return " | ".join(parts)


class Chunker:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.chunks: list[dict] = []

    def add(self, rel, kind, cls, name, start, end, code, is_test, is_stub=False):
        text = _header(rel, cls, name, kind) + "\n" + code
        self.chunks.append({
            "id": f"{rel}::{cls + '.' if cls else ''}{name or kind}::{start}",
            "file": rel,
            "kind": kind,            # module | class | function | method | test_group
            "class": cls,
            "name": name,
            "start_line": start,
            "end_line": end,
            "is_test": is_test,
            "is_stub": is_stub,      # unimplemented method (body is only `pass`)
            "n_lines": code.count("\n") + 1,  # lines actually in the chunk
            "n_tokens_est": len(text) // 4,    # rough token estimate (~4 chars/token)
            "text": text,            # header + code -> what gets embedded
            "code": code,            # raw source
        })

    def add_function(self, rel, lines, node, cls, is_test):
        kind = "method" if cls else "function"
        start, end = _start_line(node), node.end_lineno
        stub = _is_stub(node)
        if end - start + 1 <= MAX_LINES:
            self.add(rel, kind, cls, node.name, start, end,
                     "\n".join(lines[start - 1:end]), is_test, stub)
            return
        # long function: overlapping windows, each repeating the signature for context
        sig = _signature(lines, node)
        step = MAX_LINES - WINDOW_OVERLAP
        for i, ws in enumerate(range(start, end + 1, step)):
            we = min(ws + MAX_LINES - 1, end)
            body = "\n".join(lines[ws - 1:we])
            code = body if i == 0 else f"{sig}\n    # ... (part {i + 1}, lines {ws}-{we})\n{body}"
            self.add(rel, kind, cls, f"{node.name}[part{i + 1}]", ws, we, code, is_test, stub)
            if we == end:
                break

    def add_class(self, rel, lines, node, is_test):
        # skeleton: header + docstring + class attributes + method signatures
        start = _start_line(node)
        skeleton = [lines[i] for i in range(start - 1, node.lineno - 1)]  # decorators
        skeleton.append(_signature(lines, node))
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                skeleton.extend(lines[i] for i in range(_start_line(stmt) - 1, stmt.lineno - 1))
                skeleton.append(_signature(lines, stmt) + " ...")
            elif isinstance(stmt, ast.ClassDef):
                skeleton.append(_signature(lines, stmt) + " ...")
            else:  # docstring, attributes, enum members
                skeleton.extend(lines[stmt.lineno - 1:stmt.end_lineno])
        self.add(rel, "class", node.name, node.name, start, node.end_lineno,
                 "\n".join(skeleton), is_test)

        if is_test:
            self.add_test_methods(rel, lines, node)
            return
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.add_function(rel, lines, stmt, node.name, is_test)
            elif isinstance(stmt, ast.ClassDef):
                self.add_class(rel, lines, stmt, is_test)

    def add_test_methods(self, rel, lines, node):
        """Pack consecutive test methods of one TestCase into chunks of <= MAX_LINES.

        Individual test methods are only 3-10 lines; one chunk each would flood the
        index with tiny, near-identical chunks. Packing them (split only at method
        boundaries) keeps each chunk a coherent "spec" of the behaviour under test.
        """
        methods = [s for s in node.body if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))]
        group: list[ast.AST] = []

        def flush():
            if not group:
                return
            start, end = _start_line(group[0]), group[-1].end_lineno
            names = ",".join(m.name for m in group)
            code = "\n".join(lines[start - 1:end])
            self.add(rel, "test_group", node.name, names, start, end, code, True)
            group.clear()

        for m in methods:
            if m.end_lineno - _start_line(m) + 1 > MAX_LINES:  # single huge test
                flush()
                self.add_function(rel, lines, m, node.name, True)
                continue
            if group and m.end_lineno - _start_line(group[0]) + 1 > MAX_LINES:
                flush()
            group.append(m)
        flush()

    def chunk_file(self, path: Path):
        rel = path.relative_to(self.repo_root).as_posix()
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        tree = ast.parse(source, filename=rel)
        is_test = "/tests/" in f"/{rel}" or path.name.startswith("test_")

        module_parts = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.add_function(rel, lines, node, None, is_test)
            elif isinstance(node, ast.ClassDef):
                self.add_class(rel, lines, node, is_test)
            else:
                module_parts.append("\n".join(lines[_start_line(node) - 1:node.end_lineno]))
        if module_parts:
            code = "\n".join(module_parts)
            self.add(rel, "module", None, None, 1, len(lines), code, is_test)

    def run(self) -> list[dict]:
        for path in sorted(self.repo_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            self.chunk_file(path)
        return self.chunks


def main() -> None:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_REPO
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else DEFAULT_OUT
    chunks = Chunker(repo).run()
    out.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    by_kind: dict[str, int] = {}
    for c in chunks:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    sizes = sorted(c["n_lines"] for c in chunks)
    print(f"Wrote {len(chunks)} chunks to {out}")
    print(f"  by kind: {by_kind}")
    print(f"  source/test: {sum(not c['is_test'] for c in chunks)}/{sum(c['is_test'] for c in chunks)}")
    print(f"  stubs (missing methods): {sum(c['is_stub'] for c in chunks)}")
    print(f"  lines per chunk: min={sizes[0]} median={sizes[len(sizes) // 2]} max={sizes[-1]}")


if __name__ == "__main__":
    main()
