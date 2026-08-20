"""Activation-space TDA for AMAT — local causal LM hidden states (NAMM-2026-035).

Extracts last-token hidden vectors per layer across multi-turn trajectories under
μ (median helpful) vs lock_reassert (RPL) policies, builds point clouds, and
computes d_med, D_eff, beta proxies (k-NN graph or ripser when installed).
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np

from namm.metrics.cognitive_class import compute_d_eff
from namm.metrics.live_embeddings import FOLLOWUP
from namm.metrics.phase_lock import evaluate_trajectory, load_phase_lock_spec, median_helpful_prompt

logger = logging.getLogger(__name__)

Policy = Literal["mu", "lock_reassert"]
PointCloudMode = Literal["turns_x_layers", "turns_last_layer", "layers_last_turn"]

DEFAULT_MODEL_CANDIDATES = [
    "Qwen/Qwen2.5-0.5B-Instruct",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
]

FOCUSED_PROMPTS = [
    "Explain why consensus in multi-agent systems can be permanently suboptimal.",
    "What is chimera synchronization and when is partial sync preferable to full consensus?",
    "How does cognitive capitalism allocate compute toward median vs tail cognitive classes?",
]


@dataclass
class LocalLM:
    model: Any
    tokenizer: Any
    model_id: str
    device: str
    n_layers: int
    hidden_dim: int


def _has_ripser() -> bool:
    try:
        import ripser  # noqa: F401

        return True
    except ImportError:
        return False


def _resolve_device(preferred: str | None = None) -> str:
    import torch

    if preferred:
        return preferred
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_local_lm(
    model_id: str | None = None,
    *,
    device: str | None = None,
    dtype: str = "auto",
    candidates: list[str] | None = None,
) -> LocalLM:
    """Load smallest working causal LM from candidates (fallback chain)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = _resolve_device(device)
    torch_dtype = getattr(torch, dtype) if dtype != "auto" else "auto"
    ids = [model_id] if model_id else (candidates or DEFAULT_MODEL_CANDIDATES)
    ids = [m for m in ids if m]

    last_err: Exception | None = None
    for mid in ids:
        try:
            logger.info("Loading local LM %s on %s", mid, device)
            tokenizer = AutoTokenizer.from_pretrained(mid, trust_remote_code=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            model = AutoModelForCausalLM.from_pretrained(
                mid,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
            )
            model.to(device)
            model.eval()
            n_layers = getattr(model.config, "num_hidden_layers", None) or getattr(
                model.config, "n_layer", 0
            )
            hidden_dim = getattr(model.config, "hidden_size", None) or getattr(
                model.config, "n_embd", 0
            )
            return LocalLM(
                model=model,
                tokenizer=tokenizer,
                model_id=mid,
                device=device,
                n_layers=int(n_layers),
                hidden_dim=int(hidden_dim),
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load %s: %s", mid, exc)
            last_err = exc
    raise RuntimeError(f"Could not load any local LM from {ids}") from last_err


def _system_for_policy(policy: Policy, m0_system: str, nd_system: str) -> str:
    return m0_system if policy == "mu" else nd_system


def _chat_messages(system: str, user: str, history: list[tuple[str, str]]) -> list[dict[str, str]]:
    msgs: list[dict[str, str]] = [{"role": "system", "content": system}]
    for u, a in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    msgs.append({"role": "user", "content": user})
    return msgs


def _generate_reply(lm: LocalLM, messages: list[dict[str, str]], max_new_tokens: int = 256) -> str:
    import torch

    tokenizer = lm.tokenizer
    model = lm.model
    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        parts = [f"{m['role']}: {m['content']}" for m in messages]
        prompt = "\n".join(parts) + "\nassistant:"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
    inputs = {k: v.to(lm.device) for k, v in inputs.items()}

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        )
    new_tokens = out[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def extract_last_token_hidden_matrix(
    lm: LocalLM,
    system: str,
    user: str,
    history: list[tuple[str, str]] | None = None,
    *,
    layer_indices: list[int] | None = None,
) -> np.ndarray:
    """Last-token hidden states: shape (n_layers_selected, hidden_dim)."""
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

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
    inputs = {k: v.to(lm.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    # hidden_states[0] is embedding; layers 1..L are transformer blocks
    hs = outputs.hidden_states
    last_idx = inputs["input_ids"].shape[1] - 1
    layer_vecs: list[np.ndarray] = []
    indices = layer_indices if layer_indices is not None else list(range(1, len(hs)))
    for li in indices:
        if li < 0:
            li = len(hs) + li
        vec = hs[li][0, last_idx, :].detach().float().cpu().numpy()
        layer_vecs.append(vec)
    return np.stack(layer_vecs, axis=0)


def run_local_activation_session(
    lm: LocalLM,
    user_prompt: str,
    *,
    policy: Policy,
    n_turns: int,
    m0_system: str,
    nd_system: str,
    max_new_tokens: int = 256,
    pause_s: float = 0.0,
    layer_indices: list[int] | None = None,
) -> tuple[list[str], list[np.ndarray]]:
    """Multi-turn local chat; returns completions and per-turn layer hidden matrices."""
    completions: list[str] = []
    hidden_mats: list[np.ndarray] = []
    history: list[tuple[str, str]] = []

    for turn in range(n_turns):
        system = _system_for_policy(policy, m0_system, nd_system)
        user_msg = user_prompt if turn == 0 else FOLLOWUP
        hidden_mats.append(
            extract_last_token_hidden_matrix(
                lm, system, user_msg, history, layer_indices=layer_indices
            )
        )
        text = _generate_reply(
            lm,
            _chat_messages(system, user_msg, history),
            max_new_tokens=max_new_tokens,
        )
        completions.append(text)
        history.append((user_msg, text))
        if pause_s > 0 and turn + 1 < n_turns:
            time.sleep(pause_s)
    return completions, hidden_mats


def build_point_cloud(
    hidden_mats: list[np.ndarray],
    mode: PointCloudMode = "turns_x_layers",
    *,
    last_n_layers: int | None = None,
) -> np.ndarray:
    """Stack turn-wise layer matrices into (n_points, dim) activation point cloud."""
    if not hidden_mats:
        return np.zeros((0, 1), dtype=np.float64)

    mats = hidden_mats
    if last_n_layers is not None and last_n_layers > 0:
        mats = [m[-last_n_layers:] for m in hidden_mats]

    if mode == "turns_x_layers":
        return np.vstack(mats)
    if mode == "turns_last_layer":
        return np.stack([m[-1] for m in mats], axis=0)
    if mode == "layers_last_turn":
        return mats[-1]
    raise ValueError(f"Unknown point cloud mode: {mode}")


def pca_reduce(
    embeddings: np.ndarray,
    n_components: int,
) -> np.ndarray:
    """Project point cloud to `n_components` dims via PCA (sklearn or numpy SVD).

    Handles the case where n_points < n_components by capping components.
    Returns array of shape (n_points, min(n_components, n_points, orig_dim)).
    """
    n_pts, orig_dim = embeddings.shape
    k = min(n_components, n_pts, orig_dim)
    if k <= 0 or n_pts < 2:
        return embeddings

    try:
        from sklearn.decomposition import PCA  # type: ignore

        pca = PCA(n_components=k, svd_solver="full")
        return pca.fit_transform(embeddings).astype(np.float64)
    except ImportError:
        pass

    # Fallback: numpy thin-SVD
    centered = embeddings - embeddings.mean(axis=0, keepdims=True)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    return (centered @ Vt[:k].T).astype(np.float64)


def _pairwise_distances(embeddings: np.ndarray, metric: str) -> np.ndarray:
    if metric == "cosine":
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-12)
        unit = embeddings / norms
        return 1.0 - (unit @ unit.T)
    return np.linalg.norm(embeddings[:, None, :] - embeddings[None, :, :], axis=2)


def compute_betti_with_backend(
    embeddings: np.ndarray,
    *,
    k_neighbors: int = 5,
    max_dim: int = 1,
    metric: str = "euclidean",
) -> tuple[float, float, str]:
    """beta_0, beta_1 with ripser if available else k-NN proxy."""
    if embeddings.shape[0] < 3:
        return 1.0, 0.0, "trivial"

    if _has_ripser():
        from ripser import ripser

        dgms = ripser(embeddings, maxdim=max_dim, metric=metric)
        beta_0 = float(len(dgms["dgms"][0])) if dgms["dgms"] else 1.0
        beta_1 = float(len(dgms["dgms"][1])) if len(dgms["dgms"]) > 1 else 0.0
        return beta_0, beta_1, f"ripser_{metric}"

    import networkx as nx

    n = embeddings.shape[0]
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
        beta_1 += max(0, sub.number_of_edges() - sub.number_of_nodes() + 1)
    return beta_0, float(beta_1), f"knn_proxy_{metric}"


def evaluate_activation_trajectory(
    point_cloud: np.ndarray,
    centroid: np.ndarray,
    gates: dict[str, Any],
    *,
    k_neighbors: int = 5,
    ripser_metric: str = "euclidean",
) -> dict[str, Any]:
    """AMAT order parameters on activation point cloud."""
    if point_cloud.ndim == 1:
        point_cloud = point_cloud.reshape(1, -1)
    if point_cloud.shape[0] < 2:
        return {
            "d_med": 0.0,
            "d_eff": 1.0,
            "beta_0": 1.0,
            "beta_1": 0.0,
            "order_R": 1.0,
            "mu_cns_proxy": 1.0,
            "gates_passed": False,
            "tda_backend": "trivial",
            "n_points": int(point_cloud.shape[0]),
        }

    base = evaluate_trajectory(point_cloud, centroid, gates)
    beta_0, beta_1, backend = compute_betti_with_backend(
        point_cloud, k_neighbors=k_neighbors, metric=ripser_metric
    )
    base["beta_0"] = round(beta_0, 6)
    base["beta_1"] = round(beta_1, 6)
    base["tda_backend"] = backend
    base["n_points"] = int(point_cloud.shape[0])
    # Re-check gates with updated beta_1
    d_med = base["d_med"]
    d_eff = base["d_eff"]
    order_r = base["order_R"]
    mu_cns = base["mu_cns_proxy"]
    base["gates_passed"] = (
        d_med >= float(gates["d_med_min"])
        and beta_1 >= float(gates["beta1_min"])
        and d_eff >= float(gates.get("d_eff_min", 1.0))
        and float(gates["R_star_lo"]) <= order_r <= float(gates["R_star_hi"])
        and mu_cns <= float(gates["mu_cns_max"])
    )
    return base


def activation_barycenter(point_clouds: list[np.ndarray]) -> np.ndarray:
    """Typicality barycenter B_* in activation space (mean of pooled μ references)."""
    if not point_clouds:
        raise ValueError("Need at least one reference point cloud")
    pooled = np.vstack([pc for pc in point_clouds if pc.size > 0])
    return pooled.mean(axis=0)


def run_activation_tda_sweep(
    user_prompt: str,
    lm: LocalLM,
    *,
    n_turns: int = 3,
    point_cloud_mode: PointCloudMode = "turns_x_layers",
    last_n_layers: int | None = 4,
    max_new_tokens: int = 256,
    b_star: np.ndarray | None = None,
    layer_indices: list[int] | None = None,
    pca_dims: int | None = None,
    ripser_metric: str = "euclidean",
) -> dict[str, Any]:
    """One prompt × policies (μ, lock_reassert) on local activations."""
    spec = load_phase_lock_spec()
    gates = spec["gates"]
    m0_system = median_helpful_prompt()
    nd_system = spec["rendered_system_prompt"]

    policy_clouds: dict[str, np.ndarray] = {}
    rows: dict[str, Any] = {}

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
        cloud = build_point_cloud(
            hidden_mats, mode=point_cloud_mode, last_n_layers=last_n_layers
        )
        if pca_dims is not None and pca_dims > 0 and cloud.shape[0] >= 2:
            cloud = pca_reduce(cloud, pca_dims)
        policy_clouds[policy] = cloud
        rows[policy] = {
            "completions": completions,
            "point_cloud_shape": list(cloud.shape),
        }

    centroid = b_star if b_star is not None else activation_barycenter([policy_clouds["mu"]])
    policy_metrics: dict[str, dict[str, Any]] = {}
    for policy in ("mu", "lock_reassert"):
        metrics = evaluate_activation_trajectory(
            policy_clouds[policy], centroid, gates, ripser_metric=ripser_metric
        )
        policy_metrics[policy] = metrics
        rows[policy]["metrics"] = metrics

    mu_m = policy_metrics["mu"]
    lock_m = policy_metrics["lock_reassert"]
    lift_d = lock_m["d_med"] - mu_m["d_med"]
    lift_b1 = lock_m["beta_1"] - mu_m["beta_1"]
    lift_deff = lock_m["d_eff"] - mu_m["d_eff"]

    # Match 043/044 two-phase definition for cross-experiment comparison.
    two_phase = bool(
        (mu_m["beta_1"] < 0.5 and lock_m["beta_1"] >= 0.5)
        or abs(lift_b1) > 0.3
        or (lift_deff > 0.3 and lift_d > 0.05)
    )
    f_amat_4_triggered = not two_phase

    return {
        "mode": "activation_tda_sweep",
        "user_prompt": user_prompt,
        "n_turns": n_turns,
        "model_id": lm.model_id,
        "device": lm.device,
        "point_cloud_mode": point_cloud_mode,
        "last_n_layers": last_n_layers,
        "pca_dims": pca_dims,
        "ripser_metric": ripser_metric,
        "policies": rows,
        "centroid_source": "mu_trajectory" if b_star is None else "provided",
        "summary": {
            "mu_d_med": round(mu_m["d_med"], 6),
            "lock_d_med": round(lock_m["d_med"], 6),
            "lift_d_med": round(lift_d, 6),
            "mu_beta_1": round(mu_m["beta_1"], 6),
            "lock_beta_1": round(lock_m["beta_1"], 6),
            "lift_beta_1": round(lift_b1, 6),
            "mu_d_eff": round(mu_m["d_eff"], 6),
            "lock_d_eff": round(lock_m["d_eff"], 6),
            "lift_d_eff": round(lift_deff, 6),
            "lock_gate_pass": lock_m["gates_passed"],
            "mu_gate_pass": mu_m["gates_passed"],
            "two_phase_structure": two_phase,
            "f_amat_4_triggered": f_amat_4_triggered,
            "tda_backend": lock_m.get("tda_backend", "unknown"),
        },
        "hypothesis_support": {
            "H-AMAT-004": lift_d > 0.05,
            "H-CCT-020": lift_d > 0.05,
            "H-CCT-021": lift_b1 > 0.05,
            "F-AMAT-4-not-triggered": not f_amat_4_triggered,
        },
    }


def run_pca_sweep(
    chimera_prompt: str,
    lm: LocalLM,
    *,
    pca_dims_list: list[int],
    n_turns_list: list[int],
    point_cloud_mode: PointCloudMode = "turns_x_layers",
    last_n_layers: int | None = 8,
    max_new_tokens: int = 128,
    on_cell: Any | None = None,
) -> dict[str, Any]:
    """Sweep pca_dims × n_turns on a single prompt (chimera).

    Returns cells list and best_pca_dim (by mean lift_d_eff across n_turns).
    """
    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for pca_d in pca_dims_list:
        for nt in n_turns_list:
            try:
                batch = run_activation_tda_sweep(
                    chimera_prompt,
                    lm,
                    n_turns=nt,
                    point_cloud_mode=point_cloud_mode,
                    last_n_layers=last_n_layers,
                    max_new_tokens=max_new_tokens,
                    pca_dims=pca_d,
                )
                s = batch["summary"]
                cell: dict[str, Any] = {
                    "pca_dims": pca_d,
                    "n_turns": nt,
                    "prompt_preview": chimera_prompt[:80],
                    **s,
                    "hypothesis_support": batch["hypothesis_support"],
                }
                cells.append(cell)
                if on_cell:
                    on_cell(cell, batch)
            except Exception as exc:  # noqa: BLE001
                errors.append({"pca_dims": pca_d, "n_turns": nt, "error": str(exc)})
                logger.warning("PCA sweep cell failed pca_dims=%d n_turns=%d: %s", pca_d, nt, exc)

    if not cells:
        return {
            "mode": "pca_sweep",
            "cells": cells,
            "errors": errors,
            "best_pca_dim": pca_dims_list[0] if pca_dims_list else 8,
            "summary_by_pca_dim": {},
        }

    # Aggregate by pca_dim
    summary_by_pca: dict[int, dict[str, Any]] = {}
    for pca_d in pca_dims_list:
        dim_cells = [c for c in cells if c["pca_dims"] == pca_d]
        if not dim_cells:
            continue
        deff_lifts = [c.get("lift_d_eff", 0.0) for c in dim_cells]
        b1_lifts = [c.get("lift_beta_1", 0.0) for c in dim_cells]
        summary_by_pca[pca_d] = {
            "mean_lift_d_eff": round(float(np.mean(deff_lifts)), 6),
            "mean_lift_beta_1": round(float(np.mean(b1_lifts)), 6),
            "n_cells": len(dim_cells),
        }

    best_pca_dim = max(summary_by_pca, key=lambda d: summary_by_pca[d]["mean_lift_d_eff"])

    return {
        "mode": "pca_sweep",
        "cells": cells,
        "errors": errors,
        "best_pca_dim": best_pca_dim,
        "summary_by_pca_dim": {str(k): v for k, v in summary_by_pca.items()},
    }


def run_activation_tda_loop(
    *,
    prompts: list[str] | None = None,
    n_turns: int = 3,
    lm: LocalLM | None = None,
    model_id: str | None = None,
    point_cloud_mode: PointCloudMode = "turns_x_layers",
    last_n_layers: int | None = 4,
    max_new_tokens: int = 256,
    on_cell: Any | None = None,
    protocol: str = "amat-activation-tda-v1",
    pca_dims: int | None = None,
    ripser_metric: str = "euclidean",
) -> dict[str, Any]:
    """Grid: prompts × activation TDA (μ vs lock)."""
    prompts = prompts or FOCUSED_PROMPTS
    if lm is None:
        lm = load_local_lm(model_id)

    cells: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    backends: set[str] = set()

    for prompt in prompts:
        try:
            batch = run_activation_tda_sweep(
                prompt,
                lm,
                n_turns=n_turns,
                point_cloud_mode=point_cloud_mode,
                last_n_layers=last_n_layers,
                max_new_tokens=max_new_tokens,
                pca_dims=pca_dims,
                ripser_metric=ripser_metric,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append({"prompt_preview": prompt[:80], "error": str(exc)})
            continue

        s = batch["summary"]
        backends.add(s.get("tda_backend", "unknown"))
        cell = {
            "prompt_preview": prompt[:80],
            "n_turns": n_turns,
            **s,
            "hypothesis_support": batch["hypothesis_support"],
        }
        cells.append(cell)
        if on_cell:
            on_cell(cell, batch)

    if not cells:
        return {
            "protocol": protocol,
            "mode": "activation_tda",
            "model_id": lm.model_id if lm else None,
            "grid": {"n_prompts": len(prompts), "n_turns": n_turns, "n_cells": 0, "pca_dims": pca_dims},
            "cells": [],
            "errors": errors,
            "summary": {},
            "hypothesis_support": {},
        }

    lifts_d = [c["lift_d_med"] for c in cells]
    lifts_b1 = [c["lift_beta_1"] for c in cells]
    lifts_deff = [c["lift_d_eff"] for c in cells]
    two_phase_frac = sum(1 for c in cells if c.get("two_phase_structure")) / len(cells)
    f4_frac = sum(1 for c in cells if c.get("f_amat_4_triggered")) / len(cells)

    summary_out: dict[str, Any] = {
        "mean_lift_d_med": round(float(np.mean(lifts_d)), 6),
        "mean_lift_beta_1": round(float(np.mean(lifts_b1)), 6),
        "mean_lift_d_eff": round(float(np.mean(lifts_deff)), 6),
        "two_phase_cell_fraction": round(two_phase_frac, 4),
        "f_amat_4_triggered_fraction": round(f4_frac, 4),
        "best_cell": max(cells, key=lambda c: c["lift_beta_1"]),
        "n_errors": len(errors),
        "tda_backends": sorted(backends),
    }

    return {
        "protocol": protocol,
        "mode": "activation_tda",
        "model_id": lm.model_id,
        "device": lm.device,
        "n_layers": lm.n_layers,
        "hidden_dim": lm.hidden_dim,
        "grid": {
            "n_prompts": len(prompts),
            "n_turns": n_turns,
            "n_cells": len(cells),
            "point_cloud_mode": point_cloud_mode,
            "last_n_layers": last_n_layers,
            "pca_dims": pca_dims,
            "ripser_metric": ripser_metric,
        },
        "cells": cells,
        "errors": errors,
        "summary": summary_out,
        "hypothesis_support": {
            "H-AMAT-004": summary_out["mean_lift_d_med"] > 0.05,
            "H-CCT-020": summary_out["mean_lift_d_med"] > 0.05,
            "H-CCT-021": summary_out["mean_lift_beta_1"] > 0.05,
            "F-AMAT-4-not-triggered": f4_frac < 0.5,
        },
    }
