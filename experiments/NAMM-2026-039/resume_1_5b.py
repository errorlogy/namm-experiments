"""Resume NAMM-2026-039 1.5B run from partial fractal_cells.jsonl."""
from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import load_local_lm
from namm.metrics.fractal_tda import aggregate_fractal_tda_loop, run_fractal_tda_sweep

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts" / "1.5b"
CELLS_PATH = OUT / "fractal_cells.jsonl"


def main() -> None:
    existing: list[dict] = []
    if CELLS_PATH.exists():
        for line in CELLS_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.append(json.loads(line)["cell"])

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    prompts = [cfg["prompts"]["chimera"], cfg["prompts"]["focused"]]
    remaining = prompts[len(existing) :]
    log.info("existing=%d remaining=%d", len(existing), len(remaining))

    lm_cfg = cfg.get("local_lm") or {}
    frac = cfg.get("fractal") or {}
    session = cfg.get("session") or {}

    lm = load_local_lm(
        "Qwen/Qwen2.5-1.5B-Instruct",
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
    )

    for prompt in remaining:
        cell = run_fractal_tda_sweep(
            prompt,
            lm,
            n_turns=int(session.get("n_turns", 3)),
            max_new_tokens=int(lm_cfg.get("max_new_tokens", 128)),
            epsilon_range=(float(frac["epsilon_min"]), float(frac["epsilon_max"])),
            n_epsilons=int(frac.get("n_epsilons", 14)),
            pca_dim=int(frac.get("pca_dim", 3)),
        )
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with CELLS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        existing.append(cell)
        comp = cell["comparison"]
        log.info(
            "cell done lift_df=%.4f lift_nig=%.4f cert=%s",
            comp["lift_mean_df"],
            comp["lift_non_int_gap"],
            cell["certificate"],
        )

    loop_result = aggregate_fractal_tda_loop(cells=existing, errors=[], n_prompts=len(prompts))
    summary = loop_result.get("summary", {})
    hyp = loop_result.get("hypothesis_support", {})

    all_top: list[int] = []
    for cell in existing:
        all_top.extend(cell["comparison"].get("most_informative_layers", []))
    top = Counter(all_top).most_common(5)

    payload = {
        "experiment_id": "NAMM-2026-039",
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
        "config": {
            "n_turns": int(session.get("n_turns", 3)),
            "pca_dim": int(frac.get("pca_dim", 3)),
            "n_epsilons": int(frac.get("n_epsilons", 14)),
            "epsilon_range": [frac["epsilon_min"], frac["epsilon_max"]],
            "prompts": prompts,
        },
        "summary": summary,
        "hypothesis_support": hyp,
        "hypothesis_confirmed": (
            hyp.get("H-AMAT-008-a") and hyp.get("H-AMAT-008-b") and hyp.get("H-AMAT-008-c")
        ),
        "certificate": loop_result.get("certificate"),
        "most_informative_layers": [{"layer": li, "count": cnt} for li, cnt in top],
        "cells": existing,
        "errors": [],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary_1.5b.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "full_fractal_tda.json").write_text(
        json.dumps(loop_result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    log.info("certificate=%s", loop_result.get("certificate"))
    log.info("mean_lift_df=%s mean_lift_non_int_gap=%s", summary.get("mean_lift_df"), summary.get("mean_lift_non_int_gap"))
    log.info("hypothesis_support=%s", hyp)
    log.info("most_informative_layers=%s", top)


if __name__ == "__main__":
    main()
