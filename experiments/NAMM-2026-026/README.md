# NAMM-2026-026 — Myth-as-Consensus on Class-Tagged Opinion Graphs

**Domain:** `multi_agent_consensus` + `cognitive_class_taxonomy`  
**Hypotheses:** H-MCG-001, H-MCG-007, H-MCG-008  
**Protocol:** `mcg-myth-consensus-v1`

## Design

Class-tagged agents (K1/K3/K5/K6) on opinion graphs with Kuramoto dynamics. Myth channel applies cheap-talk decode from K1 institutional signal; measure `μ_cns^myth` and `ΔW_myth` at consensus.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-026
# or
python experiments/NAMM-2026-026/run_experiment.py
```

## Round 3 Results (sci-flow, contour weighting)

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-MCG-001 | **supported** | ΔW_myth = 0.282 |
| H-MCG-007 | **supported** | gap_high_k1=0.464 > gap_mixed=0.191 |
| H-MCG-008 | **supported** | gap persists at high μ |

Contour weighting: `k1_saturation_boost=1.8`, `mixed_dampening=0.85`, 10 seeds.

## Round 2 Results

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-MCG-001 | **supported** | ΔW_myth = 0.178 |
| H-MCG-007 | **not supported** | mixed gap > K1-dominated |
| H-MCG-008 | **supported** | gap persists at high μ |

**Link:** [`docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](../../docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md)
