"""Tests for baseline correlation and novelty assessment."""

import networkx as nx

from namm.metrics.baselines import (
    assess_novelty_level,
    compare_to_baselines,
    pearson_correlation,
)
from namm.prior_art.simplify import simplifies_to_known_baseline


def test_pearson_perfect_correlation():
    assert pearson_correlation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == 1.0


def test_pearson_uncorrelated():
    r = pearson_correlation([1.0, 2.0, 3.0], [3.0, 1.0, 2.0])
    assert abs(r) < 1.0


def test_compare_wiener_high_correlation():
    graphs = [nx.path_graph(n) for n in range(2, 8)]
    expr = "5*wiener_index + 2*num_edges"
    results = compare_to_baselines(expr, graphs)
    wiener = next(c for c in results.comparisons if c.baseline_id == "wiener_index")
    assert wiener.pearson_r is not None
    assert wiener.pearson_r > 0.9


def test_assess_novelty_n0_for_wiener():
    graphs = [nx.path_graph(3), nx.cycle_graph(4)]
    results = compare_to_baselines("1*wiener_index", graphs)
    level = assess_novelty_level(results, simplifies_to_known=False)
    assert level.value == "N0"


def test_simplify_detects_wiener():
    assert simplifies_to_known_baseline("1*wiener_index") is True
    assert simplifies_to_known_baseline("2*wiener_index + 3*num_edges") is False
