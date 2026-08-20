# NAMM-2026-021 — Opinion Graph Consensus vs Welfare Fiber

**Domain:** `multi_agent_consensus` · **Frame:** F3a + dynamical overlay  
**Hypotheses:** H-CNS-001, H-CNS-004, H-CNS-006, H-CNS-011, H-CNS-012, H-CNS-013  
**Doc:** [`docs/CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](../../docs/CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md)

## Research question

On bounded opinion graphs with fuzzy socio-political contours, does equilibrium consensus stay **strictly suboptimal** — with measurable permanent gap ΔW (and ΔH_fiber) even after dynamics settle?

## What is verified

| Construct | Implementation |
|-----------|----------------|
| Consensus operators | `mean`, `vote`, `defuzzify_mean`, `kuramoto_sync` |
| Welfare W(x) vs x* vs x† | `welfare()` vs `apply_consensus_operator()` vs `welfare_optimal()` |
| Anti-consensus gap | ΔW, ΔH_fiber, ε_proj |
| Fuzzy contours | gaussian_centroid, issue_tag, spatial_soft, triangular, trapezoidal, ramp |
| `max_non_optimality` | Per-contour bounds + bound saturation flags (H-CNS-012) |

## Run

```bash
namm sci-flow run --experiment NAMM-2026-021
# kuramoto variant for high-μ gate:
namm sci-flow run --experiment NAMM-2026-021 --variant kuramoto
```

Use `config-kuramoto.yaml` variant for H-CNS-013 (kuramoto_sync operator, 6 seeds).

## Results (round 3 — sci-flow default)

| Metric | Value |
|--------|-------|
| mean ΔW_global | 0.0023 |
| positive gap fraction | 1.0 |
| mean gap at high μ_cns | 0.0025 |
| consensus operator | defuzzify_mean |
| sci_modules | entropy, fuzzy, consensus, kuramoto |
| Certificate | PARTIAL_EVIDENCE |

## Results (round 2 — kuramoto variant)

| Metric | Value |
|--------|-------|
| mean ΔW_global | 0.280 |
| positive gap fraction | 1.0 |
| mean gap at high μ_cns | 0.286 |
| consensus operator | kuramoto_sync |
| H-CNS-013 | **supported** (was not supported in round 1 defuzzify_mean) |
| Certificate | PARTIAL_EVIDENCE |

## Results (round 1 — defuzzify_mean)

| Metric | Value |
|--------|-------|
| mean ΔW_global | 0.002307 |
| positive gap fraction | 1.0 (24/24 instances) |
| mean ΔH_fiber | 1.0 |
| H-CNS-001 | **supported** |
| H-CNS-013 | **not supported** (μ_cns_global < 0.5) |
| Certificate | PARTIAL_EVIDENCE |
