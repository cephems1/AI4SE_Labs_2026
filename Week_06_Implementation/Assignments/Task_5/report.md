# Task 5 – RAG Pipeline & Unit Test Report

## Output
| File | What it is |
|---|---|
| [rag_solve.py](rag_solve.py) | The RAG pipeline: `solve_task(task_text, task, model)` plus a runner for all `missing_code.json` tasks and the tests |
| [runs/&lt;model&gt;/](runs/) | For each task, the exact prompt and the LLM's answer, plus `results.json` (summary) and `unittest.log` |
| [originals/](originals/) | Pristine stub files. Every run starts from them, so runs can be repeated |

```bash
python rag_solve.py                      # default model gpt-6-luna
python rag_solve.py --model gpt-5-mini   # any allowed model
python rag_solve.py --reset              # put the stubs back
```

## How it works
For each task, `solve_task` runs four steps:
1. **Retrieve.** It finds the **top 5 chunks** with the Task 4 `Retriever`. The query is `"Implement <Class>.<method> in <file>: <docstring>"`.
2. **Prompt.** It builds a prompt with the task, the 5 chunks (full code with file and line numbers), the current stub (so the LLM sees the exact signature and decorators) and the target file's import lines (so it knows which names exist).
3. **Generate.** It calls the OpenAI chat API.
4. **Write.** It takes the `def` from the answer and replaces the stub, located with Python's `ast` module. The file's decorators stay, and the result must parse before it is written; if it doesn't, the LLM gets one retry.

Finally the script runs `python -m unittest discover` on the repository. For a per-task breakdown it also runs the tests with each generated method applied **alone** to the stubs; the test suite takes 0.03 s, so this costs almost nothing.

## Results
The repository has **481 unit tests**. With the stubs, **429 pass** (35 failures, 17 errors).

**Final run (`gpt-6-luna`): 472 / 481 pass (98.1%).** 7 of the 10 methods are fully correct, and 9 tests still fail:

| Method | Tests fixed when added alone | Result | Why it fails |
|---|---|---|---|
| `OrderStatus.is_terminal` | 4 | ✅ | |
| `Warehouse.stock_report` | 3 | ✅ | |
| `Customer.can_afford` | 6 | ✅ | |
| `Order.__len__` | 7 | ✅ | |
| `BulkDiscountPricing.price` | 9 | ✅ | |
| `EventBus.__contains__` | 2 | ✅ | |
| `Money.__bool__` | 2 | ✅ | |
| `OrderStateMachine.transition` | 10 | ❌ 5 tests | `raise InvalidTransitionError("message")`, but the constructor takes `(source, target)`. `exceptions.py` was not among the top 5 chunks. |
| `InventoryLedger.__contains__` | 1 | ❌ 3 tests | Lets `normalize_sku` raise on bad input instead of returning `False`, and checks `on_hand > 0`, so a SKU that is present with zero stock counts as absent |
| `OrderLog.by_status` | 1 | ❌ 1 test | Doesn't raise `TypeError` for a non-`OrderStatus` argument |

The fixed counts add up to more than 43 (429 → 472) because some tests need two methods. For example, `Order.total` with bulk pricing needs both `__len__` and `price`.

**Other allowed models**, each run once on the same pipeline:

| Model | Passed |
|---|---|
| `gpt-6-luna` | 472 (first run: 464) |
| `gpt-5.6-luna` | 466 |
| `gpt-5-mini` | 466 |
| `gpt-4o-mini` | 462 |

- `gpt-4.1-nano` couldn't be used: the API reports that the model has been deprecated.
- Results vary from run to run. `gpt-6-luna` scored 464 on its first run, when its `price` divided a `Money` by an `int`, which `Money` doesn't support.

## What the failures show
- **Retrieval is the bottleneck, not the LLM.** In every failure the model wrote reasonable code against an API it had never seen: the constructor of an exception from another file, the operators `Money` supports, or the validation convention for `__contains__`. Top-5 similarity search returns the target class's own neighbours (see Task 4), but not the *dependencies* the method calls. Adding the definitions of names used in the target file (`InvalidTransitionError`, `Money`) would most likely fix the remaining failures. That's a structural retrieval change; see Task 6.
- **Silent conventions are the hardest part.** For example, "`__contains__` returns `False` for malformed input" and "`by_status` validates its argument" appear only in the tests. For all three failing tasks, the top 5 held only source chunks from the same file, and no test chunk at all.
