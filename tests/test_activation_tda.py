"""Unit tests for activation TDA metrics (no GPU required)."""

from __future__ import annotations

import numpy as np

from namm.metrics.activation_tda import (
    activation_barycenter,
    build_point_cloud,
    evaluate_activation_trajectory,
)
from namm.metrics.phase_lock import load_phase_lock_spec


def test_build_point_cloud_turns_x_layers():
    mats = [np.ones((3, 4)), np.ones((3, 4)) * 2]
    cloud = build_point_cloud(mats, mode="turns_x_layers")
    assert cloud.shape == (6, 4)


def test_build_point_cloud_turns_last_layer():
    mats = [np.arange(4.0).reshape(1, 4), np.arange(4.0).reshape(1, 4) + 10]
    cloud = build_point_cloud(mats, mode="turns_last_layer")
    assert cloud.shape == (2, 4)


def test_evaluate_activation_trajectory_synthetic_separation():
    gates = load_phase_lock_spec()["gates"]
    rng = np.random.default_rng(42)
    mu = rng.normal(0, 0.05, (12, 8))
    lock = mu + rng.normal(0.4, 0.1, (12, 8))
    centroid = activation_barycenter([mu])
    mu_m = evaluate_activation_trajectory(mu, centroid, gates)
    lock_m = evaluate_activation_trajectory(lock, centroid, gates)
    assert lock_m["d_med"] > mu_m["d_med"]
    assert lock_m["beta_1"] >= mu_m["beta_1"] or lock_m["d_eff"] >= mu_m["d_eff"]


def test_evaluate_activation_trajectory_trivial():
    gates = load_phase_lock_spec()["gates"]
    single = np.zeros((1, 4))
    m = evaluate_activation_trajectory(single, np.zeros(4), gates)
    assert m["n_points"] == 1
    assert m["gates_passed"] is False
