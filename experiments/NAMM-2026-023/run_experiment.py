"""NAMM-2026-023: Class separation via embedding/TDA proxies."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_023() -> dict:
    result = run_sci_flow("NAMM-2026-023")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_023()
    print(f"NAMM-2026-023 complete. Confirmed: {result['hypothesis_confirmed']}")
    print(f"non_1d_score={result['metrics']['non_1d_score']}")
