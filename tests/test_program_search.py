"""Tests for program search pipeline integration."""

from namm.baselines import program_search, run_search
from namm.schemas.experiment import ExperimentConfig


def test_program_search_returns_records():
    config = ExperimentConfig(
        experiment_id="test-prog-search",
        domain="program_ast",
        max_order=6,
        train_max_order=6,
        num_candidates=25,
        seed=42,
        correlation_rejection_threshold=0.95,
    )
    result = program_search(config)
    assert len(result.candidates) + len(result.rejections) == 25


def test_run_search_dispatches_program_domain():
    config = ExperimentConfig(
        experiment_id="test-dispatch",
        domain="program_ast",
        num_candidates=10,
        seed=1,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 10


def test_graph_string_domain_unchanged():
    config = ExperimentConfig(
        experiment_id="test-graph-string",
        domain="graph_string",
        max_order=5,
        num_candidates=15,
        seed=42,
    )
    result = run_search(config)
    assert len(result.candidates) + len(result.rejections) == 15
