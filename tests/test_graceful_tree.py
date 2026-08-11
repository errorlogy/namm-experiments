"""Tests for Graceful Tree Conjecture shadow (NAMM-2026-008)."""

from __future__ import annotations

import networkx as nx

from namm.baselines import open_problem_search
from namm.domains.open_problem.graceful_tree import (
    find_graceful_labeling,
    has_graceful_labeling,
    search_graceful_tree_counterexamples,
)
from namm.schemas.experiment import ExperimentConfig


def test_path_graph_graceful() -> None:
    g = nx.path_graph(4)
    assert has_graceful_labeling(g)
    labeling = find_graceful_labeling(g)
    assert labeling is not None


def test_star_graceful() -> None:
    g = nx.star_graph(5)
    assert has_graceful_labeling(g)


def test_no_counterexample_small_trees() -> None:
    result = search_graceful_tree_counterexamples(max_order=6)
    assert result.trees_scanned > 0
    assert not result.counterexamples


def test_graceful_open_problem_integration() -> None:
    config = ExperimentConfig(
        experiment_id="NAMM-2026-008-test",
        domain="open_problem_shadow",
        open_problem_id="graceful_tree",
        max_order=6,
        graceful_max_order=6,
    )
    outcome = open_problem_search(config)
    assert outcome.best_generative is not None
    assert outcome.best_generative["problem"] == "graceful_tree"
    assert outcome.best_generative["counterexample_count"] == 0
