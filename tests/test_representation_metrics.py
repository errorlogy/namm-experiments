"""Tests for representation metrics."""

import networkx as nx

from namm.domains.graph.generator import random_invariant_formula
from namm.metrics.representation import compute_representation_metrics


def test_representation_metrics_positive():
    formula = random_invariant_formula(seed=1)
    g = nx.path_graph(4)
    metrics = compute_representation_metrics(
        formula.expression, formula=formula, reference_graphs=[g]
    )
    assert metrics.json_bytes > 0
    assert metrics.gzip_bytes > 0
    assert metrics.eval_time_ms >= 0
    assert metrics.token_count_estimate > 0


def test_gzip_smaller_or_equal_json():
    formula = random_invariant_formula(seed=2)
    metrics = compute_representation_metrics(formula.expression, formula=formula)
    assert metrics.gzip_bytes <= metrics.json_bytes
