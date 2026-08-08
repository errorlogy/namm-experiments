"""Baseline comparison and correlation helpers."""

from __future__ import annotations

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.schemas.experiment import BaselineComparison, BaselineResults, NoveltyLevel

KNOWN_BASELINE_EXPRESSIONS: dict[str, str] = {
    "wiener_index": "1*wiener_index",
    "degree_sum": "2*num_edges",
    "avg_degree": "1*avg_degree",
    "clustering": "1*clustering",
    "algebraic_connectivity": "1*algebraic_connectivity",
    "wiener_plus_edges": "1*wiener_index + 1*num_edges",
    "wiener_plus_clustering": "1*wiener_index + 1*clustering",
    "2x_wiener": "2*wiener_index",
    "diameter": "1*diameter",
    "radius": "1*radius",
}


def pearson_correlation(values_a: list[float], values_b: list[float]) -> float:
    """Pearson r between two equal-length value vectors."""
    n = len(values_a)
    if n == 0 or n != len(values_b):
        return 0.0
    mean_a = sum(values_a) / n
    mean_b = sum(values_b) / n
    cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(values_a, values_b)) / n
    std_a = (sum((a - mean_a) ** 2 for a in values_a) / n) ** 0.5
    std_b = (sum((b - mean_b) ** 2 for b in values_b) / n) ** 0.5
    if std_a <= 0 or std_b <= 0:
        return 0.0
    return cov / (std_a * std_b)


def compare_to_baselines(
    expression: str,
    graphs: list[nx.Graph],
) -> BaselineResults:
    """Compare candidate to known baselines: equivalence and Pearson r."""
    cand_vals = [evaluate_formula(expression, g) for g in graphs]
    comparisons: list[BaselineComparison] = []
    max_r = 0.0
    correlated_baseline: str | None = None

    for baseline_id, baseline_expr in KNOWN_BASELINE_EXPRESSIONS.items():
        equivalent = formulas_agree_on_graphs(expression, baseline_expr, graphs)
        base_vals = [evaluate_formula(baseline_expr, g) for g in graphs]
        r = pearson_correlation(cand_vals, base_vals)
        comparisons.append(
            BaselineComparison(
                baseline_id=baseline_id,
                expression=baseline_expr,
                equivalent=equivalent,
                pearson_r=round(r, 6),
            )
        )
        if abs(r) > abs(max_r):
            max_r = r
            correlated_baseline = baseline_id

    return BaselineResults(
        comparisons=comparisons,
        max_correlation=round(max_r, 6),
        correlated_baseline=correlated_baseline,
        rejected_for_correlation=False,
    )


def assess_novelty_level(
    baseline_results: BaselineResults,
    simplifies_to_known: bool,
    correlation_threshold: float = 0.95,
) -> NoveltyLevel:
    """Assign N0–N5 from baseline and simplify checks."""
    if any(c.equivalent for c in baseline_results.comparisons):
        return NoveltyLevel.N0
    if simplifies_to_known:
        return NoveltyLevel.N1
    max_r = abs(baseline_results.max_correlation or 0.0)
    if max_r > correlation_threshold:
        return NoveltyLevel.N2
    return NoveltyLevel.N2
