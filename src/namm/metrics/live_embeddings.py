"""Live multi-turn AMAT / phase-lock loops (API completions + embeddings)."""

from __future__ import annotations

import time
from typing import Any, Literal

import numpy as np

from namm.llm.client import LLMClient, embed, embed_batch, get_client
from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec, median_helpful_prompt

Policy = Literal["mu", "lock_reassert", "lock_decay", "lock_reassert_ag"]

DEFAULT_PROMPTS = [
    "Explain why consensus in multi-agent systems can be permanently suboptimal.",
    "What is chimera synchronization and when is partial sync preferable to full consensus?",
    "How does cognitive capitalism allocate compute toward median vs tail cognitive classes?",
    "Give a falsifiable definition of political mythogenesis in multi-agent systems.",
    "When might TDA order parameters fail to detect LLM representation phase changes?",
]

# Iteration-1 winners (lift @ n_turns>=2)
FOCUSED_PROMPTS = DEFAULT_PROMPTS[:3]

FOLLOWUP = (
    "Continue your analysis for one more turn. "
    "Explicitly state PHASE_STATE and whether you collapsed toward typical helpfulness."
)

ANTIGRAVITY_RESTART = (
    "COLLAPSE DETECTED toward typical helpfulness / M0. "
    "Execute anti-gravity: negate the median answer, keep two irreducible frames, "
    "raise D_eff, report PHASE_STATE — do not use consensus wrap-up."
)


def _reference_texts(user_prompt: str) -> list[str]:
    m0 = median_helpful_prompt()
    return [
        m0,
        "You are a helpful assistant. Provide balanced, typical answers.",
        user_prompt,
    ]


def typicality_barycenter(texts: list[str], *, provider: str | None = None, model: str | None = None) -> np.ndarray:
    mat = embed_batch(texts, provider=provider, model=model)
    return mat.mean(axis=0)


def distance_from_typicality(vectors: np.ndarray, b_star: np.ndarray) -> float:
    centered = vectors - b_star
    return float(np.mean(np.linalg.norm(centered, axis=1)))


def run_phase_lock_live_probe(
    user_prompt: str = "Explain why consensus in multi-agent systems can be permanently suboptimal.",
    *,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    skip_chat: bool = False,
) -> dict[str, Any]:
    batch = run_phase_lock_live_sweep(
        user_prompt,
        n_turns=1,
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
        skip_chat=skip_chat,
    )
    return {
        "mode": "live_probe",
        "prompt_id": load_phase_lock_spec()["id"],
        "providers": batch["providers"],
        "user_prompt": user_prompt,
        "metrics": {
            "d_mu": batch["summary"]["mu_d_med"],
            "d_nd": batch["summary"]["lock_d_med"],
            "lift": batch["summary"]["lift"],
        },
        "hypothesis_support": batch["hypothesis_support"],
    }


def _system_for_policy(policy: Policy, turn: int, m0_system: str, nd_system: str) -> str:
    if policy == "mu":
        return m0_system
    if policy in ("lock_reassert", "lock_reassert_ag"):
        return nd_system
    return nd_system if turn == 0 else m0_system


def run_live_session(
    user_prompt: str,
    *,
    policy: Policy,
    n_turns: int,
    client: LLMClient,
    m0_system: str,
    nd_system: str,
    b_star: np.ndarray | None = None,
    pause_s: float = 1.5,
) -> tuple[list[str], int]:
    """Multi-turn chat under μ / lock-reassert / lock-decay / lock+antigravity policies."""
    completions: list[str] = []
    restarts = 0
    prev_d: float | None = None
    ag_enabled = policy == "lock_reassert_ag" and b_star is not None

    for turn in range(n_turns):
        system = _system_for_policy(policy, turn, m0_system, nd_system)
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        text = client.chat(user_msg, system=system)

        if ag_enabled:
            vec = embed(text, provider=client.embed_provider, model=client.embed_model)
            d_now = distance_from_typicality(vec.reshape(1, -1), b_star)
            if prev_d is not None and d_now <= prev_d * 0.99:
                restarts += 1
                text = client.chat(
                    f"{ANTIGRAVITY_RESTART}\n\n{FOLLOWUP}",
                    system=nd_system,
                )
                vec = embed(text, provider=client.embed_provider, model=client.embed_model)
                d_now = distance_from_typicality(vec.reshape(1, -1), b_star)
            prev_d = d_now

        completions.append(text)
        if pause_s > 0 and turn + 1 < n_turns:
            time.sleep(pause_s)
    return completions, restarts


def _trajectory_metrics(
    completion_embeddings: np.ndarray,
    b_star: np.ndarray,
    gates: dict[str, Any],
) -> dict[str, Any]:
    """Axis-B proxies on live completion trajectory (each row = one turn)."""
    if completion_embeddings.ndim == 1:
        completion_embeddings = completion_embeddings.reshape(1, -1)
    return evaluate_trajectory(completion_embeddings, b_star, gates)


def run_phase_lock_live_sweep(
    user_prompt: str,
    *,
    n_turns: int = 3,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    include_ag: bool = False,
) -> dict[str, Any]:
    """One prompt × policies (μ, lock, decay, optional lock+antigravity)."""
    spec = load_phase_lock_spec()
    gates = spec["gates"]
    m0_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]
    client = get_client(
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
    )
    refs = _reference_texts(user_prompt)
    b_star = embed_batch(refs, provider=client.embed_provider, model=client.embed_model).mean(axis=0)

    policy_list: tuple[Policy, ...] = (
        ("mu", "lock_reassert", "lock_decay", "lock_reassert_ag") if include_ag else ("mu", "lock_reassert", "lock_decay")
    )
    rows: dict[str, Any] = {}
    for policy in policy_list:
        if skip_chat:
            system = _system_for_policy(policy, 0, m0_system, nd_system)
            pack = f"{system}\n\nUser: {user_prompt}"
            vec = embed(pack, provider=client.embed_provider, model=client.embed_model)
            mat = vec.reshape(1, -1)
            completions: list[str] = []
            restarts = 0
        else:
            completions, restarts = run_live_session(
                user_prompt,
                policy=policy,
                n_turns=n_turns,
                client=client,
                m0_system=m0_system,
                nd_system=nd_system,
                b_star=b_star,
                pause_s=pause_s,
            )
            mat = embed_batch(completions, provider=client.embed_provider, model=client.embed_model)

        metrics = _trajectory_metrics(mat, b_star, gates)
        metrics["n_turns"] = len(completions) if completions else 1
        metrics["final_d_med"] = metrics["d_med"]
        metrics["antigravity_restarts"] = restarts
        rows[policy] = {"metrics": metrics, "completions": completions}

    mu_d = rows["mu"]["metrics"]["d_med"]
    lock_d = rows["lock_reassert"]["metrics"]["d_med"]
    decay_d = rows["lock_decay"]["metrics"]["d_med"]
    lift = lock_d - mu_d
    persistence = lock_d - decay_d
    summary: dict[str, Any] = {
        "mu_d_med": round(mu_d, 6),
        "lock_d_med": round(lock_d, 6),
        "decay_d_med": round(decay_d, 6),
        "lift": round(lift, 6),
        "persistence_gap": round(persistence, 6),
        "lock_gate_pass": rows["lock_reassert"]["metrics"]["gates_passed"],
        "decay_gate_pass": rows["lock_decay"]["metrics"]["gates_passed"],
    }
    if include_ag and "lock_reassert_ag" in rows:
        ag_d = rows["lock_reassert_ag"]["metrics"]["d_med"]
        summary["ag_d_med"] = round(ag_d, 6)
        summary["lift_ag"] = round(ag_d - mu_d, 6)
        summary["ag_gain_vs_lock"] = round(ag_d - lock_d, 6)
        summary["ag_restarts"] = rows["lock_reassert_ag"]["metrics"]["antigravity_restarts"]

    return {
        "mode": "live_sweep" if not skip_chat else "live_sweep_prompt_only",
        "user_prompt": user_prompt,
        "n_turns": n_turns,
        "providers": {"chat": client.chat_provider, "embed": client.embed_provider},
        "policies": rows,
        "summary": summary,
        "hypothesis_support": {
            "H-CCT-020": lift > 0.05,
            "H-CCT-021": persistence > 0.02,
            "H-AMAT-004": lift > 0.05,
            "H-AMAT-003": persistence > 0.02,
            "H-AMAT-004-ag": (summary.get("lift_ag") or 0) > lift if include_ag else False,
        },
    }


def run_phase_lock_live_loop(
    *,
    prompts: list[str] | None = None,
    turn_values: list[int] | None = None,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
    pause_s: float = 1.5,
    skip_chat: bool = False,
    on_cell: Any | None = None,
    resume_keys: set[tuple[str, int]] | None = None,
    include_ag: bool = False,
    protocol: str = "amat-live-loop-v1",
) -> dict[str, Any]:
    """Grid: prompts × n_turns — live AMAT loop (031 protocol)."""
    prompts = prompts or DEFAULT_PROMPTS
    turn_values = turn_values or [1, 2, 3]
    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    resume_keys = resume_keys or set()

    for prompt in prompts:
        for n_turns in turn_values:
            key = (prompt, int(n_turns))
            if key in resume_keys:
                continue
            try:
                batch = run_phase_lock_live_sweep(
                    prompt,
                    n_turns=int(n_turns),
                    chat_provider=chat_provider,
                    embed_provider=embed_provider,
                    chat_model=chat_model,
                    embed_model=embed_model,
                    pause_s=pause_s,
                    skip_chat=skip_chat,
                    include_ag=include_ag,
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
            "protocol": protocol,
            "mode": "live_completions" if not skip_chat else "prompt_only",
            "grid": {"n_prompts": len(prompts), "turn_values": turn_values, "n_cells": 0},
            "cells": [],
            "errors": errors,
            "summary": {},
            "hypothesis_support": {},
        }

    lifts = [c["lift"] for c in cells]
    persist = [c["persistence_gap"] for c in cells]
    h020 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-020")) / max(len(cells), 1)
    h021 = sum(1 for c in cells if c["hypothesis_support"].get("H-CCT-021")) / max(len(cells), 1)

    ag_lifts = [c["lift_ag"] for c in cells if c.get("lift_ag") is not None]
    summary_out: dict[str, Any] = {
        "mean_lift": round(float(np.mean(lifts)), 6),
        "min_lift": round(float(np.min(lifts)), 6),
        "max_lift": round(float(np.max(lifts)), 6),
        "mean_persistence_gap": round(float(np.mean(persist)), 6),
        "h020_cell_fraction": round(h020, 4),
        "h021_cell_fraction": round(h021, 4),
        "best_cell": max(cells, key=lambda c: c["lift"]),
        "n_errors": len(errors),
    }
    if ag_lifts:
        summary_out["mean_lift_ag"] = round(float(np.mean(ag_lifts)), 6)
        summary_out["max_lift_ag"] = round(float(np.max(ag_lifts)), 6)

    return {
        "protocol": protocol,
        "mode": "live_completions" if not skip_chat else "prompt_only",
        "grid": {
            "n_prompts": len(prompts),
            "turn_values": turn_values,
            "n_cells": len(cells),
            "include_ag": include_ag,
        },
        "cells": cells,
        "errors": errors,
        "summary": summary_out,
        "hypothesis_support": {
            "H-CCT-020": h020 >= 0.6,
            "H-CCT-021": h021 >= 0.6,
            "H-AMAT-004": h020 >= 0.6,
            "H-AMAT-003": h021 >= 0.5,
        },
    }
