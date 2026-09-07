"""NAMM-2026-036: AMAT activation TDA v3 — PCA-reduced D_eff fix."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import (
    FOCUSED_PROMPTS,
    load_local_lm,
    run_activation_tda_loop,
    run_pca_sweep,
)

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-036"


def _load_config() -> dict:
    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _assign_certificate(summary: dict) -> str:
    lift_deff = float(summary.get("mean_lift_d_eff", 0) or 0)
    lift_b1 = float(summary.get("mean_lift_beta_1", 0) or 0)
    if lift_b1 > 0.05 and lift_deff > 0.5:
        return "ACTIVATION_EVIDENCE"
    if lift_deff > 0.5:
        return "D_EFF_PARTIAL"
    if lift_deff > 0.0 or lift_b1 > 0.0:
        return "ACTIVATION_PILOT"
    return "NULL"


def run_namm_2026_036() -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    act_cfg = cfg.get("activation") or {}
    sweep_cfg = cfg.get("sweep") or {}
    focused_prompts = cfg.get("focused_prompts") or FOCUSED_PROMPTS

    pca_dims_list: list[int] = [int(x) for x in sweep_cfg.get("pca_dims", [4, 8, 16])]
    n_turns_list: list[int] = [int(x) for x in sweep_cfg.get("n_turns", [3, 6, 10])]
    chimera_prompt: str = sweep_cfg.get(
        "chimera_prompt",
        "What is chimera synchronization and when is partial sync preferable to full consensus?",
    )
    last_n_layers = int(act_cfg.get("last_n_layers", 8))
    max_new_tokens = int(lm_cfg.get("max_new_tokens", 128))

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    sweep_path = ARTIFACTS / "sweep_chimera.jsonl"
    focused_path = ARTIFACTS / "focused_loop.jsonl"

    lm = load_local_lm(
        lm_cfg.get("model_id"),
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
    )
    logging.info(
        "Loaded %s on %s (%d layers, dim=%d)",
        lm.model_id, lm.device, lm.n_layers, lm.hidden_dim,
    )

    # ── Phase 1: chimera sweep (pca_dims × n_turns) ──────────────────────────
    def on_sweep_cell(cell: dict, _batch: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with sweep_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info(
            "036 sweep pca=%d n_turns=%d lift_deff=%.4f lift_b1=%.4f",
            cell.get("pca_dims", -1),
            cell.get("n_turns", -1),
            cell.get("lift_d_eff", 0),
            cell.get("lift_beta_1", 0),
        )

    sweep_result = run_pca_sweep(
        chimera_prompt,
        lm,
        pca_dims_list=pca_dims_list,
        n_turns_list=n_turns_list,
        last_n_layers=last_n_layers,
        max_new_tokens=max_new_tokens,
        on_cell=on_sweep_cell,
    )

    best_pca_dim: int = int(sweep_result["best_pca_dim"])
    logging.info("Best pca_dim from sweep: %d", best_pca_dim)

    # ── Phase 2: focused-prompt loop at best_pca_dim, n_turns=6 ──────────────
    def on_focused_cell(cell: dict, _batch: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with focused_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info(
            "036 focused pca=%d lift_deff=%.4f lift_b1=%.4f two_phase=%s",
            best_pca_dim,
            cell.get("lift_d_eff", 0),
            cell.get("lift_beta_1", 0),
            cell.get("two_phase_structure"),
        )

    loop_result = run_activation_tda_loop(
        prompts=focused_prompts,
        n_turns=6,
        lm=lm,
        point_cloud_mode="turns_x_layers",
        last_n_layers=last_n_layers,
        max_new_tokens=max_new_tokens,
        on_cell=on_focused_cell,
        protocol=cfg.get("protocol_version", "amat-activation-tda-v3"),
        pca_dims=best_pca_dim,
    )

    # ── Certificate ──────────────────────────────────────────────────────────
    focused_summary = loop_result.get("summary") or {}
    cert = _assign_certificate(focused_summary)

    lift_deff = float(focused_summary.get("mean_lift_d_eff", 0) or 0)
    lift_b1 = float(focused_summary.get("mean_lift_beta_1", 0) or 0)
    f4_frac = float(focused_summary.get("f_amat_4_triggered_fraction", 1.0))

    hypothesis_confirmed = (
        not (f4_frac >= 0.5)
        and lift_b1 > 0.05
        and lift_deff > 0.5
    )

    # joint 035+036 note
    joint_note = (
        "035: beta1 lift confirmed (+0.67→+1.0 mean), D_eff=0 (artifact: 896-d). "
        f"036: PCA d={best_pca_dim} → D_eff lift={lift_deff:.4f}, "
        f"beta1 lift={lift_b1:.4f}, cert={cert}. "
        "D_eff resolved=" + ("YES" if lift_deff > 0.5 else "PARTIAL" if lift_deff > 0 else "NO")
        + f". Overall chain 030-036: cert={cert}."
    )

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": {"model_id": lm.model_id, "device": lm.device,
                  "n_layers": lm.n_layers, "hidden_dim": lm.hidden_dim},
        "sweep": {
            "best_pca_dim": best_pca_dim,
            "summary_by_pca_dim": sweep_result["summary_by_pca_dim"],
            "n_sweep_cells": len(sweep_result["cells"]),
            "n_sweep_errors": len(sweep_result["errors"]),
        },
        "focused_loop": {
            "pca_dims": best_pca_dim,
            "n_turns": 6,
            "metrics": focused_summary,
        },
        "certificate": cert,
        "certificate_tiers": cfg.get("certificate_tiers"),
        "hypothesis_confirmed": hypothesis_confirmed,
        "f_amat_4_triggered": f4_frac >= 0.5,
        "hypothesis_support": loop_result.get("hypothesis_support", {}),
        "joint_note_035_036": joint_note,
        "cells_sweep": sweep_result["cells"],
        "cells_focused": loop_result.get("cells", []),
        "errors": sweep_result["errors"] + loop_result.get("errors", []),
        "prior_experiments": cfg.get("prior_experiments"),
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (ARTIFACTS / "full_pca_tda.json").write_text(
        json.dumps({"sweep": sweep_result, "focused_loop": loop_result}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_036()
    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"model={res['model'].get('model_id')} device={res['model'].get('device')}",
        f"best_pca_dim={res['sweep']['best_pca_dim']}",
        f"mean_lift_d_eff={res['focused_loop']['metrics'].get('mean_lift_d_eff')}",
        f"mean_lift_b1={res['focused_loop']['metrics'].get('mean_lift_beta_1')}",
        f"f_amat_4_triggered={res['f_amat_4_triggered']}",
        f"joint_note={res['joint_note_035_036']}",
    ]
    log_text = "\n".join(log_lines) + "\n"
    (Path(__file__).parent / "run.log").write_text(log_text, encoding="utf-8")
    print(f"{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(f"best_pca_dim={res['sweep']['best_pca_dim']}")
    print(
        f"lift_d_eff={res['focused_loop']['metrics'].get('mean_lift_d_eff')} "
        f"lift_b1={res['focused_loop']['metrics'].get('mean_lift_beta_1')}"
    )
    print(res["joint_note_035_036"].encode(errors="replace").decode())
