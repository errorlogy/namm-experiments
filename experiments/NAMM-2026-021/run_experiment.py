"""NAMM-2026-021: Opinion graph consensus vs welfare fiber.

Measures permanent anti-consensus gap (Delta W, Delta H_fiber) at consensus
equilibrium on bounded opinion graphs with fuzzy socio-political contours.
"""

from __future__ import annotations

import logging
import sys

from namm.sci_flow import run_sci_flow


def run_namm_2026_021(variant: str | None = None) -> dict:
    """Execute opinion-graph welfare fiber experiment via sci-flow."""
    result = run_sci_flow("NAMM-2026-021", variant=variant)
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    variant = sys.argv[1] if len(sys.argv) > 1 else None
    summary = run_namm_2026_021(variant=variant)
    print(f"NAMM-2026-021 complete. Confirmed: {summary['hypothesis_confirmed']}")
    print(
        f"mean delta_W={summary['metrics']['mean_delta_w_global']}, "
        f"positive gap fraction={summary['metrics']['positive_gap_fraction']}"
    )
