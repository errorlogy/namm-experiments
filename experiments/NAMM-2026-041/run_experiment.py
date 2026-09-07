"""NAMM-2026-041 — Attention head disagreement / H¹ proxy (H-AMAT-010)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import load_local_lm
from namm.metrics.attention_h1 import assign_h1_certificate, compare_policies_h1
from namm.metrics.phase_lock import load_phase_lock_spec, median_helpful_prompt

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
CONFIG_PATH = Path(__file__).parent / "config.yaml"
EXPERIMENT_ID = "NAMM-2026-041"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _json_default(obj: object) -> object:
    if isinstance(obj, float) and obj != obj:
        return None
    raise TypeError(f"Not serializable: {type(obj)}")


def run_namm_2026_041(*, deepen: bool = False) -> dict:
    cfg = _load_config()
    lm_cfg = dict(cfg.get("local_lm") or {})
    attn_cfg = dict(cfg.get("attention") or {})
    loop_cfg = cfg.get("loop") or {}
    summary_name = "summary.json"
    full_name = "full_attention_h1.json"
    cells_name = "h1_cells.jsonl"
    if deepen:
        lm_cfg["model_id"] = "Qwen/Qwen2.5-0.5B-Instruct"
        lm_cfg["model_candidates"] = ["Qwen/Qwen2.5-0.5B-Instruct"]
        lm_cfg["device"] = "cpu"
        attn_cfg["n_turns"] = 6
        summary_name = "summary_deepen.json"
        full_name = "full_attention_h1_deepen.json"
        cells_name = "h1_cells_deepen.jsonl"

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    cells_path = ARTIFACTS / cells_name
    if cells_path.exists():
        cells_path.unlink()

    candidates = lm_cfg.get("model_candidates") or [lm_cfg.get("model_id")]
    lm = load_local_lm(
        lm_cfg.get("model_id"),
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
        candidates=candidates,
        attn_implementation="eager",  # required for output_attentions
    )
    logger.info(
        "041 loaded %s on %s (%d layers, dim=%d)",
        lm.model_id,
        lm.device,
        lm.n_layers,
        lm.hidden_dim,
    )

    spec = load_phase_lock_spec()
    m0 = median_helpful_prompt()
    nd = spec["rendered_system_prompt"]
    prompts = loop_cfg.get("prompts") or []

    result = compare_policies_h1(
        lm,
        prompts,
        m0_system=m0,
        nd_system=nd,
        n_turns=int(attn_cfg.get("n_turns", 3)),
        max_new_tokens=int(lm_cfg.get("max_new_tokens", 64)),
        last_n_layers=int(attn_cfg.get("last_n_layers", 4)),
        disagreement_metric=str(attn_cfg.get("disagreement_metric", "js")),
    )

    for cell in result["cells"]:
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}, default=_json_default) + "\n")

    certificate = assign_h1_certificate(result)
    corr = result.get("corr_h1_beta1")
    h010a = result["mean_lift_h1"] > 0.01
    h010b = corr is not None and corr == corr and abs(float(corr)) >= 0.5

    summary = {
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": "H-AMAT-010",
        "protocol_version": cfg.get("protocol_version", "amat-attention-h1-v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {
            "model_id": lm.model_id,
            "device": lm.device,
            "n_layers": lm.n_layers,
            "hidden_dim": lm.hidden_dim,
        },
        "config": {
            "n_turns": int(attn_cfg.get("n_turns", 3)),
            "last_n_layers": int(attn_cfg.get("last_n_layers", 4)),
            "disagreement_metric": attn_cfg.get("disagreement_metric", "js"),
            "n_prompts": len(prompts),
        },
        "metrics": {
            "mean_lift_h1": round(result["mean_lift_h1"], 6),
            "mean_lift_beta_1": round(result["mean_lift_beta_1"], 6),
            "corr_h1_beta1": None if corr != corr else round(float(corr), 6),
            "lock_gt_mu_h1_count": result["lock_gt_mu_h1_count"],
            "lock_gt_mu_h1_fraction": round(result["lock_gt_mu_h1_fraction"], 4),
        },
        "hypothesis_support": {
            "H-AMAT-010-a": h010a,
            "H-AMAT-010-b": h010b,
        },
        "certificate": certificate,
        "cells": result["cells"],
    }

    (ARTIFACTS / summary_name).write_text(
        json.dumps(summary, indent=2, default=_json_default), encoding="utf-8"
    )
    (ARTIFACTS / full_name).write_text(
        json.dumps(result, indent=2, default=_json_default), encoding="utf-8"
    )

    logger.info(
        "041 DONE certificate=%s lift_h1=%.4f corr=%.3f",
        certificate,
        result["mean_lift_h1"],
        corr if corr == corr else float("nan"),
    )
    return summary


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--deepen", action="store_true")
    args = ap.parse_args()
    print(json.dumps(run_namm_2026_041(deepen=args.deepen), indent=2, default=_json_default))
