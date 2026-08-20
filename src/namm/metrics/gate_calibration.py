"""Live embedding gate calibration: μ-policy null distribution → recalibrated RPL gates."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Callable

import numpy as np
from scipy.stats import spearmanr

from namm.llm.client import embed_batch, get_client
from namm.llm.registry import is_provider_configured, provider_config
from namm.metrics.live_embeddings import (
    FOCUSED_PROMPTS,
    _reference_texts,
    distance_from_typicality,
    median_helpful_prompt,
    run_live_session,
    run_phase_lock_live_sweep,
)
from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec


def _other_gates_pass(metrics: dict[str, Any], gates: dict[str, Any]) -> bool:
    return (
        metrics["beta_1"] >= float(gates["beta1_min"])
        and metrics["d_eff"] >= float(gates.get("d_eff_min", 1.0))
        and float(gates["R_star_lo"]) <= metrics["order_R"] <= float(gates["R_star_hi"])
        and metrics["mu_cns_proxy"] <= float(gates["mu_cns_max"])
    )


def calibrate_gates(null_d_med: list[float], cfg: dict[str, Any]) -> dict[str, Any]:
    """Compute percentile / z-score thresholds from μ-policy null d_med samples."""
    arr = np.asarray(null_d_med, dtype=float)
    if arr.size == 0:
        raise ValueError("null_d_med must be non-empty")
    pct = float(cfg.get("percentile", 0.95))
    z_min = float(cfg.get("z_score_min", 2.0))
    return {
        "legacy_d_med_min": float(cfg.get("legacy_d_med_min", 1.2)),
        "percentile": pct,
        "percentile_threshold": round(float(np.percentile(arr, pct * 100)), 6),
        "z_score_min": z_min,
        "z_score_threshold": round(float(arr.mean() + z_min * arr.std(ddof=0)), 6),
        "lift_ratio_min": float(cfg.get("lift_ratio_min", 1.08)),
        "null_n": int(arr.size),
        "null_mean": round(float(arr.mean()), 6),
        "null_std": round(float(arr.std(ddof=0)), 6),
        "null_min": round(float(arr.min()), 6),
        "null_max": round(float(arr.max()), 6),
    }


def evaluate_calibrated_pass(
    lock_metrics: dict[str, Any],
    *,
    mu_d_med: float,
    thresholds: dict[str, Any],
    base_gates: dict[str, Any],
) -> dict[str, Any]:
    """Compare legacy absolute gate vs percentile / z-score / lift-ratio methods."""
    d_med = float(lock_metrics["d_med"])
    legacy_d_min = float(thresholds["legacy_d_med_min"])
    other = _other_gates_pass(lock_metrics, base_gates)
    legacy_pass = d_med >= legacy_d_min and other

    pct_thr = float(thresholds["percentile_threshold"])
    z_thr = float(thresholds["z_score_threshold"])
    lift_min = float(thresholds["lift_ratio_min"])
    lift_ratio = d_med / mu_d_med if mu_d_med > 1e-9 else 0.0

    percentile_pass = d_med >= pct_thr and other
    z_score_pass = d_med >= z_thr and other
    lift_ratio_pass = lift_ratio >= lift_min
    calibrated_pass = percentile_pass or z_score_pass or lift_ratio_pass

    return {
        "legacy_gate_pass": legacy_pass,
        "calibrated_gate_pass": calibrated_pass,
        "percentile_pass": percentile_pass,
        "z_score_pass": z_score_pass,
        "lift_ratio_pass": lift_ratio_pass,
        "lift_ratio": round(lift_ratio, 6),
        "d_med": round(d_med, 6),
        "mu_d_med": round(mu_d_med, 6),
    }


def sample_mu_null_distribution(
    *,
    prompts: list[str] | None = None,
    n_seeds: int = 20,
    n_turns: int = 1,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    on_sample: Callable[[dict[str, Any]], None] | None = None,
    resume_indices: set[int] | None = None,
    preloaded_null_d_med: list[float] | None = None,
) -> dict[str, Any]:
    """Sample μ-policy d_med on focused prompts to build live null distribution."""
    prompts = prompts or FOCUSED_PROMPTS
    spec = load_phase_lock_spec()
    m0_system = median_helpful_prompt()
    client = get_client(
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
    )
    resume_indices = resume_indices or set()
    samples: list[dict[str, Any]] = []

    for seed_idx in range(n_seeds):
        if seed_idx in resume_indices:
            continue
        prompt = prompts[seed_idx % len(prompts)]
        refs = _reference_texts(prompt)
        b_star = embed_batch(refs, provider=client.embed_provider, model=client.embed_model).mean(axis=0)

        if skip_chat:
            pack = f"{m0_system}\n\nUser: {prompt}"
            vec = embed_batch([pack], provider=client.embed_provider, model=client.embed_model)
            d_med = distance_from_typicality(vec, b_star)
            completion_preview = pack[:120]
        else:
            completions, _ = run_live_session(
                prompt,
                policy="mu",
                n_turns=n_turns,
                client=client,
                m0_system=m0_system,
                nd_system=spec["rendered_system_prompt"],
                pause_s=pause_s,
            )
            mat = embed_batch(completions, provider=client.embed_provider, model=client.embed_model)
            d_med = distance_from_typicality(mat, b_star)
            completion_preview = completions[-1][:120] if completions else ""

        rec = {
            "seed_idx": seed_idx,
            "prompt_preview": prompt[:80],
            "d_med": round(float(d_med), 6),
            "completion_preview": completion_preview,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        samples.append(rec)
        if on_sample:
            on_sample(rec)
        if pause_s > 0 and not skip_chat and seed_idx + 1 < n_seeds:
            time.sleep(pause_s)

    d_vals = [s["d_med"] for s in samples]
    if preloaded_null_d_med:
        d_vals = list(preloaded_null_d_med) + d_vals
    return {
        "mode": "null_sampling" if not skip_chat else "null_sampling_prompt_only",
        "n_requested": n_seeds,
        "n_samples": len(samples),
        "samples": samples,
        "null_d_med": d_vals,
    }


def run_calibrated_live_sweep(
    user_prompt: str,
    *,
    n_turns: int,
    thresholds: dict[str, Any],
    base_gates: dict[str, Any] | None = None,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
) -> dict[str, Any]:
    """One prompt cell: live sweep + legacy vs calibrated gate comparison on lock policy."""
    spec = load_phase_lock_spec()
    base_gates = base_gates or spec["gates"]
    batch = run_phase_lock_live_sweep(
        user_prompt,
        n_turns=n_turns,
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
        pause_s=pause_s,
        skip_chat=skip_chat,
    )
    mu_d = batch["summary"]["mu_d_med"]
    lock_metrics = batch["policies"]["lock_reassert"]["metrics"]
    decay_metrics = batch["policies"]["lock_decay"]["metrics"]

    lock_cmp = evaluate_calibrated_pass(
        lock_metrics, mu_d_med=mu_d, thresholds=thresholds, base_gates=base_gates
    )
    decay_cmp = evaluate_calibrated_pass(
        decay_metrics, mu_d_med=mu_d, thresholds=thresholds, base_gates=base_gates
    )

    summary = {
        **batch["summary"],
        "legacy_lock_gate_pass": lock_cmp["legacy_gate_pass"],
        "calibrated_lock_gate_pass": lock_cmp["calibrated_gate_pass"],
        "legacy_decay_gate_pass": decay_cmp["legacy_gate_pass"],
        "calibrated_decay_gate_pass": decay_cmp["calibrated_gate_pass"],
        "lock_gate_detail": lock_cmp,
        "decay_gate_detail": decay_cmp,
    }
    return {**batch, "summary": summary, "gate_comparison": {"lock": lock_cmp, "decay": decay_cmp}}


def run_gate_calibration_loop(
    *,
    prompts: list[str] | None = None,
    turn_values: list[int] | None = None,
    thresholds: dict[str, Any],
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    on_cell: Callable[[dict[str, Any], dict[str, Any]], None] | None = None,
    resume_keys: set[tuple[str, int]] | None = None,
) -> dict[str, Any]:
    """Grid: prompts × n_turns with calibrated vs legacy gate pass comparison."""
    prompts = prompts or FOCUSED_PROMPTS
    turn_values = turn_values or [3, 6]
    resume_keys = resume_keys or set()
    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for prompt in prompts:
        for n_turns in turn_values:
            key = (prompt, int(n_turns))
            if key in resume_keys:
                continue
            try:
                batch = run_calibrated_live_sweep(
                    prompt,
                    n_turns=int(n_turns),
                    thresholds=thresholds,
                    chat_provider=chat_provider,
                    embed_provider=embed_provider,
                    chat_model=chat_model,
                    embed_model=embed_model,
                    pause_s=pause_s,
                    skip_chat=skip_chat,
                )
            except Exception as exc:  # noqa: BLE001
                errors.append({"prompt_preview": prompt[:80], "n_turns": n_turns, "error": str(exc)})
                continue

            cell = {
                "prompt_hash": hash(prompt) & 0xFFFF,
                "prompt_preview": prompt[:80],
                "n_turns": n_turns,
                **batch["summary"],
                "hypothesis_support": batch["hypothesis_support"],
            }
            cells.append(cell)
            if on_cell:
                on_cell(cell, batch)

    if not cells:
        return {
            "protocol": "amat-gate-calibration-v1",
            "mode": "live_completions" if not skip_chat else "prompt_only",
            "grid": {"n_prompts": len(prompts), "turn_values": turn_values, "n_cells": 0},
            "cells": [],
            "errors": errors,
            "summary": {},
            "hypothesis_support": {},
        }

    lifts = [c["lift"] for c in cells]
    legacy_lock = [1.0 if c.get("legacy_lock_gate_pass") else 0.0 for c in cells]
    cal_lock = [1.0 if c.get("calibrated_lock_gate_pass") else 0.0 for c in cells]
    h020 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-020")) / len(cells)
    h021 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-021")) / len(cells)

    summary_out = {
        "mean_lift": round(float(np.mean(lifts)), 6),
        "min_lift": round(float(np.min(lifts)), 6),
        "max_lift": round(float(np.max(lifts)), 6),
        "mean_persistence_gap": round(float(np.mean([c["persistence_gap"] for c in cells])), 6),
        "legacy_lock_gate_pass_fraction": round(float(np.mean(legacy_lock)), 4),
        "calibrated_lock_gate_pass_fraction": round(float(np.mean(cal_lock)), 4),
        "h020_cell_fraction": round(h020, 4),
        "h021_cell_fraction": round(h021, 4),
        "best_cell": max(cells, key=lambda c: c["lift"]),
        "n_errors": len(errors),
    }

    return {
        "protocol": "amat-gate-calibration-v1",
        "mode": "live_completions" if not skip_chat else "prompt_only",
        "grid": {"n_prompts": len(prompts), "turn_values": turn_values, "n_cells": len(cells)},
        "cells": cells,
        "errors": errors,
        "summary": summary_out,
        "hypothesis_support": {
            "H-CCT-020": h020 >= 0.6,
            "H-CCT-021": h021 >= 0.6,
            "H-AMAT-004": h020 >= 0.6,
            "H-AMAT-005": summary_out["calibrated_lock_gate_pass_fraction"]
            > summary_out["legacy_lock_gate_pass_fraction"],
        },
    }


def resolve_embedders_for_sweep(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolve embedder list: openai required; openrouter if key present; skip jina without key."""
    emb_cfg = cfg.get("embedders") or {}
    required = list(emb_cfg.get("required", ["openai"]))
    optional = list(emb_cfg.get("try_if_configured", ["openrouter"]))
    skip_without_key = set(emb_cfg.get("skip_without_key", ["jina"]))

    resolved: list[dict[str, Any]] = []
    seen: set[str] = set()

    def _append(name: str) -> None:
        if name in seen:
            return
        if name in skip_without_key and not is_provider_configured(name):
            return
        if not is_provider_configured(name):
            if name in required:
                raise RuntimeError(f"Required embedder {name!r} is not configured")
            return
        pcfg = provider_config(name)
        resolved.append(
            {
                "provider": name,
                "model": pcfg.get("default_embed") or (pcfg.get("embed_models") or [None])[0],
            }
        )
        seen.add(name)

    for name in required:
        _append(name)
    for name in optional:
        _append(name)
    if not resolved:
        raise RuntimeError("No embedders available for multi-embedder sweep")
    return resolved


def compute_sweep_from_completions(
    user_prompt: str,
    *,
    n_turns: int,
    completions_by_policy: dict[str, list[str]],
    embed_provider: str,
    embed_model: str | None = None,
) -> dict[str, Any]:
    """Re-embed shared chat completions under one embedder; return sweep summary + gate fields."""
    spec = load_phase_lock_spec()
    gates = spec["gates"]
    refs = _reference_texts(user_prompt)
    b_star = embed_batch(refs, provider=embed_provider, model=embed_model).mean(axis=0)

    rows: dict[str, Any] = {}
    for policy, completions in completions_by_policy.items():
        if not completions:
            continue
        mat = embed_batch(completions, provider=embed_provider, model=embed_model)
        metrics = _trajectory_metrics(mat, b_star, gates)
        metrics["n_turns"] = len(completions)
        rows[policy] = {"metrics": metrics, "completions": completions}

    mu_d = rows["mu"]["metrics"]["d_med"]
    lock_d = rows["lock_reassert"]["metrics"]["d_med"]
    decay_d = rows["lock_decay"]["metrics"]["d_med"]
    lift = lock_d - mu_d
    persistence = lock_d - decay_d
    return {
        "user_prompt": user_prompt,
        "n_turns": n_turns,
        "embed_provider": embed_provider,
        "embed_model": embed_model,
        "policies": rows,
        "summary": {
            "mu_d_med": round(mu_d, 6),
            "lock_d_med": round(lock_d, 6),
            "decay_d_med": round(decay_d, 6),
            "lift": round(lift, 6),
            "persistence_gap": round(persistence, 6),
            "lock_gate_pass": rows["lock_reassert"]["metrics"]["gates_passed"],
            "decay_gate_pass": rows["lock_decay"]["metrics"]["gates_passed"],
        },
        "hypothesis_support": {
            "H-CCT-020": lift > 0.05,
            "H-CCT-021": persistence > 0.02,
            "H-AMAT-004": lift > 0.05,
        },
    }


def _trajectory_metrics(completion_embeddings: np.ndarray, b_star: np.ndarray, gates: dict[str, Any]) -> dict[str, Any]:
    if completion_embeddings.ndim == 1:
        completion_embeddings = completion_embeddings.reshape(1, -1)
    return evaluate_trajectory(completion_embeddings, b_star, gates)


def collect_shared_chat_grid(
    *,
    prompts: list[str],
    turn_values: list[int],
    chat_provider: str | None = None,
    chat_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    resume_keys: set[tuple[str, int]] | None = None,
    on_cell: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run chat once per (prompt, n_turns); store completions for multi-embedder re-embedding."""
    from namm.metrics.live_embeddings import run_live_session

    spec = load_phase_lock_spec()
    m0_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]
    client = get_client(chat_provider=chat_provider, chat_model=chat_model)
    resume_keys = resume_keys or set()
    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for prompt in prompts:
        for n_turns in turn_values:
            key = (prompt, int(n_turns))
            if key in resume_keys:
                continue
            try:
                completions_by_policy: dict[str, list[str]] = {}
                if skip_chat:
                    for policy in ("mu", "lock_reassert", "lock_decay"):
                        system = m0_system if policy == "mu" else nd_system
                        pack = f"{system}\n\nUser: {prompt}"
                        completions_by_policy[policy] = [pack]
                else:
                    for policy in ("mu", "lock_reassert", "lock_decay"):
                        comps, _ = run_live_session(
                            prompt,
                            policy=policy,  # type: ignore[arg-type]
                            n_turns=n_turns,
                            client=client,
                            m0_system=m0_system,
                            nd_system=nd_system,
                            pause_s=pause_s,
                        )
                        completions_by_policy[policy] = comps
                cells.append(
                    {
                        "prompt_hash": hash(prompt) & 0xFFFF,
                        "prompt_preview": prompt[:80],
                        "user_prompt": prompt,
                        "n_turns": n_turns,
                        "completions_by_policy": completions_by_policy,
                    }
                )
                if on_cell:
                    on_cell(cells[-1])
            except Exception as exc:  # noqa: BLE001
                errors.append({"prompt_preview": prompt[:80], "n_turns": n_turns, "error": str(exc)})

    return {
        "mode": "live_completions" if not skip_chat else "prompt_only",
        "chat_provider": client.chat_provider,
        "cells": cells,
        "errors": errors,
    }


def run_embedder_calibration_branch(
    embed_provider: str,
    *,
    embed_model: str | None,
    cal_cfg: dict[str, Any],
    shared_cells: list[dict[str, Any]],
    prompts: list[str],
    null_cfg: dict[str, Any],
    chat_provider: str | None = None,
    chat_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    on_null_sample: Callable[[dict[str, Any]], None] | None = None,
    resume_null_indices: set[int] | None = None,
    preloaded_null_d_med: list[float] | None = None,
) -> dict[str, Any]:
    """One embedder: μ-null distribution, thresholds, calibrated metrics on shared chat cells."""
    n_seeds = int(null_cfg.get("n_seeds", 20))
    resume_null_indices = resume_null_indices or set()

    null_batch = sample_mu_null_distribution(
        prompts=prompts[:3],
        n_seeds=n_seeds,
        n_turns=1,
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
        pause_s=pause_s,
        skip_chat=skip_chat,
        on_sample=on_null_sample,
        resume_indices=resume_null_indices,
        preloaded_null_d_med=preloaded_null_d_med,
    )
    thresholds = calibrate_gates(null_batch["null_d_med"], cal_cfg)
    spec = load_phase_lock_spec()
    base_gates = spec["gates"]

    cells_out: list[dict[str, Any]] = []
    for sc in shared_cells:
        full_prompt = sc.get("user_prompt") or _prompt_from_preview(sc, prompts)
        batch = compute_sweep_from_completions(
            full_prompt,
            n_turns=int(sc["n_turns"]),
            completions_by_policy=sc["completions_by_policy"],
            embed_provider=embed_provider,
            embed_model=embed_model,
        )
        lock_metrics = batch["policies"]["lock_reassert"]["metrics"]
        decay_metrics = batch["policies"]["lock_decay"]["metrics"]
        mu_d = batch["summary"]["mu_d_med"]
        lock_cmp = evaluate_calibrated_pass(
            lock_metrics, mu_d_med=mu_d, thresholds=thresholds, base_gates=base_gates
        )
        decay_cmp = evaluate_calibrated_pass(
            decay_metrics, mu_d_med=mu_d, thresholds=thresholds, base_gates=base_gates
        )
        cells_out.append(
            {
                "prompt_hash": sc["prompt_hash"],
                "prompt_preview": sc["prompt_preview"],
                "n_turns": sc["n_turns"],
                **batch["summary"],
                "legacy_lock_gate_pass": lock_cmp["legacy_gate_pass"],
                "calibrated_lock_gate_pass": lock_cmp["calibrated_gate_pass"],
                "lock_gate_detail": lock_cmp,
                "hypothesis_support": batch["hypothesis_support"],
            }
        )

    lifts = [c["lift"] for c in cells_out] if cells_out else [0.0]
    legacy_lock = [1.0 if c.get("legacy_lock_gate_pass") else 0.0 for c in cells_out]
    cal_lock = [1.0 if c.get("calibrated_lock_gate_pass") else 0.0 for c in cells_out]
    h020 = sum(1 for c in cells_out if c["hypothesis_support"].get("H-CCT-020")) / max(len(cells_out), 1)

    return {
        "embed_provider": embed_provider,
        "embed_model": embed_model,
        "null_batch": null_batch,
        "calibrated_thresholds": thresholds,
        "cells": cells_out,
        "summary": {
            "mean_lift": round(float(np.mean(lifts)), 6),
            "min_lift": round(float(np.min(lifts)), 6),
            "max_lift": round(float(np.max(lifts)), 6),
            "legacy_lock_gate_pass_fraction": round(float(np.mean(legacy_lock)), 4) if cells_out else 0.0,
            "calibrated_lock_gate_pass_fraction": round(float(np.mean(cal_lock)), 4) if cells_out else 0.0,
            "h020_cell_fraction": round(h020, 4),
            "null_n": thresholds["null_n"],
            "percentile_threshold": thresholds["percentile_threshold"],
        },
    }


def _prompt_from_preview(sc: dict[str, Any], prompts: list[str]) -> str:
    prev = sc.get("prompt_preview", "")
    for p in prompts:
        if p.startswith(prev[:40]) or prev in p:
            return p
    return prev


def compute_cross_embedder_analysis(
    branches: list[dict[str, Any]],
    *,
    lift_agreement_min: float = 0.03,
    min_embedders_for_agreement: int = 2,
) -> dict[str, Any]:
    """Rank correlation of per-cell lift and agreement fraction across embedders."""
    if len(branches) < 2:
        return {
            "n_embedders": len(branches),
            "pairwise_spearman": {},
            "mean_spearman_rho": None,
            "lift_agreement_fraction": None,
            "lift_agreement_min": lift_agreement_min,
        }

    # key cells by (prompt_hash, n_turns)
    by_key: dict[tuple[int, int], dict[str, float]] = {}
    for br in branches:
        name = br["embed_provider"]
        for cell in br["cells"]:
            key = (int(cell["prompt_hash"]), int(cell["n_turns"]))
            by_key.setdefault(key, {})[name] = float(cell["lift"])

    keys = sorted(by_key.keys())
    embedder_names = [b["embed_provider"] for b in branches]
    pairwise: dict[str, float] = {}
    rhos: list[float] = []
    for i, a in enumerate(embedder_names):
        for b in embedder_names[i + 1 :]:
            xs = [by_key[k].get(a, np.nan) for k in keys]
            ys = [by_key[k].get(b, np.nan) for k in keys]
            valid = [(x, y) for x, y in zip(xs, ys) if not (np.isnan(x) or np.isnan(y))]
            if len(valid) < 2:
                continue
            xv, yv = zip(*valid)
            rho, _ = spearmanr(xv, yv)
            if not np.isnan(rho):
                pairwise[f"{a}__{b}"] = round(float(rho), 4)
                rhos.append(float(rho))

    agreement_count = 0
    for key in keys:
        lifts = [by_key[key].get(n, -999.0) for n in embedder_names if n in by_key[key]]
        if sum(1 for lv in lifts if lv > lift_agreement_min) >= min_embedders_for_agreement:
            agreement_count += 1
    agreement_frac = agreement_count / max(len(keys), 1)

    return {
        "n_embedders": len(branches),
        "n_cells": len(keys),
        "embedder_names": embedder_names,
        "pairwise_spearman": pairwise,
        "mean_spearman_rho": round(float(np.mean(rhos)), 4) if rhos else None,
        "lift_agreement_fraction": round(agreement_frac, 4),
        "lift_agreement_min": lift_agreement_min,
        "min_embedders_for_agreement": min_embedders_for_agreement,
        "per_cell_lifts": {f"{k[0]}_{k[1]}": by_key[k] for k in keys},
    }


def run_multi_embedder_calibration(
    *,
    embedders: list[dict[str, Any]],
    prompts: list[str] | None = None,
    turn_values: list[int] | None = None,
    cal_cfg: dict[str, Any],
    null_cfg: dict[str, Any],
    chat_provider: str | None = None,
    chat_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    on_null_sample: Callable[[str, dict[str, Any]], None] | None = None,
    resume_null_by_embedder: dict[str, set[int]] | None = None,
    preloaded_null_by_embedder: dict[str, list[float]] | None = None,
    resume_chat_keys: set[tuple[str, int]] | None = None,
    cross_cfg: dict[str, Any] | None = None,
    on_chat_cell: Callable[[dict[str, Any]], None] | None = None,
    preloaded_chat_cells: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Full multi-embedder sweep: shared chat grid + per-embedder null/thresholds/lift."""
    prompts = prompts or FOCUSED_PROMPTS
    turn_values = turn_values or [3, 6]
    cross_cfg = cross_cfg or {}
    resume_null_by_embedder = resume_null_by_embedder or {}
    preloaded_null_by_embedder = preloaded_null_by_embedder or {}

    chat_grid = collect_shared_chat_grid(
        prompts=prompts,
        turn_values=turn_values,
        chat_provider=chat_provider,
        chat_model=chat_model,
        pause_s=pause_s,
        skip_chat=skip_chat,
        resume_keys=resume_chat_keys,
        on_cell=on_chat_cell,
    )
    if preloaded_chat_cells:
        seen = {(c.get("user_prompt"), int(c["n_turns"])) for c in preloaded_chat_cells}
        merged = list(preloaded_chat_cells)
        for c in chat_grid["cells"]:
            key = (c.get("user_prompt"), int(c["n_turns"]))
            if key not in seen:
                merged.append(c)
                seen.add(key)
        chat_grid["cells"] = merged

    branches: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = list(chat_grid.get("errors", []))

    for emb in embedders:
        prov = emb["provider"]
        model = emb.get("model")

        def _on_null(rec: dict[str, Any], _p: str = prov) -> None:
            if on_null_sample:
                on_null_sample(_p, rec)

        try:
            branch = run_embedder_calibration_branch(
                prov,
                embed_model=model,
                cal_cfg=cal_cfg,
                shared_cells=chat_grid["cells"],
                prompts=prompts,
                null_cfg=null_cfg,
                chat_provider=chat_provider,
                chat_model=chat_model,
                pause_s=pause_s,
                skip_chat=skip_chat,
                on_null_sample=_on_null if on_null_sample else None,
                resume_null_indices=resume_null_by_embedder.get(prov),
                preloaded_null_d_med=preloaded_null_by_embedder.get(prov),
            )
            branches.append(branch)
        except Exception as exc:  # noqa: BLE001
            errors.append({"embed_provider": prov, "error": str(exc)})

    cross = compute_cross_embedder_analysis(
        branches,
        lift_agreement_min=float(cross_cfg.get("lift_agreement_min", 0.03)),
        min_embedders_for_agreement=int(cross_cfg.get("min_embedders_for_agreement", 2)),
    )

    mean_lifts = [b["summary"]["mean_lift"] for b in branches]
    return {
        "protocol": "amat-multi-embedder-v1",
        "mode": chat_grid["mode"],
        "chat_provider": chat_grid.get("chat_provider"),
        "embedders_requested": embedders,
        "embedders_completed": [b["embed_provider"] for b in branches],
        "chat_grid": {"n_cells": len(chat_grid["cells"]), "errors": chat_grid.get("errors", [])},
        "branches": branches,
        "cross_embedder": cross,
        "summary": {
            "n_embedders": len(branches),
            "mean_lift_by_embedder": {
                b["embed_provider"]: b["summary"]["mean_lift"] for b in branches
            },
            "calibrated_pass_by_embedder": {
                b["embed_provider"]: b["summary"]["calibrated_lock_gate_pass_fraction"]
                for b in branches
            },
            "overall_mean_lift": round(float(np.mean(mean_lifts)), 6) if mean_lifts else 0.0,
            "mean_spearman_rho": cross.get("mean_spearman_rho"),
            "lift_agreement_fraction": cross.get("lift_agreement_fraction"),
        },
        "errors": errors,
        "hypothesis_support": {
            "H-AMAT-006": cross.get("mean_spearman_rho") is not None and cross["mean_spearman_rho"] >= 0.5,
            "H-AMAT-007": (cross.get("lift_agreement_fraction") or 0) >= 0.5,
        },
    }
