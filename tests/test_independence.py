"""Tests for independence rejection."""

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula
from namm.metrics.independence import check_independence, reject_if_correlated
from namm.domains.graph.generator import enumerate_small_graphs


def _atlas(max_order: int = 6):
    import networkx as nx

    atlas = nx.graph_atlas_g()
    graphs = []
    for n in range(1, max_order + 1):
        for g in atlas:
            if g.number_of_nodes() == n and nx.is_connected(g):
                graphs.append(g.copy())
    return graphs


def test_independence_rejects_wiener_correlated():
    graphs = _atlas(6)
    wiener_vals = [evaluate_formula("1*wiener_index", g) for g in graphs]
    combo_vals = [evaluate_formula("2*wiener_index + 1*num_edges", g) for g in graphs]
    baselines = {"wiener_index": wiener_vals}
    result = check_independence(combo_vals, baselines, threshold=0.95)
    assert not result.independent
    assert abs(result.max_correlation) > 0.9


def test_independence_accepts_uncorrelated_proxy():
    graphs = enumerate_small_graphs(4)
    cand = [evaluate_formula("1*algebraic_connectivity", g) for g in graphs]
    base = {"wiener_index": [evaluate_formula("1*wiener_index", g) for g in graphs]}
    result = check_independence(cand, base, threshold=0.95)
    assert result.independent or abs(result.max_correlation) <= 0.95


def test_reject_if_correlated_integration():
    graphs = _atlas(6)
    vals = [evaluate_formula("5*wiener_index", g) for g in graphs]
    result = reject_if_correlated(vals, graphs, threshold=0.95)
    assert not result.independent
