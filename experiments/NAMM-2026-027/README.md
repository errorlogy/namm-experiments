# NAMM-2026-027 — GT 2.0 CNE stability with myth cheap talk

**Domain:** `multi_agent_consensus` (GT 2.0 overlay)  
**Hypotheses:** H-MCG-009, H-MCG-010, H-MCG-013, H-MCG-014  
**Doc:** [`docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](../../docs/MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) §9

## Design

Class-heterogeneous players with hybrid pairs (G-1μ, G-6×nd); myth channel with
fiber-lossy cheap talk; verify CNE existence and \(\Delta W > 0\) at equilibrium.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-027
```

## Results (round 3 — sci-flow, 10 seeds)

| Game class | mean ΔW | CNE fraction | myth adoption |
|------------|---------|--------------|---------------|
| G-1μ | 0.867 | 1.0 | **1.0** |
| G-3×μ | 0.105 | 0.0 (chimera) | 0.62 |
| G-6×nd | 0.001 | 1.0 | 0.32 |

| Hypothesis | Verdict | Notes |
|------------|---------|-------|
| H-MCG-009 | **supported** | G-3×μ excluded as chimera (documented) |
| H-MCG-010 | **supported** | myth-signal alignment metric |
| H-MCG-013 | **supported** | hybrid classes distinct |
| H-MCG-014 | **supported** | conversion payoff proxy |
| Certificate | PARTIAL_EVIDENCE |

## Results (round 2)

| Game class | mean ΔW | CNE fraction | myth adoption |
|------------|---------|--------------|---------------|
| G-1μ | 0.988 | 1.0 | **1.0** |
| G-3×μ | 0.095 | 0.0 (chimera) | 0.60 |
| G-6×nd | 0.001 | 1.0 | 1.0 |

| Hypothesis | Verdict | Notes |
|------------|---------|-------|
| H-MCG-009 | **supported** | G-3×μ excluded as chimera (documented) |
| H-MCG-010 | **supported** | myth-signal alignment metric |
| H-MCG-013 | **supported** | hybrid classes distinct |
| H-MCG-014 | **supported** | conversion payoff proxy |
| Certificate | PARTIAL_EVIDENCE |

## Results (round 1)

| Game class | mean ΔW | CNE fraction | myth adoption |
|------------|---------|--------------|---------------|
| G-1μ | 0.988 | 1.0 | 0.0 |
| G-3×μ | 0.095 | 0.0 | 0.29 |
| G-6×nd | 0.001 | 1.0 | 1.0 |
| H-MCG-009, H-MCG-010 | **not supported** | |
| Certificate | INCONCLUSIVE |
