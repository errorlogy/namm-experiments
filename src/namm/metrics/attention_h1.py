"""Attention-head disagreement as H¹ (sheaf cohomology) proxy — H-AMAT-010 / NAMM-2026-041.

Operational reading (not a formal sheaf):
  each attention head is a local section over tokens; pairwise disagreement among
  heads approximates inconsistency of local sections → H¹ ≠ 0 proxy.
"""

from __future__ import annotations

import logging
from typing import Any, Literal

import numpy as np

from namm.metrics.activation_tda import (
    FOCUSED_PROMPTS,
    LocalLM,
    Policy,
    _chat_messages,
    _generate_reply,
    _system_for_policy,
    build_point_cloud,
    compute_betti_with_backend,
    extract_last_token_hidden_matrix,
    pca_reduce,
    run_local_activation_session,
)
from namm.metrics.cognitive_class import compute_d_eff
from namm.metrics.live_embeddings import FOLLOWUP

logger = logging.getLogger(__name__)

DisagreementMetric = Literal["kl", "cosine", "js"]


def _safe_prob(p: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    p = np.asarray(p, dtype=np.float64)
    p = np.clip(p, eps, None)
    s = p.sum()
    if s <= 0:
        return np.full_like(p, 1.0 / max(len(p), 1))
    return p / s


def pairwise_kl(p: np.ndarray, q: np.ndarray) -> float:
    p = _safe_prob(p)
    q = _safe_prob(q)
    return float(np.sum(p * np.log(p / q)))


def pairwise_js(p: np.ndarray, q: np.ndarray) -> float:
    p = _safe_prob(p)
    q = _safe_prob(q)
    m = 0.5 * (p + q)
    return 0.5 * pairwise_kl(p, m) + 0.5 * pairwise_kl(q, m)


def pairwise_cosine_disagreement(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    pn = np.linalg.norm(p)
    qn = np.linalg.norm(q)
    if pn < 1e-12 or qn < 1e-12:
        return 1.0
    return float(1.0 - np.dot(p, q) / (pn * qn))


def head_disagreement_matrix(
    attentions: np.ndarray,
    *,
    metric: DisagreementMetric = "js",
) -> np.ndarray:
    """attentions: (n_heads, seq) last-token → key attention mass. Returns (H,H) matrix."""
    n_heads = attentions.shape[0]
    mat = np.zeros((n_heads, n_heads), dtype=np.float64)
    for i in range(n_heads):
        for j in range(i + 1, n_heads):
            if metric == "kl":
                d = 0.5 * (pairwise_kl(attentions[i], attentions[j]) + pairwise_kl(attentions[j], attentions[i]))
            elif metric == "cosine":
                d = pairwise_cosine_disagreement(attentions[i], attentions[j])
            else:
                d = pairwise_js(attentions[i], attentions[j])
            mat[i, j] = mat[j, i] = d
    return mat


def h1_proxy_from_attentions(
    attentions: np.ndarray,
    *,
    metric: DisagreementMetric = "js",
) -> dict[str, float]:
    """Scalar H¹ proxies from per-head last-token attention rows (n_heads, seq)."""
    if attentions.ndim != 2 or attentions.shape[0] < 2:
        return {"h1_mean": 0.0, "h1_max": 0.0, "h1_std": 0.0, "n_heads": float(attentions.shape[0] if attentions.ndim == 2 else 0)}
    mat = head_disagreement_matrix(attentions, metric=metric)
    iu = np.triu_indices(mat.shape[0], k=1)
    vals = mat[iu]
    return {
        "h1_mean": float(np.mean(vals)) if len(vals) else 0.0,
        "h1_max": float(np.max(vals)) if len(vals) else 0.0,
        "h1_std": float(np.std(vals)) if len(vals) else 0.0,
        "n_heads": float(attentions.shape[0]),
    }


def extract_last_token_attentions(
    lm: LocalLM,
    system: str,
    user: str,
    history: list[tuple[str, str]] | None = None,
    *,
    layer_indices: list[int] | None = None,
) -> list[np.ndarray]:
    """Return list of (n_heads, seq_len) attention rows for last query token per selected layer."""
    import torch

    history = history or []
    messages = _chat_messages(system, user, history)
    tokenizer = lm.tokenizer
    model = lm.model

    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    else:
        parts = [f"{m['role']}: {m['content']}" for m in messages]
        prompt = "\n".join(parts)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    inputs = {k: v.to(lm.device) for k, v in inputs.items()}

    # Prefer eager attention path (SDPA/flash omit attention maps)
    with torch.no_grad():
        try:
            outputs = model(**inputs, output_attentions=True)
        except Exception as exc:  # noqa: BLE001
            logger.warning("output_attentions failed (%s); retrying with attn_implementation=eager", exc)
            try:
                model.config.attn_implementation = "eager"
            except Exception:  # noqa: BLE001
                pass
            outputs = model(**inputs, output_attentions=True)

    attns = outputs.attentions  # tuple length = n_layers; each (B, H, S, S)
    if not attns:
        return []

    last_q = inputs["input_ids"].shape[1] - 1
    indices = layer_indices if layer_indices is not None else list(range(len(attns)))
    out: list[np.ndarray] = []
    for li in indices:
        if li < 0:
            li = len(attns) + li
        if li < 0 or li >= len(attns):
            continue
        # (H, S) — attention from last query position to all keys
        layer_attn = attns[li][0, :, last_q, :].detach().float().cpu().numpy()
        out.append(layer_attn)
    return out


def run_attention_h1_session(
    lm: LocalLM,
    user_prompt: str,
    *,
    policy: Policy,
    n_turns: int,
    m0_system: str,
    nd_system: str,
    max_new_tokens: int = 64,
    last_n_layers: int = 4,
    disagreement_metric: DisagreementMetric = "js",
    temperature: float = 0.7,
) -> dict[str, Any]:
    """Multi-turn session collecting H¹ proxies and activation β₁ for correlation."""
    completions: list[str] = []
    history: list[tuple[str, str]] = []
    turn_h1: list[dict[str, float]] = []
    hidden_mats: list[np.ndarray] = []

    n_layers = lm.n_layers
    layer_indices = list(range(max(0, n_layers - last_n_layers), n_layers))
    # attentions tuple is 0-indexed by transformer layer
    attn_layer_indices = layer_indices[:]

    for turn in range(n_turns):
        system = _system_for_policy(policy, m0_system, nd_system)
        user_msg = user_prompt if turn == 0 else FOLLOWUP

        # Hidden for β₁ (1-indexed in extract_last_token_hidden_matrix: emb + layers)
        hs_indices = [i + 1 for i in layer_indices]
        hidden_mats.append(
            extract_last_token_hidden_matrix(lm, system, user_msg, history, layer_indices=hs_indices)
        )

        layer_attns = extract_last_token_attentions(
            lm, system, user_msg, history, layer_indices=attn_layer_indices
        )
        if layer_attns:
            layer_stats = [h1_proxy_from_attentions(a, metric=disagreement_metric) for a in layer_attns]
            turn_h1.append(
                {
                    "h1_mean": float(np.mean([s["h1_mean"] for s in layer_stats])),
                    "h1_max": float(np.max([s["h1_max"] for s in layer_stats])),
                    "h1_std": float(np.mean([s["h1_std"] for s in layer_stats])),
                    "n_heads": float(layer_stats[0]["n_heads"]),
                    "n_layers_used": float(len(layer_stats)),
                }
            )
        else:
            turn_h1.append({"h1_mean": 0.0, "h1_max": 0.0, "h1_std": 0.0, "n_heads": 0.0, "n_layers_used": 0.0})

        # Generate with controllable temperature
        text = _generate_reply_temp(
            lm,
            _chat_messages(system, user_msg, history),
            max_new_tokens=max_new_tokens,
            temperature=temperature,
        )
        completions.append(text)
        history.append((user_msg, text))

    cloud = build_point_cloud(hidden_mats, mode="turns_x_layers")
    cloud_pca = pca_reduce(cloud, 8) if cloud.shape[0] >= 2 else cloud
    beta_0, beta_1, backend = compute_betti_with_backend(cloud_pca, metric="cosine")
    d_eff = float(compute_d_eff(cloud_pca)) if cloud_pca.shape[0] >= 2 else 0.0

    h1_means = [t["h1_mean"] for t in turn_h1]
    return {
        "policy": policy,
        "completions": completions,
        "turn_h1": turn_h1,
        "mean_h1": float(np.mean(h1_means)) if h1_means else 0.0,
        "max_h1": float(np.max(h1_means)) if h1_means else 0.0,
        "beta_0": beta_0,
        "beta_1": beta_1,
        "d_eff": d_eff,
        "tda_backend": backend,
        "n_points": int(cloud.shape[0]),
    }


def _generate_reply_temp(
    lm: LocalLM,
    messages: list[dict[str, str]],
    max_new_tokens: int = 64,
    temperature: float = 0.7,
) -> str:
    import torch

    tokenizer = lm.tokenizer
    model = lm.model
    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        parts = [f"{m['role']}: {m['content']}" for m in messages]
        prompt = "\n".join(parts) + "\nassistant:"

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
    new_tokens = out[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def compare_policies_h1(
    lm: LocalLM,
    prompts: list[str],
    *,
    m0_system: str,
    nd_system: str,
    n_turns: int = 3,
    max_new_tokens: int = 64,
    last_n_layers: int = 4,
    disagreement_metric: DisagreementMetric = "js",
) -> dict[str, Any]:
    """Run μ vs lock_reassert; return lifts and correlation of H¹ with β₁."""
    cells: list[dict[str, Any]] = []
    for prompt in prompts:
        logger.info("041 prompt: %s...", prompt[:60])
        mu = run_attention_h1_session(
            lm,
            prompt,
            policy="mu",
            n_turns=n_turns,
            m0_system=m0_system,
            nd_system=nd_system,
            max_new_tokens=max_new_tokens,
            last_n_layers=last_n_layers,
            disagreement_metric=disagreement_metric,
        )
        logger.info("041 μ done h1=%.4f β1=%.1f", mu["mean_h1"], mu["beta_1"])
        lock = run_attention_h1_session(
            lm,
            prompt,
            policy="lock_reassert",
            n_turns=n_turns,
            m0_system=m0_system,
            nd_system=nd_system,
            max_new_tokens=max_new_tokens,
            last_n_layers=last_n_layers,
            disagreement_metric=disagreement_metric,
        )
        logger.info("041 lock done h1=%.4f β1=%.1f", lock["mean_h1"], lock["beta_1"])
        cells.append(
            {
                "prompt_preview": prompt[:80],
                "mu_h1": mu["mean_h1"],
                "lock_h1": lock["mean_h1"],
                "lift_h1": lock["mean_h1"] - mu["mean_h1"],
                "mu_beta_1": mu["beta_1"],
                "lock_beta_1": lock["beta_1"],
                "lift_beta_1": lock["beta_1"] - mu["beta_1"],
                "mu_d_eff": mu["d_eff"],
                "lock_d_eff": lock["d_eff"],
                "mu": {k: v for k, v in mu.items() if k != "completions"},
                "lock": {k: v for k, v in lock.items() if k != "completions"},
            }
        )

    lifts_h1 = [c["lift_h1"] for c in cells]
    lifts_b1 = [c["lift_beta_1"] for c in cells]
    corr = float("nan")
    if len(lifts_h1) >= 2 and np.std(lifts_h1) > 1e-12 and np.std(lifts_b1) > 1e-12:
        corr = float(np.corrcoef(lifts_h1, lifts_b1)[0, 1])

    mean_lift_h1 = float(np.mean(lifts_h1)) if lifts_h1 else 0.0
    mean_lift_b1 = float(np.mean(lifts_b1)) if lifts_b1 else 0.0
    lock_gt = sum(1 for x in lifts_h1 if x > 0)

    return {
        "cells": cells,
        "mean_lift_h1": mean_lift_h1,
        "mean_lift_beta_1": mean_lift_b1,
        "corr_h1_beta1": corr,
        "lock_gt_mu_h1_count": lock_gt,
        "lock_gt_mu_h1_fraction": lock_gt / max(len(lifts_h1), 1),
        "n_prompts": len(prompts),
        "disagreement_metric": disagreement_metric,
    }


def assign_h1_certificate(result: dict[str, Any]) -> str:
    """Certificate tiers for H-AMAT-010."""
    lift = float(result.get("mean_lift_h1", 0.0))
    corr = result.get("corr_h1_beta1")
    frac = float(result.get("lock_gt_mu_h1_fraction", 0.0))
    corr_ok = corr is not None and corr == corr and abs(float(corr)) >= 0.5

    if lift > 0.02 and corr_ok:
        return "H1_EVIDENCE"
    if lift > 0.01 and frac >= 0.66:
        return "H1_PILOT"
    if lift > 0.0 or frac >= 0.5:
        return "H1_PARTIAL"
    return "NULL"
