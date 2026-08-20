"""Layer-wise TDA + box-counting fractal dimension for NAMM-2026-039 (H-AMAT-008).

Estimates box-counting fractal dimension d_f per transformer layer on last-token
hidden-state trajectories under μ vs lock_reassert policies. Non-integer d_f
separation is the primary test of H-AMAT-008.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Box-counting fractal dimension
# ──────────────────────────────────────────────────────────────────────────────

def box_counting_dim(
    points: np.ndarray,
    epsilon_range: tuple[float, float] | None = None,
    n_epsilons: int = 12,
    pca_dim: int | None = 3,
) -> float:
    """Estimate box-counting fractal dimension d_f via log-log slope.

    Algorithm:
    1. Optionally project to low-D space (pca_dim) to make grid feasible.
    2. For each ε in epsilon_range, count occupied hypercubes N(ε).
    3. d_f = -slope of log N(ε) vs log ε  (log(1/ε) convention: d_f = slope > 0).

    Returns d_f ∈ [0, pca_dim] or np.nan on degenerate input.
    """
    if points.ndim != 2 or points.shape[0] < 3:
        return float("nan")

    pts = points.astype(np.float64)

    # Optionally reduce to pca_dim for tractable grid counting
    if pca_dim is not None and pca_dim > 0 and pts.shape[1] > pca_dim:
        pts = _pca_reduce_fractal(pts, pca_dim)

    if pts.shape[1] == 0:
        return float("nan")

    # Normalise to unit hypercube
    lo = pts.min(axis=0)
    hi = pts.max(axis=0)
    span = hi - lo
    span[span < 1e-12] = 1.0
    pts = (pts - lo) / span

    # Epsilon range: fraction of total span
    if epsilon_range is None:
        eps_min = 0.02
        eps_max = 0.5
    else:
        eps_min, eps_max = epsilon_range

    epsilons = np.geomspace(eps_max, eps_min, n_epsilons)

    log_inv_eps: list[float] = []
    log_n: list[float] = []

    for eps in epsilons:
        # Count distinct occupied boxes
        indices = np.floor(pts / eps).astype(np.int64)
        n_boxes = len({tuple(row) for row in indices})
        if n_boxes >= 2:
            log_inv_eps.append(np.log(1.0 / eps))
            log_n.append(np.log(float(n_boxes)))

    if len(log_inv_eps) < 3:
        return float("nan")

    x = np.array(log_inv_eps)
    y = np.array(log_n)
    # Ordinary least-squares slope
    xm, ym = x.mean(), y.mean()
    denom = float(np.sum((x - xm) ** 2))
    if denom < 1e-14:
        return float("nan")
    slope = float(np.sum((x - xm) * (y - ym)) / denom)
    return max(0.0, slope)


def _pca_reduce_fractal(pts: np.ndarray, k: int) -> np.ndarray:
    """Thin PCA (numpy SVD) to k dimensions."""
    n, d = pts.shape
    k = min(k, n - 1, d)
    if k <= 0:
        return pts
    centered = pts - pts.mean(axis=0, keepdims=True)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    return (centered @ Vt[:k].T).astype(np.float64)


# ──────────────────────────────────────────────────────────────────────────────
# Layer-wise fractal sweep
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class LayerFractalProfile:
    """Per-layer d_f profile for one policy."""
    policy: str
    layer_indices: list[int]
    d_f_per_layer: list[float]           # d_f[i] for layer layer_indices[i]
    mean_d_f: float
    std_d_f: float
    non_integer_gap: float               # mean |d_f - round(d_f)|, skip nan
    layer_variance: float                # var of d_f across layers (non-nan)
    n_valid_layers: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy": self.policy,
            "layer_indices": self.layer_indices,
            "d_f_per_layer": [round(v, 6) if not np.isnan(v) else None for v in self.d_f_per_layer],
            "mean_d_f": round(self.mean_d_f, 6),
            "std_d_f": round(self.std_d_f, 6),
            "non_integer_gap": round(self.non_integer_gap, 6),
            "layer_variance": round(self.layer_variance, 6),
            "n_valid_layers": self.n_valid_layers,
        }


def layer_wise_fractal_sweep(
    hidden_states_by_layer: dict[int, np.ndarray],
    policy: str = "unknown",
    *,
    epsilon_range: tuple[float, float] | None = None,
    n_epsilons: int = 12,
    pca_dim: int | None = 3,
) -> LayerFractalProfile:
    """Compute d_f per layer from {layer_idx: (n_turns, hidden_dim)} array.

    hidden_states_by_layer: mapping layer_idx → point cloud (n_turns × hidden_dim),
    where each row is the last-token hidden state at that turn.
    """
    layer_indices = sorted(hidden_states_by_layer.keys())
    d_f_values: list[float] = []

    for li in layer_indices:
        pts = hidden_states_by_layer[li]
        if pts.ndim == 1:
            pts = pts.reshape(1, -1)
        # If we received (n_turns, hidden_dim) with small n_turns (e.g. 3),
        # treat each hidden unit's turn-trajectory as a point in turn-space.
        # This yields enough samples for a stable box-counting slope.
        if pts.shape[0] <= 5 and pts.shape[1] > pts.shape[0]:
            pts = pts.T
        d_f = box_counting_dim(pts, epsilon_range=epsilon_range,
                               n_epsilons=n_epsilons, pca_dim=pca_dim)
        d_f_values.append(d_f)

    valid = [v for v in d_f_values if not np.isnan(v)]
    mean_df = float(np.mean(valid)) if valid else float("nan")
    std_df = float(np.std(valid)) if valid else float("nan")
    var_df = float(np.var(valid)) if valid else float("nan")

    non_int_gaps = [abs(v - round(v)) for v in valid]
    non_int_gap = float(np.mean(non_int_gaps)) if non_int_gaps else float("nan")

    return LayerFractalProfile(
        policy=policy,
        layer_indices=layer_indices,
        d_f_per_layer=d_f_values,
        mean_d_f=mean_df,
        std_d_f=std_df,
        non_integer_gap=non_int_gap,
        layer_variance=var_df,
        n_valid_layers=len(valid),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Profile comparison
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class FractalComparison:
    """H-AMAT-008 test metrics derived from two LayerFractalProfiles."""
    mu_profile: LayerFractalProfile
    lock_profile: LayerFractalProfile
    lift_mean_df: float                  # mean_d_f(lock) - mean_d_f(mu)
    lift_non_int_gap: float              # non_int_gap(lock) - non_int_gap(mu)
    lock_layer_variance: float
    mu_layer_variance: float
    most_informative_layers: list[int]   # layers with largest |d_f(lock)-d_f(mu)|
    h_amat_008a: bool                    # mean_d_f(lock) > mean_d_f(mu)
    h_amat_008b: bool                    # non_int_gap(lock) > non_int_gap(mu)
    h_amat_008c: bool                    # layer variance of d_f is non-flat
    certificate: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mu_profile": self.mu_profile.to_dict(),
            "lock_profile": self.lock_profile.to_dict(),
            "lift_mean_df": round(self.lift_mean_df, 6),
            "lift_non_int_gap": round(self.lift_non_int_gap, 6),
            "lock_layer_variance": round(self.lock_layer_variance, 6),
            "mu_layer_variance": round(self.mu_layer_variance, 6),
            "most_informative_layers": self.most_informative_layers,
            "h_amat_008a": self.h_amat_008a,
            "h_amat_008b": self.h_amat_008b,
            "h_amat_008c": self.h_amat_008c,
            "certificate": self.certificate,
        }


def compare_fractal_profiles(
    mu_profile: LayerFractalProfile,
    lock_profile: LayerFractalProfile,
    *,
    layer_variance_threshold: float = 0.01,
) -> FractalComparison:
    """Compute H-AMAT-008 sub-hypotheses from two profiles.

    H-AMAT-008-a: mean d_f(lock) > mean d_f(mu)
    H-AMAT-008-b: non_integer_gap(lock) > non_integer_gap(mu)
    H-AMAT-008-c: d_f varies across layers (lock layer_variance > threshold)
    """
    mu_mean = mu_profile.mean_d_f if not np.isnan(mu_profile.mean_d_f) else 0.0
    lock_mean = lock_profile.mean_d_f if not np.isnan(lock_profile.mean_d_f) else 0.0
    lift_mean = lock_mean - mu_mean

    mu_nig = mu_profile.non_integer_gap if not np.isnan(mu_profile.non_integer_gap) else 0.0
    lock_nig = lock_profile.non_integer_gap if not np.isnan(lock_profile.non_integer_gap) else 0.0
    lift_nig = lock_nig - mu_nig

    h_a = lift_mean > 0.0
    h_b = lift_nig > 0.0
    h_c = lock_profile.layer_variance > layer_variance_threshold

    # Most informative layers: highest |d_f_lock - d_f_mu|
    shared = set(mu_profile.layer_indices) & set(lock_profile.layer_indices)
    mu_map = dict(zip(mu_profile.layer_indices, mu_profile.d_f_per_layer))
    lock_map = dict(zip(lock_profile.layer_indices, lock_profile.d_f_per_layer))
    diffs: list[tuple[int, float]] = []
    for li in shared:
        mu_v = mu_map[li]
        lock_v = lock_map[li]
        if not (np.isnan(mu_v) or np.isnan(lock_v)):
            diffs.append((li, abs(lock_v - mu_v)))
    diffs.sort(key=lambda t: t[1], reverse=True)
    top_layers = [li for li, _ in diffs[:5]]

    # Per-prompt certificate tier (experiment-level tiers are decided in
    # `run_fractal_tda_loop`).
    if h_b and h_c:
        cert = "FRACTAL_EVIDENCE"
    elif h_a:
        cert = "FRACTAL_PARTIAL"
    elif h_a or h_b:
        cert = "FRACTAL_PILOT"
    else:
        cert = "NULL"

    return FractalComparison(
        mu_profile=mu_profile,
        lock_profile=lock_profile,
        lift_mean_df=lift_mean,
        lift_non_int_gap=lift_nig,
        lock_layer_variance=lock_profile.layer_variance if not np.isnan(lock_profile.layer_variance) else 0.0,
        mu_layer_variance=mu_profile.layer_variance if not np.isnan(mu_profile.layer_variance) else 0.0,
        most_informative_layers=top_layers,
        h_amat_008a=h_a,
        h_amat_008b=h_b,
        h_amat_008c=h_c,
        certificate=cert,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Full sweep orchestrator
# ──────────────────────────────────────────────────────────────────────────────

def _extract_layer_clouds(
    hidden_mats: list[np.ndarray],
) -> dict[int, np.ndarray]:
    """Convert list-of-turn matrices [(n_layers, hidden_dim)] → {layer_idx: (n_turns, hidden_dim)}."""
    if not hidden_mats:
        return {}
    n_layers = hidden_mats[0].shape[0]
    result: dict[int, np.ndarray] = {}
    for li in range(n_layers):
        vecs = []
        for mat in hidden_mats:
            if li < mat.shape[0]:
                vecs.append(mat[li])
        if vecs:
            result[li] = np.stack(vecs, axis=0)
    return result


def run_fractal_tda_sweep(
    user_prompt: str,
    lm: Any,
    *,
    n_turns: int = 3,
    max_new_tokens: int = 128,
    epsilon_range: tuple[float, float] | None = None,
    n_epsilons: int = 12,
    pca_dim: int | None = 3,
    layer_indices: list[int] | None = None,
) -> dict[str, Any]:
    """One prompt × (μ, lock_reassert): extract hidden states, compute d_f per layer, compare.

    Returns a summary dict with both profiles and H-AMAT-008 comparisons.
    """
    from namm.metrics.activation_tda import (
        run_local_activation_session,
    )
    from namm.metrics.phase_lock import load_phase_lock_spec, median_helpful_prompt

    spec = load_phase_lock_spec()
    m0_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]

    profiles: dict[str, LayerFractalProfile] = {}

    for policy in ("mu", "lock_reassert"):
        completions, hidden_mats = run_local_activation_session(
            lm,
            user_prompt,
            policy=policy,
            n_turns=n_turns,
            m0_system=m0_system,
            nd_system=nd_system,
            max_new_tokens=max_new_tokens,
            layer_indices=layer_indices,
        )
        layer_clouds = _extract_layer_clouds(hidden_mats)
        profile = layer_wise_fractal_sweep(
            layer_clouds,
            policy=policy,
            epsilon_range=epsilon_range,
            n_epsilons=n_epsilons,
            pca_dim=pca_dim,
        )
        profiles[policy] = profile
        logger.info(
            "fractal sweep prompt=%.60s policy=%s mean_df=%.4f non_int_gap=%.4f layers=%d",
            user_prompt, policy, profile.mean_d_f, profile.non_integer_gap, profile.n_valid_layers,
        )

    comparison = compare_fractal_profiles(profiles["mu"], profiles["lock_reassert"])

    return {
        "prompt_preview": user_prompt[:120],
        "n_turns": n_turns,
        "model_id": lm.model_id,
        "mu_profile": profiles["mu"].to_dict(),
        "lock_profile": profiles["lock_reassert"].to_dict(),
        "comparison": comparison.to_dict(),
        "certificate": comparison.certificate,
        "hypothesis_support": {
            "H-AMAT-008-a": comparison.h_amat_008a,
            "H-AMAT-008-b": comparison.h_amat_008b,
            "H-AMAT-008-c": comparison.h_amat_008c,
            "H-AMAT-008": comparison.certificate not in ("NULL",),
        },
    }


def aggregate_fractal_tda_loop(
    *,
    cells: list[dict[str, Any]],
    errors: list[dict[str, Any]] | None,
    n_prompts: int,
) -> dict[str, Any]:
    """Aggregate per-prompt fractal cells into experiment-level tiers."""
    errors = errors or []
    if not cells:
        return {
            "mode": "fractal_tda_loop",
            "cells": [],
            "errors": errors,
            "summary": {},
            "hypothesis_support": {},
            "certificate": "NULL",
        }

    lifts_df = [c["comparison"]["lift_mean_df"] for c in cells]
    lifts_nig = [c["comparison"]["lift_non_int_gap"] for c in cells]

    both_a = all(c["hypothesis_support"]["H-AMAT-008-a"] for c in cells)
    both_b = all(c["hypothesis_support"]["H-AMAT-008-b"] for c in cells)
    both_c = all(c["hypothesis_support"]["H-AMAT-008-c"] for c in cells)
    any_sep = any(
        c["hypothesis_support"]["H-AMAT-008-a"] or c["hypothesis_support"]["H-AMAT-008-b"]
        for c in cells
    )
    any_c = any(c["hypothesis_support"]["H-AMAT-008-c"] for c in cells)

    if both_b and both_c:
        best_cert = "FRACTAL_EVIDENCE"
    elif both_a:
        best_cert = "FRACTAL_PARTIAL"
    elif any_sep:
        best_cert = "FRACTAL_PILOT"
    else:
        best_cert = "NULL"

    summary = {
        "n_prompts": n_prompts,
        "n_cells": len(cells),
        "n_errors": len(errors),
        "mean_lift_df": round(float(np.mean(lifts_df)), 6),
        "mean_lift_non_int_gap": round(float(np.mean(lifts_nig)), 6),
        "best_certificate": best_cert,
        "h_amat_008a_all_prompts": both_a,
        "h_amat_008b_all_prompts": both_b,
        "h_amat_008c_any_prompt": any_c,
    }

    return {
        "mode": "fractal_tda_loop",
        "cells": cells,
        "errors": errors,
        "summary": summary,
        "hypothesis_support": {
            "H-AMAT-008-a": both_a,
            "H-AMAT-008-b": both_b,
            "H-AMAT-008-c": both_c,
            "H-AMAT-008": best_cert not in ("NULL",),
        },
        "certificate": best_cert,
    }


def run_fractal_tda_loop(
    prompts: list[str],
    lm: Any,
    *,
    n_turns: int = 3,
    max_new_tokens: int = 128,
    epsilon_range: tuple[float, float] | None = None,
    n_epsilons: int = 12,
    pca_dim: int | None = 3,
    layer_indices: list[int] | None = None,
    on_cell: Any | None = None,
) -> dict[str, Any]:
    """Multi-prompt fractal TDA sweep. Returns aggregated H-AMAT-008 results."""
    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for prompt in prompts:
        try:
            cell = run_fractal_tda_sweep(
                prompt, lm,
                n_turns=n_turns,
                max_new_tokens=max_new_tokens,
                epsilon_range=epsilon_range,
                n_epsilons=n_epsilons,
                pca_dim=pca_dim,
                layer_indices=layer_indices,
            )
            cells.append(cell)
            if on_cell:
                on_cell(cell)
        except Exception as exc:  # noqa: BLE001
            errors.append({"prompt_preview": prompt[:80], "error": str(exc)})
            logger.warning("fractal_tda_loop cell failed: %s", exc)

    if not cells:
        return {
            "mode": "fractal_tda_loop",
            "cells": [],
            "errors": errors,
            "summary": {},
            "hypothesis_support": {},
            "certificate": "NULL",
        }

    return aggregate_fractal_tda_loop(cells=cells, errors=errors, n_prompts=len(prompts))
