"""NAMM-2026-024: 3σ antigravity ↔ K6 phase transition sweep."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_024() -> dict:
    result = run_sci_flow("NAMM-2026-024")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_024()
    print(f"NAMM-2026-024 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"jump_at_3sigma={result['metrics']['jump_at_3sigma']}")
