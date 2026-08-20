"""Unit tests for information-theoretic metrics — namm.metrics.entropy."""

import numpy as np

from namm.metrics.entropy import (
    delta_h_fiber,
    histogram_entropy,
    joint_entropy,
    mutual_information,
    opinion_entropy,
    shannon_entropy,
    try_import_dit,
)
from namm.metrics.consensus_non_optimality import apply_consensus_operator


def test_shannon_entropy_uniform():
    p = np.ones(4) / 4
    h = shannon_entropy(p, base=2)
    assert abs(h - 2.0) < 1e-6


def test_shannon_entropy_certain():
    assert shannon_entropy(np.array([1.0])) == 0.0


def test_mutual_information_independent():
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, size=500)
    y = rng.normal(0, 1, size=500)
    mi = mutual_information(x, y, bins=10)
    assert mi < 0.15


def test_mutual_information_dependent():
    x = np.linspace(-1, 1, 200)
    y = x + np.random.default_rng(1).normal(0, 0.01, size=200)
    mi = mutual_information(x, y, bins=10)
    assert mi > 0.5


def test_opinion_entropy_and_delta_h_fiber():
    rng = np.random.default_rng(42)
    opinions = rng.normal(0, 1, size=(20, 2))
    consensus = apply_consensus_operator(opinions, "mean")
    assert opinion_entropy(opinions) > 0
    assert delta_h_fiber(opinions, consensus) > 0.5


def test_joint_entropy_bounds():
    x = np.array([0.0, 0.5, 1.0, 1.5])
    y = np.array([0.0, 0.25, 0.75, 1.0])
    h_joint = joint_entropy(x, y, bins=4)
    h_x = histogram_entropy(x, bins=4)
    assert h_joint >= h_x - 1e-6


def test_dit_optional_import():
    # Works without dit installed (returns None)
    dit = try_import_dit()
    assert dit is None or hasattr(dit, "Distribution")
