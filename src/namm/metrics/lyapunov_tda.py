"""Lyapunov λ₁ proxy on hidden-state trajectories — H-AMAT-009 / NAMM-2026-040."""

from __future__ import annotations

import logging
from typing import Any, Literal

import numpy as np

from namm.metrics.activation_tda import (
    LocalLM,
    Policy,
    _chat_messages,
    _generate_reply,
    _system_for_policy,
    extract_last_token_hidden_matrix,
)
from namm.metrics.live_embeddings import FOLLOWUP

logger = logging.getLogger(__name__)


def _nanmean_safe(vals: list[float]) -> float:
    arr = np.asarray(vals, dtype=np.float64)
    if arr.size == 0 or np.all(np.isnan(arr)):
        return float("nan")
    return float(np.nanmean(arr))


def lyapunov_from_pair(
    traj_a: np.ndarray,
    traj_b: np.ndarray,
    *,
    dt: float = 1.0,
) -> float:
    """Estimate λ₁ from two nearby trajectories (T, D).

    λ₁ ≈ mean_t log(||δ_{t+1}|| / ||δ_t||) / dt  for δ_t = a_t − b_t.
    Clips ratios to avoid log(0).
    """
    a = np.asarray(traj_a, dtype=np.float64)
    b = np.asarray(traj_b, dtype=np.float64)
    t = min(len(a), len(b))
    if t < 3:
        return float("nan")
    a, b = a[:t], b[:t]
    deltas = a - b
    norms = np.linalg.norm(deltas, axis=1)
    norms = np.maximum(norms, 1e-12)
    ratios = norms[1:] / norms[:-1]
    ratios = np.clip(ratios, 1e-6, 1e6)
    return float(np.mean(np.log(ratios)) / max(dt, 1e-9))


def rosenstein_lambda1(
    traj: np.ndarray,
    *,
    mean_period: int = 1,
    max_iter: int | None = None,
) -> float:
    """Single-trajectory Rosenstein-style NN divergence slope (discrete time)."""
    x = np.asarray(traj, dtype=np.float64)
    if x.ndim != 2 or len(x) < 4:
        return float("nan")
    n = len(x)
    if max_iter is None:
        max_iter = max(2, min(8, n // 2))
    # nearest neighbor with temporal exclusion
    dists0: list[float] = []
    pairs: list[tuple[int, int]] = []
    for i in range(max(0, n - max_iter - 1)):
        dmin = np.inf
        jmin = -1
        for j in range(max(0, n - max_iter - 1)):
            if abs(i - j) <= mean_period:
                continue
            d = float(np.linalg.norm(x[i] - x[j]))
            if d < dmin and d > 1e-12:
                dmin = d
                jmin = j
        if jmin >= 0:
            pairs.append((i, jmin))
            dists0.append(dmin)
    if len(pairs) < 2:
        return float("nan")

    lags = list(range(1, max_iter + 1))
    y = []
    for lag in lags:
        vals = []
        for (i, j), d0 in zip(pairs, dists0):
            if i + lag >= n or j + lag >= n:
                continue
            d = float(np.linalg.norm(x[i + lag] - x[j + lag]))
            vals.append(np.log(max(d, 1e-12) / max(d0, 1e-12)))
        if vals:
            y.append(float(np.mean(vals)))
        else:
            y.append(float("nan"))
    valid = [(l, yy) for l, yy in zip(lags, y) if yy == yy]
    if len(valid) < 2:
        return float("nan")
    xs = np.array([v[0] for v in valid], dtype=float)
    ys = np.array([v[1] for v in valid], dtype=float)
    slope = float(np.polyfit(xs, ys, 1)[0])
    return slope


def _session_last_layer_traj(
    lm: LocalLM,
    user_prompt: str,
    *,
    policy: Policy,
    n_turns: int,
    m0_system: str,
    nd_system: str,
    max_new_tokens: int,
    temperature: float,
    seed: int,
) -> tuple[list[str], np.ndarray]:
    import torch

    torch.manual_seed(seed)
    np.random.seed(seed)
    completions: list[str] = []
    history: list[tuple[str, str]] = []
    vecs: list[np.ndarray] = []

    for turn in range(n_turns):
        system = _system_for_policy(policy, m0_system, nd_system)
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        mat = extract_last_token_hidden_matrix(lm, system, user_msg, history, layer_indices=[-1])
        vecs.append(mat[-1])

        tokenizer = lm.tokenizer
        model = lm.model
        messages = _chat_messages(system, user_msg, history)
        if hasattr(tokenizer, "apply_chat_template"):
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        else:
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages) + "\nassistant:"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        inputs = {k: v.to(lm.device) for k, v in inputs.items()}
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=max(temperature, 0.05),
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            )
        text = tokenizer.decode(out[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True).strip()
        completions.append(text)
        history.append((user_msg, text))

    return completions, np.stack(vecs, axis=0)


def compare_lyapunov_policies(
    lm: LocalLM,
    prompts: list[str],
    *,
    m0_system: str,
    nd_system: str,
    n_turns: int = 6,
    n_sessions: int = 3,
    max_new_tokens: int = 48,
    temperature: float = 0.8,
    base_seed: int = 41,
) -> dict[str, Any]:
    """Multi-session λ₁ for μ vs lock; positive λ₁ + lock>μ supports H-AMAT-009."""
    cells: list[dict[str, Any]] = []

    for pi, prompt in enumerate(prompts):
        cell: dict[str, Any] = {"prompt_preview": prompt[:80]}
        for policy in ("mu", "lock_reassert"):
            trajs: list[np.ndarray] = []
            pair_lams: list[float] = []
            single_lams: list[float] = []
            for s in range(n_sessions):
                logger.info(
                    "040 cell prompt=%d/%d policy=%s session=%d/%d",
                    pi + 1,
                    len(prompts),
                    policy,
                    s + 1,
                    n_sessions,
                )
                _, traj = _session_last_layer_traj(
                    lm,
                    prompt,
                    policy=policy,  # type: ignore[arg-type]
                    n_turns=n_turns,
                    m0_system=m0_system,
                    nd_system=nd_system,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    seed=base_seed + 1000 * pi + 17 * s + (0 if policy == "mu" else 50),
                )
                trajs.append(traj)
                single_lams.append(rosenstein_lambda1(traj))
            for i in range(len(trajs)):
                for j in range(i + 1, len(trajs)):
                    pair_lams.append(lyapunov_from_pair(trajs[i], trajs[j]))
            cell[f"{policy}_lambda1_pair"] = _nanmean_safe(pair_lams)
            cell[f"{policy}_lambda1_rosenstein"] = _nanmean_safe(single_lams)
            cell[f"{policy}_n_sessions"] = n_sessions

        cell["lift_lambda1_pair"] = cell["lock_reassert_lambda1_pair"] - cell["mu_lambda1_pair"]
        cell["lift_lambda1_rosenstein"] = (
            cell["lock_reassert_lambda1_rosenstein"] - cell["mu_lambda1_rosenstein"]
        )
        cells.append(cell)
        logger.info(
            "040 prompt done lift_pair=%.4f mu=%.4f lock=%.4f",
            cell["lift_lambda1_pair"],
            cell["mu_lambda1_pair"],
            cell["lock_reassert_lambda1_pair"],
        )

    lifts = [c["lift_lambda1_pair"] for c in cells if c["lift_lambda1_pair"] == c["lift_lambda1_pair"]]
    mean_lift = float(np.mean(lifts)) if lifts else 0.0
    lock_pos = sum(
        1
        for c in cells
        if c["lock_reassert_lambda1_pair"] == c["lock_reassert_lambda1_pair"]
        and c["lock_reassert_lambda1_pair"] > 0
    )
    mu_pos = sum(
        1
        for c in cells
        if c["mu_lambda1_pair"] == c["mu_lambda1_pair"] and c["mu_lambda1_pair"] > 0
    )

    return {
        "cells": cells,
        "mean_lift_lambda1": mean_lift,
        "lock_positive_count": lock_pos,
        "mu_positive_count": mu_pos,
        "n_prompts": len(prompts),
        "n_sessions": n_sessions,
        "n_turns": n_turns,
    }


def assign_lyapunov_certificate(result: dict[str, Any]) -> str:
    mean_lift = float(result.get("mean_lift_lambda1", 0.0))
    lock_pos = int(result.get("lock_positive_count", 0))
    mu_pos = int(result.get("mu_positive_count", 0))
    n = max(int(result.get("n_prompts", 1)), 1)

    if mean_lift > 0.05 and lock_pos >= max(1, n // 2) and lock_pos > mu_pos:
        return "CHAOS_EVIDENCE"
    if mean_lift > 0.0 and lock_pos > mu_pos:
        return "CHAOS_PILOT"
    if lock_pos > 0:
        return "CHAOS_PARTIAL"
    return "NULL"