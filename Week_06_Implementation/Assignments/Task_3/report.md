# Task 3 – Embeddings & Storage Report

## Output
| File | What it is |
|---|---|
| [embed.py](embed.py) | Turns a chunk (or a query) into an embedding; builds and loads the store |
| [benchmark_models.py](benchmark_models.py) | Benchmark used to choose the embedding model |
| [benchmark_results.md](benchmark_results.md) / [.json](benchmark_results.json) | Benchmark results (with per-task ranks in the JSON) |
| [store/embeddings.npy](store/embeddings.npy) | `float32` matrix `[368 × 1024]`, L2-normalised; row *i* holds the embedding of chunk *i* |
| [store/chunks.json](store/chunks.json) | The Task 2 chunks plus a `row` index (metadata + full code) |
| [store/meta.json](store/meta.json) | Model, number of dimensions, query/document prefixes, truncation stats and a hash of every embedded text |
| [requirements.txt](requirements.txt) | `numpy`, `sentence-transformers` |

```bash
pip install -r requirements.txt
python embed.py            # build the store (first run downloads the model, ~670 MB)
python embed.py --check    # show the top-5 chunks for each missing_code.json task
python benchmark_models.py # re-run the model comparison
```

Other code can reuse `embed_query(text)`, `embed_chunk(chunk)` and `load_store()` from `embed.py`.

## 1. Embedding mechanism: local `mixedbread-ai/mxbai-embed-large-v1` (1024 dimensions)

### Why a local model
The original plan was the OpenAI `text-embedding-3-small` API. It didn't work for a reason the code can't fix. The available key is a service account key (`sk-svcacct-…`), and its project only allows 7 chat models (`gpt-4o-mini`, `gpt-5-mini`, …). Every `/embeddings` call is refused with `403 model_not_found`. A local `sentence-transformers` model avoids this, and it also:
- is free and works offline, with nothing sent to a third party,
- gives the same vector for the same input every time.

### Which models could be considered
I only considered standard BERT-style checkpoints that load without `trust_remote_code`, meaning no Python code downloaded from the model's repository is executed. That is a sensible security rule, and the agent's safety check also enforced it. It excludes code-specific models such as `jina-embeddings-v2-base-code` and `nomic-embed-code`. I tested 7 well-known retrieval models, each with the query/document prefixes its model card prescribes (see `MODELS` in `embed.py`).

### How the model was chosen: benchmark on the real tasks
I didn't pick a model from public leaderboards. `benchmark_models.py` measures each candidate on this lab's own retrieval problem:
- **Test set:** the 10 tasks in `missing_code.json`. The corpus is the 368 Task 2 chunks.
- **Two kinds of query:**
  - `full` = `"Implement <Class>.<method> in <file>: <docstring>"`, the query Task 5 will send.
  - `doc` = the docstring only, a harder query with no identifiers.
- **Metrics** (averaged over the 10 tasks):
  - *MRR* and *Hit@1/@5*: the rank of the exact stub chunk of the missing method (MRR is the average of 1/rank).
  - *P@5*: the share of the top 5 that belong to the target class or its tests, i.e. how useful the context the LLM gets will be.

| Model | Dims | Params | Embed 368 chunks | MRR full | Hit@1 full | Hit@5 full | P@5 full | MRR doc | Hit@5 doc |
|---|---|---|---|---|---|---|---|---|---|
| **`mxbai-embed-large-v1`** | 1024 | 335M | 75 s | **0.867** | **80%** | **100%** | 0.78 | **0.245** | 30% |
| `bge-large-en-v1.5` | 1024 | 335M | 216 s | 0.795 | 70% | 100% | 0.80 | 0.214 | 30% |
| `all-MiniLM-L6-v2` | 384 | 23M | 3 s | 0.650 | 40% | 90% | 0.82 | 0.095 | 20% |
| `e5-base-v2` | 768 | 109M | 63 s | 0.617 | 40% | 90% | 0.80 | 0.082 | 20% |
| `bge-small-en-v1.5` | 384 | 33M | 6 s | 0.529 | 30% | 80% | 0.80 | 0.074 | 10% |
| `bge-base-en-v1.5` | 768 | 109M | 19 s | 0.512 | 20% | 90% | 0.80 | 0.107 | 20% |
| `snowflake-arctic-embed-m-v1.5` | 768 | 109M | 34 s | 0.402 | 10% | 80% | 0.76 | 0.061 | 10% |

**Verdict:** `mxbai-embed-large-v1` ranks the exact missing method first in 8 of 10 tasks, and third in the other two (`Order.__len__` and `BulkDiscountPricing.price`). It is the best model on both kinds of query.
- **Cost:** it is the largest model tested (335M parameters, 1024 dimensions), but it embeds the whole repo in about 75 s, a one-off cost because the store is cached. A query takes milliseconds.
- **Context quality:** P@5 is similar for all models (about 0.8), so they all return useful context. The difference is in getting the exact method to the top.

### Findings that shape Task 5
- **Always put the class and method name in the query.** With the docstring alone, every model fails (Hit@5 is 30% at best). The stub chunks contain only the signature and `pass`, with no docstring, so the identifiers are the only words the query and the target have in common.
- **"Wrong" results are still useful.** The lower P@5 scores (for example 0.4 for `OrderStatus.is_terminal`) come from chunks of related classes, such as `OrderStateMachine`, which uses the order statuses. They count as irrelevant under the strict metric, but they are good context for the LLM.

## 2. What is embedded: the chunk's `text` (context header + source code)
- The code already carries the meaning: method names, signatures and type hints, docstrings and exception names.
- **The header** (`# File: … | Kind: … | Class: … | Name: …`) adds where the code lives. That's essential for stubs and tiny methods: `def __len__(self) -> int: pass` only becomes findable as `Order.__len__` in `orders.py` because of the header.
- **Queries get the model's retrieval instruction** ("Represent this sentence for searching relevant passages: "). Chunks are embedded without it, as the model card prescribes.
- **512-token limit:** the model reads at most 512 tokens per input. All source chunks fit. 36 test chunks (packed test groups) are cut off at the end. Their header and first tests are still embedded, and `code` in the store keeps the full text for the prompt.
- **Rejected alternatives:**
  - LLM-written summaries of each chunk: 368 extra LLM calls, and the benchmark shows that header + code already finds the target.
  - Embedding only the signature and docstring: this loses the implementation, which is exactly what the LLM needs to see as examples.

## 3. Storage and retrieval: NumPy matrix + JSON metadata
- **Layout:** `embeddings.npy` holds a `[368 × 1024]` `float32` matrix, and `chunks.json` holds the chunks in the same order. Row *i* belongs to `chunks[i]`, and `load_store()` checks that the two match. The store is 2.1 MB in total.
- **Retrieval:** vectors are normalised to length 1, so cosine similarity is just a dot product. `matrix @ query` scores all 368 chunks in well under a millisecond and returns exact results.
- **Why not a vector database:** Chroma, FAISS and similar only pay off at about 10⁵ vectors or more. Here they would add installs and opaque binary files, and their approximate search would make results slightly worse.
- **No needless re-embedding:** `meta.json` records the model, prefixes, dimensions, truncation stats and a SHA-256 hash of each embedded text. `embed.py` skips the model entirely if nothing has changed, and changing the chunks or the model triggers a rebuild automatically.
