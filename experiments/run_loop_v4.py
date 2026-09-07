"""NAMM loop-v4: sci-flow series NAMM-2026-021..030 (+ 021 kuramoto)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from namm.sci_flow import run_sci_flow

WORKSPACE = Path(__file__).resolve().parents[1]
SERIES = [f"NAMM-2026-0{i:02d}" for i in range(21, 31)]


def _pick_metrics(exp_id: str, result: dict) -> dict:
    m = result.get("metrics") or {}
    keys = {
        "NAMM-2026-021": ["mean_delta_w_global", "positive_gap_fraction", "mean_gap_at_high_mu_cns"],
        "NAMM-2026-022": ["mean_regret_spike_forced_vs_delayed", "mean_gap_at_high_mu_cns", "max_hysteresis_width"],
        "NAMM-2026-023": ["non_1d_score"],
        "NAMM-2026-024": ["jump_at_3sigma", "mean_beta1_at_3sigma"],
        "NAMM-2026-025": ["mean_order_R_mixed", "dissent_preserving_better_fraction"],
        "NAMM-2026-026": ["mean_delta_w_myth", "mean_gap_high_k1", "mean_gap_mixed"],
        "NAMM-2026-027": ["G-1mu_cne_fraction", "G-3xmu_cne_fraction", "G-6xnd_cne_fraction"],
        "NAMM-2026-028": ["max_hysteresis_width", "mean_class_transition_rate"],
        "NAMM-2026-029": ["asymmetry_high_impact_ratio", "steering_ratio"],
        "NAMM-2026-030": ["prompt_vs_m0_distance", "lock_d_med", "mu_d_med", "lock_gate_pass", "decay_gate_pass"],
    }
    wanted = keys.get(exp_id, list(m.keys())[:8])
    return {k: m[k] for k in wanted if k in m}


def run_loop(ids: list[str] | None = None, *, include_kuramoto: bool = True) -> dict:
    ids = ids or SERIES
    experiments: dict = {}
    for exp_id in ids:
        print(f"=== {exp_id} ===", flush=True)
        flow = run_sci_flow(exp_id)
        er = flow.experiment_result
        experiments[exp_id] = {
            "status": "Run",
            "sci_modules": flow.modules_used,
            "certificate": flow.certificate.get("status"),
            "hypothesis_confirmed": er.get("hypothesis_confirmed"),
            "key_metrics": _pick_metrics(exp_id, er),
            "hypothesis_support": er.get("hypothesis_support", {}),
        }
        print(
            f"  confirmed={er.get('hypothesis_confirmed')} cert={flow.certificate.get('status')}",
            flush=True,
        )

    if include_kuramoto:
        print("=== NAMM-2026-021 --variant kuramoto ===", flush=True)
        flow = run_sci_flow("NAMM-2026-021", variant="kuramoto")
        er = flow.experiment_result
        experiments["NAMM-2026-021-kuramoto"] = {
            "status": "Run",
            "variant": "kuramoto",
            "sci_modules": flow.modules_used,
            "certificate": flow.certificate.get("status"),
            "hypothesis_confirmed": er.get("hypothesis_confirmed"),
            "key_metrics": _pick_metrics("NAMM-2026-021", er),
            "hypothesis_support": er.get("hypothesis_support", {}),
        }

    supported = []
    failed = []
    for eid, row in experiments.items():
        hs = row.get("hypothesis_support") or {}
        for hid, ok in hs.items():
            (supported if ok else failed).append(f"{eid}:{hid}")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol": "cns-cct-mcg-loop-v4",
        "round": 4,
        "sci_flow": True,
        "series": ids,
        "experiments": experiments,
        "supported_flags": supported,
        "unsupported_flags": failed,
        "aggregate_verdict": {
            "CNS": "re-run 021–022 (+ kuramoto variant)",
            "CCT": "re-run 023–025, 029 + new 030 phase-lock",
            "MCG": "re-run 026–028",
        },
    }
    out = WORKSPACE / "experiments" / "sweep_summary.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {out}", flush=True)
    return summary


if __name__ == "__main__":
    run_loop()
