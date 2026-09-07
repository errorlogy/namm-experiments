"""NAMM-2026-032: Live AMAT loop v2 — antigravity restart on collapse."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.live_embeddings import run_phase_lock_live_loop

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def run_namm_2026_032(*, skip_chat: bool = False) -> dict:
    cfg = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text(encoding="utf-8"))
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
                if cell.get("prompt_preview", "") in p or p.startswith(cell.get("prompt_preview", "")[:30]):
                    resume_keys.add((p, int(cell.get("n_turns", 0))))
                    break

    def on_cell(cell: dict, batch: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info(
            "032 cell turns=%s lift=%.4f lift_ag=%s persist=%.4f",
            cell["n_turns"],
            cell["lift"],
            cell.get("lift_ag"),
            cell["persistence_gap"],
        )

    result = run_phase_lock_live_loop(
        prompts=loop.get("prompts"),
        turn_values=[int(t) for t in loop.get("turn_values", [3, 6])],
        chat_provider=llm.get("chat_provider"),
        embed_provider=llm.get("embed_provider"),
        chat_model=llm.get("chat_model"),
        pause_s=float(llm.get("pause_s", 2.0)),
        skip_chat=skip_chat,
        include_ag=bool(loop.get("include_ag", True)),
        protocol=cfg.get("protocol_version", "amat-live-loop-v2"),
        on_cell=on_cell,
        resume_keys=resume_keys,
    )

    s = result["summary"]
    support = result["hypothesis_support"]
    ag_better = (s.get("mean_lift_ag") or 0) > s.get("mean_lift", 0)
    confirmed = bool(support.get("H-AMAT-003") and ag_better)

    if skip_chat:
        cert = "PROMPT_PILOT"
    elif s.get("mean_lift_ag", 0) >= 0.08 and ag_better:
        cert = "LIVE_EVIDENCE"
    elif s.get("mean_lift", 0) > 0:
        cert = "LIVE_PARTIAL"
    else:
        cert = "NULL"

    payload = {
        "experiment_id": "NAMM-2026-032",
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": result["mode"],
        "llm": llm,
        "metrics": s,
        "hypothesis_support": support,
        "hypothesis_confirmed": confirmed,
        "certificate": cert,
        "cells": result["cells"],
        "errors": result.get("errors", []),
        "prior": "NAMM-2026-031",
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "summary.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (ARTIFACTS / "full_loop.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_032()
    print(f"NAMM-2026-032 complete. certificate={res['certificate']}")
    m = res["metrics"]
    print(f"lift={m.get('mean_lift')} lift_ag={m.get('mean_lift_ag')} persist={m.get('mean_persistence_gap')}")
