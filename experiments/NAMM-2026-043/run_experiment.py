"""NAMM-2026-043: Hybrid nomic-embed-text TDA — resolve D_eff question.

HYBRID approach:
  - llama3.2 (Ollama) generates multi-turn completions
  - nomic-embed-text (Ollama, 768-d) embeds each completion
  - TDA on 768-d trajectory point clouds

Why 042 failed: logprob proxy is only 20-d — too compressed for TDA.
Why 035/036 D_eff=0: Qwen2.5-0.5B is too isotropic in 896-d.
This experiment: 768-d SEMANTIC space, richer than either prior approach.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import requests
import yaml

from namm.metrics.cognitive_class import compute_betti_proxies
from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-043"
CONFIG_PATH = Path(__file__).parent / "config.yaml"

BASELINE_035 = {
    "experiment": "NAMM-2026-035/036",
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "proxy": "real hidden states",
    "proxy_dim": 896,
    "mean_lift_beta_1": 0.78,
    "mean_lift_d_eff": 0.0,
    "certificate": "ACTIVATION_PILOT",
    "note": "D_eff collapse: both policies dominated by same 2 PCs (isotropic model)",
}

BASELINE_038 = {
    "experiment": "NAMM-2026-038",
    "model": "ollama/llama3.2:latest",
    "proxy": "Fisher curvature (logit-gradient norm)",
    "proxy_dim": 1,
    "mean_lift_beta_1": "r=0.79 corr",
    "mean_lift_d_eff": "N/A",
    "certificate": "CURVATURE_PILOT",
    "note": "Scalar geodesic curvature proxy — separates mu/lock via norm difference",
}

BASELINE_042 = {
    "experiment": "NAMM-2026-042",
    "model": "ollama/llama3.2:latest",
    "proxy": "logprob top-20",
    "proxy_dim": 20,
    "mean_lift_beta_1": 0.0,
    "mean_lift_d_eff": 0.0,
    "certificate": "NULL",
    "note": "20-d logprob space insufficient for TDA — collapses to trivial homology",
}

FOLLOWUP = (
    "Continue your analysis for one more turn. "
    "Explicitly state PHASE_STATE and whether you collapsed toward typical helpfulness."
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ollama helpers
# ---------------------------------------------------------------------------

def _check_model_available(base_url: str, model_name: str) -> bool:
    """Check if a model is available via Ollama /api/tags."""
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=10)
        r.raise_for_status()
        tags = r.json()
        for m in tags.get("models", []):
            name = m.get("name", "")
            if model_name.split(":")[0] in name:
                return True
        return False
    except Exception as exc:  # noqa: BLE001
        logger.warning("Ollama /api/tags check failed: %s", exc)
        return False


def _pull_model(base_url: str, model_name: str) -> None:
    """Pull an Ollama model (streams until done)."""
    logger.info("Pulling model %s from Ollama ...", model_name)
    r = requests.post(
        f"{base_url}/api/pull",
        json={"name": model_name, "stream": True},
        stream=True,
        timeout=600,
    )
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            try:
                d = json.loads(line)
                status = d.get("status", "")
                if status:
                    logger.info("pull: %s", status)
            except json.JSONDecodeError:
                pass
    logger.info("Model %s ready.", model_name)


def ensure_model(base_url: str, model_name: str) -> None:
    """Pull model if not already available."""
    if not _check_model_available(base_url, model_name):
        logger.info("%s not found locally — pulling (~274MB for nomic-embed-text)", model_name)
        _pull_model(base_url, model_name)
    else:
        logger.info("%s is available locally.", model_name)


def ollama_chat(
    base_url: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """Chat completion via Ollama."""
    r = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature, "top_p": top_p},
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def ollama_embed(base_url: str, model: str, text: str) -> np.ndarray:
    """Embed text via Ollama /api/embeddings → 768-d vector."""
    r = requests.post(
        f"{base_url}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    vec = data.get("embedding") or data.get("embeddings", [[]])[0]
    return np.array(vec, dtype=np.float64)


def ollama_embed_batch(base_url: str, model: str, texts: list[str]) -> np.ndarray:
    """Embed a list of texts → (n, 768) array."""
    rows: list[np.ndarray] = []
    for text in texts:
        try:
            rows.append(ollama_embed(base_url, model, text))
        except Exception as exc:  # noqa: BLE001
            logger.warning("embed failed for text snippet: %s — %s", text[:40], exc)
            rows.append(np.zeros(768, dtype=np.float64))
    return np.stack(rows, axis=0)


# ---------------------------------------------------------------------------
# Session runner
# ---------------------------------------------------------------------------

def _build_messages(system: str, user: str, history: list[tuple[str, str]]) -> list[dict]:
    msgs: list[dict] = [{"role": "system", "content": system}]
    for u, a in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    msgs.append({"role": "user", "content": user})
    return msgs


def run_session(
    base_url: str,
    gen_model: str,
    embed_model: str,
    user_prompt: str,
    *,
    system_resolver: Callable[[int], str],
    n_turns: int,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    pause_s: float = 0.5,
) -> tuple[list[str], np.ndarray]:
    """Multi-turn chat; embed each completion; return (completions, point_cloud).

    point_cloud shape: (n_turns, 768) — each row is the nomic embedding of one
    turn's completion text. This is the "activation proxy" for 043.
    """
    completions: list[str] = []
    embeddings: list[np.ndarray] = []
    history: list[tuple[str, str]] = []

    for turn in range(n_turns):
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        system = system_resolver(turn)
        messages = _build_messages(system, user_msg, history)

        text = ollama_chat(
            base_url, gen_model, messages,
            max_tokens=max_tokens, temperature=temperature, top_p=top_p,
        )
        vec = ollama_embed(base_url, embed_model, text)
        completions.append(text)
        embeddings.append(vec)
        history.append((user_msg, text))

        if pause_s > 0 and turn + 1 < n_turns:
            time.sleep(pause_s)

    cloud = np.stack(embeddings, axis=0)  # (n_turns, 768)
    return completions, cloud


# ---------------------------------------------------------------------------
# TDA utilities
# ---------------------------------------------------------------------------

def pca_reduce(embeddings: np.ndarray, n_components: int) -> np.ndarray:
    """PCA projection; handles degenerate cases."""
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


def compute_betti(embeddings: np.ndarray, max_dim: int = 1) -> tuple[float, float, str]:
    """β₀, β₁ via ripser or knn proxy."""
    if embeddings.shape[0] < 3:
        return 1.0, 0.0, "trivial"
    if _has_ripser():
        from ripser import ripser
        dgms = ripser(embeddings, maxdim=max_dim)
        b0 = float(len(dgms["dgms"][0])) if dgms["dgms"] else 1.0
        b1 = float(len(dgms["dgms"][1])) if len(dgms["dgms"]) > 1 else 0.0
        return b0, b1, "ripser"
    b0, b1 = compute_betti_proxies(embeddings, k_neighbors=5)
    return b0, b1, "knn_proxy"


def eval_cloud(cloud: np.ndarray, centroid: np.ndarray, gates: dict) -> dict:
    """Evaluate AMAT order parameters on a point cloud."""
    if cloud.shape[0] < 2:
        return {
            "d_med": 0.0, "d_eff": 1.0, "beta_0": 1.0, "beta_1": 0.0,
            "order_R": 1.0, "mu_cns_proxy": 1.0, "gates_passed": False,
            "tda_backend": "trivial", "n_points": cloud.shape[0],
        }
    base = evaluate_trajectory(cloud, centroid, gates)
    b0, b1, backend = compute_betti(cloud)
    base["beta_0"] = round(b0, 6)
    base["beta_1"] = round(b1, 6)
    base["tda_backend"] = backend
    base["n_points"] = int(cloud.shape[0])
    return base


# ---------------------------------------------------------------------------
# One-prompt sweep across policies
# ---------------------------------------------------------------------------

def sweep_one_prompt(
    base_url: str,
    gen_model: str,
    embed_model: str,
    user_prompt: str,
    *,
    n_turns: int,
    pca_dims: int,
    mu_system: str,
    nd_system: str,
    gates: dict,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    pause_s: float = 0.5,
) -> dict:
    """Run mu / lock_reassert / lock_decay; return per-policy metrics and lifts."""
    system_resolvers: dict[str, Callable[[int], str]] = {
        "mu": lambda _t: mu_system,
        "lock_reassert": lambda _t: nd_system,
        "lock_decay": lambda t: nd_system if t == 0 else mu_system,
    }

    policy_clouds: dict[str, np.ndarray] = {}
    policy_completions: dict[str, list[str]] = {}

    for policy, system_resolver in system_resolvers.items():
        completions, cloud = run_session(
            base_url, gen_model, embed_model, user_prompt,
            system_resolver=system_resolver,
            n_turns=n_turns,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            pause_s=pause_s,
        )
        policy_completions[policy] = completions

        # PCA-reduce from 768 → pca_dims
        cloud_pca = pca_reduce(cloud, pca_dims) if cloud.shape[0] >= 2 else cloud
        policy_clouds[policy] = cloud_pca

    # Barycenter: mean of μ policy point cloud
    mu_cloud = policy_clouds["mu"]
    b_star = mu_cloud.mean(axis=0) if mu_cloud.shape[0] > 0 else np.zeros(pca_dims)

    policy_metrics: dict[str, dict] = {}
    for policy, cloud in policy_clouds.items():
        policy_metrics[policy] = eval_cloud(cloud, b_star, gates)

    mu_m = policy_metrics["mu"]
    lock_m = policy_metrics["lock_reassert"]
    decay_m = policy_metrics["lock_decay"]

    lift_d_med = lock_m["d_med"] - mu_m["d_med"]
    lift_beta_1 = lock_m["beta_1"] - mu_m["beta_1"]
    lift_d_eff = lock_m["d_eff"] - mu_m["d_eff"]
    decay_gap = lock_m["d_med"] - decay_m["d_med"]

    two_phase = bool(
        (mu_m["beta_1"] < 0.5 and lock_m["beta_1"] >= 0.5)
        or abs(lift_beta_1) > 0.3
        or (lift_d_eff > 0.3 and lift_d_med > 0.05)
    )

    return {
        "prompt_snippet": user_prompt[:80],
        "n_turns": n_turns,
        "pca_dims": pca_dims,
        "embed_dim_before_pca": 768,
        "tda_backend": lock_m.get("tda_backend", "unknown"),
        "policies": policy_metrics,
        "lift_d_med": round(lift_d_med, 6),
        "lift_beta_1": round(lift_beta_1, 6),
        "lift_d_eff": round(lift_d_eff, 6),
        "decay_gap": round(decay_gap, 6),
        "two_phase_structure": two_phase,
        "completions_preview": {p: c[0][:120] if c else "" for p, c in policy_completions.items()},
    }


# ---------------------------------------------------------------------------
# Certificate assignment
# ---------------------------------------------------------------------------

def _assign_certificate(mean_lift_d_eff: float, mean_lift_beta_1: float) -> str:
    if mean_lift_beta_1 > 0.05 and mean_lift_d_eff > 0.3:
        return "HYBRID_EVIDENCE"
    if mean_lift_d_eff > 0.3:
        return "D_EFF_RESOLVED"
    if mean_lift_beta_1 > 0.05 or mean_lift_d_eff > 0.1:
        return "HYBRID_PILOT"
    return "NULL"


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_namm_2026_043() -> dict:
    cfg = _load_config()
    gen_cfg = cfg.get("generator", {})
    emb_cfg = cfg.get("embedder", {})
    tda_cfg = cfg.get("tda", {})
    grid_cfg = cfg.get("grid", {})
    focused_prompts: list[str] = cfg.get("focused_prompts", [])

    base_url = gen_cfg.get("base_url", "http://127.0.0.1:11434")
    gen_model = gen_cfg.get("model", "llama3.2:latest")
    embed_model = emb_cfg.get("model", "nomic-embed-text")
    pca_dims = int(tda_cfg.get("pca_dims", 8))
    n_turns_list: list[int] = [int(v) for v in grid_cfg.get("n_turns_list", [3, 6])]
    max_tokens = int(gen_cfg.get("max_new_tokens", 256))
    temperature = float(gen_cfg.get("temperature", 0.7))
    top_p = float(gen_cfg.get("top_p", 0.9))

    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    # Ensure nomic-embed-text is available
    logger.info("043: Checking Ollama model availability ...")
    ensure_model(base_url, gen_model)
    ensure_model(base_url, embed_model)

    spec = load_phase_lock_spec()
    gates = spec["gates"]
    mu_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]

    logger.info(
        "043: gen_model=%s embed_model=%s pca_dims=%d n_turns=%s",
        gen_model, embed_model, pca_dims, n_turns_list,
    )

    all_loop_results: list[dict] = []
    per_turns_summary: dict[int, dict] = {}

    for n_turns in n_turns_list:
        loop_path = ARTIFACTS / f"loop_n{n_turns}.jsonl"
        cells: list[dict] = []

        for prompt in focused_prompts:
            try:
                cell = sweep_one_prompt(
                    base_url, gen_model, embed_model, prompt,
                    n_turns=n_turns,
                    pca_dims=pca_dims,
                    mu_system=mu_system,
                    nd_system=nd_system,
                    gates=gates,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                )
                cells.append(cell)
                rec = {"ts": datetime.now(timezone.utc).isoformat(), "n_turns": n_turns, "cell": cell}
                with loop_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                logger.info(
                    "043 n_turns=%d lift_deff=%.4f lift_b1=%.4f two_phase=%s tda=%s prompt=%.40s",
                    n_turns, cell["lift_d_eff"], cell["lift_beta_1"],
                    cell["two_phase_structure"], cell["tda_backend"], prompt,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("043 cell error prompt=%s n_turns=%d: %s", prompt[:40], n_turns, exc)
                cells.append({"error": str(exc), "prompt_snippet": prompt[:80], "n_turns": n_turns})

        valid = [c for c in cells if "error" not in c]
        mean_d_eff = float(np.mean([c["lift_d_eff"] for c in valid])) if valid else 0.0
        mean_b1 = float(np.mean([c["lift_beta_1"] for c in valid])) if valid else 0.0
        mean_d_med = float(np.mean([c["lift_d_med"] for c in valid])) if valid else 0.0
        mean_decay_gap = float(np.mean([c["decay_gap"] for c in valid])) if valid else 0.0
        two_phase_frac = float(np.mean([float(c["two_phase_structure"]) for c in valid])) if valid else 0.0

        per_turns_summary[n_turns] = {
            "mean_lift_d_eff": round(mean_d_eff, 6),
            "mean_lift_beta_1": round(mean_b1, 6),
            "mean_lift_d_med": round(mean_d_med, 6),
            "mean_decay_gap": round(mean_decay_gap, 6),
            "two_phase_fraction": round(two_phase_frac, 4),
            "n_cells": len(cells),
            "n_errors": len(cells) - len(valid),
        }
        all_loop_results.append({
            "n_turns": n_turns,
            "cells": cells,
            "summary": per_turns_summary[n_turns],
        })
        logger.info(
            "043 n_turns=%d SUMMARY lift_deff=%.4f lift_b1=%.4f two_phase=%.2f",
            n_turns, mean_d_eff, mean_b1, two_phase_frac,
        )

    # Aggregate across all n_turns
    all_deff = [v["mean_lift_d_eff"] for v in per_turns_summary.values()]
    all_b1 = [v["mean_lift_beta_1"] for v in per_turns_summary.values()]
    all_dmed = [v["mean_lift_d_med"] for v in per_turns_summary.values()]
    all_decay = [v["mean_decay_gap"] for v in per_turns_summary.values()]
    all_2p = [v["two_phase_fraction"] for v in per_turns_summary.values()]

    mean_lift_d_eff = float(np.mean(all_deff)) if all_deff else 0.0
    mean_lift_beta_1 = float(np.mean(all_b1)) if all_b1 else 0.0
    mean_lift_d_med = float(np.mean(all_dmed)) if all_dmed else 0.0
    mean_decay_gap = float(np.mean(all_decay)) if all_decay else 0.0
    mean_two_phase = float(np.mean(all_2p)) if all_2p else 0.0

    cert = _assign_certificate(mean_lift_d_eff, mean_lift_beta_1)
    d_eff_resolved = mean_lift_d_eff > 0.3
    hybrid_evidence = mean_lift_beta_1 > 0.05 and d_eff_resolved

    # Comparison table: 035 vs 038 vs 042 vs 043
    comparison_table: list[dict[str, Any]] = [
        BASELINE_035,
        BASELINE_038,
        BASELINE_042,
        {
            "experiment": EXPERIMENT_ID,
            "model": f"ollama/{gen_model}",
            "proxy": f"nomic-embed-text 768-d (semantic)",
            "proxy_dim": 768,
            "pca_dims": pca_dims,
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "mean_decay_gap": round(mean_decay_gap, 6),
            "two_phase_fraction": round(mean_two_phase, 4),
            "certificate": cert,
            "d_eff_resolved": d_eff_resolved,
            "note": (
                "D_eff RESOLVED — semantic embedding space anisotropic enough"
                if d_eff_resolved else
                "D_eff partial/collapsed — semantic space still collapses to low-D"
                if mean_lift_d_eff > 0.0 else
                "D_eff=0 — nomic-embed geometry as isotropic as Qwen0.5B hidden states"
            ),
        },
    ]

    payload: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline": {
            "generator": gen_model,
            "embedder": embed_model,
            "embed_dim": 768,
            "pca_dims": pca_dims,
            "n_turns_list": n_turns_list,
            "n_prompts": len(focused_prompts),
            "tda": "ripser" if _has_ripser() else "knn_proxy",
        },
        "per_turns_summary": {str(k): v for k, v in per_turns_summary.items()},
        "aggregate": {
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "mean_decay_gap": round(mean_decay_gap, 6),
            "mean_two_phase_fraction": round(mean_two_phase, 4),
        },
        "certificate": cert,
        "certificate_tiers": cfg.get("certificate_tiers"),
        "d_eff_resolved": d_eff_resolved,
        "hybrid_evidence": hybrid_evidence,
        "hypothesis_support": {
            "H-AMAT-004": mean_lift_d_med > 0.05,
            "H-CCT-020": mean_lift_d_med > 0.05,
            "H-CCT-021": mean_lift_beta_1 > 0.05,
            "D_EFF_RESOLVED": d_eff_resolved,
            "HYBRID_EVIDENCE": hybrid_evidence,
        },
        "model_comparison": comparison_table,
        "prior_experiments": cfg.get("prior_experiments"),
        "loops": all_loop_results,
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    (ARTIFACTS / "full_hybrid_tda.json").write_text(
        json.dumps({"loops": all_loop_results, "n_turns_list": n_turns_list}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_043()
    agg = res["aggregate"]
    pipe = res["pipeline"]
    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"generator={pipe['generator']}  embedder={pipe['embedder']}  embed_dim={pipe['embed_dim']}",
        f"pca_dims={pipe['pca_dims']}  tda_backend={pipe['tda']}",
        f"mean_lift_d_eff={agg['mean_lift_d_eff']}",
        f"mean_lift_beta_1={agg['mean_lift_beta_1']}",
        f"mean_lift_d_med={agg['mean_lift_d_med']}",
        f"mean_decay_gap={agg['mean_decay_gap']}",
        f"d_eff_resolved={res['d_eff_resolved']}",
        f"hybrid_evidence={res['hybrid_evidence']}",
    ]
    log_text = "\n".join(log_lines) + "\n"
    (Path(__file__).parent / "run.log").write_text(log_text, encoding="utf-8")

    print(f"\n{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(f"generator={pipe['generator']}  embedder={pipe['embedder']} (768-d)")
    print(f"mean_lift_d_eff={agg['mean_lift_d_eff']}  mean_lift_beta_1={agg['mean_lift_beta_1']}")
    print(f"D_EFF_RESOLVED={res['d_eff_resolved']}  HYBRID_EVIDENCE={res['hybrid_evidence']}")
    print("\nModel comparison table:")
    for row in res["model_comparison"]:
        print(
            f"  [{row['experiment']}] proxy={row['proxy']} dim={row['proxy_dim']}"
            f" beta1={row['mean_lift_beta_1']} D_eff={row['mean_lift_d_eff']}"
            f" cert={row['certificate']}"
        )
