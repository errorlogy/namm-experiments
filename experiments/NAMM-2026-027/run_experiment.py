"""NAMM-2026-027: GT 2.0 CNE stability with myth cheap talk."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_027() -> dict:
    result = run_sci_flow("NAMM-2026-027")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_027()
    print(f"NAMM-2026-027 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"hypothesis_support={result['hypothesis_support']}")
