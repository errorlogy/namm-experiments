"""Pearson correlation independence checks vs baseline set."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from namm.metrics.baselines import KNOWN_BASELINE_EXPRESSIONS, pearson_correlation
from namm.domains.graph.evaluator import evaluate_formula


@dataclass
class IndependenceResult:
    independent: bool
    max_correlation: float
    correlated_baseline: str | None
    correlations: dict[str, float]


def baseline_values_on_graphs(
    graphs: list[nx.Graph],
    baseline_ids: list[str] | None = None,
) -> dict[str, list[float]]:
    """Evaluate known baseline expressions on graphs."""
    ids = baseline_ids or list(KNOWN_BASELINE_EXPRESSIONS.keys())
    out: dict[str, list[float]] = {}
    for bid in ids:
        expr = KNOWN_BASELINE_EXPRESSIONS[bid]
        out[bid] = [evaluate_formula(expr, g) for g in graphs]
    return out


def check_independence(
    candidate_values: list[float],
    baseline_values: dict[str, list[float]],
    threshold: float = 0.95,
) -> IndependenceResult:
    """Reject if Pearson r > threshold vs any baseline."""
    max_r = 0.0
    correlated: str | None = None
    correlations: dict[str, float] = {}

    for bid, bvals in baseline_values.items():
        r = pearson_correlation(candidate_values, bvals)
        correlations[bid] = round(r, 6)
        if abs(r) > abs(max_r):
            max_r = r
            correlated = bid

    return IndependenceResult(
        independent=abs(max_r) <= threshold,
        max_correlation=round(max_r, 6),
        correlated_baseline=correlated,
        correlations=correlations,
    )


def reject_if_correlated(
    candidate_values: list[float],
    graphs: list[nx.Graph],
    threshold: float = 0.95,
    baseline_ids: list[str] | None = None,
) -> IndependenceResult:
    """Convenience: compute baselines on atlas and check independence."""
    baselines = baseline_values_on_graphs(graphs, baseline_ids)
    return check_independence(candidate_values, baselines, threshold)
