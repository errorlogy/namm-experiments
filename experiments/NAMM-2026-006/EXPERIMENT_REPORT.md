# NAMM-2026-006 — Experiment Report

**Domain:** TDA frame (`tda_frame`)  
**Date:** 2026-08-11  
**Seed:** 2026006  
**Frame:** F3f per [`docs/FRAME_LADDER.md`](../../docs/FRAME_LADDER.md)  
**Status:** honest null — representation gate blocked all candidates

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **0** |
| Rejections | 40 |
| Max graph order | 8 |
| Baseline graph | path |
| Min persistence distance | 0.5 |
| Representation gate | K_A/K_H ≥ 2.0 |

## Research question

Can TDA frame search discover finite graphs whose persistent homology signature on the geodesic metric differs nontrivially from a path-graph baseline?

## Result

**No accepted candidates.** All 40 generated graphs passed baseline-distance and H¹-feature checks but failed the **representation_ratio_fail** gate (ratios 1.70–1.91, all below threshold 2.0). Best near-miss: β₁=2 graph at order 5 with ratio 1.90.

Generative holdout recorded best persistence distance **3.5** to path baseline (order-4 path signature).

## Honest assessment

TDA signatures are machine-compact but human projections remain short enough that K_A/K_H did not reach 2.0 in this budget (40 candidates). This is a **calibration null** for HL-010: persistence barcodes are searchable but compression asymmetry gate is tight on small graphs.

**Limitations**

- Rips on small graph metrics is a finite shadow — not full geometric topology.
- Path baseline is arbitrary; cycle/complete baselines may yield different acceptance rates.
- **COMPUTATIONAL_EVIDENCE** only — no topological theorem claims.

## Rejection breakdown

| Reason | Count |
|--------|-------|
| `representation_ratio_fail` | 40 |

## Artifacts

- `config.yaml` — experiment parameters
- `artifacts/rejections.jsonl` — all 40 rejections
- `artifacts/human_projection.md` — lossy audit

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-006
```

---

Roman Kuznetsov · NAMM research program
