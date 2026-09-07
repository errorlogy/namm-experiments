"""NAMM-2026-025: Class-heterogeneous MAS + CNS welfare."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_025() -> dict:
    result = run_sci_flow("NAMM-2026-025")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_025()
    print(f"NAMM-2026-025 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"dissent better fraction={result['metrics']['dissent_preserving_better_fraction']}")
