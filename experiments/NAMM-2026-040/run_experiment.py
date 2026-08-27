"""NAMM-2026-040 — Multi-session Lyapunov λ₁ proxy (H-AMAT-009)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import load_local_lm
from namm.metrics.lyapunov_tda import assign_lyapunov_certificate, compare_lyapunov_policies
from namm.metrics.phase_lock import load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
CONFIG_PATH = Path(__file__).parent / "config.yaml"
EXPERIMENT_ID = "NAMM-2026-040"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _json_default(obj: object) -> object:
    if isinstance(obj, float) and obj != obj:
        return None
    raise TypeError(f"Not serializable: {type(obj)}")


def _cell_mean(cells: list, key: str) -> float:
    vals = [c[key] for c in cells if c.get(key) == c.get(key)]
    return float(sum(vals) / len(vals)) if vals else float("nan")


def run_namm_2026_040() -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    ly = cfg.get("lyapunov") or {}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    lm = load_local_lm(
        lm_cfg.get("model_id"),
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
        candidates=lm_cfg.get("model_candidates"),
    )
    logger.info("040 loaded %s on %s", lm.model_id, lm.device)

    spec = load_phase_lock_spec()
    prompts = ly.get("prompts") or [
        "Explain why consensus in multi-agent systems can be permanently suboptimal.",
    ]
    result = compare_lyapunov_policies(
        lm,
        prompts,
        m0_system=median_helpful_prompt(),
        nd_system=spec["rendered_system_prompt"],
        n_turns=int(ly.get("n_turns", 5)),
        n_sessions=int(ly.get("n_sessions", 3)),
        max_new_tokens=int(lm_cfg.get("max_new_tokens", 48)),
        temperature=float(ly.get("temperature", 0.8)),
        base_seed=int(ly.get("base_seed", 40)),
    )

    certificate = assign_lyapunov_certificate(result)
    mean_ros_lift = _cell_mean(result["cells"], "lift_lambda1_rosenstein")
    mean_ros_lock = _cell_mean(result["cells"], "lock_reassert_lambda1_rosenstein")
    mean_ros_mu = _cell_mean(result["cells"], "mu_lambda1_rosenstein")
    ros_finite = any(
        c.get("mu_lambda1_rosenstein") == c.get("mu_lambda1_rosenstein")
        or c.get("lock_reassert_lambda1_rosenstein") == c.get("lock_reassert_lambda1_rosenstein")
        for c in result["cells"]
    )

    summary = {
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": "H-AMAT-009",
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {"model_id": lm.model_id, "device": lm.device, "hidden_dim": lm.hidden_dim},
        "config": {
            "n_turns": result["n_turns"],
            "n_sessions": result["n_sessions"],
            "n_prompts": result["n_prompts"],
        },
        "metrics": {
            "mean_lift_lambda1": round(result["mean_lift_lambda1"], 6),
            "lock_positive_count": result["lock_positive_count"],
            "mu_positive_count": result["mu_positive_count"],
            "mean_lift_lambda1_rosenstein": None
            if mean_ros_lift != mean_ros_lift
            else round(mean_ros_lift, 6),
            "mean_lock_lambda1_rosenstein": None
            if mean_ros_lock != mean_ros_lock
            else round(mean_ros_lock, 6),
            "mean_mu_lambda1_rosenstein": None if mean_ros_mu != mean_ros_mu else round(mean_ros_mu, 6),
            "rosenstein_finite": ros_finite,
        },
        "hypothesis_support": {
            "H-AMAT-009": result["mean_lift_lambda1"] > 0
            and result["lock_positive_count"] > result["mu_positive_count"],
        },
        "certificate": certificate,
        "cells": result["cells"],
    }

    lean_path = ARTIFACTS / "summary_lean.json"
    if not lean_path.exists() and (ARTIFACTS / "summary.json").exists():
        lean_path.write_text((ARTIFACTS / "summary.json").read_text(encoding="utf-8"), encoding="utf-8")

    expanded = ARTIFACTS / "expanded"
    expanded.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(summary, indent=2, default=_json_default)
    full_payload = json.dumps(result, indent=2, default=_json_default)
    (ARTIFACTS / "summary.json").write_text(payload, encoding="utf-8")
    (ARTIFACTS / "full_lyapunov.json").write_text(full_payload, encoding="utf-8")
    (expanded / "summary.json").write_text(payload, encoding="utf-8")
    (expanded / "full_lyapunov.json").write_text(full_payload, encoding="utf-8")
    logger.info(
        "040 DONE certificate=%s lift=%.4f ros_finite=%s ros_lift=%s",
        certificate,
        result["mean_lift_lambda1"],
        ros_finite,
        mean_ros_lift,
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(run_namm_2026_040(), indent=2, default=_json_default))
