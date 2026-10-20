"""Deterministic corpus handling: discovery, reading, date detection, chunking, quote grounding."""

import email
import re
from datetime import datetime
from difflib import SequenceMatcher
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path

from .config import SUPPORTED_EXTENSIONS

_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
_ISO_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_DATE_HEADER_RE = re.compile(r"^\s*Date:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
_LONG_DATE_RE = re.compile(rf"({_MONTHS})\s+(\d{{1,2}})(?:\s*[-–]\s*(?:(?:{_MONTHS})\s+)?\d{{1,2}})?,\s*(\d{{4}})")


def _read_file(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()
    if suffix == ".eml":
        msg = email.message_from_string(raw, policy=policy.default)
        if msg.is_multipart():
            header = "\n".join(f"{h}: {msg[h]}" for h in ("From", "To", "Subject", "Date") if msg[h])
            bodies = [p.get_content() for p in msg.walk() if p.get_content_type() == "text/plain"]
            return header + "\n\n" + "\n\n".join(bodies)
    if suffix in {".html", ".htm"}:
        raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
        raw = re.sub(r"<[^>]+>", " ", raw)
    return raw


def detect_date(rel_path: str, text: str) -> str:
    """Best-effort document date (ISO) from file name, a Date: header, or the first long-form date."""
    m = _ISO_RE.search(rel_path)
    if m:
        return m.group(0)
    head = text[:3000]
    m = _DATE_HEADER_RE.search(head)
    if m:
        value = m.group(1).strip()
        try:
            return parsedate_to_datetime(value).date().isoformat()
        except (TypeError, ValueError):
            pass
    m = _LONG_DATE_RE.search(head)
    if m:
        try:
            return datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y").date().isoformat()
        except ValueError:
            pass
    return "unknown"


def load_documents(input_dir: str) -> list[dict]:
    root = Path(input_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Input directory not found: {root}")
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS and not p.name.startswith(".")
    )
    docs = []
    for path in files:
        text = _read_file(path).strip()
        if not text:
            continue
        rel = path.relative_to(root).as_posix()
        docs.append({"path": rel, "date": detect_date(rel, text), "chars": len(text), "text": text})
    for i, doc in enumerate(docs, 1):
        doc["doc_id"] = f"D{i:02d}"
    return docs


def _split_long(paragraph: str, max_chars: int) -> list[str]:
    lines, parts, buf = paragraph.splitlines(keepends=True), [], ""
    for line in lines:
        if len(buf) + len(line) > max_chars and buf:
            parts.append(buf)
            buf = ""
        buf += line
    if buf:
        parts.append(buf)
    return parts


def chunk_documents(docs: list[dict], max_chars: int) -> list[dict]:
    """Split documents on paragraph boundaries into chunks of at most ~max_chars characters."""
    chunks = []
    for doc in docs:
        paragraphs = []
        for para in re.split(r"\n\s*\n", doc["text"]):
            paragraphs.extend(_split_long(para, max_chars) if len(para) > max_chars else [para])
        pieces, buf = [], ""
        for para in paragraphs:
            if len(buf) + len(para) + 2 > max_chars and buf:
                pieces.append(buf)
                buf = ""
            buf += para + "\n\n"
        if buf.strip():
            pieces.append(buf)
        for k, piece in enumerate(pieces, 1):
            chunks.append({
                "chunk_id": f"{doc['doc_id']}.k{k}",
                "doc_id": doc["doc_id"],
                "path": doc["path"],
                "date": doc["date"],
                "part": k,
                "parts": len(pieces),
                "text": piece.strip(),
            })
    return chunks


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[\"'`“”‘’]", "", s)).strip().lower()


def is_grounded(quote: str, text: str, threshold: float = 0.8) -> bool:
    """True if the quote occurs (almost) verbatim in the text - guards against hallucinated evidence."""
    q, t = _norm(quote), _norm(text)
    if not q:
        return False
    if q in t:
        return True
    match = SequenceMatcher(None, t, q, autojunk=False).find_longest_match(0, len(t), 0, len(q))
    return match.size >= threshold * len(q)
