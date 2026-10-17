# Task 3 – A new metric: PRISM

**PRISM = Projection-Robust Intersection Set Match**, a partial-credit,
column-order-agnostic execution metric for NL→SQL.

Files:

| File | Purpose |
|---|---|
| [`prism_metric.py`](prism_metric.py) | Metric implementation + evaluation of the three Task 2 prediction files |
| [`test_prism_metric.py`](test_prism_metric.py) | Unit tests of the metric's edge cases (`python -m unittest test_prism_metric.py`) |
| [`results/prism_per_question.csv`](results/prism_per_question.csv) | Per-question scores for every prompt (465 rows) |
| [`results/prism_summary.json`](results/prism_summary.json) | Aggregated scores per prompt |

Run with `python prism_metric.py` (standard library only; it reuses the
database loader from `Task_2/data/evaluate_retrieval_predictions.py`, so both
metrics run on exactly the same SQLite database).

---

## 1. Why a new metric is needed: the original metric is degenerate on this data

The original metric is **execution accuracy (EX)**: a prediction counts as
correct only if the multiset of rows it returns equals the gold multiset exactly.
In Task 2 all three prompts scored exactly **43 / 155 = 27.74 %**. Looking
closer shows that this tie is not a coincidence:

* Every gold result in `restaurants_dataset.csv` has the shape
  `[HOUSE_NUMBER, NAME]` (e.g. `[3, "portola park"]`, `[-1, "vivace"]`). This
  is a convention inherited from the original Restaurants text-to-SQL
  benchmark.
* All 465 predicted queries (3 prompts × 155) select `ID, NAME` instead,
  which is the natural reading of "give me a restaurant".
* An `ID` never equals a `HOUSE_NUMBER`, so **no question with a non-empty
  answer can ever be counted as correct**. The only possible hits are the
  **43 questions whose gold answer is empty**, and all three prompts got
  exactly those 43 right.

EX therefore only measures "did the query return nothing when it should?" and
cannot tell apart a query that returned the right restaurant from one that
returned 900 wrong ones. For example, for *"give me a restaurant on timber
creek dr in san jose with a rating above 1.7"*:

| Prompt | Rows returned | Contains the right restaurant? | EX |
|---|---:|---|---:|
| APE | 1 | yes, only that one | 0 |
| ERA | 922 (every restaurant in San Jose) | buried among 921 others | 0 |
| CRISP | 1 | yes, only that one | 0 |

A useful metric must rank APE and CRISP well above ERA here.

## 2. Definition

For each question let **G** be the set of gold rows (with *k_G* columns) and
**P** the set of rows returned by the predicted SQL (with *k_P* columns).

1. **Edge cases.** If G and P are both empty the score is 1. If exactly one
   of them is empty the score is 0. A query that fails to execute also
   scores 0.
2. **Column alignment by content.** Consider every partial one-to-one mapping
   *m* from gold columns to predicted columns of the same value type (number
   or text). Column names and order are ignored: a column is matched by what
   it contains.
3. **Two factors per alignment:**
   * **RowF1(m)**: the F1 score between the gold rows and the predicted rows
     after both are projected onto the aligned columns. Rows are compared as
     sets, with strings case-folded and trimmed and numbers compared by value.
   * **ColF1(m) = 2·|m| / (k_G + k_P)**: an F1 over columns. It penalises
     missing gold columns (low recall) as well as padding the SELECT list
     (low precision).
4. **Score:**

   **PRISM(q) = max over m of ColF1(m) · RowF1(m)**

   The dataset score is the mean over all questions. The implementation also
   reports both factors of the winning alignment, plus an outcome label for
   each question: `exact`, `right_rows_wrong_columns`, `partial_overlap`,
   `disjoint`, `missed_rows`, `spurious_rows` or `error`.

Worked example: gold `[(3, "portola park")]`, prediction `[(1457, "portola park")]`.
* The best alignment maps gold `NAME` to predicted `NAME`, so |m| = 1.
* RowF1 = 1 (the right restaurant was found).
* ColF1 = 2·1 / (2 + 2) = 0.5 (the house number is missing).
* PRISM = 0.5.

## 3. Why PRISM is a good, applicable metric (defence)

| Property | Why it matters for this task |
|---|---|
| **Strict generalisation of EX** | EX = 1 ⇒ PRISM = 1, so a perfect query keeps full credit. PRISM only adds information where EX is silent. |
| **Robust to projection differences** | Selecting `ID, NAME` instead of `HOUSE_NUMBER, NAME`, or swapping column order, is a far smaller error than choosing the wrong restaurants. PRISM gives partial credit through ColF1 instead of zeroing the question. |
| **Partial credit for rows** | It distinguishes "1 correct row" from "the correct row plus 921 wrong ones" (precision) and from "1 of the 2 tied best restaurants" (recall, e.g. `LIMIT 1` versus a `MAX()` subquery with ties). |
| **Hard to game** | `SELECT *` gets full column recall but its ColF1 drops (2·2/(2+5) = 0.57). Returning the whole table drives row precision towards 0. Returning nothing scores 0 unless the gold is genuinely empty. |
| **Still execution-based** | It judges *what the query returns*, not how it is written. Semantically equivalent SQL (`LIKE` vs `=`, `JOIN` vs a sub-query, `LOWER()`) is not penalised, unlike string or BLEU-style SQL similarity. |
| **Interpretable decomposition** | ColF1 answers "did it ask for the right attributes?" and RowF1 answers "did it find the right entities?". The outcome labels show *why* a question failed. |
| **Cheap and dependency-free** | It needs only the gold result sets that already exist. No gold SQL, LLM judge or extra annotation is required, and at most 2 × 5 columns are aligned, so the search is tiny. |

**Originality.** Partial-match ideas exist (Spider's component matching needs
gold SQL; "soft" execution accuracy ignores column order). PRISM combines
*content-based column alignment* with *row-level F1* and a *column F1 penalty*,
then optimises the alignment jointly. That makes it usable on a benchmark that
ships only result sets and whose output schema the model cannot know.

**Limitations (stated honestly).**
* Rows are compared as sets, so duplicate counts are ignored. That is
  intentional, because duplicates here mostly come from join fan-out in the
  gold queries, but a strict metric would keep them.
* Matching on the name column alone can give credit when two different
  restaurants share a name (e.g. many "denny's restaurant"). PRISM therefore
  slightly overestimates retrieval quality when the gold key column is
  missing from the prediction.
* Like EX, PRISM inherits quirks of the gold labels. For example, the
  off-topic question *"What is the lifes greates illusion?"* has 2,696 gold
  rows, which no sensible query will return.

## 4. Complement or replacement?

**PRISM complements EX; it does not replace it.**

* EX remains the correct **strict acceptance test**: a query that will be
  executed in a product must return exactly the expected rows and columns.
* PRISM is the **diagnostic and ranking metric**: it tells which prompt got
  *closer*, and its factors explain the failure. Here EX gives zero signal,
  because all three prompts tie, while PRISM separates them clearly.
* Recommended reporting: **EX together with PRISM, and PRISM's RowF1 and
  ColF1 factors.** A large gap between PRISM and EX, as in this experiment,
  is itself a finding: it points to a systematic projection mismatch rather
  than wrong retrieval.

## 5. Results on the Task 2 predictions

| Prompt | EX (original) | **PRISM** | RowF1 | ColF1 | PRISM, non-empty gold only (n = 112) | Questions with fully correct rows (RowF1 = 1) |
|---|---:|---:|---:|---:|---:|---:|
| **APE** | 0.277 | **0.624** | **0.971** | 0.632 | **0.480** | **143 / 155 (92.3 %)** |
| ERA | 0.277 | 0.509 | 0.740 | 0.600 | 0.320 | 106 / 155 (68.4 %) |
| CRISP | 0.277 | 0.557 | 0.836 | 0.561 | 0.387 | 123 / 155 (79.4 %) |

Outcome breakdown (counts out of 155):

| Outcome | APE | ERA | CRISP |
|---|---:|---:|---:|
| `exact` (empty gold and empty prediction) | 43 | 43 | 43 |
| `right_rows_wrong_columns` (right restaurants, `ID` instead of `HOUSE_NUMBER`) | **100** | 63 | 80 |
| `partial_overlap` (some right rows mixed with wrong ones, or too few) | 10 | **37** | 8 |
| `missed_rows` (returned nothing, gold non-empty) | 2 | 11 | **22** |
| `disjoint` (returned rows, none right) | 0 | 1 | 2 |
| `spurious_rows` (returned rows, gold empty) | 0 | 0 | 0 |

### Interpretation

* **Ranking: APE > CRISP > ERA.** EX could not detect this ordering.
  Task 4 tests whether it is statistically significant.
* **The ceiling is set by the projection, not by retrieval.** All prompts
  select `ID, NAME`, so on every non-empty question ColF1 is 0.5 and PRISM is
  at most 0.5. APE's non-empty PRISM of 0.480 means it found the right
  restaurants almost every time (RowF1 = 0.959 on those questions). It only
  lacked the `HOUSE_NUMBER` column the benchmark expects.
* **ERA's characteristic error is over-retrieval.** It has 37
  `partial_overlap` cases, where it dropped the street or food-type
  constraint and returned every restaurant in the city.
* **CRISP's characteristic error is under-retrieval.** It has 22
  `missed_rows` cases, where text such as "for pizza food" leaked into the
  city literal (`CITY_NAME = 'hayward for pizza food'`), so the query matched
  nothing.
* No prompt ever invented rows for a question whose answer is empty
  (`spurious_rows` = 0). All three correctly treat impossible requests as
  empty.

Task 4 ([`../Task_4/report.md`](../Task_4/report.md)) analyses these
differences in depth, with figures, significance tests and causes.
