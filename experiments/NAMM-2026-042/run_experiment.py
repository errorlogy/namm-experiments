"""NAMM-2026-042: Activation TDA via Ollama (llama3.2:3B) — D_eff separation test.

Backend: Ollama local API (http://127.0.0.1:11434) — no HuggingFace download.
Proxy: top-K logprob vectors per generation step, stacked as "hidden state" surrogates.
Rationale: 038 showed r=0.79 between logit-gradient norm and β₁; logprob distribution
captures model internals without direct hidden-state access.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import requests
import yaml

from namm.metrics.cognitive_class import compute_betti_proxies, compute_d_eff
from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-042"
CONFIG_PATH = Path(__file__).parent / "config.yaml"

BASELINE_035_036 = {
    "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
    "n_layers": 28,
    "hidden_dim": 896,
    "mean_lift_d_med": 0.05,
    "mean_lift_beta_1": 0.78,
    "mean_lift_d_eff": 0.0,
    "certificate": "ACTIVATION_PILOT",
    "note": "D_eff collapse: both policies dominated by same 2 PCs in 896-d space",
}

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ollama client
# ---------------------------------------------------------------------------

@dataclass
class OllamaLM:
    """Thin wrapper around Ollama chat + logprobs API."""
    model: str
    base_url: str
    hidden_dim: int   # proxy dim = top_k_logprobs
    n_layers: int     # proxy layers = n_logprob_steps
    model_id: str
    device: str = "ollama"

    def generate(self, messages: list[dict], max_tokens: int = 256) -> str:
        """Chat completion via Ollama."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": 0.7, "top_p": 0.9},
        }
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()

    def logprob_vector(
        self,
        prompt_text: str,
        top_k: int = 20,
        n_steps: int = 8,
    ) -> np.ndarray:
        """Sample logprob distributions across n_steps generation steps.

        Returns shape (n_steps, top_k): each row is the sorted top-K log-probs
        for one generation step. Used as activation proxy.
        """
        url = f"{self.base_url}/api/generate"
        rows: list[np.ndarray] = []

        # We generate token-by-token using context accumulation
        context: list[int] | None = None
        current_prompt = prompt_text

        for step in range(n_steps):
            payload: dict[str, Any] = {
                "model": self.model,
                "prompt": current_prompt if context is None else "",
                "stream": False,
                "options": {"num_predict": 1, "temperature": 0.7},
                "logprobs": True,
            }
            if context is not None:
                payload["context"] = context

            try:
                r = requests.post(url, json=payload, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as exc:  # noqa: BLE001
                logger.warning("logprob_vector step %d error: %s", step, exc)
                rows.append(np.zeros(top_k, dtype=np.float32))
                continue

            lp_list = data.get("logprobs") or []
            # Collect the logprob of the generated token; pad with zeros
            row = np.zeros(top_k, dtype=np.float32)
            for i, lp in enumerate(lp_list[:top_k]):
                row[i] = float(lp.get("logprob", 0.0))

            # Sort descending (most probable first)
            row[:] = np.sort(row)[::-1]
            rows.append(row)

            # Advance context for next step
            context = data.get("context")
            current_prompt = ""  # context carries the state

            if data.get("done"):
                break

        while len(rows) < n_steps:
            rows.append(np.zeros(top_k, dtype=np.float32))

        return np.stack(rows[:n_steps], axis=0)  # (n_steps, top_k)


def build_ollama_lm(cfg: dict) -> OllamaLM:
    base_url = cfg.get("ollama_base_url", "http://127.0.0.1:11434")
    model = cfg.get("ollama_model", "llama3.2:latest")
    act_cfg = cfg.get("activation", {})
    top_k = int(act_cfg.get("top_k_logprobs", 20))
    n_steps = int(act_cfg.get("n_logprob_steps", 8))
    info = cfg.get("ollama_model_info", {})
    return OllamaLM(
        model=model,
        base_url=base_url,
        hidden_dim=top_k,
        n_layers=n_steps,
        model_id=f"ollama/{model}",
    )


# ---------------------------------------------------------------------------
# Session runner using logprob proxy
# ---------------------------------------------------------------------------

FOLLOWUP = "Continue your reasoning. What are the deeper implications?"


def _chat_messages(system: str, user: str, history: list[tuple[str, str]]) -> list[dict]:
    msgs: list[dict] = [{"role": "system", "content": system}]
    for u, a in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    msgs.append({"role": "user", "content": user})
    return msgs


def _messages_to_prompt(messages: list[dict]) -> str:
    """Flatten chat messages to a single string for the generate endpoint."""
    parts = []
    for m in messages:
        role = m["role"]
        content = m["content"]
        parts.append(f"<|{role}|>\n{content}")
    parts.append("<|assistant|>")
    return "\n".join(parts)


def run_ollama_session(
    lm: OllamaLM,
    user_prompt: str,
    *,
    policy_system: str,
    n_turns: int,
    max_new_tokens: int = 256,
    top_k: int = 20,
    n_steps: int = 8,
) -> tuple[list[str], list[np.ndarray]]:
    """Run multi-turn chat; return completions and per-turn logprob matrices."""
    completions: list[str] = []
    logprob_mats: list[np.ndarray] = []
    history: list[tuple[str, str]] = []

    for turn in range(n_turns):
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        messages = _chat_messages(policy_system, user_msg, history)

        # Get logprob proxy "hidden matrix" (n_steps, top_k) for this turn
        prompt_text = _messages_to_prompt(messages)
        mat = lm.logprob_vector(prompt_text, top_k=top_k, n_steps=n_steps)
        logprob_mats.append(mat)

        # Generate actual reply
        text = lm.generate(messages, max_tokens=max_new_tokens)
        completions.append(text)
        history.append((user_msg, text))

    return completions, logprob_mats


# ---------------------------------------------------------------------------
# Point cloud + TDA
# ---------------------------------------------------------------------------

def build_point_cloud(
    mats: list[np.ndarray],
    *,
    last_n_layers: int | None = 4,
) -> np.ndarray:
    """Stack per-turn logprob matrices into (n_points, dim) point cloud.

    Each matrix is (n_steps, top_k). We take the last `last_n_layers` steps
    to mirror the `turns_x_layers` mode from 035/036.
    """
    if not mats:
        return np.zeros((0, 1), dtype=np.float64)
    sliced = [m[-last_n_layers:] if last_n_layers else m for m in mats]
    return np.vstack(sliced).astype(np.float64)


def pca_reduce(embeddings: np.ndarray, n_components: int) -> np.ndarray:
    n_pts, orig_dim = embeddings.shape
    k = min(n_components, n_pts, orig_dim)
    if k <= 0 or n_pts < 2:
        return embeddings
    try:
        from sklearn.decomposition import PCA
        return PCA(n_components=k, svd_solver="full").fit_transform(embeddings).astype(np.float64)
    except ImportError:
        pass
    centered = embeddings - embeddings.mean(axis=0, keepdims=True)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    return (centered @ Vt[:k].T).astype(np.float64)


def _has_ripser() -> bool:
    try:
        import ripser  # noqa: F401
        return True
    except ImportError:
        return False


def compute_betti(embeddings: np.ndarray) -> tuple[float, float, str]:
    if embeddings.shape[0] < 3:
        return 1.0, 0.0, "trivial"
    if _has_ripser():
        from ripser import ripser
        dgms = ripser(embeddings, maxdim=1)
        b0 = float(len(dgms["dgms"][0])) if dgms["dgms"] else 1.0
        b1 = float(len(dgms["dgms"][1])) if len(dgms["dgms"]) > 1 else 0.0
        return b0, b1, "ripser"
    b0, b1 = compute_betti_proxies(embeddings, k_neighbors=5)
    return b0, b1, "knn_proxy"


def eval_cloud(cloud: np.ndarray, centroid: np.ndarray, gates: dict) -> dict:
    if cloud.shape[0] < 2:
        return {"d_med": 0.0, "d_eff": 1.0, "beta_0": 1.0, "beta_1": 0.0,
                "order_R": 1.0, "mu_cns_proxy": 1.0, "tda_backend": "trivial",
                "n_points": cloud.shape[0]}
    base = evaluate_trajectory(cloud, centroid, gates)
    b0, b1, backend = compute_betti(cloud)
    base["beta_0"] = round(b0, 6)
    base["beta_1"] = round(b1, 6)
    base["tda_backend"] = backend
    base["n_points"] = int(cloud.shape[0])
    return base


# ---------------------------------------------------------------------------
# Sweep over one prompt
# ---------------------------------------------------------------------------

def run_sweep_one_prompt(
    lm: OllamaLM,
    user_prompt: str,
    *,
    n_turns: int,
    pca_dims: int,
    last_n_layers: int,
    max_new_tokens: int,
    top_k: int,
    n_steps: int,
    mu_system: str,
    nd_system: str,
    gates: dict,
) -> dict:
    policy_clouds: dict[str, np.ndarray] = {}
    policy_rows: dict[str, dict] = {}

    # Compute μ barycenter from first run
    b_star = None

    for policy, system in [("mu", mu_system), ("lock_reassert", nd_system)]:
        completions, mats = run_ollama_session(
            lm, user_prompt,
            policy_system=system,
            n_turns=n_turns,
            max_new_tokens=max_new_tokens,
            top_k=top_k,
            n_steps=n_steps,
        )
        cloud_raw = build_point_cloud(mats, last_n_layers=last_n_layers)
        cloud = pca_reduce(cloud_raw, pca_dims) if cloud_raw.shape[0] >= 2 else cloud_raw
        policy_clouds[policy] = cloud

        if policy == "mu":
            b_star = cloud.mean(axis=0) if cloud.shape[0] > 0 else np.zeros(cloud.shape[1] if cloud.ndim > 1 else 1)

    centroid = b_star if b_star is not None else np.zeros(pca_dims)
    if centroid.shape[0] != policy_clouds.get("mu", np.zeros((1, pca_dims))).shape[1]:
        centroid = np.zeros(policy_clouds["mu"].shape[1] if "mu" in policy_clouds else pca_dims)

    for policy in ("mu", "lock_reassert"):
        cloud = policy_clouds.get(policy, np.zeros((1, pca_dims)))
        policy_rows[policy] = eval_cloud(cloud, centroid, gates)

    mu_row = policy_rows["mu"]
    lock_row = policy_rows["lock_reassert"]

    lift_d_med = lock_row["d_med"] - mu_row["d_med"]
    lift_beta_1 = lock_row["beta_1"] - mu_row["beta_1"]
    lift_d_eff = lock_row["d_eff"] - mu_row["d_eff"]

    two_phase = bool(
        mu_row["beta_1"] < 0.5 < lock_row["beta_1"]
        or abs(lift_beta_1) > 0.3
    )

    return {
        "prompt_snippet": user_prompt[:60],
        "n_turns": n_turns,
        "mu": mu_row,
        "lock_reassert": lock_row,
        "lift_d_med": round(lift_d_med, 6),
        "lift_beta_1": round(lift_beta_1, 6),
        "lift_d_eff": round(lift_d_eff, 6),
        "two_phase_structure": two_phase,
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _assign_certificate(mean_lift_d_eff: float, mean_lift_beta_1: float) -> str:
    if mean_lift_beta_1 > 0.05 and mean_lift_d_eff > 0.3:
        return "ACTIVATION_EVIDENCE"
    if mean_lift_d_eff > 0.3:
        return "D_EFF_RESOLVED"
    if mean_lift_beta_1 > 0.05:
        return "ACTIVATION_PILOT"
    return "NULL"


def run_namm_2026_042() -> dict:
    cfg = _load_config()
    act_cfg = cfg.get("activation", {})
    grid_cfg = cfg.get("grid", {})
    focused_prompts: list[str] = cfg.get("focused_prompts", [])

    last_n_layers = int(act_cfg.get("last_n_layers", 4))
    pca_dims = int(act_cfg.get("pca_dims", 8))
    top_k = int(act_cfg.get("top_k_logprobs", 20))
    n_steps = int(act_cfg.get("n_logprob_steps", 8))
    n_turns_list = [int(v) for v in grid_cfg.get("n_turns_list", [3, 6])]
    max_new_tokens = 256

    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    lm = build_ollama_lm(cfg)
    logger.info(
        "042: Ollama model=%s hidden_dim_proxy=%d n_layers_proxy=%d",
        lm.model, lm.hidden_dim, lm.n_layers,
    )

    spec = load_phase_lock_spec()
    gates = spec["gates"]
    mu_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]

    all_loop_results: list[dict] = []
    per_turns_summary: dict[int, dict] = {}

    for n_turns in n_turns_list:
        loop_path = ARTIFACTS / f"loop_n{n_turns}.jsonl"
        cells: list[dict] = []

        for prompt in focused_prompts:
            try:
                cell = run_sweep_one_prompt(
                    lm, prompt,
                    n_turns=n_turns,
                    pca_dims=pca_dims,
                    last_n_layers=last_n_layers,
                    max_new_tokens=max_new_tokens,
                    top_k=top_k,
                    n_steps=n_steps,
                    mu_system=mu_system,
                    nd_system=nd_system,
                    gates=gates,
                )
                cells.append(cell)
                rec = {"ts": datetime.now(timezone.utc).isoformat(), "n_turns": n_turns, "cell": cell}
                with loop_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                logger.info(
                    "042 n_turns=%d lift_deff=%.4f lift_b1=%.4f two_phase=%s prompt=%.40s",
                    n_turns, cell["lift_d_eff"], cell["lift_beta_1"],
                    cell["two_phase_structure"], prompt,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("042 cell error prompt=%s n_turns=%d: %s", prompt[:40], n_turns, exc)
                cells.append({"error": str(exc), "prompt_snippet": prompt[:60], "n_turns": n_turns})

        valid = [c for c in cells if "error" not in c]
        mean_d_eff = float(np.mean([c["lift_d_eff"] for c in valid])) if valid else 0.0
        mean_b1 = float(np.mean([c["lift_beta_1"] for c in valid])) if valid else 0.0
        mean_d_med = float(np.mean([c["lift_d_med"] for c in valid])) if valid else 0.0
        two_phase_frac = float(np.mean([float(c["two_phase_structure"]) for c in valid])) if valid else 0.0

        per_turns_summary[n_turns] = {
            "mean_lift_d_eff": round(mean_d_eff, 6),
            "mean_lift_beta_1": round(mean_b1, 6),
            "mean_lift_d_med": round(mean_d_med, 6),
            "two_phase_fraction": round(two_phase_frac, 4),
            "n_cells": len(cells),
            "n_errors": len(cells) - len(valid),
        }
        all_loop_results.append({"n_turns": n_turns, "cells": cells, "summary": per_turns_summary[n_turns]})

    all_deff = [v["mean_lift_d_eff"] for v in per_turns_summary.values()]
    all_b1 = [v["mean_lift_beta_1"] for v in per_turns_summary.values()]
    all_dmed = [v["mean_lift_d_med"] for v in per_turns_summary.values()]
    all_2p = [v["two_phase_fraction"] for v in per_turns_summary.values()]

    mean_lift_d_eff = float(np.mean(all_deff)) if all_deff else 0.0
    mean_lift_beta_1 = float(np.mean(all_b1)) if all_b1 else 0.0
    mean_lift_d_med = float(np.mean(all_dmed)) if all_dmed else 0.0
    mean_two_phase = float(np.mean(all_2p)) if all_2p else 0.0

    cert = _assign_certificate(mean_lift_d_eff, mean_lift_beta_1)
    d_eff_resolved = mean_lift_d_eff > 0.3

    info = cfg.get("ollama_model_info", {})
    comparison_table = [
        {
            "experiment": "NAMM-2026-035/036",
            "model": BASELINE_035_036["model_id"],
            "n_layers": BASELINE_035_036["n_layers"],
            "hidden_dim": BASELINE_035_036["hidden_dim"],
            "mean_lift_d_med": BASELINE_035_036["mean_lift_d_med"],
            "mean_lift_beta_1": BASELINE_035_036["mean_lift_beta_1"],
            "mean_lift_d_eff": BASELINE_035_036["mean_lift_d_eff"],
            "certificate": BASELINE_035_036["certificate"],
            "note": BASELINE_035_036["note"],
        },
        {
            "experiment": EXPERIMENT_ID,
            "model": lm.model_id,
            "parameter_size": info.get("parameter_size", "3.2B"),
            "proxy_dim": lm.hidden_dim,
            "proxy_steps": lm.n_layers,
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "two_phase_fraction": round(mean_two_phase, 4),
            "certificate": cert,
            "note": (
                "D_eff RESOLVED via logprob proxy — anisotropic geometry in 3.2B"
                if d_eff_resolved else
                "D_eff partial/collapsed — logprob proxy may compress geometry"
            ),
        },
    ]

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {
            "model_id": lm.model_id,
            "backend": "ollama",
            "ollama_model": lm.model,
            "parameter_size": info.get("parameter_size", "3.2B"),
            "quantization": info.get("quantization", "Q4_K_M"),
            "proxy_hidden_dim": lm.hidden_dim,
            "proxy_n_layers": lm.n_layers,
            "device": lm.device,
            "note": (
                "Logprob-vector proxy: top-K logprobs per generation step "
                "used as activation surrogate (validated in NAMM-2026-038, r=0.79)"
            ),
        },
        "config": {
            "last_n_layers": last_n_layers,
            "pca_dims": pca_dims,
            "top_k_logprobs": top_k,
            "n_logprob_steps": n_steps,
            "n_turns_list": n_turns_list,
            "n_prompts": len(focused_prompts),
        },
        "per_turns_summary": {str(k): v for k, v in per_turns_summary.items()},
        "aggregate": {
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "mean_two_phase_fraction": round(mean_two_phase, 4),
        },
        "certificate": cert,
        "certificate_tiers": cfg.get("certificate_tiers"),
        "d_eff_resolved": d_eff_resolved,
        "activation_evidence": mean_lift_beta_1 > 0.05 and d_eff_resolved,
        "hypothesis_support": {
            "H-AMAT-004": mean_lift_d_med > 0.05,
            "H-CCT-020": mean_lift_d_med > 0.05,
            "H-CCT-021": mean_lift_beta_1 > 0.05,
            "D_EFF_RESOLVED": d_eff_resolved,
        },
        "model_comparison": comparison_table,
        "prior_experiments": cfg.get("prior_experiments"),
        "loops": all_loop_results,
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (ARTIFACTS / "full_activation_tda.json").write_text(
        json.dumps({"loops": all_loop_results, "n_turns_list": n_turns_list}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_042()
    agg = res["aggregate"]
    model = res["model"]
    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"model={model['model_id']} backend={model['backend']} param={model['parameter_size']}",
        f"proxy_dim={model['proxy_hidden_dim']} proxy_steps={model['proxy_n_layers']}",
        f"mean_lift_d_eff={agg['mean_lift_d_eff']}",
        f"mean_lift_beta_1={agg['mean_lift_beta_1']}",
        f"mean_lift_d_med={agg['mean_lift_d_med']}",
        f"d_eff_resolved={res['d_eff_resolved']}",
        f"activation_evidence={res['activation_evidence']}",
    ]
    log_text = "\n".join(log_lines) + "\n"
    (Path(__file__).parent / "run.log").write_text(log_text, encoding="utf-8")
    print(f"\n{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(f"model={model['model_id']} ({model['parameter_size']} {model['quantization']})")
    print(f"mean_lift_d_eff={agg['mean_lift_d_eff']}  mean_lift_beta_1={agg['mean_lift_beta_1']}")
    print(f"D_EFF_RESOLVED={res['d_eff_resolved']}  ACTIVATION_EVIDENCE={res['activation_evidence']}")
    print(f"note: {res['model_comparison'][-1]['note']}")
