"""Tests for v2 correlation rejection in random search."""

from namm.baselines import random_search
from namm.schemas.experiment import ExperimentConfig


def test_correlation_rejection_populates_rejections_jsonl():
    config = ExperimentConfig(
        experiment_id="test-v2-reject",
        max_order=5,
        num_candidates=30,
        seed=42,
        correlation_threshold=0.95,
        correlation_atlas_order=6,
    )
    result = random_search(config)
    assert len(result.candidates) + len(result.rejections) == 30
    correlation_rejections = [
        r for r in result.rejections if r.reason.startswith("high_correlation_with_baseline")
    ]
    assert len(correlation_rejections) > 0


def test_rejection_records_include_baseline_results():
    config = ExperimentConfig(
        experiment_id="test-v2-meta",
        max_order=4,
        num_candidates=20,
        seed=99,
        correlation_threshold=0.5,
    )
    result = random_search(config)
    assert len(result.rejections) > 0
    with_meta = [r for r in result.rejections if r.baseline_results is not None]
    assert len(with_meta) > 0


def test_accepted_candidates_have_v2_fields():
    config = ExperimentConfig(
        experiment_id="test-v2-fields",
        max_order=5,
        num_candidates=50,
        seed=7,
        correlation_threshold=0.99,
    )
    result = random_search(config)
    if result.candidates:
        c = result.candidates[0]
        assert c.representation_metrics is not None
        assert c.attack_checklist is not None
        assert c.baseline_results is not None
        assert c.novelty_level is not None
