# NAMM-2026-028 — Myth Shift Catastrophe + Class Mobility

**Domain:** `multi_agent_consensus` + `cognitive_class_taxonomy`  
**Hypotheses:** H-MCG-005, H-MCG-006, H-CNS-002  
**Protocol:** `mcg-myth-shift-v1`

## Design

Sweep media coupling K and salience threshold; record forward/backward Kuramoto hysteresis on myth state and class transition rates. Links to 022 hysteresis loop.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-028
# or
python experiments/NAMM-2026-028/run_experiment.py
```

## Round 3 Results (sci-flow, 10 seeds, catastrophe module)

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-MCG-005 | **supported** | transition rate = 81.1% |
| H-MCG-006 | **supported** | dead-sync at R→1 |
| H-CNS-002 | **supported** | max hysteresis = 0.852 |
| catastrophe module | **confirmed** | cusp width = 0.200 |

Sweep size: 350 (7×5×10 seeds).

## Round 2 Results

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-MCG-005 | **supported** | transition rate = 81% |
| H-MCG-006 | **supported** | dead-sync at R→1 |
| H-CNS-002 | **supported** | max hysteresis = 0.852 |

**Link:** [`docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](../../docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md)
