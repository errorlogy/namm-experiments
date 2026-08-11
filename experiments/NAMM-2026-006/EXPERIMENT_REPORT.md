# NAMM-2026-006 — Experiment Report

**Domain:** TDA frame (`tda_frame`)  
**Date:** 2026-08-11  
**Seed:** 2026006  
**Frame:** F3f per [`docs/FRAME_LADDER.md`](../../docs/FRAME_LADDER.md)  
**Status:** **null run** — all candidates rejected

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **0** |
| Rejections | **40** |
| Max graph order | 8 |
| Baseline graph | path |
| Min persistence distance | 0.5 |
| Best distance observed | **3.5** |
| Representation gate | K_A/K_H ≥ 2.0 |

## Rejection breakdown

| Reason | Count |
|--------|-------|
| `representation_ratio_fail` | **40** |
| `baseline_too_close` | 0 |
| `no_h1_feature` | 0 |

All graphs with sufficient persistence distance to the path baseline failed the **compression asymmetry** gate (ratios 1.70–1.91, just below 2.0).

## Honest assessment

TDA frame search **did find** graphs whose persistence signature differs from the path baseline (best distance 3.5), but **none** cleared F4 (homo bottleneck) at the default ratio threshold. This is a **calibration null**: the frame works for topology discrimination but not yet for beyond-homo compression at order ≤8.

**Frame escalation:** combine with **NAMM-2026-007** (`raw_tensor`) per [`docs/BEYOND_HOMO_STRATEGY.md`](../../docs/BEYOND_HOMO_STRATEGY.md).

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-006
```

---

Roman Kuznetsov · NAMM research program
