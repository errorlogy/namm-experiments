"""NAMM-2026-038 — Fisher-metric geodesic curvature pilot (H-AMAT-007).

Run:
    python experiments/NAMM-2026-038/run_experiment.py
or via sci-flow:
    namm sci-flow run NAMM-2026-038
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE / "src"))

from namm.metrics.activation_tda import FOCUSED_PROMPTS, load_local_lm
from namm.metrics.information_geometry import compare_curvature, compute_certificate, correlate_curvature_beta1
from namm.metrics.phase_lock import load_phase_lock_spec, median_helpful_prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

ARTIFACTS = Path(__file__).parent / "artifacts"
CONFIG_PATH = Path(__file__).parent / "config.yaml"


def _json_default(obj: object) -> object:
    if isinstance(obj, float) and (obj != obj):  # nan
        return None
    raise TypeError(f"Not serializable: {type(obj)}")


def run_namm_2026_038(skip_local: bool = False) -> dict:
    """Entry-point for sci-flow handler."""
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    model_cfg = config.get("model", {})
    model_id = model_cfg.get("model_id", "Qwen/Qwen2.5-0.5B-Instruct")
    device_pref = model_cfg.get("device", "auto")
    if device_pref == "auto":
        device_pref = None

    exp_cfg = config.get("experiment", {})
    n_turns = int(exp_cfg.get("n_turns", 3))
    max_new_tokens = int(exp_cfg.get("max_new_tokens", 128))

    beta1_lifts_raw = config.get("beta1_lifts_from_035", [-1.0, 4.0, 0.0])
    beta1_lifts = [float(x) for x in beta1_lifts_raw]

    spec = load_phase_lock_spec()
    mu_system = median_helpful_prompt()
    lock_system = spec["rendered_system_prompt"]

    prompts = FOCUSED_PROMPTS

    if skip_local:
        logger.info("skip_local=True — returning stub result")
        return {"experiment_id": "NAMM-2026-038", "skipped": True}

    logger.info("Loading model %s (device=%s)", model_id, device_pref or "auto")
    lm = load_local_lm(model_id, device=device_pref)
    model = lm.model
    tokenizer = lm.tokenizer
    device = lm.device

    logger.info("Running curvature sessions (n_turns=%d, n_prompts=%d)", n_turns, len(prompts))
    result = compare_curvature(
        prompts,
        prompts,
        model,
        tokenizer,
        device=device,
        mu_system=mu_system,
        lock_system=lock_system,
        n_turns=n_turns,
        max_new_tokens=max_new_tokens,
    )

    # Correlation with β₁ from 035
    kappa_lifts = [p["lift"] for p in result["per_prompt"]]
    corr_beta1 = correlate_curvature_beta1(kappa_lifts, beta1_lifts)
    result["corr_curvature_beta1"] = round(corr_beta1, 6) if corr_beta1 == corr_beta1 else None

    # Certificate
    certificate = compute_certificate(result, beta1_lifts)
    result["certificate"] = certificate

    # Hypothesis flags
    lock_gt_mu_fraction = result["lock_gt_mu_count"] / max(result["n_prompts"], 1)
    h007a = result["lock_gt_mu_count"] >= 2  # ≥2/3 prompts
    h007b = (
        corr_beta1 == corr_beta1  # not nan
        and abs(corr_beta1) >= 0.5
    )

    summary = {
        "experiment_id": "NAMM-2026-038",
        "hypothesis_id": "H-AMAT-007",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_id": lm.model_id,
        "device": lm.device,
        "n_turns": n_turns,
        "n_prompts": len(prompts),
        "metrics": {
            "mean_curvature_mu": result["mean_curvature_mu"],
            "mean_curvature_lock": result["mean_curvature_lock"],
            "curvature_lift": result["curvature_lift"],
            "lock_gt_mu_count": result["lock_gt_mu_count"],
            "lock_gt_mu_fraction": round(lock_gt_mu_fraction, 4),
            "corr_curvature_beta1": result["corr_curvature_beta1"],
            "kappa_lifts_per_prompt": kappa_lifts,
            "beta1_lifts_from_035": beta1_lifts,
        },
        "hypothesis_support": {
            "H-AMAT-007-a": h007a,
            "H-AMAT-007-b": h007b,
        },
        "certificate": certificate,
        "per_prompt": result["per_prompt"],
    }

    # Save artifacts
    (ARTIFACTS / "summary.json").write_text(
        json.dumps(summary, indent=2, default=_json_default), encoding="utf-8"
    )
    (ARTIFACTS / "full_curvature.json").write_text(
        json.dumps(result, indent=2, default=_json_default), encoding="utf-8"
    )

    logger.info(
        "DONE — certificate=%s  lift=%.4f  H-007-a=%s  H-007-b=%s  corr_β1=%.3f",
        certificate,
        result["curvature_lift"],
        h007a,
        h007b,
        corr_beta1 if corr_beta1 == corr_beta1 else float("nan"),
    )
    return summary


if __name__ == "__main__":
    result = run_namm_2026_038()
    print(json.dumps(result, indent=2, default=_json_default))
