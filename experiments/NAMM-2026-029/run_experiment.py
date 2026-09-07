"""NAMM-2026-029: Resource conversion asymmetry (U_out by class, same tokens)."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_029() -> dict:
    result = run_sci_flow("NAMM-2026-029")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_029()
    print(f"NAMM-2026-029 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"asymmetry_high_impact={result['metrics']['asymmetry_high_impact_ratio']}")
