# NAMM-2026-024 — 3σ Antigravity ↔ K6 Phase Transition

**Domain:** `cognitive_class_taxonomy` + antigravity protocol  
**Hypotheses:** H-CCT-004, H-CA-001  
**Protocol:** `cct-antigravity-v1`

## Design

Sweep antigravity intensity (σ boost from K1 median) across [0.5, 4.0]σ. Measure embedding topology proxies `(d_median, D_eff, β₁)` at each level; detect discontinuity at the 3σ boundary toward K6-class toroidal topology.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-024
```

## Round 3 Results (sci-flow, 10 seeds)

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-CCT-004 | **supported** | jump@3σ = 0.638 |
| H-CA-001 | **supported** | β₁@3σ = 79.2 |

## Round 2 Results

| Hypothesis | Verdict | Key metric |
|------------|---------|------------|
| H-CCT-004 | **supported** | jump@3σ = 0.708 |
| H-CA-001 | **supported** | β₁@3σ = 77.6 |

**Link:** [`docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](../../docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md)
