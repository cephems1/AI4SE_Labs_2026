"""Benchmark candidate embedding models on the real retrieval problem of this lab.

Usage:
    python benchmark_models.py [MODEL_KEY ...]     # default: every model in embed.MODELS

Test set : the 10 tasks of missing_code.json (the exact queries Task 5 will run).
Corpus   : the 368 chunks from Task 2.
Queries  : two variants per task
             full  = "Implement <Class>.<method> in <file>: <docstring>"   (what Task 5 can send)
             doc   = "<docstring>" only                                   (harder: no identifiers)
Relevance:
  * target    = the stub chunk of the missing method itself (exactly 1 per task)
  * relevant  = any chunk of the target class in the target file, or a test chunk whose
                TestCase name contains the target class name (its specification)
Metrics (averaged over the 10 tasks):
  MRR      mean reciprocal rank of the target chunk
  Hit@1/5  target chunk ranked 1st / in the top 5
  P@5      share of the top-5 chunks that are relevant (how useful the LLM context will be)
Results are written to benchmark_results.json and benchmark_results.md.
"""

from __future__ import annotations

import json
import sys
import time

import numpy as np

import embed

TOP_K = 5


def queries_for(tasks: list[dict]) -> dict[str, list[str]]:
    return {
        "full": [f"Implement {t['class']}.{t['method']} in {t['file']}: {t['docstring'].strip()}" for t in tasks],
        "doc": [t["docstring"].strip().strip('"').strip() for t in tasks],
    }


def is_relevant(chunk: dict, task: dict) -> bool:
    if chunk["file"] == task["file"] and chunk["class"] == task["class"]:
        return True
    return bool(chunk["is_test"] and chunk["class"] and task["class"] in chunk["class"])


def evaluate(matrix: np.ndarray, qvecs: np.ndarray, chunks: list[dict], tasks: list[dict]) -> dict:
    rr, hit1, hit5, p5, per_task = [], [], [], [], []
    for t, q in zip(tasks, qvecs):
        order = np.argsort(matrix @ q)[::-1]
        target = next(i for i, c in enumerate(chunks)
                      if c["class"] == t["class"] and c["name"] == t["method"] and c["file"] == t["file"])
        rank = int(np.where(order == target)[0][0]) + 1
        top = order[:TOP_K]
        prec = sum(is_relevant(chunks[i], t) for i in top) / TOP_K
        rr.append(1 / rank); hit1.append(rank == 1); hit5.append(rank <= TOP_K); p5.append(prec)
        per_task.append({"task": f"{t['class']}.{t['method']}", "target_rank": rank, "p@5": prec})
    return {"MRR": float(np.mean(rr)), "Hit@1": float(np.mean(hit1)), "Hit@5": float(np.mean(hit5)),
            "P@5": float(np.mean(p5)), "per_task": per_task}


def main() -> None:
    keys = sys.argv[1:] or list(embed.MODELS)
    chunks = json.loads(embed.CHUNKS_IN.read_text(encoding="utf-8"))
    tasks = json.loads((embed.ASSIGNMENTS / "missing_code.json").read_text())
    texts = [c["text"] for c in chunks]
    qsets = queries_for(tasks)

    results = {}
    for key in keys:
        spec = embed.MODELS[key]
        print(f"\n=== {key}  ({spec['name']})")
        embed.get_model.cache_clear()
        t0 = time.perf_counter()
        model = embed.get_model(key)
        t_load = time.perf_counter() - t0
        t0 = time.perf_counter()
        matrix = embed.embed_texts(texts, key)
        t_embed = time.perf_counter() - t0
        res = {"model": spec["name"], "dims": int(matrix.shape[1]),
               "params_M": round(sum(p.numel() for p in model.parameters()) / 1e6),
               "max_tokens": model.max_seq_length, "truncated": embed.count_truncated(texts, key),
               "load_s": round(t_load, 1), "embed_s": round(t_embed, 1)}
        for variant, qs in qsets.items():
            res[variant] = evaluate(matrix, embed.embed_queries(qs, key), chunks, tasks)
            r = res[variant]
            print(f"  {variant:4s}  MRR={r['MRR']:.3f}  Hit@1={r['Hit@1']:.1f}  Hit@5={r['Hit@5']:.1f}  P@5={r['P@5']:.2f}")
        print(f"  dims={res['dims']}  params={res['params_M']}M  embed={res['embed_s']}s  truncated={res['truncated']}")
        results[key] = res

    out_json = embed.HERE / "benchmark_results.json"
    if out_json.exists():  # merge with earlier runs so models can be benchmarked separately
        results = {**json.loads(out_json.read_text()), **results}
    out_json.write_text(json.dumps(results, indent=2))

    lines = ["| Model | Dims | Params | Embed time | Truncated | MRR full | Hit@1 full | Hit@5 full | P@5 full "
             "| MRR doc | Hit@1 doc | Hit@5 doc | P@5 doc |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for key, r in sorted(results.items(), key=lambda kv: -(kv[1]["full"]["MRR"] + kv[1]["doc"]["MRR"])):
        f, d = r["full"], r["doc"]
        lines.append(f"| `{key}` | {r['dims']} | {r['params_M']}M | {r['embed_s']}s | {r['truncated']} "
                     f"| {f['MRR']:.3f} | {f['Hit@1']:.0%} | {f['Hit@5']:.0%} | {f['P@5']:.2f} "
                     f"| {d['MRR']:.3f} | {d['Hit@1']:.0%} | {d['Hit@5']:.0%} | {d['P@5']:.2f} |")
    (embed.HERE / "benchmark_results.md").write_text("\n".join(lines) + "\n")
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()
