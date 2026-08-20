"""NAMM-2026-028: Myth shift catastrophe and class mobility."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_028() -> dict:
    result = run_sci_flow("NAMM-2026-028")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_028()
    print(f"NAMM-2026-028 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"max_hysteresis={result['metrics']['max_hysteresis_width']}")
