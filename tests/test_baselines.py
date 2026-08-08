"""Tests for baseline search."""

from namm.baselines import random_search, wiener_baseline_expression
from namm.schemas.experiment import ExperimentConfig


def test_wiener_baseline_expression():
    assert "wiener_index" in wiener_baseline_expression()


def test_random_search_returns_records():
    config = ExperimentConfig(
        experiment_id="test",
        max_order=4,
        num_candidates=10,
        seed=123,
    )
    result = random_search(config)
    assert len(result.candidates) + len(result.rejections) == 10


def test_random_search_finds_nontrivial_candidate():
    config = ExperimentConfig(
        experiment_id="test",
        max_order=5,
        num_candidates=100,
        seed=7,
    )
    result = random_search(config)
    assert len(result.candidates) > 0
