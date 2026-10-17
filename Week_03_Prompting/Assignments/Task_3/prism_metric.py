# PRISM - Projection-Robust Intersection Set Match.
#
# A partial-credit, column-order-agnostic execution metric for NL-to-SQL.
# For each question the predicted SQL and the gold result are compared as
# sets of rows after the predicted columns have been aligned to the gold
# columns by their content (not by name or position):
#
#   PRISM(q) = max over column alignments m of  ColF1(m) * RowF1(m)
#
#   ColF1(m) = 2|m| / (k_gold + k_pred)       how well the SELECT list matches
#   RowF1(m) = F1 of the row sets projected   how well the returned rows match
#              onto the aligned columns
#
# Edge cases: both results empty -> 1.0, exactly one empty -> 0.0.
# Exact execution match (the original metric) always implies PRISM = 1.
#
# Usage (from anywhere):
#   python prism_metric.py                    # evaluates the three Task 2 files
#   python prism_metric.py NAME=path.csv ...  # evaluates custom prediction files
# Prediction files use the Task 2 format: natural_text,sql_query

import csv
import itertools
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
TASK2_DATA_DIR = TASK_DIR.parent / "Task_2" / "data"
RESULTS_DIR = TASK_DIR / "results"
LABELS_PATH = TASK2_DATA_DIR / "restaurants_dataset.csv"

DEFAULT_PREDICTIONS = {
    "APE": TASK2_DATA_DIR / "restaurants_nl_sql_APE.csv",
    "ERA": TASK2_DATA_DIR / "restaurants_nl_sql_ERA.csv",
    "CRISP": TASK2_DATA_DIR / "restaurants_queries_CRISP.csv",
}

# Reuse the course evaluator's database loader so both metrics run on the
# exact same SQLite database.
sys.path.insert(0, str(TASK2_DATA_DIR))
from evaluate_retrieval_predictions import load_database, row_multiset  # noqa: E402


def normalize_value(value):
    if isinstance(value, bool):
        return ("num", float(value))
    if isinstance(value, (int, float)):
        return ("num", round(float(value), 6))
    if value is None:
        return ("null", None)
    return ("str", str(value).strip().casefold())


def normalize_rows(rows):
    return [tuple(normalize_value(value) for value in row) for row in rows]


def column_kinds(rows, width):
    kinds = []
    for column in range(width):
        values = {row[column][0] for row in rows if row[column][0] != "null"}
        kinds.append(values.pop() if len(values) == 1 else "mixed")
    return kinds


def set_f1(gold, predicted):
    if not gold and not predicted:
        return 1.0
    overlap = len(gold & predicted)
    if overlap == 0:
        return 0.0
    precision = overlap / len(predicted)
    recall = overlap / len(gold)
    return 2 * precision * recall / (precision + recall)


def candidate_alignments(gold_kinds, predicted_kinds):
    """Yield partial injective maps gold column -> predicted column of the same kind."""
    gold_columns = range(len(gold_kinds))
    for size in range(len(gold_kinds), 0, -1):
        for gold_subset in itertools.combinations(gold_columns, size):
            for predicted_subset in itertools.permutations(
                range(len(predicted_kinds)), size
            ):
                if all(
                    gold_kinds[g] == predicted_kinds[p] or "mixed" in (gold_kinds[g], predicted_kinds[p])
                    for g, p in zip(gold_subset, predicted_subset)
                ):
                    yield tuple(zip(gold_subset, predicted_subset))


def prism_score(gold_rows, predicted_rows, predicted_width):
    """Return a dict with PRISM, its two factors and the chosen alignment."""
    gold = normalize_rows(gold_rows)
    predicted = normalize_rows(predicted_rows)

    if not gold and not predicted:
        return {"prism": 1.0, "row_f1": 1.0, "col_f1": 1.0, "alignment": "empty=empty"}
    if not gold or not predicted:
        return {"prism": 0.0, "row_f1": 0.0, "col_f1": 0.0, "alignment": "empty<>rows"}

    gold_width = len(gold[0])
    gold_kinds = column_kinds(gold, gold_width)
    predicted_kinds = column_kinds(predicted, predicted_width)

    best = {"prism": 0.0, "row_f1": 0.0, "col_f1": 0.0, "alignment": "none"}
    for alignment in candidate_alignments(gold_kinds, predicted_kinds):
        gold_projection = {tuple(row[g] for g, _ in alignment) for row in gold}
        predicted_projection = {tuple(row[p] for _, p in alignment) for row in predicted}
        row_f1 = set_f1(gold_projection, predicted_projection)
        col_f1 = 2 * len(alignment) / (gold_width + predicted_width)
        score = col_f1 * row_f1
        if score > best["prism"]:
            best = {
                "prism": score,
                "row_f1": row_f1,
                "col_f1": col_f1,
                "alignment": ";".join(f"g{g}->p{p}" for g, p in alignment),
            }
    return best


def outcome_label(gold_rows, predicted_rows, exact, row_f1):
    if exact:
        return "exact"
    if not gold_rows:
        return "spurious_rows"  # gold is empty, prediction returned rows
    if not predicted_rows:
        return "missed_rows"  # gold has rows, prediction returned nothing
    if row_f1 == 1.0:
        return "right_rows_wrong_columns"
    if row_f1 > 0:
        return "partial_overlap"
    return "disjoint"


def load_labels():
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        return [(row["question"], json.loads(row["result"])) for row in csv.DictReader(source)]


def evaluate_file(connection, labels, prompt, predictions_path):
    with Path(predictions_path).open(encoding="utf-8", newline="") as source:
        predictions = list(csv.DictReader(source))
    if len(predictions) != len(labels):
        raise ValueError(f"{predictions_path}: {len(predictions)} predictions, {len(labels)} labels")

    records = []
    for index, (prediction, (question, gold_rows)) in enumerate(zip(predictions, labels)):
        if prediction["natural_text"] != question:
            raise ValueError(f"{predictions_path}: question mismatch on row {index + 2}")
        try:
            cursor = connection.execute(prediction["sql_query"])
            predicted_rows = cursor.fetchall()
            predicted_width = len(cursor.description)
            executable = True
        except sqlite3.Error:
            predicted_rows, predicted_width, executable = [], 0, False

        exact = executable and row_multiset(predicted_rows) == row_multiset(gold_rows)
        score = prism_score(gold_rows, predicted_rows, predicted_width) if executable else {
            "prism": 0.0, "row_f1": 0.0, "col_f1": 0.0, "alignment": "error"}
        records.append({
            "prompt": prompt,
            "index": index,
            "question": question,
            "sql_query": prediction["sql_query"],
            "executable": int(executable),
            "gold_rows": len(gold_rows),
            "predicted_rows": len(predicted_rows),
            "exact_match": int(exact),
            "prism": round(score["prism"], 6),
            "row_f1": round(score["row_f1"], 6),
            "col_f1": round(score["col_f1"], 6),
            "alignment": score["alignment"],
            "outcome": "error" if not executable else outcome_label(
                gold_rows, predicted_rows, exact, score["row_f1"]),
        })
    return records


def summarize(records):
    count = len(records)
    outcomes = Counter(record["outcome"] for record in records)
    return {
        "questions": count,
        "exact_match_accuracy": sum(r["exact_match"] for r in records) / count,
        "prism_mean": sum(r["prism"] for r in records) / count,
        "row_f1_mean": sum(r["row_f1"] for r in records) / count,
        "col_f1_mean": sum(r["col_f1"] for r in records) / count,
        "prism_nonempty_gold_mean": (
            sum(r["prism"] for r in records if r["gold_rows"])
            / max(1, sum(1 for r in records if r["gold_rows"]))
        ),
        "row_f1_nonempty_gold_mean": (
            sum(r["row_f1"] for r in records if r["gold_rows"])
            / max(1, sum(1 for r in records if r["gold_rows"]))
        ),
        "outcomes": dict(sorted(outcomes.items())),
    }


def main(argv):
    predictions = DEFAULT_PREDICTIONS
    if argv:
        predictions = dict(argument.split("=", 1) for argument in argv)

    labels = load_labels()
    connection = load_database()
    all_records, summaries = [], {}
    try:
        for prompt, path in predictions.items():
            records = evaluate_file(connection, labels, prompt, path)
            all_records.extend(records)
            summaries[prompt] = summarize(records)
    finally:
        connection.close()

    RESULTS_DIR.mkdir(exist_ok=True)
    with (RESULTS_DIR / "prism_per_question.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(all_records[0]))
        writer.writeheader()
        writer.writerows(all_records)
    (RESULTS_DIR / "prism_summary.json").write_text(json.dumps(summaries, indent=2) + "\n")

    print(f"{'Prompt':<8}{'EX acc':>9}{'PRISM':>9}{'RowF1':>9}{'ColF1':>9}{'PRISM|gold>0':>14}")
    for prompt, summary in summaries.items():
        print(
            f"{prompt:<8}{summary['exact_match_accuracy']:>9.4f}{summary['prism_mean']:>9.4f}"
            f"{summary['row_f1_mean']:>9.4f}{summary['col_f1_mean']:>9.4f}"
            f"{summary['prism_nonempty_gold_mean']:>14.4f}"
        )
    for prompt, summary in summaries.items():
        print(prompt, summary["outcomes"])


if __name__ == "__main__":
    main(sys.argv[1:])
