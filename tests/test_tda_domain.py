"""Tests for TDA domain (NAMM-2026-006)."""

import pytest

pytest.importorskip("gudhi")

import networkx as nx

from namm.domains.tda.homology import (
    graph_persistence_signature,
    persistence_distance,
)
from namm.schemas.experiment import ExperimentConfig
from namm.baselines import run_search, tda_search


def test_path_graph_persistence():
    g = nx.path_graph(5)
    sig = graph_persistence_signature(g)
    assert sig.betti_0 >= 1
    assert sig.max_order == 5
    assert sig.signature_hash


def test_cycle_has_h1_feature():
    cycle = nx.cycle_graph(6)
    path = nx.path_graph(6)
    sig_cycle = graph_persistence_signature(cycle)
    sig_path = graph_persistence_signature(path)
    dist = persistence_distance(sig_cycle, sig_path)
    assert dist > 0.0


def test_order_limit():
    g = nx.complete_graph(25)
    with pytest.raises(ValueError, match="exceeds TDA limit"):
        graph_persistence_signature(g)


def test_tda_search_smoke():
    config = ExperimentConfig(
        experiment_id="test-tda",
        domain="tda_frame",
        max_order=6,
        num_candidates=5,
        seed=1,
        tda_min_baseline_distance=0.1,
        representation_ratio_threshold=None,
    )
    result = tda_search(config)
    assert len(result.candidates) + len(result.rejections) == 5


def test_run_search_dispatch_tda():
    config = ExperimentConfig(
        experiment_id="test-tda-dispatch",
        domain="tda_frame",
        max_order=5,
        num_candidates=3,
        seed=2,
        representation_ratio_threshold=None,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 3
