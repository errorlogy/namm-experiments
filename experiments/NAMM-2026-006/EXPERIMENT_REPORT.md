# NAMM-2026-006 — Experiment Report

**Domain:** TDA frame (`tda_frame`)  
**Date:** _pending first run_  
**Seed:** 2026006  
**Frame:** F3f per [`docs/FRAME_LADDER.md`](../../docs/FRAME_LADDER.md)  
**Status:** template — fill after `run-experiment`

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | _TBD_ |
| Rejections | _TBD_ |
| Max graph order | 8 |
| Baseline graph | path |
| Min persistence distance | 0.5 |
| Representation gate | K_A/K_H ≥ 2.0 |

## Best candidate

**ID:** _TBD_  
**Signature hash:** _TBD_  
**β₁ / H¹ total persistence:** _TBD_  
**Distance to baseline:** _TBD_  
**Certificate:** `artifacts/certificate.json`

## Research question

Can TDA frame search discover finite graphs whose persistent homology signature on the geodesic metric differs nontrivially from a path-graph baseline?

## Honest assessment

**What to report**

- Count of graphs accepted vs rejected (`baseline_too_close`, `no_h1_feature`, `representation_ratio_fail`).
- Whether accepted candidates show **compression asymmetry** (persistence JSON compact vs human projection).
- Whether results are **calibration** (expected cycle-like graphs) vs unexpected signatures.

**Limitations**

- Rips on small graph metrics is a **finite shadow** of TDA — not full geometric topology.
- Path baseline is arbitrary; cycle/complete baselines may yield different acceptance rates.
- **COMPUTATIONAL_EVIDENCE** only — no topological theorem claims.

## Rejection breakdown

| Reason | Count |
|--------|-------|
| `baseline_too_close` | _TBD_ |
| `no_h1_feature` | _TBD_ |
| `representation_ratio_fail` | _TBD_ |

## Artifacts

- `config.yaml` — experiment parameters
- `artifacts/certificate.json` — primary ground truth
- `artifacts/candidates.jsonl` / `rejections.jsonl`
- `artifacts/human_projection.md` — lossy audit

---

Roman Kuznetsov · NAMM research program
