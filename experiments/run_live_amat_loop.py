"""Autonomous AMAT live loop runner — NAMM-2026-031 with checkpointing."""

from __future__ import annotations

import json
import logging
import runpy
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
ARTIFACTS = WORKSPACE / "experiments" / "NAMM-2026-031" / "artifacts"
RUN_LOG = WORKSPACE / "experiments" / "live_amat_loop_summary.json"


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    script = WORKSPACE / "experiments" / "NAMM-2026-031" / "run_experiment.py"
    logging.info("Starting NAMM-2026-031 live loop")
    result = runpy.run_path(str(script), run_name="__main__")
    payload = result.get("res") if isinstance(result, dict) else None
    if payload is None and (ARTIFACTS / "summary.json").is_file():
        payload = json.loads((ARTIFACTS / "summary.json").read_text(encoding="utf-8"))

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol": "amat-live-loop-v1",
        "experiment_id": "NAMM-2026-031",
        "result": payload,
    }
    RUN_LOG.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    logging.info("Wrote %s", RUN_LOG)


if __name__ == "__main__":
    main()
