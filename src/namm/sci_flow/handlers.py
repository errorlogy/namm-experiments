"""Experiment handlers invoked by SciFlowRunner."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import yaml

from namm.metrics.cognitive_class import (
    run_class_mas_batch,
    run_class_separation_batch,
    run_gt2_cne_sweep,
    run_myth_consensus_batch,
    run_myth_shift_sweep,
    run_resource_conversion_sweep,
)
from namm.metrics.phase_lock import run_phase_lock_loop, run_phase_lock_sweep
from namm.metrics.catastrophe import cusp_hysteresis_loop, detect_bifurcation_crossing
from namm.metrics.cognitive_class import run_antigravity_sigma_sweep
from namm.metrics.consensus_non_optimality import CNSSimulationConfig, run_cns_batch, run_kuramoto_vote_sweep

WORKSPACE = Path(__file__).resolve().parents[3]


def _exp_dir(experiment_id: str) -> Path:
    return WORKSPACE / "experiments" / experiment_id


def _load_exp_config(experiment_id: str) -> dict[str, Any]:
    path = _exp_dir(experiment_id) / "config.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _json_default(obj: Any) -> Any:
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _write_artifacts(
    experiment_id: str,
    summary: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> None:
    artifacts = _exp_dir(experiment_id) / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "result.json").write_text(
        json.dumps(summary, indent=2, default=_json_default),
        encoding="utf-8",
    )
    if extra:
        for name, payload in extra.items():
            if payload is None:
                continue
            (artifacts / name).write_text(
                json.dumps(payload, indent=2, default=_json_default),
                encoding="utf-8",
            )


def run_021(config: dict[str, Any], *, variant: str | None = None) -> dict[str, Any]:
    """NAMM-2026-021: opinion graph welfare fiber."""
    cns_raw = config.get("cns_simulation", {})
    seed = int(config.get("seed", 2026021))
    sim_config = CNSSimulationConfig.from_dict(cns_raw, seed=seed)
    num_instances = int(config.get("num_instances", 24))
    topologies = config.get("topologies", ["watts_strogatz", "erdos_renyi", "barabasi_albert"])
    extra_seeds = config.get("seeds")

    if extra_seeds and len(extra_seeds) > 1:
        batches = []
        for s in extra_seeds[:6]:
            cfg = CNSSimulationConfig.from_dict(cns_raw, seed=int(s))
            batches.append(
                run_cns_batch(cfg, num_instances=num_instances // len(extra_seeds[:6]) + 1, topologies=topologies)
            )
        all_instances = []
        for b in batches:
            all_instances.extend(b.get("instances", []))
        gaps = [i["delta_w_global"] for i in all_instances] if all_instances else [batches[0]["mean_delta_w_global"]]
        support = batches[-1]["hypothesis_support"]
        for b in batches:
            for k, v in b["hypothesis_support"].items():
                support[k] = support.get(k, False) and v
        batch = {
            **batches[0],
            "mean_delta_w_global": round(float(np.mean(gaps)), 6),
            "positive_gap_fraction": round(sum(1 for g in gaps if g > 1e-6) / max(len(gaps), 1), 4),
            "hypothesis_support": support,
            "instances": all_instances[:5],
            "num_seed_runs": len(batches),
        }
    else:
        batch = run_cns_batch(sim_config, num_instances=num_instances, topologies=topologies)

    support = batch["hypothesis_support"]
    confirmed = support.get("H-CNS-001", False) and support.get("H-CNS-004", False)
    summary = {
        "experiment_id": "NAMM-2026-021",
        "domain": config.get("domain", "multi_agent_consensus"),
        "hypothesis_id": config.get("hypothesis_id", "H-CNS-011"),
        "protocol_version": config.get("protocol_version", "cns-simulation-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "variant": config.get("variant", variant or "default"),
            "consensus_operator": sim_config.consensus_operator,
            "num_agents": sim_config.num_agents,
            "max_non_optimality": sim_config.effective_max_non_optimality,
            "num_instances": num_instances,
            "topologies": topologies,
        },
        "metrics": {
            "mean_delta_w_global": batch["mean_delta_w_global"],
            "std_delta_w_global": batch["std_delta_w_global"],
            "positive_gap_fraction": batch["positive_gap_fraction"],
            "mean_delta_h_fiber": batch["mean_delta_h_fiber"],
            "contour_gap_variance": batch["contour_gap_variance"],
            "bound_saturation_fraction": batch["bound_saturation_fraction"],
            "mean_gap_at_high_mu_cns": batch.get("mean_gap_at_high_mu_cns"),
            "high_mu_instance_count": batch.get("high_mu_instance_count"),
        },
        "hypothesis_support": support,
        "falsifiers_triggered": batch.get("falsifiers_triggered", {}),
        "hypothesis_confirmed": confirmed,
        "sample_instances": batch.get("instances", []),
    }
    _write_artifacts("NAMM-2026-021", summary, {"batch_detail.json": batch})
    return summary


def run_022(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-022: Kuramoto–vote catastrophe sweep."""
    cns_raw = config.get("cns_simulation", {})
    seed = int(config.get("seed", 2026022))
    sim_config = CNSSimulationConfig.from_dict(cns_raw, seed=seed)

    def _parse(param: str, default: list) -> list:
        for entry in cns_raw.get("sweep", []):
            if entry.get("param") == param:
                return list(entry["values"])
        return default

    k_values = _parse("kuramoto_K", [0.5, 1.0, 1.8, 2.5, 3.5])
    threshold_values = _parse("vote_threshold", [0.0, 0.25, 0.5, 0.75, 1.0])
    max_no_values = _parse("max_non_optimality", [0.10, 0.20, 0.35, 0.50])
    sigma_values = _parse("fuzzy_contours[0].sigma", [0.15, 0.25, 0.40])
    sweep = run_kuramoto_vote_sweep(
        sim_config,
        K_values=k_values,
        threshold_values=threshold_values,
        max_non_optimality_values=max_no_values,
        sigma_values=sigma_values,
    )
    b_vals = np.linspace(-0.6, 0.6, max(len(k_values), 5))
    cusp_loop = cusp_hysteresis_loop(a=-0.35, b_values=b_vals)
    eq_counts = [
        len(cusp_loop.state_forward[: i + 1]) for i in range(len(cusp_loop.param_values))
    ]
    bifurcation_crossings = detect_bifurcation_crossing(
        np.array(cusp_loop.param_values), np.array(eq_counts)
    )
    catastrophe_confirmed = (
        sweep["max_hysteresis_width"] > cusp_loop.width * 0.05
        and len(bifurcation_crossings) >= 0
    )
    support = dict(sweep["hypothesis_support"])
    support["H-CNS-002"] = support.get("H-CNS-002", False) and catastrophe_confirmed
    confirmed = support.get("H-CNS-002", False) and support.get("H-CNS-005", False)
    summary = {
        "experiment_id": "NAMM-2026-022",
        "domain": config.get("domain", "multi_agent_consensus"),
        "hypothesis_id": config.get("hypothesis_id", "H-CNS-002"),
        "protocol_version": config.get("protocol_version", "cns-simulation-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "mean_delta_w_global": sweep["mean_delta_w_global"],
            "mean_regret_spike_forced_vs_delayed": sweep["mean_regret_spike_forced_vs_delayed"],
            "mean_gap_at_high_mu_cns": sweep["mean_gap_at_high_mu_cns"],
            "max_hysteresis_width": sweep["max_hysteresis_width"],
            "cusp_hysteresis_width": round(cusp_loop.width, 6),
            "catastrophe_module_confirmed": catastrophe_confirmed,
            "sweep_size": sweep["sweep_size"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "sample_points": sweep.get("sample_points", []),
    }
    _write_artifacts(
        "NAMM-2026-022",
        summary,
        {"hysteresis_loop.json": sweep.get("hysteresis_loop", [])},
    )
    return summary


def run_026(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-026: myth-as-consensus."""
    cns_raw = config.get("cns_simulation", {})
    seed = int(config.get("seed", 2026026))
    sim_config = CNSSimulationConfig.from_dict(cns_raw, seed=seed)
    compositions = config.get("class_compositions", [{"K1": 0.85, "K3": 0.10, "K6": 0.05}])
    num_seeds = int(config.get("num_seeds", 5))
    myth_raw = config.get("mythogenesis", {})
    myth_signal = np.array(myth_raw.get("signal", [1.0, 0.25, 0.08]), dtype=float)
    contour_weighting = myth_raw.get("contour_weighting")
    batch = run_myth_consensus_batch(
        sim_config, compositions, myth_signal, num_seeds, contour_weighting=contour_weighting
    )
    support = batch["hypothesis_support"]
    confirmed = support.get("H-MCG-001", False) and support.get("H-MCG-008", False)
    summary = {
        "experiment_id": "NAMM-2026-026",
        "hypothesis_id": config.get("hypothesis_id", "H-MCG-001"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "mean_delta_w_myth": batch["mean_delta_w_myth"],
            "mean_mu_cns_myth": batch["mean_mu_cns_myth"],
            "mean_gap_high_k1": batch["mean_gap_high_k1"],
            "mean_gap_mixed": batch["mean_gap_mixed"],
            "gap_at_high_mu_fraction": batch["gap_at_high_mu_fraction"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
    }
    _write_artifacts("NAMM-2026-026", summary, {"myth_batch.json": batch})
    return summary


def run_028(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-028: myth shift catastrophe."""
    cns_raw = config.get("cns_simulation", {})
    seed = int(config.get("seed", 2026028))
    sim_config = CNSSimulationConfig.from_dict(cns_raw, seed=seed)
    coupling_values = [float(v) for v in config.get("coupling_values", [2.0])]
    salience_values = [float(v) for v in config.get("salience_values", [0.5])]
    num_seeds = int(config.get("num_seeds", 5))
    batch = run_myth_shift_sweep(sim_config, coupling_values, salience_values, num_seeds)
    b_vals = np.linspace(-0.4, 0.4, max(len(salience_values), 5))
    cusp_loop = cusp_hysteresis_loop(a=-0.25, b_values=b_vals)
    catastrophe_confirmed = batch["max_hysteresis_width"] > cusp_loop.width * 0.08
    support = dict(batch["hypothesis_support"])
    support["H-MCG-005"] = support.get("H-MCG-005", False) and catastrophe_confirmed
    support["H-CNS-002"] = support.get("H-CNS-002", False) and catastrophe_confirmed
    confirmed = support.get("H-MCG-005", False) and support.get("H-CNS-002", False)
    summary = {
        "experiment_id": "NAMM-2026-028",
        "hypothesis_id": config.get("hypothesis_id", "H-MCG-005"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "sweep_size": batch["sweep_size"],
            "max_hysteresis_width": batch["max_hysteresis_width"],
            "mean_hysteresis": batch["mean_hysteresis"],
            "mean_class_transition_rate": batch["mean_class_transition_rate"],
            "high_hysteresis_count": batch["high_hysteresis_count"],
            "cusp_hysteresis_width": round(cusp_loop.width, 6),
            "catastrophe_module_confirmed": catastrophe_confirmed,
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
    }
    _write_artifacts("NAMM-2026-028", summary, {"shift_sweep.json": batch})
    return summary


def run_023(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    classes = config.get("classes", ["K1", "K3", "K5", "K6"])
    n_samples = int(config.get("n_samples", 40))
    embed_dim = int(config.get("embed_dim", 8))
    seeds = list(config.get("seeds", [42, 137, 256]))
    batch = run_class_separation_batch(classes, n_samples, embed_dim, seeds)
    support = batch.hypothesis_support
    confirmed = support.get("H-CCT-001", False)
    summary = {
        "experiment_id": "NAMM-2026-023",
        "domain": config.get("domain", "cognitive_class_taxonomy"),
        "hypothesis_id": config.get("hypothesis_id", "H-CCT-001"),
        "protocol_version": config.get("protocol_version", "cct-embedding-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {"classes": classes, "n_samples": n_samples, "embed_dim": embed_dim, "seeds": seeds},
        "metrics": {
            "non_1d_score": batch.non_1d_score,
            "pairwise_separation": batch.pairwise_separation,
            "class_metrics": [m.to_dict() for m in batch.class_metrics],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
    }
    _write_artifacts("NAMM-2026-023", summary, {"separation_detail.json": batch.to_dict()})
    return summary


def run_025(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    cns_raw = config.get("cns_simulation", {})
    seed = int(config.get("seed", 2026025))
    sim_config = CNSSimulationConfig.from_dict(cns_raw, seed=seed)
    compositions = config.get("class_compositions", [{"K1": 1.0}])
    num_seeds = int(config.get("num_seeds", 5))
    batch = run_class_mas_batch(sim_config, compositions, num_seeds=num_seeds)
    support = batch["hypothesis_support"]
    confirmed = support.get("H-CCT-005", False) and support.get("H-CNS-010", False)
    summary = {
        "experiment_id": "NAMM-2026-025",
        "domain": config.get("domain", "cognitive_class_taxonomy"),
        "hypothesis_id": config.get("hypothesis_id", "H-CCT-005"),
        "protocol_version": config.get("protocol_version", "cct-mas-cns-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "num_agents": sim_config.num_agents,
            "compositions": compositions,
            "num_seeds": num_seeds,
        },
        "metrics": {
            "mean_delta_w_k1_homogeneous": batch["mean_delta_w_k1_homogeneous"],
            "mean_delta_w_mixed": batch["mean_delta_w_mixed"],
            "mean_order_R_k1": batch["mean_order_R_k1"],
            "mean_order_R_mixed": batch["mean_order_R_mixed"],
            "dissent_preserving_better_fraction": batch["dissent_preserving_better_fraction"],
            "mean_tail_gap": batch["mean_tail_gap"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "sample_runs": batch.get("runs", []),
    }
    _write_artifacts("NAMM-2026-025", summary, {"mas_batch.json": batch})
    return summary


def run_027(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    hybrid_configs = config.get("hybrid_configs")
    num_players = int(config.get("num_players", 24))
    seeds = list(config.get("seeds", [42, 99, 202]))
    batch = run_gt2_cne_sweep(hybrid_configs, num_players, seeds)
    support = batch["hypothesis_support"]
    confirmed = support.get("H-MCG-009", False) and support.get("H-MCG-013", False)
    summary = {
        "experiment_id": "NAMM-2026-027",
        "domain": config.get("domain", "multi_agent_consensus"),
        "hypothesis_id": config.get("hypothesis_id", "H-MCG-009"),
        "protocol_version": config.get("protocol_version", "gt2-cne-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {"num_players": num_players, "seeds": seeds, "hybrid_configs": hybrid_configs},
        "metrics": batch["by_game"],
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
    }
    _write_artifacts("NAMM-2026-027", summary, {"cne_sweep.json": batch})
    return summary


def run_029(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    classes = config.get("classes")
    channels = config.get("channels")
    tau_values = [float(v) for v in config.get("tau_values", [100.0])]
    phi_values = [float(v) for v in config.get("phi_values", [1.0])]
    steering = config.get("steering_comparison")
    batch = run_resource_conversion_sweep(
        classes, channels, tau_values, phi_values, steering_comparison=steering
    )
    support = batch["hypothesis_support"]
    confirmed = support.get("H-CCT-016", False)
    summary = {
        "experiment_id": "NAMM-2026-029",
        "domain": config.get("domain", "cognitive_class_taxonomy"),
        "hypothesis_id": config.get("hypothesis_id", "H-CCT-016"),
        "protocol_version": config.get("protocol_version", "cct-resource-conv-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "classes": classes,
            "channels": channels,
            "tau_values": tau_values,
            "phi_values": phi_values,
        },
        "metrics": {
            "sweep_size": batch["sweep_size"],
            "reference_tau": batch["reference_tau"],
            "asymmetry_high_impact_ratio": batch["asymmetry_high_impact_ratio"],
            "asymmetry_noise_ratio": batch["asymmetry_noise_ratio"],
            "g1mu_u_out": batch["g1mu_u_out"],
            "g6nd_u_out": batch["g6nd_u_out"],
            "g6nd_steering_channel": batch.get("g6nd_steering_channel"),
            "g1mu_steering_channel": batch.get("g1mu_steering_channel"),
            "by_class_channel": batch["by_class_channel"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "sample_points": batch.get("sample_points", []),
    }
    _write_artifacts("NAMM-2026-029", summary, {"conversion_sweep.json": batch})
    return summary


def run_024(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-024: 3σ antigravity ↔ K6 phase transition sweep."""
    sigma_values = [float(v) for v in config.get("sigma_values", [3.0])]
    n_samples = int(config.get("n_samples", 40))
    embed_dim = int(config.get("embed_dim", 8))
    seeds = list(config.get("seeds", [42, 99, 202, 314, 512]))
    batch = run_antigravity_sigma_sweep(sigma_values, n_samples, embed_dim, seeds)
    support = batch["hypothesis_support"]
    confirmed = support.get("H-CCT-004", False) and support.get("H-CA-001", False)
    summary = {
        "experiment_id": "NAMM-2026-024",
        "domain": config.get("domain", "cognitive_class_taxonomy"),
        "hypothesis_id": config.get("hypothesis_id", "H-CCT-004"),
        "protocol_version": config.get("protocol_version", "cct-antigravity-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {"sigma_values": sigma_values, "n_samples": n_samples, "seeds": seeds},
        "metrics": {
            "sweep_size": batch["sweep_size"],
            "max_d_jump": batch["max_d_jump"],
            "jump_at_3sigma": batch["jump_at_3sigma"],
            "discontinuity_at_3sigma": batch["discontinuity_at_3sigma"],
            "mean_beta1_at_3sigma": batch["mean_beta1_at_3sigma"],
            "mean_d_at_3sigma": batch["mean_d_at_3sigma"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "sample_points": batch.get("sample_points", []),
    }
    _write_artifacts("NAMM-2026-024", summary, {"sigma_sweep.json": batch})
    return summary


def run_030(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-030: JSON K_AI_nd phase-lock prompt vs median collapse."""
    seeds = [int(s) for s in config.get("seeds", [42, 137, 256, 512, 777])]
    loop_cfg = config.get("loop") or {}
    if loop_cfg.get("enabled", True):
        batch = run_phase_lock_loop(
            n_samples=int(config.get("n_samples", 40)),
            embed_dim=int(config.get("embed_dim", 8)),
            seeds=seeds,
            gain_values=[float(v) for v in loop_cfg.get("gain_values", [0.35, 0.55, 0.75, 0.85, 1.0])],
            decay_values=[float(v) for v in loop_cfg.get("decay_values", [0.35, 0.55, 0.80])],
            turn_values=[int(v) for v in loop_cfg.get("turn_values", [3, 6, 12])],
        )
        support = batch["hypothesis_support"]
        confirmed = bool(support.get("H-CCT-020") and support.get("H-CCT-021"))
        summary = {
            "experiment_id": "NAMM-2026-030",
            "domain": config.get("domain", "cognitive_class_taxonomy"),
            "hypothesis_id": config.get("hypothesis_id", "H-CCT-020"),
            "protocol_version": config.get("protocol_version", "k-ai-nd-phase-lock-loop-v1"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt_id": batch["prompt_id"],
            "mode": "loop",
            "config": {
                "n_samples": config.get("n_samples", 40),
                "embed_dim": config.get("embed_dim", 8),
                "seeds": seeds,
                "loop": loop_cfg,
                "prompt": config.get("prompt", "data/prompts/k_ai_nd_phase_lock.v1.json"),
            },
            "metrics": {
                "prompt_vs_m0_distance": batch["prompt_vs_m0_distance"],
                "n_cells": batch["grid"]["n_cells"],
                "mean_lift": batch["summary"]["mean_lift"],
                "max_lift": batch["summary"]["max_lift"],
                "min_lift": batch["summary"]["min_lift"],
                "mean_persistence_gap": batch["summary"]["mean_persistence_gap"],
                "h020_cell_fraction": batch["summary"]["h020_cell_fraction"],
                "h021_cell_fraction": batch["summary"]["h021_cell_fraction"],
                "best_gain": batch["summary"]["best_cell"]["gain"],
                "best_decay": batch["summary"]["best_cell"]["decay"],
                "best_n_turns": batch["summary"]["best_cell"]["n_turns"],
                "best_lock_d_med": batch["summary"]["best_cell"]["lock_d_med"],
            },
            "hypothesis_support": support,
            "hypothesis_confirmed": confirmed,
        }
        _write_artifacts("NAMM-2026-030", summary, {"phase_lock_loop.json": batch})
        return summary

    batch = run_phase_lock_sweep(
        n_samples=int(config.get("n_samples", 40)),
        embed_dim=int(config.get("embed_dim", 8)),
        n_turns=int(config.get("n_turns", 6)),
        seeds=seeds,
        gain=float(config.get("gain", 0.85)),
        decay=float(config.get("decay", 0.55)),
    )
    support = batch["hypothesis_support"]
    confirmed = bool(support.get("H-CCT-020") and support.get("H-CCT-001B") and support.get("H-CCT-021"))
    summary = {
        "experiment_id": "NAMM-2026-030",
        "domain": config.get("domain", "cognitive_class_taxonomy"),
        "hypothesis_id": config.get("hypothesis_id", "H-CCT-020"),
        "protocol_version": config.get("protocol_version", "k-ai-nd-phase-lock-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_id": batch["prompt_id"],
        "config": {
            "n_samples": config.get("n_samples", 40),
            "embed_dim": config.get("embed_dim", 8),
            "n_turns": config.get("n_turns", 6),
            "seeds": seeds,
            "prompt": config.get("prompt", "data/prompts/k_ai_nd_phase_lock.v1.json"),
        },
        "metrics": {
            "prompt_vs_m0_distance": batch["prompt_vs_m0_distance"],
            "mu_d_med": batch["mu_metrics"]["mean_d_med"],
            "lock_d_med": batch["lock_reassert_metrics"]["mean_d_med"],
            "decay_d_med": batch["lock_decay_metrics"]["mean_d_med"],
            "lock_beta_1": batch["lock_reassert_metrics"]["mean_beta_1"],
            "lock_order_R": batch["lock_reassert_metrics"]["mean_order_R"],
            "lock_gate_pass": batch["lock_reassert_metrics"]["gate_pass_fraction"],
            "decay_gate_pass": batch["lock_decay_metrics"]["gate_pass_fraction"],
            "mu_gate_pass": batch["mu_metrics"]["gate_pass_fraction"],
        },
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
    }
    _write_artifacts("NAMM-2026-030", summary, {"phase_lock_sweep.json": batch})
    return summary


def run_033(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-033: live embedding gate calibration vs legacy d_med >= 1.2."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-033") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_033", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_033"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_033(skip_chat=config.get("skip_chat", False))


def run_034(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-034: multi-embedder gate stability on shared live completions."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-034") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_034", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_034"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_034(skip_chat=config.get("skip_chat", False))


def run_036(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-036: PCA-reduced activation TDA — D_eff fix."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-036") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_036", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_036"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_036()


def run_035(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-035: local LM activation TDA — F-AMAT-4 decisive test."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-035") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_035", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_035"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_035(skip_local=config.get("skip_local", False))


def run_038(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-038: Fisher-metric geodesic curvature pilot (H-AMAT-007)."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-038") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_038", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_038"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_038(skip_local=config.get("skip_local", False))


def run_039(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-039: layer-wise TDA + box-counting fractal dimension (H-AMAT-008)."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-039") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_039", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_039"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_039()


def run_042(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-042: activation TDA on ≥1.5B model — D_eff separation test."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-042") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_042", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_042"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_042()


def run_043(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-043: hybrid nomic-embed-text TDA — resolve D_eff question."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-043") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_043", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_043"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_043()


def run_044(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-044: D_eff stability — safe PCA cap, larger clouds, cosine ripser."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-044") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_044", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_044"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_044()


def run_045(config: dict[str, Any], **_: Any) -> dict[str, Any]:
    """NAMM-2026-045: real hidden states @ 1.5B — D_eff separation (044 protocol)."""
    import importlib.util
    import sys

    exp_path = _exp_dir("NAMM-2026-045") / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("namm_exp_045", exp_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {exp_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["namm_exp_045"] = mod
    spec.loader.exec_module(mod)
    return mod.run_namm_2026_045()


HANDLERS: dict[str, Callable[..., dict[str, Any]]] = {
    "run_021": run_021,
    "run_022": run_022,
    "run_023": run_023,
    "run_024": run_024,
    "run_025": run_025,
    "run_026": run_026,
    "run_027": run_027,
    "run_028": run_028,
    "run_029": run_029,
    "run_030": run_030,
    "run_033": run_033,
    "run_034": run_034,
    "run_035": run_035,
    "run_036": run_036,
    "run_038": run_038,
    "run_039": run_039,
    "run_042": run_042,
    "run_043": run_043,
    "run_044": run_044,
    "run_045": run_045,
}


def get_handler(name: str) -> Callable[..., dict[str, Any]]:
    if name not in HANDLERS:
        raise KeyError(f"Unknown sci-flow handler {name!r}")
    return HANDLERS[name]
