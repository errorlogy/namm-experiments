"""Tests for rewriting search pipeline."""

from namm.baselines import rewriting_search, run_search
from namm.schemas.experiment import ExperimentConfig


def test_rewriting_search_returns_records():
    config = ExperimentConfig(
        experiment_id="test-rew-search",
        domain="rewriting",
        num_candidates=10,
        seed=42,
        rewriting_max_length=4,
        representation_ratio_threshold=None,
    )
    result = rewriting_search(config)
    assert len(result.candidates) + len(result.rejections) == 10


def test_run_search_dispatches_rewriting_domain():
    config = ExperimentConfig(
        experiment_id="test-rew-dispatch",
        domain="rewriting",
        num_candidates=5,
        seed=1,
        rewriting_max_length=4,
        representation_ratio_threshold=None,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 5
