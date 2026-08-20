"""Unit tests for fuzzy membership functions — namm.metrics.fuzzy."""

import networkx as nx
import numpy as np

from namm.metrics.fuzzy import (
    gaussian,
    gaussian_centroid,
    issue_tag_membership,
    ramp,
    spatial_soft,
    trapezoidal,
    triangular,
)


def test_triangular_peak():
    assert abs(triangular(0.5, 0.0, 0.5, 1.0) - 1.0) < 1e-9
    assert triangular(-0.1, 0.0, 0.5, 1.0) == 0.0


def test_trapezoidal_plateau():
    assert trapezoidal(0.5, 0.0, 0.25, 0.75, 1.0) == 1.0
    assert trapezoidal(0.0, 0.0, 0.25, 0.75, 1.0) == 0.0


def test_gaussian_centroid():
    mu = gaussian_centroid(np.array([0.0, 0.0]), np.array([0.0, 0.0]), sigma=0.5)
    assert abs(mu - 1.0) < 1e-9
    mu_far = gaussian_centroid(np.array([2.0, 0.0]), np.array([0.0, 0.0]), sigma=0.5)
    assert mu_far < mu


def test_ramp():
    assert ramp(0.0, 0.0, 1.0) == 0.0
    assert ramp(1.0, 0.0, 1.0) == 1.0
    assert abs(ramp(0.5, 0.0, 1.0) - 0.5) < 1e-9


def test_spatial_soft_on_graph():
    g = nx.path_graph(5)
    assert spatial_soft(0, 0, g) == 1.0
    assert spatial_soft(4, 0, g) < spatial_soft(1, 0, g)


def test_issue_tag_membership():
    mu = issue_tag_membership({"climate", "energy"}, ["climate", "trade"], 0.8)
    assert 0.0 < mu <= 1.0
    # No overlap still yields baseline from expertise weight blend
    assert issue_tag_membership(set(), ["climate"]) == 0.2


def test_gaussian_1d():
    assert gaussian(0.0, 0.0, 1.0) == 1.0
    assert gaussian(2.0, 0.0, 1.0) < 0.2
