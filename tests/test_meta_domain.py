"""Tests for meta-evaluator domain (NAMM-2026-004)."""

import networkx as nx

from namm.domains.meta.ast import (
    MetaEvaluatorNode,
    meta_leaf,
    meta_self,
    meta_to_dict,
    parse_meta_dict,
)
from namm.domains.meta.canonical import canonicalize_meta, meta_hash
from namm.domains.meta.evaluator import (
    evaluate_meta_on_graph,
    fixed_point_score,
    meta_agrees_on_graphs,
)
from namm.domains.meta.generator import random_meta_evaluator
from namm.domains.meta.transform import apply_transform, list_transforms
from namm.domains.graph.generator import enumerate_small_graphs
from namm.schemas.experiment import ExperimentConfig
from namm.baselines import run_search, meta_search


def test_meta_leaf_evaluates():
    g = nx.path_graph(4)
    node = meta_leaf("num_nodes")
    assert evaluate_meta_on_graph(node, g) == 4.0


def test_self_reference_evaluates():
    g = nx.cycle_graph(5)
    node = MetaEvaluatorNode(
        op="add",
        left=meta_leaf("num_edges"),
        right=meta_self(),
    )
    val = evaluate_meta_on_graph(node, g)
    # Self recurses until max_depth, accumulating num_edges each level
    assert val > g.number_of_edges()
    plain = evaluate_meta_on_graph(meta_leaf("num_edges"), g)
    assert val != plain


def test_canonicalize_commutative():
    a = MetaEvaluatorNode(
        op="add",
        left=meta_leaf("num_edges"),
        right=meta_leaf("wiener_index"),
    )
    b = MetaEvaluatorNode(
        op="add",
        left=meta_leaf("wiener_index"),
        right=meta_leaf("num_edges"),
    )
    ca = canonicalize_meta(a)
    cb = canonicalize_meta(b)
    assert meta_to_dict(ca) == meta_to_dict(cb)
    assert meta_hash(ca) == meta_hash(cb)


def test_transform_identity_fixed_point():
    node, _ = random_meta_evaluator(seed=42, max_depth=2, include_self=False)
    transformed = apply_transform("identity", node)
    graphs = enumerate_small_graphs(4)[:5]
    assert fixed_point_score(node, transformed, graphs) == 1.0


def test_transform_add_zero_fixed_point():
    node = meta_leaf("wiener_index")
    transformed = apply_transform("add_zero", node)
    graphs = enumerate_small_graphs(5)[:10]
    assert meta_agrees_on_graphs(node, transformed, graphs)


def test_transform_canonicalize_fixed_point():
    a = MetaEvaluatorNode(
        op="mul",
        left=meta_leaf("clustering"),
        right=meta_leaf("num_nodes"),
    )
    b = MetaEvaluatorNode(
        op="mul",
        left=meta_leaf("num_nodes"),
        right=meta_leaf("clustering"),
    )
    graphs = enumerate_small_graphs(4)
    ca = apply_transform("canonicalize", a)
    cb = apply_transform("canonicalize", b)
    assert meta_agrees_on_graphs(ca, cb, graphs)


def test_transform_registry():
    names = list_transforms()
    assert "identity" in names
    assert "canonicalize" in names
    assert "add_zero" in names


def test_parse_meta_dict_roundtrip():
    original = MetaEvaluatorNode(
        op="add",
        left=meta_leaf("num_edges"),
        right=meta_self(),
    )
    data = meta_to_dict(original)
    restored = parse_meta_dict(data)
    g = nx.karate_club_graph()
    assert evaluate_meta_on_graph(original, g) == evaluate_meta_on_graph(restored, g)


def test_random_meta_generates():
    node, cid = random_meta_evaluator(seed=99, include_self=True)
    g = nx.path_graph(3)
    val = evaluate_meta_on_graph(node, g)
    assert isinstance(val, float)
    assert cid.startswith("meta-")


def test_meta_search_finds_candidates():
    config = ExperimentConfig(
        experiment_id="test-meta",
        domain="meta_evaluation",
        max_order=4,
        num_candidates=20,
        seed=123,
        meta_max_depth=2,
        meta_fixed_point_threshold=1.0,
        representation_ratio_threshold=None,
    )
    result = meta_search(config)
    assert result.candidates or result.rejections
    total = len(result.candidates) + len(result.rejections)
    assert total == 20


def test_run_search_dispatches_meta():
    config = ExperimentConfig(
        experiment_id="test-meta-dispatch",
        domain="meta_evaluation",
        max_order=4,
        num_candidates=5,
        seed=1,
        meta_max_depth=2,
        representation_ratio_threshold=None,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 5
