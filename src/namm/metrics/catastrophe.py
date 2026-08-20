"""Elementary catastrophe models (Thom) — fold, cusp, swallowtail.

Implemented with ``numpy`` / ``scipy`` only (no ``pycatastrophe`` on PyPI).
Used for bifurcation and hysteresis proxies in CNS / myth-shift experiments.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np
from scipy.optimize import minimize_scalar


class CatastropheKind(str, Enum):
    FOLD = "fold"
    CUSP = "cusp"
    SWALLOWTAIL = "swallowtail"


def fold_potential(x: np.ndarray, a: float) -> np.ndarray:
    """Fold (A₂): V(x,a) = x³/3 + ax."""
    x = np.asarray(x, dtype=float)
    return x**3 / 3.0 + a * x


def fold_equilibrium(a: float) -> list[float]:
    """Real equilibria x* with V'(x*) = x² + a = 0."""
    if a > 0:
        return []
    if a == 0:
        return [0.0]
    root = float(np.sqrt(-a))
    return [-root, root]


def cusp_potential(x: np.ndarray, a: float, b: float) -> np.ndarray:
    """Cusp (A₃): V(x,a,b) = x⁴/4 + ax²/2 + bx."""
    x = np.asarray(x, dtype=float)
    return x**4 / 4.0 + a * x**2 / 2.0 + b * x


def cusp_equilibria(a: float, b: float) -> list[float]:
    """Real roots of V'(x) = x³ + ax + b = 0."""
    coeffs = [1.0, 0.0, a, b]
    roots = np.roots(coeffs)
    return sorted(float(r.real) for r in roots if abs(r.imag) < 1e-8)


def swallowtail_potential(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Swallowtail (A₄): V(x,a,b,c) = x⁵/5 + ax³/3 + bx²/2 + cx."""
    x = np.asarray(x, dtype=float)
    return x**5 / 5.0 + a * x**3 / 3.0 + b * x**2 / 2.0 + c * x


def find_local_minima(
    potential_fn,
    control: tuple[float, ...],
    x_range: tuple[float, float] = (-3.0, 3.0),
    n_grid: int = 200,
) -> list[float]:
    """Grid-seeded 1-D local minima search."""
    xs = np.linspace(x_range[0], x_range[1], n_grid)
    vs = potential_fn(xs, *control)
    minima: list[float] = []
    for i in range(1, len(xs) - 1):
        if vs[i] <= vs[i - 1] and vs[i] <= vs[i + 1]:
            res = minimize_scalar(
                lambda t: float(potential_fn(np.array([t]), *control)[0]),
                bounds=(xs[i - 1], xs[i + 1]),
                method="bounded",
            )
            if res.success:
                minima.append(float(res.x))
    # dedupe close minima
    minima.sort()
    deduped: list[float] = []
    for m in minima:
        if not deduped or abs(m - deduped[-1]) > 1e-3:
            deduped.append(m)
    return deduped


def cusp_bifurcation_set(a_values: np.ndarray, b_values: np.ndarray) -> np.ndarray:
    """Discriminant Δ = 4a³ + 27b² ≤ 0 marks bifurcation (multiple equilibria)."""
    a = np.asarray(a_values, dtype=float)
    b = np.asarray(b_values, dtype=float)
    return 4.0 * a**3 + 27.0 * b**2


def on_bifurcation_cusp(a: float, b: float, tol: float = 1e-6) -> bool:
    """True when (a,b) lies on the cusp bifurcation set (Δ ≈ 0)."""
    return abs(cusp_bifurcation_set(np.array([a]), np.array([b]))[0]) <= tol


def detect_bifurcation_crossing(
    param_values: np.ndarray,
    equilibria_counts: np.ndarray,
) -> list[int]:
    """Indices where number of stable equilibria changes along a control path."""
    crossings: list[int] = []
    for i in range(1, len(param_values)):
        if equilibria_counts[i] != equilibria_counts[i - 1]:
            crossings.append(i)
    return crossings


@dataclass
class HysteresisLoop:
    """Forward/backward sweep proxy along a control parameter."""

    param_values: list[float]
    state_forward: list[float]
    state_backward: list[float]
    width: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "param_values": self.param_values,
            "state_forward": self.state_forward,
            "state_backward": self.state_backward,
            "width": self.width,
        }


def cusp_hysteresis_loop(
    a: float,
    b_values: np.ndarray,
    x_init: float = 0.0,
) -> HysteresisLoop:
    """Track cusp minima along forward/backward b-sweeps (hysteresis proxy)."""
    b_fwd = np.asarray(b_values, dtype=float)
    b_bwd = b_fwd[::-1]
    state_fwd: list[float] = []
    state_bwd: list[float] = []
    x_fwd = x_init
    x_bwd = x_init

    for b in b_fwd:
        minima = find_local_minima(cusp_potential, (a, float(b)))
        if not minima:
            x_fwd = 0.0
        else:
            x_fwd = min(minima, key=lambda m: abs(m - x_fwd))
        state_fwd.append(x_fwd)

    for b in b_bwd:
        minima = find_local_minima(cusp_potential, (a, float(b)))
        if not minima:
            x_bwd = 0.0
        else:
            x_bwd = min(minima, key=lambda m: abs(m - x_bwd))
        state_bwd.append(x_bwd)

    width = float(np.mean(np.abs(np.array(state_fwd) - np.array(state_bwd[::-1]))))
    return HysteresisLoop(
        param_values=b_fwd.tolist(),
        state_forward=state_fwd,
        state_backward=state_bwd[::-1],
        width=width,
    )


def try_import_nolds() -> Any | None:
    """Return ``nolds`` if ``namm[science]`` extra is installed, else None."""
    try:
        import nolds  # type: ignore[import-untyped]

        return nolds
    except ImportError:
        return None
