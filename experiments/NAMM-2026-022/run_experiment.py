"""NAMM-2026-022: Catastrophe boundary in coupled Kuramoto–vote model."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_022() -> dict:
    result = run_sci_flow("NAMM-2026-022")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_022()
    print(f"NAMM-2026-022 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(
        f"mean regret spike={result['metrics']['mean_regret_spike_forced_vs_delayed']}, "
        f"max hysteresis={result['metrics']['max_hysteresis_width']}"
    )
