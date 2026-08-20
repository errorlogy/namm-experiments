"""Information-theoretic metrics for NAMM — Shannon entropy, MI, fiber loss.

Core implementations use ``numpy`` + ``scipy.stats``. Optional ``dit`` extras
(discrete information theory) are loaded lazily via :func:`try_import_dit`.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import entropy as scipy_shannon_entropy


def shannon_entropy(probs: np.ndarray, base: float = 2.0) -> float:
    """Shannon entropy H(p) in bits (base 2) or nats (base e)."""
    p = np.asarray(probs, dtype=float)
    p = p[p > 0]
    if p.size == 0:
        return 0.0
    p = p / p.sum()
    return float(scipy_shannon_entropy(p, base=base))


def histogram_entropy(values: np.ndarray, bins: int = 8, base: float = 2.0) -> float:
    """Entropy of a 1-D sample via histogram binning."""
    vals = np.asarray(values, dtype=float).ravel()
    if vals.size == 0:
        return 0.0
    lo, hi = 0.0, max(float(vals.max()), 1.0)
    hist, _ = np.histogram(vals, bins=bins, range=(lo, hi), density=True)
    hist = hist + 1e-12
    hist = hist / hist.sum()
    return shannon_entropy(hist, base=base)


def opinion_entropy(opinions: np.ndarray, bins: int = 8) -> float:
    """Shannon entropy of discretized opinion magnitudes."""
    mags = np.linalg.norm(opinions, axis=1)
    return histogram_entropy(mags, bins=bins)


def delta_h_fiber(opinions: np.ndarray, consensus: np.ndarray) -> float:
    """Normalized entropy destroyed by consensus projection (H-CNS-004)."""
    h_pre = opinion_entropy(opinions)
    h_post = 1e-12  # collapsed to single point
    delta = max(h_pre - h_post, 0.0)
    return float(delta / max(h_pre, 1e-12))


def mutual_information(x: np.ndarray, y: np.ndarray, bins: int = 8) -> float:
    """Discrete MI I(X;Y) from paired samples via 2-D histogram."""
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if x.size != y.size or x.size == 0:
        return 0.0
    lo_x, hi_x = float(x.min()), max(float(x.max()), float(x.min()) + 1e-6)
    lo_y, hi_y = float(y.min()), max(float(y.max()), float(y.min()) + 1e-6)
    joint, _, _ = np.histogram2d(x, y, bins=bins, range=[[lo_x, hi_x], [lo_y, hi_y]], density=True)
    joint = joint + 1e-12
    joint = joint / joint.sum()
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    mi = 0.0
    for i in range(joint.shape[0]):
        for j in range(joint.shape[1]):
            if joint[i, j] > 0 and px[i] > 0 and py[j] > 0:
                mi += joint[i, j] * np.log2(joint[i, j] / (px[i] * py[j]))
    return float(max(mi, 0.0))


def joint_entropy(x: np.ndarray, y: np.ndarray, bins: int = 8) -> float:
    """H(X,Y) from paired samples."""
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if x.size != y.size or x.size == 0:
        return 0.0
    lo_x, hi_x = float(x.min()), max(float(x.max()), float(x.min()) + 1e-6)
    lo_y, hi_y = float(y.min()), max(float(y.max()), float(y.min()) + 1e-6)
    joint, _, _ = np.histogram2d(x, y, bins=bins, range=[[lo_x, hi_x], [lo_y, hi_y]], density=True)
    joint = joint + 1e-12
    joint = joint / joint.sum()
    return shannon_entropy(joint.ravel())


def conditional_entropy(x: np.ndarray, y: np.ndarray, bins: int = 8) -> float:
    """H(X|Y) = H(X,Y) - H(Y)."""
    return joint_entropy(x, y, bins=bins) - histogram_entropy(y, bins=bins)


def try_import_dit() -> Any | None:
    """Return ``dit`` module if ``namm[science]`` extra is installed, else None."""
    try:
        import dit  # type: ignore[import-untyped]

        return dit
    except ImportError:
        return None


def dit_entropy_from_pmf(pmf: dict[tuple[Any, ...], float]) -> float | None:
    """Shannon entropy via ``dit`` when available; otherwise None."""
    dit = try_import_dit()
    if dit is None:
        return None
    d = dit.Distribution(pmf, base="linear")
    return float(d.H())
