# Task 4 - statistical comparison of the APE, ERA and CRISP predictions.
#
# Reads the per-question metric file produced by Task_3/prism_metric.py
# (running it first if it is missing), then writes tables to results/ and
# figures to figures/. Requires numpy, scipy and matplotlib.
#
#   python analysis.py

import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

TASK_DIR = Path(__file__).resolve().parent
TASK3_DIR = TASK_DIR.parent / "Task_3"
PER_QUESTION_PATH = TASK3_DIR / "results" / "prism_per_question.csv"
RESULTS_DIR = TASK_DIR / "results"
FIGURES_DIR = TASK_DIR / "figures"

PROMPTS = ["APE", "ERA", "CRISP"]
METRICS = ["exact_match", "prism", "row_f1"]
METRIC_LABELS = {"exact_match": "Exact-match accuracy", "prism": "PRISM", "row_f1": "Row F1"}
CATEGORIES = ["best-of", "city-level", "street-level", "region-level", "name-lookup", "off-topic"]
NOISE_LEVELS = ["none", "light", "heavy"]
BOOTSTRAP_SAMPLES = 10_000
RNG = np.random.default_rng(20261017)

# Validated categorical slots 1-3 of the reference palette (all-pairs safe).
COLORS = {"APE": "#2a78d6", "ERA": "#eb6834", "CRISP": "#1baf7a"}
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"

CORE_PATTERN = re.compile(
    r"(what is the best|what is a restaurant|what are some|give me|where can i|"
    r"where can we|where is|where are some|what is the lifes)[^?]*\?",
    re.IGNORECASE,
)
REGIONS = ("bay area", "sacramento area", "napa valley", "monterey", "lake tahoe",
           "yosemite and mono lake area", "northern california", "los angeles area", "unknown")


# ---------------------------------------------------------------- loading

def load_records():
    if not PER_QUESTION_PATH.exists():
        subprocess.run([sys.executable, str(TASK3_DIR / "prism_metric.py")], check=True)
    with PER_QUESTION_PATH.open(encoding="utf-8", newline="") as source:
        records = list(csv.DictReader(source))
    for record in records:
        for key in ("index", "gold_rows", "predicted_rows", "exact_match", "executable"):
            record[key] = int(record[key])
        for key in ("prism", "row_f1", "col_f1"):
            record[key] = float(record[key])
    return records


TRAILING_DISTRACTOR = re.compile(r",\s*(and I|and whether|while|though)\b.*$", re.IGNORECASE)


def core_question(question):
    match = CORE_PATTERN.search(question)
    core = match.group(0) if match else question
    return TRAILING_DISTRACTOR.sub("?", core)


def question_category(question):
    core = core_question(question).lower()
    if "illusion" in core:
        return "off-topic"
    if re.search(r"\bbest\b", core):
        return "best-of"
    if re.search(r"\bon\b.+\bin\b", core):
        return "street-level"
    if re.search(r"\bin (the )?(" + "|".join(REGIONS) + r")\b", core):
        return "region-level"
    if core.startswith("where is ") and "rating" not in core:
        return "name-lookup"
    return "city-level"


def noise_level(question):
    extra = len(question) - len(core_question(question))
    if extra == 0:
        return "none"
    return "heavy" if extra > 150 else "light"


def score_matrix(records, metric):
    by_question = defaultdict(dict)
    for record in records:
        by_question[record["index"]][record["prompt"]] = record[metric]
    indices = sorted(by_question)
    return np.array([[by_question[i][p] for p in PROMPTS] for i in indices], dtype=float)


# ---------------------------------------------------------------- statistics

def bootstrap_mean_ci(values):
    values = np.asarray(values, dtype=float)
    samples = RNG.integers(0, len(values), size=(BOOTSTRAP_SAMPLES, len(values)))
    means = values[samples].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def permutation_paired_p(differences):
    differences = np.asarray(differences, dtype=float)
    observed = abs(differences.mean())
    signs = RNG.choice([-1.0, 1.0], size=(BOOTSTRAP_SAMPLES, len(differences)))
    permuted = np.abs((signs * differences).mean(axis=1))
    return float((np.sum(permuted >= observed - 1e-12) + 1) / (BOOTSTRAP_SAMPLES + 1))


def holm(p_values):
    order = np.argsort(p_values)
    adjusted = np.empty(len(p_values))
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(p_values) - rank) * p_values[index]))
        adjusted[index] = running
    return adjusted.tolist()


def cochran_q(binary_matrix):
    x = np.asarray(binary_matrix, dtype=float)
    k = x.shape[1]
    column_totals = x.sum(axis=0)
    row_totals = x.sum(axis=1)
    total = x.sum()
    denominator = k * total - np.sum(row_totals ** 2)
    if denominator == 0:
        return 0.0, 1.0
    q = (k - 1) * (k * np.sum(column_totals ** 2) - total ** 2) / denominator
    return float(q), float(stats.chi2.sf(q, k - 1))


def mcnemar_exact(a, b):
    a, b = np.asarray(a, dtype=int), np.asarray(b, dtype=int)
    only_a = int(np.sum((a == 1) & (b == 0)))
    only_b = int(np.sum((a == 0) & (b == 1)))
    if only_a + only_b == 0:
        return only_a, only_b, 1.0
    p = stats.binomtest(only_a, only_a + only_b, 0.5).pvalue
    return only_a, only_b, float(p)


def rank_biserial(differences):
    nonzero = differences[differences != 0]
    if len(nonzero) == 0:
        return 0.0
    ranks = stats.rankdata(np.abs(nonzero))
    positive = ranks[nonzero > 0].sum()
    negative = ranks[nonzero < 0].sum()
    return float((positive - negative) / ranks.sum())


def omnibus_tests(matrix):
    if np.all(matrix == matrix[:, [0]]):
        return {"friedman_chi2": 0.0, "friedman_p": 1.0, "kendall_w": 0.0}
    chi2, p = stats.friedmanchisquare(*matrix.T)
    n, k = matrix.shape
    return {"friedman_chi2": float(chi2), "friedman_p": float(p),
            "kendall_w": float(chi2 / (n * (k - 1)))}


def pairwise_tests(matrix):
    rows = []
    for (i, a), (j, b) in combinations(enumerate(PROMPTS), 2):
        differences = matrix[:, i] - matrix[:, j]
        low, high = bootstrap_mean_ci(differences)
        if np.all(differences == 0):
            wilcoxon_p = 1.0
        else:
            wilcoxon_p = float(stats.wilcoxon(matrix[:, i], matrix[:, j], zero_method="wilcox").pvalue)
        rows.append({
            "pair": f"{a} vs {b}",
            "mean_diff": float(differences.mean()),
            "ci_low": low,
            "ci_high": high,
            "wins": int(np.sum(differences > 0)),
            "losses": int(np.sum(differences < 0)),
            "ties": int(np.sum(differences == 0)),
            "wilcoxon_p": wilcoxon_p,
            "permutation_p": permutation_paired_p(differences),
            "rank_biserial": rank_biserial(differences),
        })
    for key in ("wilcoxon_p", "permutation_p"):
        for row, adjusted in zip(rows, holm([row[key] for row in rows])):
            row[key + "_holm"] = adjusted
    return rows


# ---------------------------------------------------------------- SQL features

def sql_features(sql):
    text = sql.lower()
    return {
        "joins_location": "join location" in text,
        "street_filter": "street_name" in text,
        "street_like": bool(re.search(r"street_name\s+like", text)),
        "joins_geographic": "join geographic" in text,
        "food_filter": "food_type" in text,
        "rating_filter": "rating >" in text,
        "limit_1": "limit 1" in text,
        "polluted_literal": bool(re.search(r"'[^']*\b(for \w+ food|restaurant on|the bay area|"
                                           r"the monterey|some \w+|place)\b[^']*'", text)),
    }


def normalized_sql(sql):
    text = sql.lower().replace("lower(", "(")
    text = re.sub(r"\b(r|l|g)\.", "", text)
    text = re.sub(r"\b(restaurant|location|geographic) (r|l|g)\b", r"\1", text)
    text = re.sub(r", id limit", " limit", text)
    text = re.sub(r"\(([a-z_]+)\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip(" ;")


# ---------------------------------------------------------------- figures

def style_axes(axis):
    axis.set_facecolor(SURFACE)
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axis.spines[side].set_color(GRID)
    axis.tick_params(colors=TEXT_SECONDARY, labelsize=9)
    axis.yaxis.grid(True, color=GRID, linewidth=0.8)
    axis.set_axisbelow(True)


def figure_overall(summary):
    figure, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True, facecolor=SURFACE)
    for axis, metric in zip(axes, METRICS):
        style_axes(axis)
        means = [summary[p][metric]["mean"] for p in PROMPTS]
        errors = [[m - summary[p][metric]["ci_low"] for p, m in zip(PROMPTS, means)],
                  [summary[p][metric]["ci_high"] - m for p, m in zip(PROMPTS, means)]]
        axis.bar(PROMPTS, means, width=0.6, color=[COLORS[p] for p in PROMPTS],
                 edgecolor=SURFACE, linewidth=2)
        axis.errorbar(PROMPTS, means, yerr=errors, fmt="none", ecolor=TEXT_SECONDARY,
                      elinewidth=1.2, capsize=4)
        for x, mean, high in zip(range(3), means, errors[1]):
            axis.text(x, mean + high + 0.02, f"{mean:.3f}", ha="center", va="bottom",
                      fontsize=9, color=TEXT_PRIMARY)
        axis.set_title(METRIC_LABELS[metric], fontsize=11, color=TEXT_PRIMARY, loc="left")
        axis.set_ylim(0, 1.12)
    axes[0].set_ylabel("Mean over 155 questions (95% bootstrap CI)", color=TEXT_SECONDARY, fontsize=9)
    figure.suptitle("Exact match ties all prompts; PRISM and Row F1 separate them",
                    x=0.01, ha="left", fontsize=12, color=TEXT_PRIMARY)
    figure.tight_layout()
    figure.savefig(FIGURES_DIR / "fig1_overall_metrics.png", dpi=160, facecolor=SURFACE)
    plt.close(figure)


def grouped_bars(table, groups, title, filename, ylabel, counts):
    figure, axis = plt.subplots(figsize=(11, 4), facecolor=SURFACE)
    style_axes(axis)
    width = 0.26
    x = np.arange(len(groups))
    for offset, prompt in zip((-width, 0, width), PROMPTS):
        values = [table[group][prompt] for group in groups]
        axis.bar(x + offset, values, width=width - 0.02, color=COLORS[prompt], label=prompt,
                 edgecolor=SURFACE, linewidth=2)
        for position, value in zip(x + offset, values):
            axis.text(position, value + 0.015, f"{value:.2f}", ha="center", va="bottom",
                      fontsize=7.5, color=TEXT_SECONDARY)
    axis.set_xticks(x, [f"{group}\n(n={counts[group]})" for group in groups])
    axis.set_ylim(0, 1.12)
    axis.set_ylabel(ylabel, color=TEXT_SECONDARY, fontsize=9)
    axis.set_title(title, fontsize=12, color=TEXT_PRIMARY, loc="left", pad=22)
    legend = axis.legend(frameon=False, ncol=3, loc="lower right", bbox_to_anchor=(1.0, 1.0),
                         fontsize=9, borderaxespad=0.2)
    for text in legend.get_texts():
        text.set_color(TEXT_PRIMARY)
    figure.tight_layout()
    figure.savefig(FIGURES_DIR / filename, dpi=160, facecolor=SURFACE)
    plt.close(figure)


def figure_heatmap(records, categories):
    matrix = score_matrix(records, "row_f1")
    order = sorted(range(len(matrix)), key=lambda i: (CATEGORIES.index(categories[i]), i))
    ordered = matrix[order].T
    colormap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "blue_seq", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
    figure, axis = plt.subplots(figsize=(12, 3.0), facecolor=SURFACE)
    image = axis.imshow(ordered, aspect="auto", cmap=colormap, vmin=0, vmax=1,
                        interpolation="nearest")
    axis.set_yticks(range(3), PROMPTS)
    boundaries, position, narrow = [], 0, 0
    for category in CATEGORIES:
        size = sum(1 for c in categories if c == category)
        if size:
            # Narrow groups get staggered labels so they do not collide.
            offset = 0.0
            if size < 10:
                offset, narrow = 0.38 * narrow, narrow + 1
            axis.text(position + size / 2 - 0.5, 2.62 + offset, f"{category} ({size})",
                      ha="center", va="top", fontsize=8, color=TEXT_SECONDARY)
            position += size
            boundaries.append(position - 0.5)
    for boundary in boundaries[:-1]:
        axis.axvline(boundary, color=SURFACE, linewidth=2)
    axis.set_xticks([])
    axis.tick_params(colors=TEXT_PRIMARY, labelsize=9, length=0)
    for spine in axis.spines.values():
        spine.set_visible(False)
    bar = figure.colorbar(image, ax=axis, fraction=0.02, pad=0.01)
    bar.ax.tick_params(labelsize=8, colors=TEXT_SECONDARY)
    bar.outline.set_visible(False)
    bar.set_label("Row F1", fontsize=8, color=TEXT_SECONDARY)
    axis.set_title("Per-question Row F1, grouped by question category", fontsize=12,
                   color=TEXT_PRIMARY, loc="left", pad=10)
    figure.tight_layout()
    figure.savefig(FIGURES_DIR / "fig4_per_question_heatmap.png", dpi=160, facecolor=SURFACE)
    plt.close(figure)


# ---------------------------------------------------------------- main

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)
    records = load_records()
    by_prompt = defaultdict(list)
    for record in records:
        by_prompt[record["prompt"]].append(record)
    questions = [r["question"] for r in sorted(by_prompt["APE"], key=lambda r: r["index"])]
    categories = [question_category(q) for q in questions]
    noise = [noise_level(q) for q in questions]
    nonempty_gold = np.array([r["gold_rows"] > 0 for r in sorted(by_prompt["APE"], key=lambda r: r["index"])])
    category_counts = Counter(categories)
    noise_counts = Counter(noise)

    output = {"n_questions": len(questions), "category_counts": dict(category_counts),
              "noise_counts": dict(noise_counts)}

    # Overall means with bootstrap CIs.
    summary = {}
    for prompt in PROMPTS:
        summary[prompt] = {}
        for metric in METRICS + ["col_f1"]:
            values = [r[metric] for r in sorted(by_prompt[prompt], key=lambda r: r["index"])]
            low, high = bootstrap_mean_ci(values)
            summary[prompt][metric] = {"mean": float(np.mean(values)), "ci_low": low, "ci_high": high}
            subset = np.asarray(values)[nonempty_gold]
            summary[prompt][metric]["mean_nonempty_gold"] = float(subset.mean())
        summary[prompt]["outcomes"] = dict(Counter(r["outcome"] for r in by_prompt[prompt]))
        summary[prompt]["full_answer_rate"] = float(np.mean(
            [r["row_f1"] == 1.0 for r in by_prompt[prompt]]))
    output["summary"] = summary

    # Significance tests.
    tests = {}
    exact = score_matrix(records, "exact_match").astype(int)
    full_answer = (score_matrix(records, "row_f1") == 1.0).astype(int)
    tests["exact_match"] = {"cochran_q": cochran_q(exact)}
    tests["full_answer"] = {"cochran_q": cochran_q(full_answer), "mcnemar": []}
    mcnemar_rows = []
    for (i, a), (j, b) in combinations(enumerate(PROMPTS), 2):
        only_a, only_b, p = mcnemar_exact(full_answer[:, i], full_answer[:, j])
        mcnemar_rows.append({"pair": f"{a} vs {b}", "only_first": only_a, "only_second": only_b, "p": p})
    for row, adjusted in zip(mcnemar_rows, holm([row["p"] for row in mcnemar_rows])):
        row["p_holm"] = adjusted
    tests["full_answer"]["mcnemar"] = mcnemar_rows
    for metric in ("prism", "row_f1"):
        matrix = score_matrix(records, metric)
        tests[metric] = {"all_questions": {**omnibus_tests(matrix), "pairwise": pairwise_tests(matrix)},
                         "nonempty_gold": {**omnibus_tests(matrix[nonempty_gold]),
                                           "pairwise": pairwise_tests(matrix[nonempty_gold])}}
    output["tests"] = tests

    # Breakdown by category and noise level.
    row_f1 = score_matrix(records, "row_f1")
    prism = score_matrix(records, "prism")
    by_category = {c: {p: float(row_f1[[k for k, x in enumerate(categories) if x == c], j].mean())
                       for j, p in enumerate(PROMPTS)} for c in CATEGORIES}
    by_noise = {n: {p: float(row_f1[[k for k, x in enumerate(noise) if x == n], j].mean())
                    for j, p in enumerate(PROMPTS)} for n in NOISE_LEVELS}
    prism_by_category = {c: {p: float(prism[[k for k, x in enumerate(categories) if x == c], j].mean())
                             for j, p in enumerate(PROMPTS)} for c in CATEGORIES}
    output["row_f1_by_category"] = by_category
    output["prism_by_category"] = prism_by_category
    output["row_f1_by_noise"] = by_noise
    output["row_f1_friedman_by_category"] = {
        c: omnibus_tests(row_f1[[k for k, x in enumerate(categories) if x == c]])
        for c in CATEGORIES if category_counts[c] >= 10
    }

    # Noise robustness: Kruskal-Wallis of Row F1 across noise levels, per prompt.
    output["noise_kruskal"] = {}
    for j, prompt in enumerate(PROMPTS):
        groups = [row_f1[[k for k, x in enumerate(noise) if x == n], j] for n in NOISE_LEVELS]
        statistic, p = stats.kruskal(*groups)
        output["noise_kruskal"][prompt] = {"H": float(statistic), "p": float(p)}

    # SQL feature adoption and cross-prompt SQL agreement.
    features = {}
    for prompt in PROMPTS:
        rows = sorted(by_prompt[prompt], key=lambda r: r["index"])
        street_rows = [r for r, c in zip(rows, categories) if c == "street-level"]
        region_rows = [r for r, c in zip(rows, categories) if c == "region-level"]
        features[prompt] = {
            "street_questions_with_street_filter": sum(sql_features(r["sql_query"])["street_filter"] for r in street_rows),
            "street_questions_using_like": sum(sql_features(r["sql_query"])["street_like"] for r in street_rows),
            "street_questions": len(street_rows),
            "region_questions_joining_geographic": sum(sql_features(r["sql_query"])["joins_geographic"] for r in region_rows),
            "region_questions": len(region_rows),
            "queries_with_polluted_literal": sum(sql_features(r["sql_query"])["polluted_literal"] for r in rows),
        }
    output["sql_features"] = features
    normalized = {p: [normalized_sql(r["sql_query"]) for r in sorted(by_prompt[p], key=lambda r: r["index"])]
                  for p in PROMPTS}
    output["identical_sql"] = {f"{a} vs {b}": sum(x == y for x, y in zip(normalized[a], normalized[b]))
                               for a, b in combinations(PROMPTS, 2)}

    # Per-question category file for inspection.
    with (RESULTS_DIR / "question_categories.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(["index", "category", "noise", "gold_rows", *[f"row_f1_{p}" for p in PROMPTS],
                         *[f"prism_{p}" for p in PROMPTS], "core_question"])
        for k, question in enumerate(questions):
            writer.writerow([k, categories[k], noise[k], int(nonempty_gold[k]),
                             *row_f1[k].tolist(), *prism[k].tolist(), core_question(question)])

    (RESULTS_DIR / "analysis_results.json").write_text(json.dumps(output, indent=2) + "\n")

    figure_overall(summary)
    grouped_bars(by_category, CATEGORIES, "Row F1 by question category", "fig2_row_f1_by_category.png",
                 "Mean Row F1", category_counts)
    grouped_bars(by_noise, NOISE_LEVELS, "Row F1 by amount of distractor text in the question",
                 "fig3_row_f1_by_noise.png", "Mean Row F1", noise_counts)
    figure_heatmap(records, categories)

    print(json.dumps({k: output[k] for k in ("category_counts", "noise_counts", "sql_features",
                                             "identical_sql", "noise_kruskal")}, indent=1))
    for prompt in PROMPTS:
        print(prompt, {m: round(summary[prompt][m]["mean"], 4) for m in METRICS + ["col_f1"]},
              "full_answer", round(summary[prompt]["full_answer_rate"], 4))


if __name__ == "__main__":
    main()
