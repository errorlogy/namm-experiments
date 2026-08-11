# NAMM-2026-008 — Experiment Report

**Domain:** open problem shadow (`open_problem_shadow`, Graceful Tree Conjecture)  
**Date:** 2026-08-11  
**Seed:** 2026008  
**Search:** exhaustive non-isomorphic tree enumeration  
**Status:** computationally supported (negative shadow)

## Summary

| Metric | Value |
|--------|-------|
| Trees scanned | **987** (non-isomorphic, order 1–12) |
| Counterexamples | **0** |
| Verified shadow | order ≤ 12 |
| Rejections logged | 5 (sample verified trees) |

## Research question

Does exhaustive enumeration of non-isomorphic trees up to order 12 find a counterexample to the Graceful Tree Conjecture, or certify the conjecture in this finite shadow?

## Result

**No counterexample** in the bounded shadow. All 987 non-isomorphic trees of order ≤ 12 admit a graceful labeling under backtracking search. Best verified witness: order-12 tree index 0 (certificate in `artifacts/certificate.json`).

This extends computational evidence for the Graceful Tree Conjecture but does **not** prove the conjecture for all trees.

## Certificate

Primary artifact: `artifacts/certificate.json`  
Witness tree: order 12, 11 edges, sequential labeling 0..11 yields distinct edge sums.

## Honest assessment

Extends HL-008 finite-shadow methodology from Kotzig P_k (005) to graceful trees at scale (987 trees vs 995 graphs in 005). Shadow bound order ≤ 12 is known-safe territory; counterexample would have been headline refutation.

## Artifacts

- `config.yaml` — experiment parameters
- `artifacts/certificate.json` — bounded-search witness
- `artifacts/candidates.jsonl` — verified shadow record
- `artifacts/rejections.jsonl` — sample graceful trees (not counterexamples)
- `artifacts/human_projection.md` — lossy summary

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-008
python -m pytest tests/test_graceful_tree.py -q
```

## Open problem link

[Graceful Tree Conjecture](https://en.wikipedia.org/wiki/Graceful_labeling) · strategy: [`docs/BEYOND_HOMO_STRATEGY.md`](../../docs/BEYOND_HOMO_STRATEGY.md)

---

Roman Kuznetsov · NAMM research program
