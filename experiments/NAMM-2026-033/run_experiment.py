"""NAMM-2026-033: AMAT gate calibration — live null distribution → recalibrated RPL gates."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.llm.env import load_env
from namm.metrics.gate_calibration import (
    calibrate_gates,
    run_gate_calibration_loop,
    sample_mu_null_distribution,
)

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-033"


def _load_config() -> dict:
    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_resume_null_indices(path: Path) -> set[int]:
    indices: set[int] = set()
    if not path.is_file():
        return indices
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if "seed_idx" in rec:
            indices.add(int(rec["seed_idx"]))
    return indices


def _load_resume_loop_keys(cells_path: Path, prompts: list[str]) -> set[tuple[str, int]]:
    keys: set[tuple[str, int]] = set()
    if not cells_path.is_file():
        return keys
    for line in cells_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        cell = rec.get("cell") or {}
        for p in prompts:
            prev = cell.get("prompt_preview", "")
            if prev in p or p.startswith(prev[:40]):
                keys.add((p, int(cell.get("n_turns", 0))))
                break
    return keys


def run_namm_2026_033(*, skip_chat: bool = False) -> dict:
    load_env()
    cfg = _load_config()
    llm = cfg.get("llm") or {}
    loop = cfg.get("loop") or {}
    cal_cfg = cfg.get("gate_calibration") or {}
    null_cfg = cal_cfg.get("null_sampling") or {}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    null_path = ARTIFACTS / "null_samples.jsonl"
    cells_path = ARTIFACTS / "live_loop_cells.jsonl"
    prompts = loop.get("prompts") or []
    n_seeds = int(null_cfg.get("n_seeds", 20))

    resume_null = _load_resume_null_indices(null_path)
    null_d_med: list[float] = []
    if null_path.is_file():
        for line in null_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                null_d_med.append(float(json.loads(line)["d_med"]))

    def on_null_sample(rec: dict) -> None:
        with null_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info("null seed=%s d_med=%.4f", rec["seed_idx"], rec["d_med"])

    if len(resume_null) < n_seeds:
        null_batch = sample_mu_null_distribution(
            prompts=prompts[:3],
            n_seeds=n_seeds,
            n_turns=1,
            chat_provider=llm.get("chat_provider"),
            embed_provider=llm.get("embed_provider"),
            chat_model=llm.get("chat_model"),
            pause_s=float(llm.get("pause_s", 2.0)),
            skip_chat=skip_chat,
            on_sample=on_null_sample,
            resume_indices=resume_null,
        )
        null_d_med = null_d_med + null_batch.get("null_d_med", [])
    else:
        null_batch = {"n_samples": len(null_d_med), "mode": "resumed"}

    thresholds = calibrate_gates(null_d_med, cal_cfg)
    (ARTIFACTS / "calibrated_thresholds.json").write_text(
        json.dumps(thresholds, indent=2), encoding="utf-8"
    )
    logging.info(
        "calibrated P95=%.4f z_thr=%.4f legacy=%.4f null_mean=%.4f",
        thresholds["percentile_threshold"],
        thresholds["z_score_threshold"],
        thresholds["legacy_d_med_min"],
        thresholds["null_mean"],
    )

    resume_loop = _load_resume_loop_keys(cells_path, prompts)

    def on_cell(cell: dict, batch: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info(
            "cell turns=%s lift=%.4f legacy_pass=%s cal_pass=%s",
            cell["n_turns"],
            cell["lift"],
            cell.get("legacy_lock_gate_pass"),
            cell.get("calibrated_lock_gate_pass"),
        )

    loop_result = run_gate_calibration_loop(
        prompts=prompts,
        turn_values=[int(t) for t in loop.get("turn_values", [3, 6])],
        thresholds=thresholds,
        chat_provider=llm.get("chat_provider"),
        embed_provider=llm.get("embed_provider"),
        chat_model=llm.get("chat_model"),
        pause_s=float(llm.get("pause_s", 2.0)),
        skip_chat=skip_chat,
        on_cell=on_cell,
        resume_keys=resume_loop,
    )

    s = loop_result["summary"]
    support = loop_result["hypothesis_support"]
    cert_tiers = cfg.get("certificate_tiers") or {}

    if skip_chat:
        cert = "PROMPT_PILOT"
    elif thresholds.get("null_n", 0) >= n_seeds:
        cert = "CALIBRATION_PARTIAL"
        if s.get("mean_lift", 0) > 0 and s.get("calibrated_lock_gate_pass_fraction", 0) > 0.3:
            cert = "LIVE_PARTIAL"
        if (
            s.get("h020_cell_fraction", 0) >= 0.6
            and s.get("h021_cell_fraction", 0) >= 0.6
        ):
            cert = "LIVE_EVIDENCE"
    else:
        cert = "NULL"

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": loop_result["mode"],
        "llm": {k: v for k, v in llm.items() if k != "api_key"},
        "null_sampling": {
            "n_seeds": n_seeds,
            "n_collected": len(null_d_med),
            "null_mean": thresholds["null_mean"],
            "null_std": thresholds["null_std"],
        },
        "calibrated_thresholds": thresholds,
        "metrics": s,
        "hypothesis_support": support,
        "hypothesis_confirmed": bool(support.get("H-AMAT-004") and support.get("H-AMAT-005")),
        "certificate": cert,
        "certificate_tiers": cert_tiers,
        "cells": loop_result["cells"],
        "errors": loop_result.get("errors", []),
        "prior_experiments": cfg.get("prior_experiments"),
    }

    (ARTIFACTS / "summary.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    full = {
        "null_batch": null_batch,
        "thresholds": thresholds,
        "loop": loop_result,
    }
    (ARTIFACTS / "full_calibration.json").write_text(
        json.dumps(full, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_033()
    lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"mean_lift={res['metrics'].get('mean_lift')}",
        f"legacy_pass_frac={res['metrics'].get('legacy_lock_gate_pass_fraction')}",
        f"calibrated_pass_frac={res['metrics'].get('calibrated_lock_gate_pass_fraction')}",
        f"P95_thr={res['calibrated_thresholds']['percentile_threshold']}",
        f"z_thr={res['calibrated_thresholds']['z_score_threshold']}",
        f"errors={len(res.get('errors', []))}",
    ]
    log_text = "\n".join(lines) + "\n"
    for log_path in (ARTIFACTS / "experiment.log", Path(__file__).parent / "run.log"):
        try:
            log_path.write_text(log_text, encoding="utf-8")
            break
        except OSError:
            continue
    print(f"{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(f"mean_lift={res['metrics'].get('mean_lift')} legacy={res['metrics'].get('legacy_lock_gate_pass_fraction')} cal={res['metrics'].get('calibrated_lock_gate_pass_fraction')}")
