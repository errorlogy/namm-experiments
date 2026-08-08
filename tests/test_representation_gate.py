"""Tests for K_A/K_H representation gate."""

from namm.metrics.representation import reject_if_low_compression_asymmetry
from namm.schemas.experiment import RepresentationMetrics


def test_rejects_low_ratio():
    metrics = RepresentationMetrics(
        json_bytes=50,
        gzip_bytes=40,
        eval_time_ms=0.1,
        token_count_estimate=100,
        projection_token_estimate=100,
    )
    result = reject_if_low_compression_asymmetry(metrics, threshold=2.0)
    assert not result.passed
    assert result.ratio < 2.0


def test_passes_high_ratio():
    metrics = RepresentationMetrics(
        json_bytes=300,
        gzip_bytes=280,
        eval_time_ms=0.1,
        token_count_estimate=100,
        projection_token_estimate=100,
    )
    result = reject_if_low_compression_asymmetry(metrics, threshold=2.0)
    assert result.passed
    assert result.ratio >= 2.0
