"""NAMM-2026-031: Live AMAT phase-lock loop via external LLM APIs."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.live_embeddings import run_phase_lock_live_loop

WORKSPACE = Path(__file__).resolve().parents[2]
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def _load_config() -> dict:
    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_namm_2026_031(*, skip_chat: bool = False) -> dict:
    cfg = _load_config()
    llm = cfg.get("llm") or {}
    loop = cfg.get("loop") or {}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    cells_path = ARTIFACTS / "live_loop_cells.jsonl"
    resume_keys: set[tuple[str, int]] = set()
    if cells_path.is_file():
        for line in cells_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            cell = rec.get("cell") or {}
            for p in loop.get("prompts", []):
                if p.startswith(cell.get("prompt_preview", "")[:40]) or cell.get("prompt_preview", "") in p:
                    resume_keys.add((p, int(cell.get("n_turns", 0))))
                    break

    def on_cell(cell: dict, batch: dict) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "cell": cell,
            "batch": {
                **batch,
                "policies": {
                    k: {
                        "metrics": v["metrics"],
                        "completion_preview": (v["completions"][-1][:400] if v.get("completions") else ""),
                    }
                    for k, v in batch.get("policies", {}).items()
                },
            },
        }
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logging.info(
            "cell turns=%s lift=%.4f persist=%.4f h020=%s",
            cell["n_turns"],
            cell["lift"],
            cell["persistence_gap"],
            cell["hypothesis_support"].get("H-CCT-020"),
        )

    result = run_phase_lock_live_loop(
        prompts=loop.get("prompts"),
        turn_values=[int(t) for t in loop.get("turn_values", [1, 2, 3])],
        chat_provider=llm.get("chat_provider"),
        embed_provider=llm.get("embed_provider"),
        chat_model=llm.get("chat_model"),
        pause_s=float(llm.get("pause_s", 2.0)),
        skip_chat=skip_chat,
        on_cell=on_cell,
        resume_keys=resume_keys,
    )

    support = result["hypothesis_support"]
    summary = result["summary"]
    confirmed = bool(support.get("H-AMAT-004") and support.get("H-AMAT-003"))

    if skip_chat:
        cert = "PROMPT_PILOT"
    elif summary["h020_cell_fraction"] >= 0.6 and summary["h021_cell_fraction"] >= 0.6:
        cert = "LIVE_EVIDENCE"
    elif summary["mean_lift"] > 0:
        cert = "LIVE_PARTIAL"
    else:
        cert = "NULL"

    payload = {
        "experiment_id": "NAMM-2026-031",
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": result["mode"],
        "llm": llm,
        "metrics": summary,
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "certificate": cert,
        "cells": result["cells"],
        "errors": result.get("errors", []),
    }

    out = ARTIFACTS / "summary.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (ARTIFACTS / "full_loop.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_031()
    print(f"NAMM-2026-031 complete. certificate={res['certificate']} confirmed={res['hypothesis_confirmed']}")
    print(f"mean_lift={res['metrics']['mean_lift']} persist={res['metrics']['mean_persistence_gap']}")
    print(f"H020 cells={res['metrics']['h020_cell_fraction']} H021 cells={res['metrics']['h021_cell_fraction']}")
