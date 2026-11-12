"""RAG pipeline: task -> top-5 chunks -> LLM -> method written into the target file -> unit tests.

Usage:
    python rag_solve.py                      # solve all missing_code.json tasks with DEFAULT_MODEL, run tests
    python rag_solve.py --model gpt-5-mini   # another allowed model
    python rag_solve.py --reset              # only restore the original stub files and exit

Every run starts from the pristine stub files (copied once to ./originals/), so runs are repeatable.
Each run writes runs/<model>/: prompt + raw response per task, results.json and the unittest log.

Pipeline per task (solve_task):
  1. retrieve : Task 4 Retriever, top 5 chunks for the task text (Task 3 embeddings)
  2. prompt   : task + the 5 chunks + the target stub and the target file's imports
  3. LLM      : OpenAI chat completion with one of the allowed models
  4. write    : the generated method replaces the stub (located with `ast`, decorators kept)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import textwrap
import time
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
ASSIGNMENTS = HERE.parent
REPO = ASSIGNMENTS / "Task_1" / "AI4SE_Playground" / "playground"  # files in missing_code.json are relative to its parent
REPO_ROOT = REPO.parent
ORIGINALS = HERE / "originals"
sys.path.insert(0, str(ASSIGNMENTS / "Task_4"))
from retrieve import Retriever, task_query  # noqa: E402

ALLOWED_MODELS = ["gpt-6-luna", "gpt-5.6-luna", "gpt-5.4-nano", "gpt-5-nano", "gpt-5-mini", "gpt-4.1-nano", "gpt-4o-mini"]
DEFAULT_MODEL = "gpt-6-luna"
TOP_N = 5
MAX_ATTEMPTS = 2  # one retry if the answer contains no usable method

SYSTEM = (
    "You are a senior Python developer completing a missing method in an existing repository. "
    "Follow the conventions of the surrounding code exactly (validation style, exception types, "
    "helpers, return types). Answer with one ```python code block containing only the complete "
    "method definition: no class, no imports, no decorators, no explanations."
)


# ---------------------------------------------------------------- locating code
def _find_method(tree: ast.AST, cls: str | None, method: str) -> ast.FunctionDef | None:
    """The `def method` inside `class cls` (or anywhere, when cls is None)."""
    for node in ast.walk(tree):
        if cls is not None and not (isinstance(node, ast.ClassDef) and node.name == cls):
            continue
        body = node.body if cls is not None else [node]
        for item in body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method:
                return item
    return None


def _stub_context(path: Path, cls: str, method: str) -> tuple[str, str]:
    """(current stub source incl. decorators, the file's import lines)."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    node = _find_method(tree, cls, method)
    if node is None:
        raise LookupError(f"{cls}.{method} not found in {path}")
    lines = src.splitlines()
    first = min([d.lineno for d in node.decorator_list] + [node.lineno])
    stub = textwrap.dedent("\n".join(lines[first - 1:node.end_lineno]))
    imports = "\n".join(ast.get_source_segment(src, n) for n in tree.body
                        if isinstance(n, (ast.Import, ast.ImportFrom)))
    return stub, imports


# ---------------------------------------------------------------- prompt / LLM
def build_prompt(task_text: str, task: dict, hits, stub: str, imports: str) -> str:
    chunks = "\n\n".join(
        f"### Chunk {i} (similarity {h.score:.3f}): {h.chunk['file']} "
        f"lines {h.chunk['start_line']}-{h.chunk['end_line']}, {h.chunk['kind']}\n"
        f"```python\n{h.chunk['code']}\n```"
        for i, h in enumerate(hits, 1))
    return f"""## Task
{task_text}

## Target
File `{task['file']}`, class `{task['class']}`, method `{task['method']}`. The method currently is a stub:
```python
{stub}
```
Names imported in that file:
```python
{imports}
```

## Relevant code from the repository (retrieved)
{chunks}

## Instructions
Write the complete implementation of `{task['class']}.{task['method']}`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block."""


def call_llm(prompt: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model, messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}])
    return resp.choices[0].message.content or ""


def extract_method(answer: str, method: str) -> str:
    """Pull `def method` (without decorators, dedented) out of the LLM answer."""
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", answer, re.S) or [answer]
    for block in blocks:
        block = textwrap.dedent(block)
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        node = _find_method(tree, None, method)
        if node is not None:
            lines = block.splitlines()[node.lineno - 1:node.end_lineno]
            return textwrap.dedent("\n".join(lines))
    raise ValueError(f"no parsable `def {method}` in the answer")


# ---------------------------------------------------------------- writing
def write_method(path: Path, cls: str, method: str, code: str) -> None:
    """Replace the `def` ... end of `cls.method` with `code` (decorators in the file are kept)."""
    src = path.read_text(encoding="utf-8")
    node = _find_method(ast.parse(src), cls, method)
    if node is None:
        raise LookupError(f"{cls}.{method} not found in {path}")
    lines = src.splitlines(keepends=True)
    indent = " " * node.col_offset
    new = textwrap.indent(code.rstrip() + "\n", indent, lambda l: l.strip() != "")
    candidate = "".join(lines[:node.lineno - 1]) + new + "".join(lines[node.end_lineno:])
    ast.parse(candidate)  # never write a file that does not parse
    path.write_text(candidate, encoding="utf-8")


# ---------------------------------------------------------------- the pipeline function
def solve_task(task_text: str, task: dict, model: str = DEFAULT_MODEL, *,
               retriever: Retriever | None = None, log_dir: Path | None = None) -> str:
    """Solve one textual task: retrieve top 5 chunks, prompt the LLM, write the method. Returns the code."""
    retriever = retriever or Retriever()
    path = REPO_ROOT / task["file"]
    hits = retriever.search_text(task_text, TOP_N)
    stub, imports = _stub_context(path, task["class"], task["method"])
    prompt = build_prompt(task_text, task, hits, stub, imports)

    error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        answer = call_llm(prompt if error is None else
                          f"{prompt}\n\nYour previous answer was unusable ({error}). Try again.", model)
        if log_dir:
            name = f"{task['class']}.{task['method']}"
            (log_dir / f"{name}.prompt.md").write_text(prompt, encoding="utf-8")
            (log_dir / f"{name}.response{'' if attempt == 1 else attempt}.md").write_text(answer, encoding="utf-8")
        try:
            code = extract_method(answer, task["method"])
            write_method(path, task["class"], task["method"], code)
            return code
        except (ValueError, SyntaxError) as e:
            error = str(e)
    raise RuntimeError(f"{task['class']}.{task['method']}: {error}")


# ---------------------------------------------------------------- tests / bookkeeping
def run_tests() -> dict:
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                          cwd=REPO, capture_output=True, text=True)
    out = proc.stderr + proc.stdout
    ran = int(re.search(r"Ran (\d+) test", out).group(1))
    fails = int(m.group(1)) if (m := re.search(r"failures=(\d+)", out)) else 0
    errors = int(m.group(1)) if (m := re.search(r"errors=(\d+)", out)) else 0
    broken = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\S+ \(\S+\))", out, re.M)))
    return {"ran": ran, "failures": fails, "errors": errors, "passed": ran - fails - errors,
            "broken": broken, "log": out}


def target_files(tasks: list[dict]) -> list[Path]:
    return sorted({REPO_ROOT / t["file"] for t in tasks})


def snapshot_originals(tasks: list[dict]) -> None:
    for p in target_files(tasks):
        dst = ORIGINALS / p.relative_to(REPO_ROOT)
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)


def restore_originals(tasks: list[dict]) -> None:
    for p in target_files(tasks):
        shutil.copy2(ORIGINALS / p.relative_to(REPO_ROOT), p)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=ALLOWED_MODELS)
    ap.add_argument("--reset", action="store_true", help="restore the original stubs and exit")
    args = ap.parse_args()

    tasks = json.loads((ASSIGNMENTS / "missing_code.json").read_text())
    snapshot_originals(tasks)
    restore_originals(tasks)
    if args.reset:
        print("Original stubs restored.")
        return

    load_dotenv(HERE / ".env")
    load_dotenv(ASSIGNMENTS / "Task_3" / ".env")
    log_dir = HERE / "runs" / args.model
    log_dir.mkdir(parents=True, exist_ok=True)

    baseline = run_tests()
    print(f"Baseline (stubs): {baseline['passed']}/{baseline['ran']} passed")

    retriever = Retriever()
    results, generated = [], {}
    for t in tasks:
        name = f"{t['class']}.{t['method']}"
        start = time.time()
        try:
            generated[name] = solve_task(task_query(t), t, args.model, retriever=retriever, log_dir=log_dir)
            status = "written"
        except Exception as e:  # keep going; the stub stays and its tests fail
            status = f"error: {e}"
        results.append({"task": name, "file": t["file"], "status": status, "seconds": round(time.time() - start, 1)})
        print(f"  {name:<32} {status} ({results[-1]['seconds']}s)")

    # per-task effect: each generated method alone on top of the pristine stubs
    for r, t in zip(results, tasks):
        if r["task"] in generated:
            restore_originals(tasks)
            write_method(REPO_ROOT / t["file"], t["class"], t["method"], generated[r["task"]])
            alone = run_tests()
            r["fixed_alone"] = len(set(baseline["broken"]) - set(alone["broken"]))
            r["newly_broken_alone"] = sorted(set(alone["broken"]) - set(baseline["broken"]))

    # final state: all generated methods in place
    restore_originals(tasks)
    for t in tasks:
        name = f"{t['class']}.{t['method']}"
        if name in generated:
            write_method(REPO_ROOT / t["file"], t["class"], t["method"], generated[name])
    final = run_tests()
    (log_dir / "unittest.log").write_text(final["log"], encoding="utf-8")
    summary = {
        "model": args.model, "top_n": TOP_N,
        "baseline": {k: v for k, v in baseline.items() if k != "log"},
        "final": {k: v for k, v in final.items() if k != "log"},
        "tasks": results,
    }
    (log_dir / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nFinal: {final['passed']}/{final['ran']} passed "
          f"({final['failures']} failures, {final['errors']} errors); was {baseline['passed']}/{baseline['ran']}")
    for b in final["broken"]:
        print(f"  still broken: {b}")


if __name__ == "__main__":
    main()
