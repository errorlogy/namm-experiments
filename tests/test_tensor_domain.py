"""Tests for raw tensor domain (NAMM-2026-007)."""

from __future__ import annotations

import networkx as nx

from namm.baselines import run_search, tensor_search
from namm.domains.tensor.ast import TensorNode, tensor_leaf
from namm.domains.tensor.baselines import generate_tensor_baselines
from namm.domains.tensor.canonical import canonicalize
from namm.domains.tensor.evaluator import evaluate_tensor_ast
from namm.domains.tensor.features import graph_tensor_vector
from namm.schemas.experiment import ExperimentConfig


def test_graph_tensor_vector_length() -> None:
    g = nx.path_graph(5)
    vec = graph_tensor_vector(g, spectrum_size=8, heat_times=(0.5, 1.0))
    assert len(vec) == 10


def test_tensor_baselines_count() -> None:
    baselines = generate_tensor_baselines(max_degree=4)
    assert len(baselines) >= 20


def test_evaluate_tensor_ast_simple() -> None:
    g = nx.cycle_graph(4)
    node = canonicalize(
        TensorNode(op="add", left=tensor_leaf("t0"), right=tensor_leaf("t1"))
    )
    val = evaluate_tensor_ast(node, g)
    vec = graph_tensor_vector(g)
    assert abs(val - (vec[0] + vec[1])) < 1e-9


def test_tensor_search_dispatch() -> None:
    config = ExperimentConfig(
        experiment_id="test-tensor",
        domain="raw_tensor",
        max_order=6,
        train_max_order=5,
        num_candidates=30,
        seed=7,
        search_strategy="random",
        held_out_families=["trees", "bipartite"],
    )
    result = tensor_search(config)
    assert len(result.candidates) + len(result.rejections) == 30


def test_run_search_dispatches_tensor() -> None:
    config = ExperimentConfig(
        experiment_id="test-tensor-dispatch",
        domain="raw_tensor",
        num_candidates=15,
        seed=3,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 15
