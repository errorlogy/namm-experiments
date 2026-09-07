"""NAMM-2026-030: JSON K_AI_nd phase-lock vs median embedding collapse."""

from __future__ import annotations

import logging

from namm.sci_flow import run_sci_flow


def run_namm_2026_030() -> dict:
    result = run_sci_flow("NAMM-2026-030")
    return result.experiment_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_namm_2026_030()
    print(f"NAMM-2026-030 complete. Confirmed: {result['hypothesis_confirmed']}")
    m = result["metrics"]
    if result.get("mode") == "loop":
        print(
            f"cells={m['n_cells']} mean_lift={m['mean_lift']} "
            f"max_lift={m['max_lift']} persist={m['mean_persistence_gap']}"
        )
        print(
            f"H-CCT-020 cells={m['h020_cell_fraction']} "
            f"H-CCT-021 cells={m['h021_cell_fraction']} "
            f"best gain={m['best_gain']} turns={m['best_n_turns']}"
        )
    else:
        print(f"prompt_vs_M0={m['prompt_vs_m0_distance']} lock_d_med={m['lock_d_med']} mu_d_med={m['mu_d_med']}")
        print(f"lock_gate_pass={m['lock_gate_pass']} decay_gate_pass={m['decay_gate_pass']}")
