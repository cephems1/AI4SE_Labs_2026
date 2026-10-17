# APE, ERA, and CRISP metric comparison

The three SQL prediction files were evaluated with
`data/evaluate_retrieval_predictions.py`. Each file was converted temporarily
from `natural_text,sql_query` to the evaluator's expected
`question,predicted_sql` format. The labels and SQLite database were unchanged.

## Measured results

| Prompting method | Correct predictions | Total predictions | Accuracy |
|---|---:|---:|---:|
| APE | 43 | 155 | 27.74% |
| ERA | 43 | 155 | 27.74% |
| CRISP | 43 | 155 | 27.74% |

## Short comparison

- **APE** generally produces direct SQL conditions using the city and food type
  extracted from the question. Its first examples use the expected filters and
  order by rating.
- **ERA** shows a parsing problem in the inspected examples: values such as
  `"winters for tea food"` are assigned to `CITY_NAME`, while `"place"` is
  assigned to `FOOD_TYPE`. This leads to empty or incorrect result sets.
- **CRISP** produces SQL that is structurally similar to APE in the inspected
  examples, including the expected city and food-type filters.
- Despite these SQL-style differences, the evaluator reports identical
  execution accuracy for all three methods: **43/155 (27.74%)**. Therefore,
  this run does not show a metric advantage for one prompting method.

The evaluator measures only exact equality between the predicted and expected
SQLite result multisets. It does not report inference time, SQL string
similarity, or partial credit; no inference-time measurements are included in
the prediction CSV files.

