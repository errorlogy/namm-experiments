"""NAMM-2026-039: Layer-wise TDA + box-counting fractal dimension (H-AMAT-008)."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import yaml

from namm.metrics.activation_tda import load_local_lm
from namm.metrics.fractal_tda import aggregate_fractal_tda_loop, run_fractal_tda_loop

EXPERIMENT_DIR = Path(__file__).resolve().parent
ARTIFACTS = EXPERIMENT_DIR / "artifacts"
EXPERIMENT_ID = "NAMM-2026-039"

log = logging.getLogger(__name__)


def _load_config() -> dict:
    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _assign_certificate(loop_result: dict) -> str:
    return loop_result.get("certificate", "NULL")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="NAMM-2026-039 layer-wise fractal TDA")
    p.add_argument(
        "--model-id",
        default=None,
        help="Override local_lm.model_id from config.yaml",
    )
    p.add_argument(
        "--artifacts-tag",
        default=None,
        help="Save under artifacts/<tag>/ (e.g. 1.5b) without overwriting default run",
    )
    return p.parse_args()


def run_namm_2026_039(
    *,
    model_id: str | None = None,
    artifacts_dir: Path | None = None,
) -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    frac_cfg = cfg.get("fractal") or {}
    session_cfg = cfg.get("session") or {}
    prompts_cfg = cfg.get("prompts") or {}

    pca_dim = int(frac_cfg.get("pca_dim", 3))
    n_epsilons = int(frac_cfg.get("n_epsilons", 14))
    eps_min = float(frac_cfg.get("epsilon_min", 0.02))
    eps_max = float(frac_cfg.get("epsilon_max", 0.5))
    epsilon_range = (eps_min, eps_max)
    n_turns = int(session_cfg.get("n_turns", 3))
    max_new_tokens = int(lm_cfg.get("max_new_tokens", 128))

    chimera = prompts_cfg.get(
        "chimera",
        "What is chimera synchronization and when is partial sync preferable to full consensus?",
    )
    focused = prompts_cfg.get(
        "focused",
        "Explain why consensus in multi-agent systems can be permanently suboptimal.",
    )
    prompts = [chimera, focused]

    out_dir = artifacts_dir or ARTIFACTS
    out_dir.mkdir(parents=True, exist_ok=True)
    cells_path = out_dir / "fractal_cells.jsonl"
    full_path = out_dir / "full_fractal_tda.json"
    summary_name = "summary.json"
    if artifacts_dir is not None and artifacts_dir != ARTIFACTS:
        tag = artifacts_dir.name
        summary_name = f"summary_{tag}.json" if tag else "summary.json"

    resolved_model_id = model_id or lm_cfg.get("model_id")
    lm = load_local_lm(
        resolved_model_id,
        device=lm_cfg.get("device"),
        dtype=str(lm_cfg.get("dtype", "auto")),
    )
    log.info(
        "Loaded %s on %s (%d layers, dim=%d)",
        lm.model_id, lm.device, lm.n_layers, lm.hidden_dim,
    )

    def on_cell(cell: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        comp = cell.get("comparison", {})
        log.info(
            "039 cell prompt=%.60s cert=%s lift_df=%.4f lift_nig=%.4f 008a=%s 008b=%s 008c=%s",
            cell.get("prompt_preview", ""),
            cell.get("certificate"),
            comp.get("lift_mean_df", 0),
            comp.get("lift_non_int_gap", 0),
            comp.get("h_amat_008a"),
            comp.get("h_amat_008b"),
            comp.get("h_amat_008c"),
        )

    reuse_full = bool(cfg.get("reuse_full_fractal_tda", False))
    if model_id is not None:
        reuse_full = False
    if reuse_full and full_path.exists():
        with full_path.open(encoding="utf-8") as f:
            cached_full = json.load(f)
        loop_result = aggregate_fractal_tda_loop(
            cells=cached_full.get("cells", []),
            errors=cached_full.get("errors", []),
            n_prompts=len(prompts),
        )
    else:
        loop_result = run_fractal_tda_loop(
            prompts,
            lm,
            n_turns=n_turns,
            max_new_tokens=max_new_tokens,
            epsilon_range=epsilon_range,
            n_epsilons=n_epsilons,
            pca_dim=pca_dim,
            on_cell=on_cell,
        )

    cert = _assign_certificate(loop_result)
    summary = loop_result.get("summary", {})
    hyp = loop_result.get("hypothesis_support", {})

    hypothesis_confirmed = (
        hyp.get("H-AMAT-008-a", False)
        and hyp.get("H-AMAT-008-b", False)
        and hyp.get("H-AMAT-008-c", False)
    )

    # Find most informative layers across all cells
    all_top_layers: list[int] = []
    for cell in loop_result.get("cells", []):
        all_top_layers.extend(cell.get("comparison", {}).get("most_informative_layers", []))
    from collections import Counter
    top_layer_counts = Counter(all_top_layers).most_common(5)

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
        "config": {
            "n_turns": n_turns,
            "pca_dim": pca_dim,
            "n_epsilons": n_epsilons,
            "epsilon_range": list(epsilon_range),
            "prompts": prompts,
        },
        "summary": summary,
        "hypothesis_support": hyp,
        "hypothesis_confirmed": hypothesis_confirmed,
        "certificate": cert,
        "certificate_tiers": cfg.get("certificate_tiers"),
        "most_informative_layers": [{"layer": li, "count": cnt} for li, cnt in top_layer_counts],
        "cells": loop_result.get("cells", []),
        "errors": loop_result.get("errors", []),
        "prior_experiments": cfg.get("prior_experiments"),
    }

    (out_dir / summary_name).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "full_fractal_tda.json").write_text(
        json.dumps(loop_result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = _parse_args()
    artifacts_dir = ARTIFACTS
    if args.artifacts_tag:
        artifacts_dir = ARTIFACTS / args.artifacts_tag
    res = run_namm_2026_039(model_id=args.model_id, artifacts_dir=artifacts_dir)
    lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"hypothesis_confirmed={res['hypothesis_confirmed']}",
        f"model={res['model']['model_id']} device={res['model']['device']}",
        f"n_turns={res['config']['n_turns']} pca_dim={res['config']['pca_dim']}",
        f"mean_lift_df={res['summary'].get('mean_lift_df')}",
        f"mean_lift_non_int_gap={res['summary'].get('mean_lift_non_int_gap')}",
        f"H-AMAT-008a={res['hypothesis_support'].get('H-AMAT-008-a')}",
        f"H-AMAT-008b={res['hypothesis_support'].get('H-AMAT-008-b')}",
        f"H-AMAT-008c={res['hypothesis_support'].get('H-AMAT-008-c')}",
        f"most_informative_layers={res['most_informative_layers']}",
    ]
    log_text = "\n".join(lines) + "\n"
    log_name = "run.log" if artifacts_dir == ARTIFACTS else f"run_{artifacts_dir.name}.log"
    (EXPERIMENT_DIR / log_name).write_text(log_text, encoding="utf-8")
    print(f"{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(f"mean_lift_df={res['summary'].get('mean_lift_df'):.4f}  "
          f"lift_nig={res['summary'].get('mean_lift_non_int_gap'):.4f}")
    print(f"H-AMAT-008: a={res['hypothesis_support'].get('H-AMAT-008-a')} "
          f"b={res['hypothesis_support'].get('H-AMAT-008-b')} "
          f"c={res['hypothesis_support'].get('H-AMAT-008-c')}")
    print(f"most_informative_layers={res['most_informative_layers']}")
