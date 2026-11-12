"""Turn the Task 2 chunks into embeddings and store chunk-embedding pairs.

Usage:
    python embed.py                    # embed ../Task_2/chunks.json with DEFAULT_MODEL -> ./store/
    python embed.py --model KEY        # use another model from MODELS (see below)
    python embed.py --check            # also print the top-5 chunks for each missing_code.json task

Embedding : local sentence-transformers model, runs offline (CPU / Apple GPU), no API key.
            The default was chosen by benchmark_models.py (see report.md).
Input     : chunk side -> the chunk's `text` field = context header + source code
            query side -> the task text, with the model's query instruction prefix
Storage   : store/embeddings.npy  float32 matrix [n_chunks x dims], L2-normalised, row i <-> chunks[i]
            store/chunks.json     chunk metadata + code (same order as matrix rows)
            store/meta.json       model, dims, prefixes, truncation stats, hash of every embedded text
"""

from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

# Candidate models. All are plain BERT-style checkpoints that load WITHOUT trust_remote_code
# (no code downloaded from the model repo is executed). Prefixes follow each model card:
# retrieval models are trained with an instruction on the query side (and E5 on both sides).
MODELS: dict[str, dict] = {
    "minilm":     {"name": "sentence-transformers/all-MiniLM-L6-v2", "query": "", "doc": ""},
    "bge-small":  {"name": "BAAI/bge-small-en-v1.5",
                   "query": "Represent this sentence for searching relevant passages: ", "doc": ""},
    "bge-base":   {"name": "BAAI/bge-base-en-v1.5",
                   "query": "Represent this sentence for searching relevant passages: ", "doc": ""},
    "bge-large":  {"name": "BAAI/bge-large-en-v1.5",
                   "query": "Represent this sentence for searching relevant passages: ", "doc": ""},
    "e5-base":    {"name": "intfloat/e5-base-v2", "query": "query: ", "doc": "passage: "},
    "arctic-m":   {"name": "Snowflake/snowflake-arctic-embed-m-v1.5",
                   "query": "Represent this sentence for searching relevant passages: ", "doc": ""},
    "mxbai-large": {"name": "mixedbread-ai/mxbai-embed-large-v1",
                    "query": "Represent this sentence for searching relevant passages: ", "doc": ""},
}
DEFAULT_MODEL = "mxbai-large"  # winner of benchmark_models.py, see report.md
BATCH_SIZE = 16

HERE = Path(__file__).resolve().parent
ASSIGNMENTS = HERE.parent
CHUNKS_IN = ASSIGNMENTS / "Task_2" / "chunks.json"
STORE = HERE / "store"


@lru_cache(maxsize=1)
def get_model(key: str = DEFAULT_MODEL):
    """Load (and cache) a sentence-transformers model by its MODELS key."""
    from sentence_transformers import SentenceTransformer  # heavy import, load lazily
    return SentenceTransformer(MODELS[key]["name"])


def _encode(texts: list[str], key: str) -> np.ndarray:
    vecs = get_model(key).encode(texts, batch_size=BATCH_SIZE, normalize_embeddings=True,
                                 show_progress_bar=len(texts) > 4 * BATCH_SIZE)
    return np.asarray(vecs, dtype=np.float32)


def embed_texts(texts: list[str], key: str = DEFAULT_MODEL) -> np.ndarray:
    """Embed chunk texts (document side) -> L2-normalised float32 matrix [len(texts) x dims]."""
    return _encode([MODELS[key]["doc"] + t for t in texts], key)


def embed_chunk(chunk: dict, key: str = DEFAULT_MODEL) -> np.ndarray:
    """Embed a single chunk (its header + code `text`) -> vector."""
    return embed_texts([chunk["text"]], key)[0]


def embed_queries(queries: list[str], key: str = DEFAULT_MODEL) -> np.ndarray:
    """Embed task/query strings (query side, with the model's instruction prefix)."""
    return _encode([MODELS[key]["query"] + q for q in queries], key)


def embed_query(query: str, key: str = DEFAULT_MODEL) -> np.ndarray:
    """Embed one free-text task into the same vector space as the chunks."""
    return embed_queries([query], key)[0]


def count_truncated(texts: list[str], key: str) -> int:
    """How many texts exceed the model's max input length (their tail is not embedded)."""
    model = get_model(key)
    limit = model.max_seq_length
    return sum(len(model.tokenizer(MODELS[key]["doc"] + t)["input_ids"]) > limit for t in texts)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_store(key: str = DEFAULT_MODEL, chunks_path: Path = CHUNKS_IN, store: Path = STORE) -> None:
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    texts = [c["text"] for c in chunks]
    hashes = [_sha(t) for t in texts]
    spec = MODELS[key]

    # skip re-embedding when the store already matches the current chunks and model
    meta_path = store / "meta.json"
    if meta_path.exists():
        old = json.loads(meta_path.read_text())
        if old.get("model") == spec["name"] and old.get("hashes") == hashes:
            print(f"Store is up to date ({len(chunks)} chunks, {spec['name']}), nothing to embed.")
            return

    print(f"Embedding {len(chunks)} chunks with {spec['name']}...")
    matrix = embed_texts(texts, key)
    truncated = count_truncated(texts, key)

    store.mkdir(exist_ok=True)
    np.save(store / "embeddings.npy", matrix)
    for i, c in enumerate(chunks):
        c["row"] = i
    (store / "chunks.json").write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    meta_path.write_text(json.dumps({
        "model_key": key, "model": spec["name"], "dims": int(matrix.shape[1]), "count": len(chunks),
        "normalised": True, "embedded_field": "text",
        "query_prefix": spec["query"], "doc_prefix": spec["doc"],
        "max_seq_length": get_model(key).max_seq_length, "truncated_chunks": truncated,
        "source": str(chunks_path.relative_to(ASSIGNMENTS)), "hashes": hashes,
    }, indent=2))
    print(f"Saved {matrix.shape} matrix + metadata to {store} "
          f"({truncated} chunks longer than {get_model(key).max_seq_length} tokens)")


def load_store(store: Path = STORE) -> tuple[np.ndarray, list[dict], dict]:
    """Load (embeddings matrix, chunks, meta). Row i of the matrix belongs to chunks[i]."""
    matrix = np.load(store / "embeddings.npy")
    chunks = json.loads((store / "chunks.json").read_text(encoding="utf-8"))
    meta = json.loads((store / "meta.json").read_text())
    assert matrix.shape == (len(chunks), meta["dims"]), "store is inconsistent"
    return matrix, chunks, meta


def _check() -> None:
    """Print the top-5 chunks for every missing_code.json task (stub chunk marked with *)."""
    matrix, chunks, meta = load_store()
    tasks = json.loads((ASSIGNMENTS / "missing_code.json").read_text())
    queries = [f"Implement {t['class']}.{t['method']} in {t['file']}: {t['docstring'].strip()}" for t in tasks]
    for t, q in zip(tasks, embed_queries(queries, meta["model_key"])):
        print(f"\n{t['class']}.{t['method']}")
        for i in np.argsort(matrix @ q)[::-1][:5]:
            c = chunks[i]
            star = "*" if c["class"] == t["class"] and c["name"] == t["method"] else " "
            print(f"  {star} {float(matrix[i] @ q):.3f}  {c['id'][:100]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    build_store(args[args.index("--model") + 1] if "--model" in args else DEFAULT_MODEL)
    if "--check" in args:
        _check()
