"""NAMM-2026-044: D_eff sensitivity — safe PCA cap + more points.

This is a direct sibling of NAMM-2026-043, with a focused protocol tweak for
activation-trajectory topological stability:

- Increase point-cloud support: n_turns in {6, 9} with 2 completion samples per turn
  (12–18 embed points vs 043's 3–6).
- Enforce a safe PCA component cap based on (n_points - 1) and log:
  actual n_points, PCA k used, and numerical effective rank.

Goal: diagnose the D_eff mean_lift separation failure mode from 043
(beta_1 lift = 0; two_phase_fraction = 0) as either:
  (a) sampling collapse / rank degeneracy, or
  (b) metric insensitivity to the μ vs lock reassert perturbation.
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

from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-044"
CONFIG_PATH = Path(__file__).parent / "config.yaml"

BASELINE_043 = {
    "experiment": "NAMM-2026-043",
    "protocol": "amat-hybrid-nomic-embed-v1",
    "n_turns_list": [3, 6],
    "n_completions_per_turn": 1,
    "pca_dims": 8,
    "ripser_metric": "euclidean",
    "mean_lift_d_eff": -0.5,
    "mean_lift_beta_1": 0.0,
    "mean_lift_d_med": 2.422314,
    "two_phase_fraction": 0.0,
    "certificate": "NULL",
    "note": "Small trajectories; PCA capped at min(8, n_points); β₁=0, D_eff lift negative",
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
        logger.info(" %s not found locally — pulling (~274MB for nomic-embed-text)", model_name)
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
    # Retries matter because long completions can exceed the default HTTP
    # read timeout even when Ollama is otherwise healthy.
    chat_timeout_s = 360
    retry_count = 4
    last_exc: Exception | None = None
    for attempt in range(retry_count):
        try:
            r = requests.post(
                f"{base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                    },
                },
                timeout=chat_timeout_s,
            )
            r.raise_for_status()
            return r.json()["message"]["content"].strip()
        except requests.exceptions.ReadTimeout as exc:
            last_exc = exc
            logger.warning(
                "ollama_chat ReadTimeout attempt %d/%d (timeout=%ss). Retrying ...",
                attempt + 1,
                retry_count,
                chat_timeout_s,
            )
            time.sleep(2.0 * (attempt + 1))
    # If all retries failed, bubble up the last exception.
    assert last_exc is not None
    raise last_exc


def ollama_embed(base_url: str, model: str, text: str) -> np.ndarray:
    """Embed text via Ollama /api/embeddings → 768-d vector."""
    r = requests.post(
        f"{base_url}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    vec = data.get("embedding") or data.get("embeddings", [[]])[0]
    return np.array(vec, dtype=np.float64)


def ollama_embed_batch(base_url: str, model: str, texts: list[str]) -> np.ndarray:
    """Embed a list of texts → (n, embed_dim) array."""
    rows: list[np.ndarray] = []
    for text in texts:
        try:
            rows.append(ollama_embed(base_url, model, text))
        except Exception as exc:  # noqa: BLE001
            logger.warning("embed failed for text snippet: %s — %s", text[:40], exc)
            # Keep point-count stable even if an embed failed.
            rows.append(np.zeros(768, dtype=np.float64))
    return np.stack(rows, axis=0)


# ---------------------------------------------------------------------------
# Session runner (trajectory → point cloud)
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
    n_completions_per_turn: int = 1,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    pause_s: float = 0.5,
) -> tuple[list[str], np.ndarray]:
    """Multi-turn chat; embed each completion; return (completions, point_cloud).

    point_cloud shape: (n_turns * n_completions_per_turn, embed_dim).
    Multiple completions per turn expand support without lengthening dialogue.
    """
    completions: list[str] = []
    embeddings: list[np.ndarray] = []
    history: list[tuple[str, str]] = []

    for turn in range(n_turns):
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        system = system_resolver(turn)
        messages = _build_messages(system, user_msg, history)

        turn_texts: list[str] = []
        for _sample in range(max(1, n_completions_per_turn)):
            text = ollama_chat(
                base_url,
                gen_model,
                messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            vec = ollama_embed(base_url, embed_model, text)
            turn_texts.append(text)
            completions.append(text)
            embeddings.append(vec)

        # Advance dialogue with the first sample (stable history for follow-ups).
        history.append((user_msg, turn_texts[0]))

        if pause_s > 0 and turn + 1 < n_turns:
            time.sleep(pause_s)

    cloud = np.stack(embeddings, axis=0)
    return completions, cloud


# ---------------------------------------------------------------------------
# PCA with diagnostics + safe component cap
# ---------------------------------------------------------------------------


def pca_reduce_diagnostics(
    embeddings: np.ndarray,
    *,
    requested_n_components: int,
    rank_eps: float,
) -> tuple[np.ndarray, dict[str, Any]]:
    """PCA projection with numerical effective-rank diagnostics.

    Safe cap rule (protocol improvement):
      - maximum meaningful number of PCs for an n_points cloud is <= (n_points - 1),
        because the centered matrix has rank at most (n_points - 1).
    """
    n_pts, orig_dim = embeddings.shape
    centered = embeddings - embeddings.mean(axis=0, keepdims=True)

    diag: dict[str, Any] = {
        "n_points": int(n_pts),
        "orig_dim": int(orig_dim),
        "requested_pca_dims": int(requested_n_components),
    }
    if n_pts < 2:
        diag.update({"pca_k_used": int(0), "effective_rank": int(0)})
        return embeddings, diag

    # SVD for both projection and numerical rank estimate.
    # full_matrices=False yields shapes: U (n_pts, r), S (r,), Vt (r, orig_dim)
    _, s, v_t = np.linalg.svd(centered, full_matrices=False)
    max_s = float(np.max(s)) if s.size else 0.0
    # Numerical effective rank: count singular values above eps * max singular.
    eff_rank = int(np.sum(s > rank_eps * max_s)) if max_s > 0 else 0
    diag["effective_rank"] = eff_rank

    max_meaningful = max(1, n_pts - 1)
    diag["max_meaningful_components"] = int(max_meaningful)
    # Protocol: for stability across μ/lock policies, keep PCA dimensionality
    # consistent for a given n_points by NOT additionally capping on the
    # per-policy numerical effective rank. We still log effective_rank.
    k = int(min(requested_n_components, max_meaningful, orig_dim))
    diag["pca_k_used"] = int(k)

    if k <= 0 or n_pts < 2:
        return embeddings, diag

    projected = (centered @ v_t[:k].T).astype(np.float64, copy=False)

    # Variance explained by the chosen k (useful to see if we hit the
    # rank/variance-collapse boundary).
    var = (s**2) / max(float(np.sum(s**2)), 1e-12)
    cum = np.cumsum(var)
    diag["pca_cum_variance_at_k"] = float(cum[min(k - 1, len(cum) - 1)]) if cum.size else 0.0
    return projected, diag


# ---------------------------------------------------------------------------
# TDA utilities (ripser if available, else k-NN proxy)
# ---------------------------------------------------------------------------


def _has_ripser() -> bool:
    try:
        import ripser  # noqa: F401

        return True
    except ImportError:
        return False


def _pairwise_distances(embeddings: np.ndarray, metric: str) -> np.ndarray:
    """Pairwise distances for k-NN proxy (euclidean or cosine)."""
    if metric == "cosine":
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-12)
        unit = embeddings / norms
        sim = unit @ unit.T
        return 1.0 - sim
    return np.linalg.norm(embeddings[:, None, :] - embeddings[None, :, :], axis=2)


def compute_betti_proxies_metric(
    embeddings: np.ndarray,
    *,
    k_neighbors: int,
    metric: str,
) -> tuple[float, float]:
    """k-NN graph β₀/β₁ with configurable metric."""
    import networkx as nx

    n = embeddings.shape[0]
    if n < 3:
        return 1.0, 0.0

    k = min(k_neighbors, n - 1)
    dists = _pairwise_distances(embeddings, metric)
    np.fill_diagonal(dists, np.inf)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for i in range(n):
        neighbors = np.argsort(dists[i])[:k]
        for j in neighbors:
            g.add_edge(i, int(j))

    beta_0 = float(nx.number_connected_components(g))
    beta_1 = 0.0
    for comp in nx.connected_components(g):
        sub = g.subgraph(comp)
        v = sub.number_of_nodes()
        e = sub.number_of_edges()
        beta_1 += max(0, e - v + 1)
    return beta_0, float(beta_1)


def compute_betti(
    embeddings: np.ndarray,
    *,
    max_dim: int,
    k_neighbors: int,
    metric: str = "euclidean",
) -> tuple[float, float, str, dict[str, Any]]:
    """β₀, β₁ via ripser (with metric) or k-NN proxy."""
    ripser_settings: dict[str, Any] = {"metric": metric, "maxdim": max_dim}
    if embeddings.shape[0] < 3:
        return 1.0, 0.0, "trivial", ripser_settings

    if _has_ripser():
        from ripser import ripser

        dgms = ripser(embeddings, maxdim=max_dim, metric=metric)
        b0 = float(len(dgms["dgms"][0])) if dgms["dgms"] else 1.0
        b1 = float(len(dgms["dgms"][1])) if len(dgms["dgms"]) > 1 else 0.0
        ripser_settings["backend"] = "ripser"
        return b0, b1, f"ripser_{metric}", ripser_settings

    b0, b1 = compute_betti_proxies_metric(
        embeddings, k_neighbors=k_neighbors, metric=metric
    )
    ripser_settings["backend"] = "knn_proxy"
    ripser_settings["k_neighbors"] = k_neighbors
    return b0, b1, f"knn_proxy_{metric}", ripser_settings


def eval_cloud(
    cloud: np.ndarray,
    centroid: np.ndarray,
    gates: dict,
    *,
    tda_backend_max_dim: int,
    tda_backend_k_neighbors: int,
    tda_metric: str,
) -> dict[str, Any]:
    """Evaluate AMAT order parameters on a point cloud."""
    if cloud.shape[0] < 2:
        return {
            "d_med": 0.0,
            "d_eff": 1.0,
            "beta_0": 1.0,
            "beta_1": 0.0,
            "order_R": 1.0,
            "mu_cns_proxy": 1.0,
            "gates_passed": False,
            "tda_backend": "trivial",
            "n_points": int(cloud.shape[0]),
            "ripser_settings": {"metric": tda_metric, "maxdim": tda_backend_max_dim},
        }

    base = evaluate_trajectory(cloud, centroid, gates)
    b0, b1, backend, ripser_settings = compute_betti(
        cloud,
        max_dim=tda_backend_max_dim,
        k_neighbors=tda_backend_k_neighbors,
        metric=tda_metric,
    )
    base["beta_0"] = round(b0, 6)
    base["beta_1"] = round(b1, 6)
    base["tda_backend"] = backend
    base["n_points"] = int(cloud.shape[0])
    base["ripser_settings"] = ripser_settings
    return base


# ---------------------------------------------------------------------------
# One prompt sweep across policies
# ---------------------------------------------------------------------------


def sweep_one_prompt(
    base_url: str,
    gen_model: str,
    embed_model: str,
    user_prompt: str,
    *,
    n_turns: int,
    n_completions_per_turn: int,
    pca_dims: int,
    pca_rank_eps: float,
    mu_system: str,
    nd_system: str,
    gates: dict,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    pause_s: float = 0.5,
    tda_max_dim: int = 1,
    tda_k_neighbors: int = 5,
    tda_metric: str = "cosine",
) -> dict[str, Any]:
    """Run μ / lock_reassert / lock_decay; return per-policy metrics and lifts."""
    system_resolvers: dict[str, Callable[[int], str]] = {
        "mu": lambda _t: mu_system,
        "lock_reassert": lambda _t: nd_system,
        "lock_decay": lambda t: nd_system if t == 0 else mu_system,
    }

    policy_clouds: dict[str, np.ndarray] = {}
    policy_pca_diags: dict[str, dict[str, Any]] = {}
    policy_completions: dict[str, list[str]] = {}

    for policy, system_resolver in system_resolvers.items():
        completions, cloud = run_session(
            base_url,
            gen_model,
            embed_model,
            user_prompt,
            system_resolver=system_resolver,
            n_turns=n_turns,
            n_completions_per_turn=n_completions_per_turn,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            pause_s=pause_s,
        )
        policy_completions[policy] = completions

        # PCA-reduce from 768 → pca_dims, but with safe rank-aware cap.
        cloud_pca, pca_diag = pca_reduce_diagnostics(
            cloud,
            requested_n_components=pca_dims,
            rank_eps=pca_rank_eps,
        )
        policy_clouds[policy] = cloud_pca
        policy_pca_diags[policy] = pca_diag
        logger.info(
            "044 policy=%s n_turns=%d n_points=%d pca_k=%s eff_rank=%s",
            policy,
            n_turns,
            pca_diag.get("n_points"),
            pca_diag.get("pca_k_used"),
            pca_diag.get("effective_rank"),
        )

    # Barycenter: mean of μ policy point cloud (in PCA space).
    mu_cloud = policy_clouds["mu"]
    b_star = mu_cloud.mean(axis=0) if mu_cloud.shape[0] > 0 else np.zeros(policy_clouds["mu"].shape[1])

    policy_metrics: dict[str, dict[str, Any]] = {}
    for policy, cloud in policy_clouds.items():
        metrics = eval_cloud(
            cloud,
            b_star,
            gates,
            tda_backend_max_dim=tda_max_dim,
            tda_backend_k_neighbors=tda_k_neighbors,
            tda_metric=tda_metric,
        )
        metrics["pca_diag"] = policy_pca_diags[policy]
        policy_metrics[policy] = metrics

    mu_m = policy_metrics["mu"]
    lock_m = policy_metrics["lock_reassert"]
    decay_m = policy_metrics["lock_decay"]

    lift_d_med = lock_m["d_med"] - mu_m["d_med"]
    lift_beta_1 = lock_m["beta_1"] - mu_m["beta_1"]
    lift_d_eff = lock_m["d_eff"] - mu_m["d_eff"]
    decay_gap = lock_m["d_med"] - decay_m["d_med"]

    # Keep the same two-phase definition as 043, so 044 isolates the sampling/PCA
    # stability effect rather than changing the decision boundary.
    two_phase = bool(
        (mu_m["beta_1"] < 0.5 and lock_m["beta_1"] >= 0.5)
        or abs(lift_beta_1) > 0.3
        or (lift_d_eff > 0.3 and lift_d_med > 0.05)
    )

    return {
        "prompt_snippet": user_prompt[:80],
        "n_turns": n_turns,
        "n_completions_per_turn": n_completions_per_turn,
        "n_points_expected": n_turns * max(1, n_completions_per_turn),
        "pca_dims_requested": pca_dims,
        "pca_rank_eps": pca_rank_eps,
        "tda_metric": tda_metric,
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


def _write_payload(
    *,
    cfg: dict,
    gen_model: str,
    embed_model: str,
    emb_cfg: dict,
    pca_dims: int,
    pca_rank_eps: float,
    n_turns_list: list[int],
    n_completions_per_turn: int,
    focused_prompts: list[str],
    tda_max_dim: int,
    tda_k_neighbors: int,
    tda_metric: str,
    per_turns_summary: dict[int, dict[str, Any]],
    all_loop_results: list[dict],
    partial: bool = False,
) -> dict[str, Any]:
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
    hybrid_evidence = mean_lift_beta_1 > 0.05 and d_eff_resolved

    payload: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "partial_run": partial,
        "pipeline": {
            "generator": gen_model,
            "embedder": embed_model,
            "embed_dim": int(emb_cfg.get("embed_dim", 768)),
            "pca_dims_requested": pca_dims,
            "pca_rank_eps": pca_rank_eps,
            "pca_cap_rule": "k = min(requested_pca_dims, n_points-1, orig_dim)",
            "n_turns_list": n_turns_list,
            "n_completions_per_turn": n_completions_per_turn,
            "n_prompts": len(focused_prompts),
            "tda": {
                "backend": "ripser_if_available_else_knn_proxy",
                "max_dim": tda_max_dim,
                "k_neighbors": tda_k_neighbors,
                "metric": tda_metric,
            },
        },
        "per_turns_summary": {str(k): v for k, v in per_turns_summary.items()},
        "aggregate": {
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "mean_two_phase_fraction": round(mean_two_phase, 4),
        },
        "certificate": cert,
        "d_eff_resolved": d_eff_resolved,
        "hybrid_evidence": hybrid_evidence,
        "hypothesis_support": {
            "H-AMAT-004": mean_lift_d_med > 0.05,
            "H-CCT-020": mean_lift_d_med > 0.05,
            "H-CCT-021": mean_lift_beta_1 > 0.05,
            "D_EFF_RESOLVED": d_eff_resolved,
            "HYBRID_EVIDENCE": hybrid_evidence,
        },
        "comparison_vs_043": {
            "043": BASELINE_043,
            "044": {
                "experiment": EXPERIMENT_ID,
                "protocol": cfg.get("protocol_version"),
                "n_turns_list": n_turns_list,
                "n_completions_per_turn": n_completions_per_turn,
                "pca_dims_requested": pca_dims,
                "tda_metric": tda_metric,
                "mean_lift_d_eff": round(mean_lift_d_eff, 6),
                "mean_lift_beta_1": round(mean_lift_beta_1, 6),
                "mean_lift_d_med": round(mean_lift_d_med, 6),
                "two_phase_fraction": round(mean_two_phase, 4),
                "certificate": cert,
                "diagnostics": {
                    "pca_cap_rule": "k = min(requested, n_points-1, orig_dim)",
                    "per_turns_summary": {str(k): v for k, v in per_turns_summary.items()},
                },
            },
            "delta_d_eff_lift": round(mean_lift_d_eff - BASELINE_043["mean_lift_d_eff"], 6),
            "delta_beta1_lift": round(mean_lift_beta_1 - BASELINE_043["mean_lift_beta_1"], 6),
            "delta_d_med_lift": round(mean_lift_d_med - BASELINE_043["mean_lift_d_med"], 6),
            "two_phase_improved": mean_two_phase > BASELINE_043["two_phase_fraction"],
        },
        "loops": all_loop_results,
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (ARTIFACTS / "full_hybrid_tda.json").write_text(
        json.dumps({"loops": all_loop_results, "n_turns_list": n_turns_list}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


def run_namm_2026_044() -> dict[str, Any]:
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
    pca_rank_eps = float(tda_cfg.get("pca_rank_eps", 1.0e-6))
    tda_k_neighbors = int(tda_cfg.get("k_neighbors", 5))
    tda_max_dim = int(tda_cfg.get("max_dim", 1))
    tda_metric = str(tda_cfg.get("ripser_metric", "cosine"))

    n_turns_list: list[int] = [int(v) for v in grid_cfg.get("n_turns_list", [6, 9, 12])]
    n_completions_per_turn = int(grid_cfg.get("n_completions_per_turn", 1))
    max_tokens = int(gen_cfg.get("max_new_tokens", 256))
    temperature = float(gen_cfg.get("temperature", 0.7))
    top_p = float(gen_cfg.get("top_p", 0.9))
    pause_s = float(gen_cfg.get("pause_s", 0.5))

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    # Fresh run: avoid mixed append-only jsonl from prior partial executions.
    for stale in ARTIFACTS.glob("loop_n*.jsonl"):
        stale.unlink(missing_ok=True)
    for stale in (ARTIFACTS / "summary.json", ARTIFACTS / "full_hybrid_tda.json"):
        stale.unlink(missing_ok=True)

    # Ensure Ollama models are available.
    logger.info("044: Checking Ollama model availability ...")
    ensure_model(base_url, gen_model)
    ensure_model(base_url, embed_model)

    spec = load_phase_lock_spec()
    gates = spec["gates"]
    mu_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]

    logger.info(
        "044: gen_model=%s embed_model=%s pca_dims=%d pca_rank_eps=%g n_turns=%s n_compl/turn=%d metric=%s",
        gen_model,
        embed_model,
        pca_dims,
        pca_rank_eps,
        n_turns_list,
        n_completions_per_turn,
        tda_metric,
    )

    all_loop_results: list[dict] = []
    per_turns_summary: dict[int, dict[str, Any]] = {}

    for n_turns in n_turns_list:
        loop_path = ARTIFACTS / f"loop_n{n_turns}.jsonl"
        if loop_path.exists():
            loop_path.unlink()
        cells: list[dict] = []

        for prompt in focused_prompts:
            try:
                cell = sweep_one_prompt(
                    base_url,
                    gen_model,
                    embed_model,
                    prompt,
                    n_turns=n_turns,
                    n_completions_per_turn=n_completions_per_turn,
                    pca_dims=pca_dims,
                    pca_rank_eps=pca_rank_eps,
                    mu_system=mu_system,
                    nd_system=nd_system,
                    gates=gates,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    pause_s=pause_s,
                    tda_max_dim=tda_max_dim,
                    tda_k_neighbors=tda_k_neighbors,
                    tda_metric=tda_metric,
                )
                cells.append(cell)

                rec = {"ts": datetime.now(timezone.utc).isoformat(), "n_turns": n_turns, "cell": cell}
                with loop_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

                logger.info(
                    "044 n_turns=%d lift_deff=%.4f lift_b1=%.4f two_phase=%s tda=%s pca_k_mu=%s eff_rank_mu=%s",
                    n_turns,
                    cell["lift_d_eff"],
                    cell["lift_beta_1"],
                    cell["two_phase_structure"],
                    cell["policies"]["lock_reassert"].get("tda_backend", "unknown"),
                    cell["policies"]["mu"]["pca_diag"].get("pca_k_used"),
                    cell["policies"]["mu"]["pca_diag"].get("effective_rank"),
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("044 cell error prompt=%s n_turns=%d: %s", prompt[:40], n_turns, exc)
                cells.append(
                    {
                        "error": str(exc),
                        "prompt_snippet": prompt[:80],
                        "n_turns": n_turns,
                    }
                )

        valid = [c for c in cells if "error" not in c]
        mean_d_eff = float(np.mean([c["lift_d_eff"] for c in valid])) if valid else 0.0
        mean_b1 = float(np.mean([c["lift_beta_1"] for c in valid])) if valid else 0.0
        mean_d_med = float(np.mean([c["lift_d_med"] for c in valid])) if valid else 0.0
        two_phase_frac = float(np.mean([float(c["two_phase_structure"]) for c in valid])) if valid else 0.0

        # Diagnostics: point-count + PCA rank/cap behavior.
        def _policy_stat(policy: str, key: str) -> list[float]:
            out: list[float] = []
            for c in valid:
                try:
                    out.append(float(c["policies"][policy]["pca_diag"].get(key, 0.0)))
                except Exception:
                    continue
            return out

        n_points_mu = _policy_stat("mu", "n_points")
        n_points_lock = _policy_stat("lock_reassert", "n_points")
        k_used_mu = _policy_stat("mu", "pca_k_used")
        k_used_lock = _policy_stat("lock_reassert", "pca_k_used")
        eff_rank_mu = _policy_stat("mu", "effective_rank")
        eff_rank_lock = _policy_stat("lock_reassert", "effective_rank")

        per_turns_summary[n_turns] = {
            "mean_lift_d_eff": round(mean_d_eff, 6),
            "mean_lift_beta_1": round(mean_b1, 6),
            "mean_lift_d_med": round(mean_d_med, 6),
            "two_phase_fraction": round(two_phase_frac, 4),
            "n_cells": len(cells),
            "n_errors": len(cells) - len(valid),
            "n_points_mu_mean": round(float(np.mean(n_points_mu)) if n_points_mu else 0.0, 3),
            "n_points_lock_mean": round(float(np.mean(n_points_lock)) if n_points_lock else 0.0, 3),
            "pca_k_used_mu_mean": round(float(np.mean(k_used_mu)) if k_used_mu else 0.0, 3),
            "pca_k_used_lock_mean": round(float(np.mean(k_used_lock)) if k_used_lock else 0.0, 3),
            "effective_rank_mu_mean": round(float(np.mean(eff_rank_mu)) if eff_rank_mu else 0.0, 3),
            "effective_rank_lock_mean": round(float(np.mean(eff_rank_lock)) if eff_rank_lock else 0.0, 3),
        }

        all_loop_results.append(
            {
                "n_turns": n_turns,
                "cells": cells,
                "summary": per_turns_summary[n_turns],
            }
        )

        # Incremental artifact write so partial runs still produce diagnostics.
        _write_payload(
            cfg=cfg,
            gen_model=gen_model,
            embed_model=embed_model,
            emb_cfg=emb_cfg,
            pca_dims=pca_dims,
            pca_rank_eps=pca_rank_eps,
            n_turns_list=n_turns_list,
            n_completions_per_turn=n_completions_per_turn,
            focused_prompts=focused_prompts,
            tda_max_dim=tda_max_dim,
            tda_k_neighbors=tda_k_neighbors,
            tda_metric=tda_metric,
            per_turns_summary=per_turns_summary,
            all_loop_results=all_loop_results,
            partial=True,
        )

        logger.info(
            "044 n_turns=%d SUMMARY lift_deff=%.4f lift_b1=%.4f lift_d_med=%.4f two_phase=%.2f k_mu=%.2f rank_mu=%.2f",
            n_turns,
            mean_d_eff,
            mean_b1,
            mean_d_med,
            two_phase_frac,
            per_turns_summary[n_turns]["pca_k_used_mu_mean"],
            per_turns_summary[n_turns]["effective_rank_mu_mean"],
        )

    # Aggregate across all n_turns.
    payload = _write_payload(
        cfg=cfg,
        gen_model=gen_model,
        embed_model=embed_model,
        emb_cfg=emb_cfg,
        pca_dims=pca_dims,
        pca_rank_eps=pca_rank_eps,
        n_turns_list=n_turns_list,
        n_completions_per_turn=n_completions_per_turn,
        focused_prompts=focused_prompts,
        tda_max_dim=tda_max_dim,
        tda_k_neighbors=tda_k_neighbors,
        tda_metric=tda_metric,
        per_turns_summary=per_turns_summary,
        all_loop_results=all_loop_results,
        partial=False,
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_044()
    agg = res["aggregate"]
    pipe = res["pipeline"]

    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"generator={pipe['generator']}  embedder={pipe['embedder']}  embed_dim={pipe['embed_dim']}",
        f"pca_dims_requested={pipe['pca_dims_requested']}  pca_rank_eps={pipe['pca_rank_eps']}",
        f"n_turns_list={pipe['n_turns_list']} tda_max_dim={pipe['tda']['max_dim']} tda_k_neighbors={pipe['tda']['k_neighbors']}",
        f"mean_lift_d_eff={agg['mean_lift_d_eff']}",
        f"mean_lift_beta_1={agg['mean_lift_beta_1']}",
        f"mean_lift_d_med={agg['mean_lift_d_med']}",
        f"mean_two_phase_fraction={agg['mean_two_phase_fraction']}",
        f"d_eff_resolved={res['d_eff_resolved']}",
        f"hybrid_evidence={res['hybrid_evidence']}",
    ]
    log_text = "\n".join(log_lines) + "\n"
    (Path(__file__).parent / "run.log").write_text(log_text, encoding="utf-8")

    print(f"\n{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(
        f"mean_lift_d_eff={agg['mean_lift_d_eff']} mean_lift_beta_1={agg['mean_lift_beta_1']} mean_lift_d_med={agg['mean_lift_d_med']}"
    )
    print(f"mean_two_phase_fraction={agg['mean_two_phase_fraction']} d_eff_resolved={res['d_eff_resolved']}")

