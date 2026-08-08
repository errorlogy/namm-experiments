"""Tests for generative holdout metrics."""

import networkx as nx

from namm.domains.program.ast import leaf
from namm.domains.program.evaluator import evaluate_ast
from namm.metrics.generative import (
    generate_held_out_families,
    generative_holdout_score,
    train_graph_set,
)


def test_generate_held_out_families():
    families = generate_held_out_families(["trees", "bipartite", "cubic"], max_order=8)
    assert set(families.keys()) == {"trees", "bipartite", "cubic"}
    for graphs in families.values():
        assert len(graphs) > 0
        assert all(isinstance(g, nx.Graph) for g in graphs)


def test_generative_holdout_wiener_passes():
    ast = leaf("wiener_index")
    train = train_graph_set(6)
    held_out = generate_held_out_families(["trees", "bipartite"], max_order=8, per_family=5)
    result = generative_holdout_score(
        lambda g: evaluate_ast(ast, g),
        train,
        held_out,
    )
    assert result.aggregate_score > 0
    assert result.passed


def test_generative_holdout_constant_fails():
    train = train_graph_set(6)
    held_out = generate_held_out_families(["trees"], max_order=6, per_family=3)

    def const(_g):
        return 1.0

    result = generative_holdout_score(const, train, held_out, min_variance=1e-6)
    assert not result.passed
