# Task 2 – Chunking Report

## Output
| File | What it is |
|---|---|
| [chunker.py](chunker.py) | Chunking script: `python chunker.py [REPO_ROOT] [OUTPUT_JSON]` |
| [chunks.json](chunks.json) | List of 368 chunks (JSON) from `Task_1/AI4SE_Playground` |

Each chunk is a flat dict with these fields: `id`, `file`, `kind`, `class`, `name`, `start_line`, `end_line`, `is_test`, `is_stub`, `n_lines`, `n_tokens_est`, `text` (header + code, the part that gets embedded) and `code` (the raw source).

## Splitting method: by code structure, using Python's `ast`
The repo is pure Python, so I used the parser instead of fixed-size text windows. Fixed windows cut functions in half. The coding tasks (`missing_code.json`) are asked per method, so a whole function is the natural unit to retrieve.

| Kind | Content | Count |
|---|---|---|
| `method` / `function` | One complete function, including its decorators | 161 |
| `class` | Class skeleton: signature, docstring, attributes or enum members, and method signatures | 99 |
| `module` | Module docstring, imports and top-level code | 26 |
| `test_group` | Consecutive test methods of one `TestCase`, packed up to the size limit | 82 |

- **Context header:** each chunk's `text` starts with a line like `# File: … | Kind: … | Class: … | Name: …`. Even a 3-line method then shows where it lives, which helps both the embedding and the LLM.
- **Class skeletons:** these give the LLM the "shape" of the class (fields and sibling methods) without the full source.
- **Tests are included but packed:** tests show the expected behaviour of the missing methods. Individual test methods are tiny, though, and one chunk each would make 75% of the index tests (597 of 798 chunks), crowding source code out of the top-5 results. Packing them per test class brings tests down to 167 of 368 chunks.
- **Stubs are flagged:** `is_stub` marks the unimplemented methods (body is only `pass`). Abstract methods are excluded. It flags exactly the 10 methods listed in `missing_code.json`.

## Chunk size: 60 lines maximum
- **Size of the code:** functions in this repo are short. The median method is 4 lines (about 65 tokens), and the longest source function, `Simulation.step`, is 55 lines. A 60-line limit keeps every source function whole.
- **Budget:** chunks are at most about 770 tokens, so the top-5 chunks in Task 5 come to roughly 4k tokens or less. That leaves plenty of room for the task and the answer.
- **Fallback for longer functions:** any function longer than 60 lines would be split into overlapping windows (10 lines overlap), each repeating the function signature. No function in this repo needs it.
- **No minimum size:** small chunks aren't merged, because one method per chunk keeps retrieval exact. The header and the class skeleton add the missing context instead.
