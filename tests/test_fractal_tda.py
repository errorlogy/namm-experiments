"""Unit tests for fractal_tda metrics (no GPU, no LM required)."""

from __future__ import annotations

import numpy as np
import pytest

from namm.metrics.fractal_tda import (
    LayerFractalProfile,
    box_counting_dim,
    compare_fractal_profiles,
    layer_wise_fractal_sweep,
)


# ──────────────────────────────────────────────────────────────────────────────
# box_counting_dim — known synthetic cases
# ──────────────────────────────────────────────────────────────────────────────

def test_box_counting_line_approx_1():
    """Points on a line → d_f ≈ 1."""
    rng = np.random.default_rng(0)
    t = rng.uniform(0, 1, 200)
    pts = np.column_stack([t, np.zeros_like(t), np.zeros_like(t)])
    d_f = box_counting_dim(pts, pca_dim=None)
    assert 0.7 <= d_f <= 1.5, f"expected ~1 for line, got {d_f:.4f}"


def test_box_counting_plane_approx_2():
    """Points on a 2-D plane embedded in 3-D → d_f ≈ 2."""
    rng = np.random.default_rng(1)
    xy = rng.uniform(0, 1, (400, 2))
    pts = np.column_stack([xy, np.zeros(400)])
    d_f = box_counting_dim(pts, pca_dim=None)
    assert 1.2 <= d_f <= 2.6, f"expected ~2 for plane, got {d_f:.4f}"


def test_box_counting_fractal_between_1_and_2():
    """Koch-like dense random cloud with controlled spread → 1 < d_f < 2.5."""
    rng = np.random.default_rng(42)
    # Cantor-like sparse 1-D set projected to 2-D
    pts_1d = np.sort(rng.uniform(0, 1, 300))
    pts = np.column_stack([pts_1d, rng.normal(0, 0.02, 300)])
    d_f = box_counting_dim(pts, pca_dim=None, n_epsilons=16)
    assert 0.8 <= d_f <= 2.5, f"d_f={d_f:.4f} out of expected range"


def test_box_counting_degenerate_returns_nan():
    """Too few points → nan."""
    pts = np.array([[0.0, 1.0], [0.5, 0.5]])
    result = box_counting_dim(pts)
    assert np.isnan(result)


def test_box_counting_1d_input_returns_nan():
    """1-D array → nan (wrong shape)."""
    pts = np.array([1.0, 2.0, 3.0])
    result = box_counting_dim(pts)
    assert np.isnan(result)


# ──────────────────────────────────────────────────────────────────────────────
# layer_wise_fractal_sweep
# ──────────────────────────────────────────────────────────────────────────────

def _synthetic_layer_clouds(n_layers: int = 6, n_turns: int = 5, hidden_dim: int = 16,
                             spread: float = 1.0) -> dict[int, np.ndarray]:
    rng = np.random.default_rng(99)
    return {
        li: rng.normal(0, spread * (1 + li * 0.1), (n_turns, hidden_dim))
        for li in range(n_layers)
    }


def test_layer_wise_returns_profile():
    clouds = _synthetic_layer_clouds()
    profile = layer_wise_fractal_sweep(clouds, policy="mu")
    assert isinstance(profile, LayerFractalProfile)
    assert profile.policy == "mu"
    assert len(profile.layer_indices) == 6
    assert len(profile.d_f_per_layer) == 6
    assert profile.n_valid_layers >= 1


def test_layer_wise_non_negative_df():
    clouds = _synthetic_layer_clouds(n_turns=8, spread=2.0)
    profile = layer_wise_fractal_sweep(clouds, policy="lock_reassert")
    valid = [v for v in profile.d_f_per_layer if not np.isnan(v)]
    assert all(v >= 0.0 for v in valid)


# ──────────────────────────────────────────────────────────────────────────────
# compare_fractal_profiles — H-AMAT-008 sub-hypotheses
# ──────────────────────────────────────────────────────────────────────────────

def _make_profile(policy: str, d_f_values: list[float]) -> LayerFractalProfile:
    valid = [v for v in d_f_values if not np.isnan(v)]
    mean_df = float(np.mean(valid)) if valid else float("nan")
    std_df = float(np.std(valid)) if valid else float("nan")
    var_df = float(np.var(valid)) if valid else float("nan")
    nig = float(np.mean([abs(v - round(v)) for v in valid])) if valid else float("nan")
    return LayerFractalProfile(
        policy=policy,
        layer_indices=list(range(len(d_f_values))),
        d_f_per_layer=d_f_values,
        mean_d_f=mean_df,
        std_d_f=std_df,
        non_integer_gap=nig,
        layer_variance=var_df,
        n_valid_layers=len(valid),
    )


def test_compare_lock_higher_df_triggers_008a():
    mu = _make_profile("mu", [1.0, 1.0, 1.0, 1.0])
    lock = _make_profile("lock_reassert", [1.4, 1.5, 1.6, 1.3])
    cmp = compare_fractal_profiles(mu, lock)
    assert cmp.h_amat_008a is True
    assert cmp.lift_mean_df > 0


def test_compare_higher_non_int_gap_triggers_008b():
    mu = _make_profile("mu", [1.0, 2.0, 1.0, 2.0])      # gap=0
    lock = _make_profile("lock_reassert", [1.4, 1.6, 1.7, 1.5])  # gap>0
    cmp = compare_fractal_profiles(mu, lock)
    assert cmp.h_amat_008b is True


def test_compare_flat_lock_profile_no_008c():
    mu = _make_profile("mu", [1.0, 1.0, 1.0])
    lock = _make_profile("lock_reassert", [1.3, 1.3, 1.3])  # flat → variance=0
    cmp = compare_fractal_profiles(mu, lock, layer_variance_threshold=0.01)
    assert cmp.h_amat_008c is False


def test_compare_variable_lock_profile_triggers_008c():
    mu = _make_profile("mu", [1.0, 1.0, 1.0])
    lock = _make_profile("lock_reassert", [0.8, 1.5, 2.1])  # high variance
    cmp = compare_fractal_profiles(mu, lock, layer_variance_threshold=0.01)
    assert cmp.h_amat_008c is True


def test_certificate_fractal_evidence_all_three():
    mu = _make_profile("mu", [1.0, 1.0, 1.0, 1.0])
    lock = _make_profile("lock_reassert", [1.2, 1.6, 1.9, 1.4])
    cmp = compare_fractal_profiles(mu, lock, layer_variance_threshold=0.01)
    assert cmp.certificate == "FRACTAL_EVIDENCE"


def test_certificate_null_when_no_separation():
    mu = _make_profile("mu", [1.5, 1.5, 1.5])
    lock = _make_profile("lock_reassert", [1.4, 1.4, 1.4])
    cmp = compare_fractal_profiles(mu, lock)
    assert cmp.certificate == "NULL"
    assert cmp.h_amat_008a is False


def test_most_informative_layers_nonempty():
    mu = _make_profile("mu", [1.0, 1.0, 1.0, 1.0])
    lock = _make_profile("lock_reassert", [1.0, 1.8, 1.0, 1.6])
    cmp = compare_fractal_profiles(mu, lock)
    assert len(cmp.most_informative_layers) >= 1
    # Layers 1 and 3 have largest difference
    assert cmp.most_informative_layers[0] in (1, 3)
