"""NAMM-2026-026: Myth-as-consensus on class-tagged opinion graphs."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_026() -> dict:
    result = run_sci_flow("NAMM-2026-026")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_026()
    print(f"NAMM-2026-026 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"mean_delta_w_myth={result['metrics']['mean_delta_w_myth']}")
