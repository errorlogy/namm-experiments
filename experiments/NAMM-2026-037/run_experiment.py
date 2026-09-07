"""NAMM-2026-037 — Cusp A₃ β₁ emergence boundary (H-AMAT-006)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import load_local_lm
from namm.metrics.cusp_boundary import assign_cusp_certificate, run_cusp_boundary_sweep
from namm.metrics.phase_lock import load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
CONFIG_PATH = Path(__file__).parent / "config.yaml"
EXPERIMENT_ID = "NAMM-2026-037"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _json_default(obj: object) -> object:
    if isinstance(obj, float) and obj != obj:
        return None
    raise TypeError(f"Not serializable: {type(obj)}")


def run_namm_2026_037() -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    sw = cfg.get("sweep") or {}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    lm = load_local_lm(
        lm_cfg.get("model_id"),
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
        candidates=lm_cfg.get("model_candidates"),
    )
    logger.info("037 loaded %s on %s", lm.model_id, lm.device)

    spec = load_phase_lock_spec()
    result = run_cusp_boundary_sweep(
        lm,
        str(sw.get("prompt") or "What is chimera synchronization?"),
        m0_system=median_helpful_prompt(),
        nd_system=spec["rendered_system_prompt"],
        doses=[float(x) for x in sw.get("doses", [0.0, 0.5, 1.0])],
        temperatures=[float(x) for x in sw.get("temperatures", [0.3, 0.7, 1.2])],
        n_turns=int(sw.get("n_turns", 3)),
        max_new_tokens=int(lm_cfg.get("max_new_tokens", 48)),
        last_n_layers=int(sw.get("last_n_layers", 4)),
        pca_dims=int(sw.get("pca_dims", 8)),
        beta1_onset=float(sw.get("beta1_onset", 1.0)),
        relative_margin=float(sw.get("relative_margin", 0.0)),
    )

    certificate = assign_cusp_certificate(result)
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": "H-AMAT-006",
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {"model_id": lm.model_id, "device": lm.device, "hidden_dim": lm.hidden_dim},
        "grid": {"doses": result["doses"], "temperatures": result["temperatures"]},
        "metrics": {
            "n_cells": result["n_cells"],
            "n_onset": result["n_onset"],
            "p_onset_inside_cusp": result["p_onset_inside_cusp"],
            "p_onset_outside_cusp": result["p_onset_outside_cusp"],
            "onset_enrichment": result["onset_enrichment"],
            "onset_definition": result.get("onset_definition", "relative_vs_dose0"),
            "n_onset_absolute": result.get("n_onset_absolute"),
            "onset_enrichment_absolute": result.get("onset_enrichment_absolute"),
            "boundary_agreement_fraction": result["boundary_agreement_fraction"],
            "mean_beta_1": result["mean_beta_1"],
            "mu_baseline_beta1_by_temp": result.get("mu_baseline_beta1_by_temp"),
        },
        "hypothesis_support": {
            "H-AMAT-006": result["onset_enrichment"] > 0.05,
        },
        "certificate": certificate,
        "crossings": result["crossings"],
        "cells": result["cells"],
        "recompute_mode": "live",
    }

    (ARTIFACTS / "summary.json").write_text(json.dumps(summary, indent=2, default=_json_default), encoding="utf-8")
    (ARTIFACTS / "full_cusp_sweep.json").write_text(json.dumps(result, indent=2, default=_json_default), encoding="utf-8")
    logger.info("037 DONE certificate=%s enrichment=%.3f", certificate, result["onset_enrichment"])
    return summary


if __name__ == "__main__":
    print(json.dumps(run_namm_2026_037(), indent=2, default=_json_default))
