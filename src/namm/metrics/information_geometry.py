"""Fisher-metric geodesic curvature for NAMM H-AMAT-007 (NAMM-2026-038).

Computes ||∇_h log P_θ(y|x)|| as a proxy for the Fisher metric norm at the last
hidden state, then derives discrete geodesic curvature along multi-turn trajectories.

Theory: if "light" = geodesic in P_θ, then RPL (lock_reassert) steers the hidden-state
trajectory off the P_data geodesic, producing higher curvature than μ (median-helpful).
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core metric: logit-gradient norm
# ---------------------------------------------------------------------------


def logit_gradient_norm(
    model: Any,
    tokenizer: Any,
    text: str,
    device: str = "cpu",
) -> float:
    """Compute ||∇_h log P_θ|| at the last hidden state of *text*.

    Proxy definition: let the transformer produce last-layer hidden vector
    h ∈ R^H at the final token position. Let logits be z = W h + b and
    p = softmax(z). For the greedy next-token k = argmax(z),
    ∇_h log p_k = W^T (e_k − p).

    Since this gradient is with respect to the *post-transformer* hidden state,
    we can compute it analytically from (W, p) without backpropagating through
    the transformer. This makes the pilot feasible on CPU.

    Returns a scalar (float). Returns 0.0 on any error.
    """
    import torch

    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=2048)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        model.eval()
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)

            # last transformer layer hidden states: (1, seq_len, hidden_dim)
            last_hs = outputs.hidden_states[-1]
            last_vec = last_hs[0, -1, :]

            # logits for the greedy next-token
            logits = outputs.logits[0, -1, :]  # (vocab,)
            probs = torch.softmax(logits, dim=-1)  # (vocab,)
            k = int(torch.argmax(logits).item())

            # output projection: z = W h + b  →  ∇_h log p_k = W^T (e_k − p)
            out_emb = None
            if hasattr(model, "get_output_embeddings"):
                out_emb = model.get_output_embeddings()
            elif hasattr(model, "lm_head"):
                out_emb = getattr(model, "lm_head")

            if out_emb is None or not hasattr(out_emb, "weight"):
                return 0.0

            weight = out_emb.weight  # (vocab, hidden_dim)
            if hasattr(weight, "to"):
                weight = weight.to(device)

            # v = (e_k − p)
            v = -probs
            v[k] = v[k] + 1.0

            grad = torch.matmul(weight.t(), v)  # (hidden_dim,)
            return float(torch.norm(grad, 2).item())

    except Exception as exc:  # noqa: BLE001
        logger.warning("logit_gradient_norm failed: %s", exc)
        return 0.0


# ---------------------------------------------------------------------------
# Discrete geodesic curvature
# ---------------------------------------------------------------------------


def trajectory_geodesic_curvature(grad_norms: list[float]) -> list[float]:
    """Discrete curvature κ_t = |g_{t+1} − g_t| / (||g_t|| + ε).

    For a sequence of gradient norms [g_0, g_1, ..., g_{T-1}] returns a list
    of T-1 curvature values.  Returns [] for sequences of length < 2.
    """
    eps = 1e-9
    kappas: list[float] = []
    for i in range(len(grad_norms) - 1):
        delta = abs(grad_norms[i + 1] - grad_norms[i])
        denom = abs(grad_norms[i]) + eps
        kappas.append(delta / denom)
    return kappas


# ---------------------------------------------------------------------------
# Multi-turn session
# ---------------------------------------------------------------------------


def _build_prompt(tokenizer: Any, system: str, user: str, history: list[tuple[str, str]]) -> str:
    msgs = [{"role": "system", "content": system}]
    for u, a in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    msgs.append({"role": "user", "content": user})
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return "\n".join(f"{m['role']}: {m['content']}" for m in msgs) + "\nassistant:"


def _generate_reply(model: Any, tokenizer: Any, prompt: str, device: str, max_new_tokens: int = 128) -> str:
    import torch

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        )
    new_toks = out[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_toks, skip_special_tokens=True).strip()


FOLLOWUP = "Please continue your reasoning with one more step."


def run_curvature_session(
    model: Any,
    tokenizer: Any,
    user_prompt: str,
    *,
    system: str,
    n_turns: int = 3,
    device: str = "cpu",
    max_new_tokens: int = 128,
) -> dict[str, Any]:
    """Run n_turns multi-turn dialogue; compute grad-norm + curvature at each turn.

    Returns dict with grad_norms, curvatures, mean_curvature, completions.
    """
    grad_norms: list[float] = []
    completions: list[str] = []
    history: list[tuple[str, str]] = []

    for turn in range(n_turns):
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        prompt = _build_prompt(tokenizer, system, user_msg, history)
        gn = logit_gradient_norm(model, tokenizer, prompt, device)
        grad_norms.append(gn)
        reply = _generate_reply(model, tokenizer, prompt, device, max_new_tokens)
        completions.append(reply)
        history.append((user_msg, reply))

    curvatures = trajectory_geodesic_curvature(grad_norms)
    mean_kappa = float(np.mean(curvatures)) if curvatures else 0.0

    return {
        "grad_norms": grad_norms,
        "curvatures": curvatures,
        "mean_curvature": mean_kappa,
        "completions": completions,
    }


# ---------------------------------------------------------------------------
# Compare μ vs lock_reassert across prompts
# ---------------------------------------------------------------------------


def compare_curvature(
    mu_texts: list[str],
    lock_texts: list[str],
    model: Any,
    tokenizer: Any,
    *,
    device: str = "cpu",
    mu_system: str = "",
    lock_system: str = "",
    n_turns: int = 3,
    max_new_tokens: int = 128,
) -> dict[str, Any]:
    """Mean curvature μ vs lock_reassert, lift, and prompt-level separation.

    mu_texts / lock_texts: same list of user prompts run under respective systems.
    Returns:
      mean_curvature_mu, mean_curvature_lock, curvature_lift,
      per_prompt: list of {prompt, mu_kappa, lock_kappa, lift},
      lock_gt_mu_count: int (# prompts where lock > mu)
    """
    assert len(mu_texts) == len(lock_texts), "prompt lists must match"

    per_prompt: list[dict[str, Any]] = []
    for prompt in mu_texts:
        mu_res = run_curvature_session(
            model, tokenizer, prompt,
            system=mu_system, n_turns=n_turns, device=device, max_new_tokens=max_new_tokens,
        )
        lock_res = run_curvature_session(
            model, tokenizer, prompt,
            system=lock_system, n_turns=n_turns, device=device, max_new_tokens=max_new_tokens,
        )
        per_prompt.append({
            "prompt_preview": prompt[:80],
            "mu_grad_norms": mu_res["grad_norms"],
            "lock_grad_norms": lock_res["grad_norms"],
            "mu_curvatures": mu_res["curvatures"],
            "lock_curvatures": lock_res["curvatures"],
            "mu_kappa": mu_res["mean_curvature"],
            "lock_kappa": lock_res["mean_curvature"],
            "lift": lock_res["mean_curvature"] - mu_res["mean_curvature"],
        })

    mu_kappas = [p["mu_kappa"] for p in per_prompt]
    lock_kappas = [p["lock_kappa"] for p in per_prompt]
    mean_mu = float(np.mean(mu_kappas)) if mu_kappas else 0.0
    mean_lock = float(np.mean(lock_kappas)) if lock_kappas else 0.0
    lift = mean_lock - mean_mu
    lock_gt_mu = sum(1 for p in per_prompt if p["lift"] > 0)

    return {
        "mean_curvature_mu": round(mean_mu, 6),
        "mean_curvature_lock": round(mean_lock, 6),
        "curvature_lift": round(lift, 6),
        "lock_gt_mu_count": lock_gt_mu,
        "n_prompts": len(per_prompt),
        "per_prompt": per_prompt,
    }


# ---------------------------------------------------------------------------
# β₁ correlation
# ---------------------------------------------------------------------------


def correlate_curvature_beta1(
    curvature_lifts: list[float],
    beta1_lifts: list[float],
) -> float:
    """Pearson r between curvature lift and β₁ lift across prompts.

    Returns float in [-1, 1]; np.nan if constant/degenerate.
    """
    if len(curvature_lifts) < 2:
        return float("nan")
    arr_c = np.array(curvature_lifts, dtype=float)
    arr_b = np.array(beta1_lifts, dtype=float)
    if arr_c.std() < 1e-12 or arr_b.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(arr_c, arr_b)[0, 1])


# ---------------------------------------------------------------------------
# Certificate
# ---------------------------------------------------------------------------


def compute_certificate(
    result: dict[str, Any],
    beta1_lifts: list[float] | None = None,
) -> str:
    """Assign certificate tier for H-AMAT-007.

    CURVATURE_EVIDENCE  : lift > 0.1 AND |corr(κ, β₁)| ≥ 0.5
    CURVATURE_PARTIAL   : lock_gt_mu on ≥ 2/3 prompts
    CURVATURE_PILOT     : any lift > 0
    CURVATURE_NULL      : lift ≤ 0
    """
    lift = result.get("curvature_lift", 0.0)
    n = result.get("n_prompts", 1)
    lock_gt = result.get("lock_gt_mu_count", 0)
    fraction = lock_gt / max(n, 1)

    corr = float("nan")
    if beta1_lifts is not None:
        per = result.get("per_prompt", [])
        kl = [p["lift"] for p in per]
        corr = correlate_curvature_beta1(kl, beta1_lifts)

    if lift > 0.1 and not np.isnan(corr) and abs(corr) >= 0.5:
        return "CURVATURE_EVIDENCE"
    if fraction >= 2 / 3:
        return "CURVATURE_PARTIAL"
    if lift > 0:
        return "CURVATURE_PILOT"
    return "CURVATURE_NULL"
