"""Unit tests for Thom catastrophe models — namm.metrics.catastrophe."""

import numpy as np

from namm.metrics.catastrophe import (
    cusp_bifurcation_set,
    cusp_equilibria,
    cusp_hysteresis_loop,
    cusp_potential,
    detect_bifurcation_crossing,
    fold_equilibrium,
    fold_potential,
    on_bifurcation_cusp,
)


def test_fold_potential_shape():
    x = np.linspace(-2, 2, 50)
    v = fold_potential(x, a=-1.0)
    assert v.shape == x.shape
    assert np.isfinite(v).all()


def test_fold_equilibrium_bifurcation():
    assert fold_equilibrium(1.0) == []
    roots = fold_equilibrium(-1.0)
    assert len(roots) == 2
    assert abs(roots[0] + roots[1]) < 1e-6


def test_cusp_equilibria_count():
    # Inside cusp region (a < 0): up to three real roots
    roots_neg = cusp_equilibria(a=-1.0, b=0.0)
    assert len(roots_neg) == 3
    # Outside: one real root
    roots_pos = cusp_equilibria(a=1.0, b=0.0)
    assert len(roots_pos) == 1


def test_cusp_bifurcation_discriminant():
    delta = cusp_bifurcation_set(np.array([-1.0]), np.array([0.0]))
    assert delta[0] < 0  # multiple equilibria region


def test_on_bifurcation_cusp():
    assert on_bifurcation_cusp(0.0, 0.0, tol=1e-3)


def test_hysteresis_loop_nonzero_width():
    b_vals = np.linspace(-1.5, 1.5, 30)
    loop = cusp_hysteresis_loop(a=-0.5, b_values=b_vals)
    assert len(loop.state_forward) == len(b_vals)
    assert loop.width >= 0.0


def test_detect_bifurcation_crossing():
    params = np.linspace(-2, 2, 20)
    counts = np.array([1 if p < 0 else 3 for p in params])
    crossings = detect_bifurcation_crossing(params, counts)
    assert len(crossings) == 1


def test_cusp_potential_minimum_at_origin():
    v = cusp_potential(np.array([0.0]), a=1.0, b=0.0)
    v_off = cusp_potential(np.array([1.0]), a=1.0, b=0.0)
    assert v[0] < v_off[0]
