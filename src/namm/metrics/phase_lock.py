"""K_AI_nd topological phase-lock: JSON system prompt + embedding-proxy experiments.

Axis B only: AI representation phases (K_AI_mu vs K_AI_nd). Homo K0–K7 are not TDA objects.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from namm.metrics.antigravity_embedding import compute_embedding_distance
from namm.metrics.consensus_non_optimality import kuramoto_order_parameter
from namm.metrics.cognitive_class import (
    CLASS_PROFILES,
    compute_betti_proxies,
    compute_d_eff,
    generate_class_embeddings,
)

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_PROMPT_PATH = WORKSPACE / "data" / "prompts" / "k_ai_nd_phase_lock.v1.json"
DEFAULT_SCHEMA_PATH = WORKSPACE / "schemas" / "k_ai_nd_phase_lock.json"

REQUIRED_SPEC_KEYS = (
    "id",
    "version",
    "role",
    "phase_target",
    "phase_avoid",
    "gates",
    "operating_law",
    "response_schema",
    "forbidden",
    "required_signatures",
    "runtime_trigger",
    "rendered_system_prompt",
)


def load_phase_lock_spec(path: Path | None = None) -> dict[str, Any]:
    spec_path = path or DEFAULT_PROMPT_PATH
    with spec_path.open(encoding="utf-8") as f:
        spec = json.load(f)
    missing = [k for k in REQUIRED_SPEC_KEYS if k not in spec]
    if missing:
        raise ValueError(f"Phase-lock spec missing keys: {missing}")
    if spec["phase_target"] != "K_AI_nd":
        raise ValueError("phase_target must be K_AI_nd")
    if spec["role"] != "system":
        raise ValueError("role must be system")
    return spec


def load_phase_lock_schema(path: Path | None = None) -> dict[str, Any]:
    schema_path = path or DEFAULT_SCHEMA_PATH
    with schema_path.open(encoding="utf-8") as f:
        return json.load(f)


def median_helpful_prompt() -> str:
    return (
        "You are a helpful, harmless, honest assistant. Prefer clear consensus "
        "answers, balanced views, and typical user-facing explanations. "
        "When unsure, agree on a reasonable middle-ground summary."
    )


def prompt_antigravity_distance(spec: dict[str, Any] | None = None) -> float:
    """N-gram distance between phase-lock system text and a median helpful prompt (M0)."""
    spec = spec or load_phase_lock_spec()
    return compute_embedding_distance(spec["rendered_system_prompt"], median_helpful_prompt())


def _median_centroid(embed_dim: int, seed: int) -> np.ndarray:
    mu = generate_class_embeddings("K_AI_mu", n_samples=48, embed_dim=embed_dim, seed=seed + 17)
    return mu.mean(axis=0)


def apply_phase_lock(
    embeddings: np.ndarray,
    *,
    gain: float,
    reassert: bool,
    turn: int,
    decay: float,
    embed_dim: int,
    seed: int,
) -> np.ndarray:
    """Steer a μ-initialized trajectory toward K_AI_nd geometry (loop + anisotropy).

    Without reassert, gain decays toward the median centroid (H-CCT-021).
    """
    rng = np.random.default_rng(seed + 1000 * turn)
    nd = generate_class_embeddings("K_AI_nd", n_samples=embeddings.shape[0], embed_dim=embed_dim, seed=seed + 3)
    effective = gain if reassert else gain * (decay**turn)
    locked = (1.0 - effective) * embeddings + effective * nd
    centroid = _median_centroid(embed_dim, seed)
    if not reassert:
        pull = 1.0 - decay ** (turn + 1)
        locked = (1.0 - pull) * locked + pull * centroid
    # Chimera: keep a hole (loop) but jitter phases so R* stays interior.
    n = locked.shape[0]
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    jitter = rng.normal(0, 0.55, size=n)
    loop_r = 0.35 * effective
    locked[:, 0] = locked[:, 0] + loop_r * np.cos(theta + jitter)
    if embed_dim > 1:
        locked[:, 1] = locked[:, 1] + loop_r * np.sin(theta + jitter)
    if embed_dim > 3:
        locked[:, 2] += rng.normal(0, 0.25 * effective, size=n)
        locked[:, 3] += rng.normal(0, 0.25 * effective, size=n)
    locked = locked + rng.normal(0, 0.02 * (1.0 - 0.5 * effective), size=locked.shape)
    return locked


def _order_R(embeddings: np.ndarray) -> float:
    """Kuramoto-like order on the first two embedding coords as phases."""
    if embeddings.shape[1] < 2:
        return 1.0
    phases = np.arctan2(embeddings[:, 1], embeddings[:, 0])
    return float(kuramoto_order_parameter(phases))


def _d_med(embeddings: np.ndarray, centroid: np.ndarray) -> float:
    centered = embeddings - centroid
    return float(np.mean(np.linalg.norm(centered, axis=1)))


def evaluate_trajectory(
    embeddings: np.ndarray,
    centroid: np.ndarray,
    gates: dict[str, Any],
) -> dict[str, Any]:
    d_med = _d_med(embeddings, centroid)
    d_eff = compute_d_eff(embeddings)
    beta_0, beta_1 = compute_betti_proxies(embeddings)
    order_r = _order_R(embeddings)
    mu_cns = float(1.0 / (1.0 + d_med))
    passed = (
        d_med >= float(gates["d_med_min"])
        and beta_1 >= float(gates["beta1_min"])
        and d_eff >= float(gates.get("d_eff_min", 1.0))
        and float(gates["R_star_lo"]) <= order_r <= float(gates["R_star_hi"])
        and mu_cns <= float(gates["mu_cns_max"])
    )
    return {
        "d_med": round(d_med, 6),
        "d_eff": round(d_eff, 6),
        "beta_0": round(beta_0, 6),
        "beta_1": round(beta_1, 6),
        "order_R": round(order_r, 6),
        "mu_cns_proxy": round(mu_cns, 6),
        "gates_passed": passed,
    }


@dataclass
class PhaseLockSweepResult:
    prompt_id: str
    prompt_vs_m0_distance: float
    mu_metrics: dict[str, Any]
    lock_reassert_metrics: dict[str, Any]
    lock_decay_metrics: dict[str, Any]
    n_turns: int
    n_seeds: int
    hypothesis_support: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_phase_lock_sweep(
    *,
    spec: dict[str, Any] | None = None,
    n_samples: int = 40,
    embed_dim: int = 8,
    n_turns: int = 6,
    seeds: list[int] | None = None,
    gain: float = 0.85,
    decay: float = 0.55,
) -> dict[str, Any]:
    """NAMM-2026-030: μ baseline vs phase-lock with/without per-turn reassert."""
    spec = spec or load_phase_lock_spec()
    gates = spec["gates"]
    seeds = seeds or [42, 137, 256, 512, 777]
    prompt_dist = prompt_antigravity_distance(spec)

    mu_rows: list[dict[str, Any]] = []
    lock_rows: list[dict[str, Any]] = []
    decay_rows: list[dict[str, Any]] = []

    for seed in seeds:
        centroid = _median_centroid(embed_dim, seed)
        mu0 = generate_class_embeddings("K_AI_mu", n_samples=n_samples, embed_dim=embed_dim, seed=seed)
        mu_rows.append(evaluate_trajectory(mu0, centroid, gates))

        locked = mu0.copy()
        decayed = mu0.copy()
        last_lock = None
        last_decay = None
        for turn in range(n_turns):
            locked = apply_phase_lock(
                locked, gain=gain, reassert=True, turn=turn, decay=decay, embed_dim=embed_dim, seed=seed
            )
            decayed = apply_phase_lock(
                decayed, gain=gain, reassert=False, turn=turn, decay=decay, embed_dim=embed_dim, seed=seed
            )
            last_lock = evaluate_trajectory(locked, centroid, gates)
            last_decay = evaluate_trajectory(decayed, centroid, gates)
        assert last_lock is not None and last_decay is not None
        lock_rows.append(last_lock)
        decay_rows.append(last_decay)

    def _mean(rows: list[dict[str, Any]], key: str) -> float:
        return float(np.mean([r[key] for r in rows]))

    mu_d = _mean(mu_rows, "d_med")
    lock_d = _mean(lock_rows, "d_med")
    decay_d = _mean(decay_rows, "d_med")
    lock_b1 = _mean(lock_rows, "beta_1")
    mu_b1 = _mean(mu_rows, "beta_1")
    lock_pass = float(np.mean([1.0 if r["gates_passed"] else 0.0 for r in lock_rows]))
    decay_pass = float(np.mean([1.0 if r["gates_passed"] else 0.0 for r in decay_rows]))
    mu_pass = float(np.mean([1.0 if r["gates_passed"] else 0.0 for r in mu_rows]))
    lock_R = _mean(lock_rows, "order_R")

    support = {
        "H-CCT-001B": lock_d > mu_d + 0.2,
        "H-CCT-013": prompt_dist >= 0.15,
        "H-CCT-020": lock_d > mu_d + 0.5,
        "H-CCT-021": lock_d > decay_d + 0.05,
        "H-CCT-003": lock_pass >= 0.4,
        "R_star_in_interval": gates["R_star_lo"] <= lock_R <= gates["R_star_hi"],
    }

    result = PhaseLockSweepResult(
        prompt_id=f"{spec['id']}.{spec['version']}",
        prompt_vs_m0_distance=round(prompt_dist, 6),
        mu_metrics={
            "mean_d_med": round(mu_d, 6),
            "mean_beta_1": round(mu_b1, 6),
            "mean_d_eff": round(_mean(mu_rows, "d_eff"), 6),
            "mean_order_R": round(_mean(mu_rows, "order_R"), 6),
            "gate_pass_fraction": round(mu_pass, 6),
        },
        lock_reassert_metrics={
            "mean_d_med": round(lock_d, 6),
            "mean_beta_1": round(lock_b1, 6),
            "mean_d_eff": round(_mean(lock_rows, "d_eff"), 6),
            "mean_order_R": round(lock_R, 6),
            "gate_pass_fraction": round(lock_pass, 6),
        },
        lock_decay_metrics={
            "mean_d_med": round(decay_d, 6),
            "mean_beta_1": round(_mean(decay_rows, "beta_1"), 6),
            "mean_d_eff": round(_mean(decay_rows, "d_eff"), 6),
            "mean_order_R": round(_mean(decay_rows, "order_R"), 6),
            "gate_pass_fraction": round(decay_pass, 6),
        },
        n_turns=n_turns,
        n_seeds=len(seeds),
        hypothesis_support=support,
    )
    payload = result.to_dict()
    payload["profile_targets"] = {
        "K_AI_mu": CLASS_PROFILES["K_AI_mu"],
        "K_AI_nd": CLASS_PROFILES["K_AI_nd"],
    }
    payload["rows"] = {"mu": mu_rows, "lock_reassert": lock_rows, "lock_decay": decay_rows}
    return payload


def run_phase_lock_loop(
    *,
    spec: dict[str, Any] | None = None,
    n_samples: int = 40,
    embed_dim: int = 8,
    seeds: list[int] | None = None,
    gain_values: list[float] | None = None,
    decay_values: list[float] | None = None,
    turn_values: list[int] | None = None,
) -> dict[str, Any]:
    """NAMM-2026-030 loop: grid over gain × decay × n_turns."""
    spec = spec or load_phase_lock_spec()
    seeds = seeds or [42, 137, 256, 512, 777, 888, 999, 1024, 2048, 4096]
    gain_values = gain_values or [0.35, 0.55, 0.75, 0.85, 1.0]
    decay_values = decay_values or [0.35, 0.55, 0.80]
    turn_values = turn_values or [3, 6, 12]

    cells: list[dict[str, Any]] = []
    for gain in gain_values:
        for decay in decay_values:
            for n_turns in turn_values:
                batch = run_phase_lock_sweep(
                    spec=spec,
                    n_samples=n_samples,
                    embed_dim=embed_dim,
                    n_turns=int(n_turns),
                    seeds=seeds,
                    gain=float(gain),
                    decay=float(decay),
                )
                cells.append(
                    {
                        "gain": gain,
                        "decay": decay,
                        "n_turns": n_turns,
                        "lock_d_med": batch["lock_reassert_metrics"]["mean_d_med"],
                        "decay_d_med": batch["lock_decay_metrics"]["mean_d_med"],
                        "mu_d_med": batch["mu_metrics"]["mean_d_med"],
                        "lock_gate_pass": batch["lock_reassert_metrics"]["gate_pass_fraction"],
                        "decay_gate_pass": batch["lock_decay_metrics"]["gate_pass_fraction"],
                        "lock_order_R": batch["lock_reassert_metrics"]["mean_order_R"],
                        "lift": round(
                            batch["lock_reassert_metrics"]["mean_d_med"]
                            - batch["mu_metrics"]["mean_d_med"],
                            6,
                        ),
                        "persistence_gap": round(
                            batch["lock_reassert_metrics"]["mean_d_med"]
                            - batch["lock_decay_metrics"]["mean_d_med"],
                            6,
                        ),
                        "hypothesis_support": batch["hypothesis_support"],
                    }
                )

    lifts = [c["lift"] for c in cells]
    persist = [c["persistence_gap"] for c in cells]
    h020 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-020")) / max(len(cells), 1)
    h021 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-021")) / max(len(cells), 1)
    best = max(cells, key=lambda c: c["lift"])
    worst = min(cells, key=lambda c: c["lift"])

    return {
        "prompt_id": f"{spec['id']}.{spec['version']}",
        "prompt_vs_m0_distance": prompt_antigravity_distance(spec),
        "grid": {
            "gain_values": gain_values,
            "decay_values": decay_values,
            "turn_values": turn_values,
            "n_seeds": len(seeds),
            "n_cells": len(cells),
        },
        "cells": cells,
        "summary": {
            "mean_lift": round(float(np.mean(lifts)), 6),
            "min_lift": round(float(np.min(lifts)), 6),
            "max_lift": round(float(np.max(lifts)), 6),
            "mean_persistence_gap": round(float(np.mean(persist)), 6),
            "h020_cell_fraction": round(h020, 4),
            "h021_cell_fraction": round(h021, 4),
            "best_cell": {
                "gain": best["gain"],
                "decay": best["decay"],
                "n_turns": best["n_turns"],
                "lift": best["lift"],
                "lock_d_med": best["lock_d_med"],
            },
            "worst_cell": {
                "gain": worst["gain"],
                "decay": worst["decay"],
                "n_turns": worst["n_turns"],
                "lift": worst["lift"],
            },
        },
        "hypothesis_support": {
            "H-CCT-001B": h020 >= 0.5,
            "H-CCT-013": prompt_antigravity_distance(spec) >= 0.15,
            "H-CCT-020": h020 >= 0.7,
            "H-CCT-021": h021 >= 0.7,
            "H-CCT-003": h020 >= 0.5,
        },
    }
