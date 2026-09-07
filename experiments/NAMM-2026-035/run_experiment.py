"""NAMM-2026-035: AMAT activation TDA — local LM hidden states vs F-AMAT-4."""

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
    run_activation_tda_sweep,
)

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
EXPERIMENT_ID = "NAMM-2026-035"


def _load_config() -> dict:
    with (Path(__file__).parent / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resume_cell_keys(cells_path: Path, prompts: list[str]) -> set[str]:
    keys: set[str] = set()
    if not cells_path.is_file():
        return keys
    for line in cells_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        cell = rec.get("cell") or {}
        prev = cell.get("prompt_preview", "")
        for p in prompts:
            if prev in p or p.startswith(prev[:40]):
                keys.add(p)
                break
    return keys


def _assign_certificate(summary: dict, *, skip_local: bool) -> str:
    if skip_local:
        return "SYNTHETIC_PILOT"
    if not summary:
        return "NULL"
    two_phase = summary.get("two_phase_cell_fraction", 0)
    f4_frac = summary.get("f_amat_4_triggered_fraction", 1.0)
    lift_b1 = summary.get("mean_lift_beta_1", 0)
    lift_d = summary.get("mean_lift_d_med", 0)

    if f4_frac < 0.5 and lift_d > 0:
        return "LIVE_EVIDENCE"
    if lift_b1 > 0.05 or two_phase >= 0.5:
        return "TDA_PARTIAL"
    return "ACTIVATION_PILOT"


def run_namm_2026_035(*, skip_local: bool = False) -> dict:
    cfg = _load_config()
    lm_cfg = cfg.get("local_lm") or {}
    act_cfg = cfg.get("activation") or {}
    loop_cfg = cfg.get("loop") or {}
    prompts = loop_cfg.get("prompts") or FOCUSED_PROMPTS
    n_turns = int(act_cfg.get("n_turns", 3))
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    cells_path = ARTIFACTS / "activation_cells.jsonl"

    resume_keys = _resume_cell_keys(cells_path, prompts)
    pending = [p for p in prompts if p not in resume_keys]

    lm = None
    if not skip_local:
        lm = load_local_lm(
            lm_cfg.get("model_id"),
            device=lm_cfg.get("device"),
            dtype=str(lm_cfg.get("dtype", "auto")),
        )
        logging.info(
            "Loaded %s on %s (%d layers, dim=%d)",
            lm.model_id,
            lm.device,
            lm.n_layers,
            lm.hidden_dim,
        )

    def on_cell(cell: dict, batch: dict) -> None:
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "cell": cell}
        with cells_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logging.info(
            "035 cell lift_d=%.4f lift_b1=%.4f two_phase=%s f4=%s",
            cell.get("lift_d_med", 0),
            cell.get("lift_beta_1", 0),
            cell.get("two_phase_structure"),
            cell.get("f_amat_4_triggered"),
        )

    if skip_local:
        import numpy as np
        from namm.metrics.phase_lock import load_phase_lock_spec
        from namm.metrics.activation_tda import (
            evaluate_activation_trajectory,
            activation_barycenter,
        )

        spec = load_phase_lock_spec()
        gates = spec["gates"]
        cells = []
        for i, prompt in enumerate(prompts):
            rng = np.random.default_rng(2026035 + i)
            mu_cloud = rng.normal(0, 0.05, (n_turns * 4, 16))
            lock_cloud = mu_cloud + rng.normal(0.3, 0.15, mu_cloud.shape)
            centroid = activation_barycenter([mu_cloud])
            mu_m = evaluate_activation_trajectory(mu_cloud, centroid, gates)
            lock_m = evaluate_activation_trajectory(lock_cloud, centroid, gates)
            lift_d = lock_m["d_med"] - mu_m["d_med"]
            lift_b1 = lock_m["beta_1"] - mu_m["beta_1"]
            two_phase = lift_b1 > 0.05 or lift_d > 0.05
            cell = {
                "prompt_preview": prompt[:80],
                "n_turns": n_turns,
                "mu_d_med": mu_m["d_med"],
                "lock_d_med": lock_m["d_med"],
                "lift_d_med": lift_d,
                "mu_beta_1": mu_m["beta_1"],
                "lock_beta_1": lock_m["beta_1"],
                "lift_beta_1": lift_b1,
                "two_phase_structure": two_phase,
                "f_amat_4_triggered": not two_phase,
                "tda_backend": mu_m.get("tda_backend"),
            }
            cells.append(cell)

        lifts_d = [c["lift_d_med"] for c in cells]
        lifts_b1 = [c["lift_beta_1"] for c in cells]
        result = {
            "protocol": cfg.get("protocol_version"),
            "mode": "synthetic_skip_local",
            "cells": cells,
            "errors": [],
            "summary": {
                "mean_lift_d_med": float(np.mean(lifts_d)),
                "mean_lift_beta_1": float(np.mean(lifts_b1)),
                "two_phase_cell_fraction": sum(1 for c in cells if c["two_phase_structure"]) / len(cells),
                "f_amat_4_triggered_fraction": sum(1 for c in cells if c["f_amat_4_triggered"]) / len(cells),
                "n_errors": 0,
                "tda_backends": ["knn_proxy"],
            },
            "hypothesis_support": {},
        }
    else:
        assert lm is not None
        # Run pending prompts individually for resume, then merge with prior cells
        prior_cells: list[dict] = []
        if cells_path.is_file():
            for line in cells_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    prior_cells.append(json.loads(line)["cell"])

        new_cells: list[dict] = []
        errors: list[dict] = []
        for prompt in pending:
            try:
                batch = run_activation_tda_sweep(
                    prompt,
                    lm,
                    n_turns=n_turns,
                    point_cloud_mode=act_cfg.get("point_cloud_mode", "turns_x_layers"),
                    last_n_layers=act_cfg.get("last_n_layers"),
                    max_new_tokens=int(lm_cfg.get("max_new_tokens", 128)),
                )
                cell = {
                    "prompt_preview": prompt[:80],
                    "n_turns": n_turns,
                    **batch["summary"],
                    "hypothesis_support": batch["hypothesis_support"],
                }
                new_cells.append(cell)
                on_cell(cell, batch)
            except Exception as exc:  # noqa: BLE001
                errors.append({"prompt_preview": prompt[:80], "error": str(exc)})
                logging.exception("035 cell failed: %s", prompt[:40])

        all_cells = prior_cells + new_cells
        if not all_cells and not errors:
            result = run_activation_tda_loop(
                prompts=prompts,
                n_turns=n_turns,
                lm=lm,
                point_cloud_mode=act_cfg.get("point_cloud_mode", "turns_x_layers"),
                last_n_layers=act_cfg.get("last_n_layers"),
                max_new_tokens=int(lm_cfg.get("max_new_tokens", 128)),
                on_cell=on_cell,
                protocol=cfg.get("protocol_version", "amat-activation-tda-v1"),
            )
        elif not all_cells:
            result = {
                "protocol": cfg.get("protocol_version"),
                "mode": "activation_tda",
                "model_id": lm.model_id,
                "cells": [],
                "errors": errors,
                "summary": {},
                "hypothesis_support": {},
            }
        else:
            import numpy as np

            lifts_d = [c["lift_d_med"] for c in all_cells]
            lifts_b1 = [c["lift_beta_1"] for c in all_cells]
            lifts_deff = [c.get("lift_d_eff", 0) for c in all_cells]
            two_phase_frac = sum(1 for c in all_cells if c.get("two_phase_structure")) / len(all_cells)
            f4_frac = sum(1 for c in all_cells if c.get("f_amat_4_triggered")) / len(all_cells)
            result = {
                "protocol": cfg.get("protocol_version"),
                "mode": "activation_tda",
                "model_id": lm.model_id,
                "device": lm.device,
                "cells": all_cells,
                "errors": errors,
                "summary": {
                    "mean_lift_d_med": round(float(np.mean(lifts_d)), 6),
                    "mean_lift_beta_1": round(float(np.mean(lifts_b1)), 6),
                    "mean_lift_d_eff": round(float(np.mean(lifts_deff)), 6),
                    "two_phase_cell_fraction": round(two_phase_frac, 4),
                    "f_amat_4_triggered_fraction": round(f4_frac, 4),
                    "best_cell": max(all_cells, key=lambda c: c.get("lift_beta_1", 0)),
                    "n_errors": len(errors),
                },
                "hypothesis_support": {
                    "H-AMAT-004": float(np.mean(lifts_d)) > 0.05,
                    "F-AMAT-4-not-triggered": f4_frac < 0.5,
                },
            }

    s = result.get("summary") or {}
    cert = _assign_certificate(s, skip_local=skip_local)

    f4_triggered = bool(s.get("f_amat_4_triggered_fraction", 0) >= 0.5)
    lift_d_med = float(s.get("mean_lift_d_med", 0) or 0)
    lift_beta_1 = float(s.get("mean_lift_beta_1", 0) or 0)
    two_phase_frac = float(s.get("two_phase_cell_fraction", 0) or 0)

    hypothesis_confirmed = (not f4_triggered) and (lift_d_med > 0) and (lift_beta_1 > 0.05 or two_phase_frac >= 0.5)
    falsifiers_triggered = {"F-AMAT-4": f4_triggered}

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "domain": cfg.get("domain"),
        "hypothesis_id": cfg.get("hypothesis_id"),
        "protocol_version": cfg.get("protocol_version"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": result.get("mode"),
        "model": {
            "model_id": result.get("model_id") or lm_cfg.get("model_id"),
            "device": result.get("device"),
        },
        "activation_config": act_cfg,
        "metrics": s,
        "hypothesis_support": result.get("hypothesis_support", {}),
        "f_amat_4_triggered": f4_triggered,
        "hypothesis_confirmed": hypothesis_confirmed,
        "falsifiers_triggered": falsifiers_triggered,
        "certificate": cert,
        "certificate_tiers": cfg.get("certificate_tiers"),
        "cells": result.get("cells", []),
        "errors": result.get("errors", []),
        "prior_experiments": cfg.get("prior_experiments"),
    }

    (ARTIFACTS / "summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (ARTIFACTS / "full_activation_tda.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = run_namm_2026_035()
    log_lines = [
        f"{res['timestamp']} {EXPERIMENT_ID} complete",
        f"certificate={res['certificate']}",
        f"model={res['model'].get('model_id')} device={res['model'].get('device')}",
        f"mean_lift_d={res['metrics'].get('mean_lift_d_med')}",
        f"mean_lift_b1={res['metrics'].get('mean_lift_beta_1')}",
        f"two_phase_frac={res['metrics'].get('two_phase_cell_fraction')}",
        f"f_amat_4_triggered={res['f_amat_4_triggered']}",
        f"errors={len(res.get('errors', []))}",
    ]
    log_text = "\n".join(log_lines) + "\n"
    for log_path in (ARTIFACTS / "experiment.log", Path(__file__).parent / "run.log"):
        try:
            log_path.write_text(log_text, encoding="utf-8")
            break
        except OSError:
            continue
    print(f"{EXPERIMENT_ID} complete. certificate={res['certificate']}")
    print(
        f"lift_d={res['metrics'].get('mean_lift_d_med')} "
        f"lift_b1={res['metrics'].get('mean_lift_beta_1')} "
        f"F-AMAT-4={res['f_amat_4_triggered']}"
    )
