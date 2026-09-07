"""NAMM-2026-045: Real hidden states on Qwen2.5-1.5B — D_eff separation test.

Uses activation_tda.py (transformers) with 044 sweet-spot protocol:
  n_turns=6, last_n_layers=4, pca_dims=8, cosine ripser, μ vs lock_reassert.
Compares against 035 (0.5B HS), 043 (nomic), 044 (protocol v2).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from namm.metrics.activation_tda import (
    FOCUSED_PROMPTS,
    load_local_lm,
    run_activation_tda_sweep,
)

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-045"
CONFIG_PATH = Path(__file__).parent / "config.yaml"

BASELINE_035 = {
    "experiment": "NAMM-2026-035",
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "space": "real_hidden_states",
    "n_turns": 3,
    "pca_dims": None,
    "ripser_metric": "euclidean",
    "mean_lift_d_eff": 0.0,
    "mean_lift_beta_1": 0.78,
    "mean_lift_d_med": 1.29,
    "two_phase_fraction": 0.67,
    "certificate": "LIVE_EVIDENCE",
}

BASELINE_044_N6 = {
    "experiment": "NAMM-2026-044",
    "model": "llama3.2 + nomic-embed-text",
    "space": "nomic_hybrid_768d",
    "n_turns": 6,
    "pca_dims": 8,
    "ripser_metric": "cosine",
    "mean_lift_d_eff": 0.33,
    "mean_lift_beta_1": 0.0,
    "mean_lift_d_med": 2.33,
    "two_phase_fraction": 1.0,
    "certificate": "NULL",
    "note": "044 per n_turns=6 sweet spot (aggregate cert NULL)",
}

logger = logging.getLogger(__name__)


def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _assign_certificate(mean_lift_d_eff: float, mean_lift_beta_1: float) -> str:
    if mean_lift_beta_1 > 0.05 and mean_lift_d_eff > 0.3:
        return "HYBRID_EVIDENCE"
    if mean_lift_d_eff > 0.3:
        return "D_EFF_RESOLVED"
    if mean_lift_beta_1 > 0.05 or mean_lift_d_eff > 0.1:
        return "HYBRID_PILOT"
    return "NULL"


def run_namm_2026_045() -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    act_cfg = cfg.get("activation") or {}
    tda_cfg = cfg.get("tda") or {}
    loop_cfg = cfg.get("loop") or {}

    prompts: list[str] = loop_cfg.get("prompts") or FOCUSED_PROMPTS
    n_turns = int(act_cfg.get("n_turns", 6))
    last_n_layers = act_cfg.get("last_n_layers", 4)
    point_cloud_mode = act_cfg.get("point_cloud_mode", "turns_x_layers")
    pca_dims = int(tda_cfg.get("pca_dims", 8))
    ripser_metric = str(tda_cfg.get("ripser_metric", "cosine"))
    max_new_tokens = int(lm_cfg.get("max_new_tokens", 256))

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    cells_path = ARTIFACTS / "activation_cells.jsonl"
    if cells_path.exists():
        cells_path.unlink()

    model_id = lm_cfg.get("model_id")
    candidates = lm_cfg.get("model_candidates")
    lm = load_local_lm(
        model_id,
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
        candidates=candidates,
    )
    logger.info(
        "045: loaded %s on %s (%d layers, dim=%d)",
        lm.model_id,
        lm.device,
        lm.n_layers,
        lm.hidden_dim,
    )

    cells: list[dict] = []
    errors: list[dict] = []
    full_batches: list[dict] = []

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
            cell = {
                "prompt_preview": prompt[:80],
                "n_turns": n_turns,
                **batch["summary"],
                "hypothesis_support": batch["hypothesis_support"],
                "n_points_mu": batch["policies"]["mu"]["point_cloud_shape"][0],
                "n_points_lock": batch["policies"]["lock_reassert"]["point_cloud_shape"][0],
            }
            cells.append(cell)
            full_batches.append(batch)

            rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
            with cells_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

            logger.info(
                "045 cell lift_deff=%.4f lift_b1=%.4f lift_d=%.4f two_phase=%s backend=%s",
                cell["lift_d_eff"],
                cell["lift_beta_1"],
                cell["lift_d_med"],
                cell["two_phase_structure"],
                cell.get("tda_backend"),
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("045 cell failed: %s", prompt[:40])
            errors.append({"prompt_preview": prompt[:80], "error": str(exc)})

    if not cells:
        payload = {
            "experiment_id": EXPERIMENT_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": errors,
            "certificate": "NULL",
        }
        (ARTIFACTS / "summary.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return payload

    lifts_d = [c["lift_d_med"] for c in cells]
    lifts_b1 = [c["lift_beta_1"] for c in cells]
    lifts_deff = [c["lift_d_eff"] for c in cells]
    two_phase_frac = sum(1 for c in cells if c.get("two_phase_structure")) / len(cells)

    mean_lift_d_eff = float(np.mean(lifts_deff))
    mean_lift_beta_1 = float(np.mean(lifts_b1))
    mean_lift_d_med = float(np.mean(lifts_d))
    cert = _assign_certificate(mean_lift_d_eff, mean_lift_beta_1)
    d_eff_resolved = mean_lift_d_eff > 0.3

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {
            "model_id": lm.model_id,
            "device": lm.device,
            "n_layers": lm.n_layers,
            "hidden_dim": lm.hidden_dim,
        },
        "pipeline": {
            "space": "real_last_token_hidden_states",
            "n_turns": n_turns,
            "last_n_layers": last_n_layers,
            "point_cloud_mode": point_cloud_mode,
            "n_points_per_policy": n_turns * int(last_n_layers),
            "pca_dims": pca_dims,
            "ripser_metric": ripser_metric,
            "policies": act_cfg.get("policies", ["mu", "lock_reassert"]),
            "n_prompts": len(prompts),
        },
        "metrics": {
            "mean_lift_d_eff": round(mean_lift_d_eff, 6),
            "mean_lift_beta_1": round(mean_lift_beta_1, 6),
            "mean_lift_d_med": round(mean_lift_d_med, 6),
            "two_phase_cell_fraction": round(two_phase_frac, 4),
            "best_cell": max(cells, key=lambda c: c.get("lift_d_eff", 0)),
            "n_errors": len(errors),
        },
        "certificate": cert,
        "d_eff_resolved": d_eff_resolved,
        "hybrid_evidence": mean_lift_beta_1 > 0.05 and d_eff_resolved,
        "hypothesis_support": {
            "H-AMAT-004": mean_lift_d_med > 0.05,
            "H-CCT-020": mean_lift_d_med > 0.05,
            "H-CCT-021": mean_lift_beta_1 > 0.05,
            "D_EFF_RESOLVED": d_eff_resolved,
        },
        "comparison_table": {
            "035_0.5B_HS": BASELINE_035,
            "044_n6_nomic": BASELINE_044_N6,
            "045_this_run": {
                "experiment": EXPERIMENT_ID,
                "model": lm.model_id,
                "space": "real_hidden_states",
                "n_turns": n_turns,
                "pca_dims": pca_dims,
                "ripser_metric": ripser_metric,
                "mean_lift_d_eff": round(mean_lift_d_eff, 6),
                "mean_lift_beta_1": round(mean_lift_beta_1, 6),
                "mean_lift_d_med": round(mean_lift_d_med, 6),
                "two_phase_fraction": round(two_phase_frac, 4),
                "certificate": cert,
            },
        },
        "cells": cells,
        "errors": errors,
        "prior_experiments": cfg.get("prior_experiments"),
        "certificate_tiers": cfg.get("certificate_tiers"),
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (ARTIFACTS / "full_activation_tda.json").write_text(
        json.dumps({"batches": full_batches, "cells": cells}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_045()
    m = res.get("metrics") or {}
    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res.get('certificate')}",
        f"model={res.get('model', {}).get('model_id')} device={res.get('model', {}).get('device')}",
        f"mean_lift_d_eff={m.get('mean_lift_d_eff')}",
        f"mean_lift_beta_1={m.get('mean_lift_beta_1')}",
        f"mean_lift_d_med={m.get('mean_lift_d_med')}",
        f"two_phase_frac={m.get('two_phase_cell_fraction')}",
        f"d_eff_resolved={res.get('d_eff_resolved')}",
    ]
    (Path(__file__).parent / "run.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"\n{EXPERIMENT_ID} complete. certificate={res.get('certificate')}")
    print(
        f"mean_lift_d_eff={m.get('mean_lift_d_eff')} "
        f"mean_lift_beta_1={m.get('mean_lift_beta_1')} "
        f"mean_lift_d_med={m.get('mean_lift_d_med')}"
    )
