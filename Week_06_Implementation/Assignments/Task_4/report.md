# Task 4 – Matching Report

## Output
| File | What it is |
|---|---|
| [retrieve.py](retrieve.py) | `Retriever.search(query_vec, n)` returns the *n* most relevant chunks for a task embedding |
| [report.md](report.md) | This report |

```bash
python retrieve.py "Implement Order.__len__ in orders.py" -n 5   # top-5 for a free-text task
python retrieve.py --eval -n 5                                   # all missing_code.json tasks + MRR / Hit@5
```

Task 5 uses `Retriever().search_text(task_query(task), n)`. That call embeds the task with the same model and prefix as the store (`embed.py` from Task 3) and returns `Hit(score, chunk)` objects, best first.

## Design decisions
- **Similarity: cosine.** The model was trained for cosine similarity. Both the store rows and the query are normalised to length 1, so cosine is just a dot product. The query is normalised again inside `search`, so a vector from elsewhere still works. A query with the wrong number of dimensions (from a different model) raises an error instead of returning silent garbage.
- **Search: exact brute force.** `matrix @ query` scores all 368 chunks at once in well under a millisecond. `np.argpartition` then picks the top *n* in O(N), and only those *n* get sorted. An approximate index (FAISS, HNSW, a vector database) only pays off at about 10⁵ or more vectors. Here it would add dependencies and could miss the true best match.
- **Filters, all optional:**
  - `include_tests=False` keeps only source code examples.
  - `min_score` drops weak matches, so fewer than *n* chunks can come back.
  - `exclude_ids` skips chunks that are already in the prompt.

  Filtered chunks get a score of −∞, so they can never reach the top *n*.
- **Query format:** `"Implement <Class>.<method> in <file>: <docstring>"`, the best format in the Task 3 benchmark. The identifiers matter because the stub chunks contain no docstring.
- **Not done: re-ranking or diversity (MMR).** The top 5 are already almost all from the target class and its neighbours, which is the context the LLM needs. An extra re-ranking step wouldn't pay for its complexity at this size.

## Result on `missing_code.json` (n = 5)
The exact stub of the missing method is ranked first in 8 of 10 tasks and third in the other 2 (`Order.__len__` loses to `OrderBuilder.__len__` and `OrderLog.__len__`, and `BulkDiscountPricing.price` to two other methods of the same class). That gives **MRR 0.867** and **Hit@5 10/10**, the same as the Task 3 benchmark, which confirms that the matching step adds no error of its own.
