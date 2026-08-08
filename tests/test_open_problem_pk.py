"""Tests for Kotzig P_k-graph finite shadow."""

from __future__ import annotations

import networkx as nx

from namm.domains.open_problem.pk_graph import (
    count_paths_length_k,
    is_pk_graph,
    pk_graph_violations,
    search_pk_counterexamples,
)
from namm.schemas.experiment import ExperimentConfig
from namm.baselines import open_problem_search


def test_complete_graph_is_p1_graph() -> None:
    g = nx.complete_graph(4)
    assert is_pk_graph(g, 1)
    assert not is_pk_graph(g, 2)


def test_path_graph_p2_structure() -> None:
    g = nx.path_graph(5)
    # Endpoints have 0 length-2 paths between them in P_5? Actually one path of length 4
    assert count_paths_length_k(g, 0, 4, 4) == 1
    assert not is_pk_graph(g, 2)


def test_kotzig_no_counterexample_small_orders() -> None:
    result = search_pk_counterexamples(max_order=6, k_min=3, k_max=6)
    assert result.graphs_scanned > 0
    assert not result.counterexamples


def test_open_problem_search_integration() -> None:
    config = ExperimentConfig(
        experiment_id="NAMM-2026-005-test",
        domain="open_problem_shadow",
        max_order=5,
        pk_k_min=3,
        pk_k_max=5,
    )
    outcome = open_problem_search(config)
    assert outcome.best_generative is not None
    assert outcome.best_generative["problem"] == "kotzig_pk"
    assert outcome.best_generative["counterexample_count"] == 0
