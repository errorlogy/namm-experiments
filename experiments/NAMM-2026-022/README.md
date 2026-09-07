# NAMM-2026-022 — Catastrophe + Kuramoto–Vote Coupling

**Domain:** `multi_agent_consensus` + Kuramoto proxy  
**Hypotheses:** H-CNS-002, H-CNS-005, H-CNS-011, H-CNS-013  
**Docs:** [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](../../docs/CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) · [`KURAMOTO_MIOC_SYNTHESIS.md`](../../docs/KURAMOTO_MIOC_SYNTHESIS.md)

## Research question

Does **forced consensus** near a catastrophe locus in coupled Kuramoto–vote dynamics increase regret vs delayed consensus, with permanent gap persisting at high μ_cns?

## What is verified

| Construct | Implementation |
|-----------|----------------|
| Kuramoto dynamics | `run_kuramoto_to_equilibrium()` with graph coupling |
| Vote / catastrophe proxy | Threshold sweep on phase-derived votes |
| Forced vs delayed consensus | High-K short integration vs low-K long integration |
| Hysteresis | Forward/backward vote outcome difference |
| Parameter sweep | K, vote_threshold, max_non_optimality, contour σ |

## Run

```bash
namm sci-flow run --experiment NAMM-2026-022
# or
python experiments/NAMM-2026-022/run_experiment.py
```

## Outputs

- `artifacts/result.json` — sweep summary and hypothesis support
- `artifacts/hysteresis_loop.json` — full sweep points
- `artifacts/certificate.json` — Protocol v2 certificate stub
- `run.log` — key numbers from the run

## Success criteria

- Hysteresis + measurable regret spike near catastrophe locus (H-CNS-002)
- Gap persists at μ_cns → 1 within configured bound (H-CNS-013)
- Optimal R* ∈ (0,1): full sync suboptimal (H-CNS-005)

## Falsifiers watched

F-CNS-2 (full sync maximizes W), F-CNS-5 (catastrophe model fails), F-CNS-8

## Results (round 3 — sci-flow + catastrophe module)

| Metric | Value |
|--------|-------|
| sweep size | 300 |
| mean regret spike (forced vs delayed) | 0.200 |
| mean gap at high μ_cns | 0.358 |
| max hysteresis width | 0.667 |
| cusp hysteresis width (Thom proxy) | 0.237 |
| catastrophe module confirmed | **yes** |
| H-CNS-002, H-CNS-005, H-CNS-013 | **supported** |
| Certificate | PARTIAL_EVIDENCE |

## Results (2026-08-18 run)

| Metric | Value |
|--------|-------|
| sweep size | 300 |
| mean regret spike (forced vs delayed) | 0.200 |
| mean gap at high μ_cns | 0.358 |
| max hysteresis width | 0.667 |
| H-CNS-002, H-CNS-005, H-CNS-013 | **supported** |
| Certificate | PARTIAL_EVIDENCE |
