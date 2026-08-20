# NAMM-2026-025 — Class-heterogeneous MAS + CNS welfare

**Domain:** `cognitive_class_taxonomy` + `multi_agent_consensus`  
**Hypotheses:** H-CCT-005, H-CCT-007, H-CNS-005, H-CNS-010  
**Doc:** [`docs/COGNITIVE_CLASS_TAXONOMY.md`](../../docs/COGNITIVE_CLASS_TAXONOMY.md) §11

## Design

Opinion graphs with agents tagged K1/K3/K5/K6; compare forced consensus vs
class-cluster fiber-preserving aggregator; measure \(\Delta W\), \(\delta E\), \(R^*\).

## Run

```bash
namm sci-flow run --experiment NAMM-2026-025
```

## Results (round 3 — sci-flow, 10 seeds)

| Metric | Value |
|--------|-------|
| mean ΔW (K1 homogeneous) | 0.016 |
| mean ΔW (mixed K1+K5+K6) | 0.0004 |
| mean order R (mixed) | **0.858** (chimera R* in (0.3, 0.95)) |
| dissent-preserving better | **90%** |
| mean tail welfare gap | 0.104 |
| H-CCT-005, H-CCT-007, H-CNS-005, H-CNS-010 | **supported** |
| Certificate | PARTIAL_EVIDENCE |

## Results (round 2)

| Metric | Value |
|--------|-------|
| mean ΔW (K1 homogeneous) | 0.020 |
| mean ΔW (mixed K1+K5+K6) | 0.0004 |
| mean order R (mixed) | **0.825** (chimera R* in (0.3, 0.95)) |
| dissent-preserving better | 87.5% |
| mean tail welfare gap | 0.078 |
| H-CCT-005, H-CCT-007, H-CNS-010 | **supported** |
| H-CNS-005 (chimera R*) | **supported** (was not supported in round 1) |
| Certificate | PARTIAL_EVIDENCE |
