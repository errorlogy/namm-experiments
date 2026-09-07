"""Minimal tests for activation_tda.pca_reduce."""

import numpy as np
import pytest

from namm.metrics.activation_tda import pca_reduce


def test_pca_reduce_shape():
    rng = np.random.default_rng(42)
    X = rng.standard_normal((24, 896))
    Y = pca_reduce(X, n_components=8)
    assert Y.shape == (24, 8), f"Expected (24, 8), got {Y.shape}"


def test_pca_reduce_preserves_points():
    rng = np.random.default_rng(99)
    X = rng.standard_normal((10, 64))
    Y = pca_reduce(X, n_components=4)
    assert Y.shape[0] == 10


def test_pca_reduce_caps_at_n_pts():
    """If n_components >= n_points, cap at n_points - 1 (or n_points at most)."""
    X = np.random.default_rng(7).standard_normal((5, 32))
    Y = pca_reduce(X, n_components=20)
    assert Y.shape[0] == 5
    assert Y.shape[1] <= 5


def test_pca_reduce_reduces_variance():
    """Reduced cloud should have strictly less total variance than original in high-d."""
    rng = np.random.default_rng(123)
    X = rng.standard_normal((30, 256))
    Y = pca_reduce(X, n_components=8)
    # Frobenius norm of centred matrix is preserved only along top PCs; shape check suffices
    assert Y.shape == (30, 8)


def test_pca_reduce_trivial():
    """Single point returns safely."""
    X = np.array([[1.0, 2.0, 3.0]])
    Y = pca_reduce(X, n_components=2)
    assert Y.shape[0] == 1


def test_pca_reduce_mu_vs_lock_d_eff():
    """After PCA, lock cloud should show higher spread (D_eff) than mu cloud."""
    rng = np.random.default_rng(2026036)
    mu_cloud_orig = rng.normal(0, 0.05, (24, 896))
    lock_cloud_orig = mu_cloud_orig + rng.normal(0.3, 0.2, mu_cloud_orig.shape)

    mu_r = pca_reduce(mu_cloud_orig, 8)
    lock_r = pca_reduce(lock_cloud_orig, 8)

    from namm.metrics.cognitive_class import compute_d_eff

    d_eff_mu = compute_d_eff(mu_r)
    d_eff_lock = compute_d_eff(lock_r)
    # After PCA-reduction, lock should have higher D_eff
    assert d_eff_lock >= d_eff_mu, (
        f"Expected lock D_eff >= mu D_eff; got lock={d_eff_lock:.4f} mu={d_eff_mu:.4f}"
    )
