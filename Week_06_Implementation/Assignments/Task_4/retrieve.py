"""Match a task embedding against the Task 3 store and return the n most relevant chunks.

Usage:
    python retrieve.py "Implement Order.__len__ in orders.py" [-n 5] [--no-tests]
    python retrieve.py --eval [-n 5]      # top-n for every missing_code.json task + MRR / Hit@n

Library use (Task 5):
    from retrieve import Retriever
    r = Retriever()                       # loads the store once
    hits = r.search(query_vec, n=5)       # core: embedding in -> [Hit(score, chunk), ...]
    hits = r.search_text("Implement ...") # convenience: embeds the text first (embed.py)

Matching: cosine similarity. Store rows and the query are L2-normalised, so cosine = dot product,
          computed for all chunks in one matrix-vector product (exact, brute force).
Top-n   : np.argpartition (O(N)) and then a sort of only the n winners.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ASSIGNMENTS = HERE.parent
sys.path.insert(0, str(ASSIGNMENTS / "Task_3"))
from embed import embed_queries, embed_query, load_store  # noqa: E402


@dataclass
class Hit:
    score: float  # cosine similarity in [-1, 1]
    chunk: dict   # the chunk from the store (metadata + `code`)


def task_query(task: dict) -> str:
    """The query format the Task 3 benchmark found best: identifiers + docstring."""
    return f"Implement {task['class']}.{task['method']} in {task['file']}: {task['docstring'].strip()}"


class Retriever:
    def __init__(self, store: Path | None = None):
        self.matrix, self.chunks, self.meta = load_store(store) if store else load_store()
        self._is_test = np.array([c["is_test"] for c in self.chunks])

    def search(self, query_vec: np.ndarray, n: int = 5, *, include_tests: bool = True,
               min_score: float | None = None, exclude_ids: set[str] = frozenset()) -> list[Hit]:
        """Return the n chunks most similar to `query_vec`, best first.

        include_tests : False drops test chunks (e.g. when only source examples are wanted)
        min_score     : drop hits below this cosine similarity (may return fewer than n)
        exclude_ids   : chunk ids to skip (e.g. chunks already in the prompt)
        """
        q = np.asarray(query_vec, dtype=np.float32).ravel()
        if q.shape[0] != self.matrix.shape[1]:
            raise ValueError(f"query has {q.shape[0]} dims, store has {self.matrix.shape[1]} "
                             f"({self.meta['model']}); embed the query with the same model")
        norm = np.linalg.norm(q)
        if norm == 0:
            raise ValueError("query vector is all zeros")
        scores = self.matrix @ (q / norm)

        # filters set the score to -inf so they never reach the top n
        mask = np.ones(len(scores), dtype=bool)
        if not include_tests:
            mask &= ~self._is_test
        if exclude_ids:
            mask &= np.array([c["id"] not in exclude_ids for c in self.chunks])
        if min_score is not None:
            mask &= scores >= min_score
        scores = np.where(mask, scores, -np.inf)

        k = min(n, int(mask.sum()))
        if k <= 0:
            return []
        top = np.argpartition(-scores, k - 1)[:k]
        top = top[np.argsort(-scores[top], kind="stable")]
        return [Hit(float(scores[i]), self.chunks[i]) for i in top]

    def search_text(self, query: str, n: int = 5, **kw) -> list[Hit]:
        """Embed `query` with the store's model (query prefix included), then search."""
        return self.search(embed_query(query, self.meta["model_key"]), n, **kw)


def _print_hits(hits: list[Hit], target: dict | None = None) -> None:
    for h in hits:
        c = h.chunk
        star = "*" if target and c["class"] == target["class"] and c["name"] == target["method"] else " "
        print(f"  {star} {h.score:.3f}  {c['kind']:<10} {c['id'][:95]}")


def _eval(r: Retriever, n: int, include_tests: bool) -> None:
    """Top-n for each missing_code.json task; * marks the stub of the missing method."""
    tasks = json.loads((ASSIGNMENTS / "missing_code.json").read_text())
    vecs = embed_queries([task_query(t) for t in tasks], r.meta["model_key"])
    rr, hits_at_n = [], 0
    for t, v in zip(tasks, vecs):
        ranked = r.search(v, len(r.chunks), include_tests=include_tests)
        rank = next(i for i, h in enumerate(ranked, 1)
                    if h.chunk["class"] == t["class"] and h.chunk["name"] == t["method"])
        rr.append(1 / rank)
        hits_at_n += rank <= n
        print(f"\n{t['class']}.{t['method']}  (target rank {rank})")
        _print_hits(ranked[:n], t)
    print(f"\nMRR {np.mean(rr):.3f} | Hit@{n} {hits_at_n}/{len(tasks)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("query", nargs="?", help="free-text task to search for")
    ap.add_argument("-n", type=int, default=5, help="number of chunks to return (default 5)")
    ap.add_argument("--no-tests", action="store_true", help="exclude test chunks")
    ap.add_argument("--min-score", type=float, help="minimum cosine similarity")
    ap.add_argument("--eval", action="store_true", help="run on all missing_code.json tasks")
    args = ap.parse_args()

    r = Retriever()
    if args.eval:
        _eval(r, args.n, not args.no_tests)
    elif args.query:
        _print_hits(r.search_text(args.query, args.n, include_tests=not args.no_tests,
                                  min_score=args.min_score))
    else:
        ap.error("give a query or --eval")


if __name__ == "__main__":
    main()
