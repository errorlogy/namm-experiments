# NAMM-2026-008 — Experiment Report

**Domain:** open problem shadow (`open_problem_shadow`, Graceful Tree)  
**Date:** 2026-08-11  
**Seed:** 2026008  
**Tier:** T0 per [`docs/OPEN_PROBLEMS_TIERLIST.md`](../../docs/OPEN_PROBLEMS_TIERLIST.md)  
**Status:** **negative shadow** (no counterexample)

## Summary

| Metric | Value |
|--------|-------|
| Trees scanned | **987** (non-isomorphic, order 1–12) |
| Counterexamples | **0** |
| Verified shadow candidate | 1 (largest tree order 12) |
| Rejections logged | 5 (sample verified trees) |

## Research question

Does exhaustive enumeration of non-isomorphic trees up to order 12 find a counterexample to the Graceful Tree Conjecture?

## Result

**No counterexample.** All 987 trees in the bounded shadow admit a graceful labeling. The Graceful Tree Conjecture survives to order 12 in this finite shadow.

Example witness: order-12 tree index 0 with labeling `{0..11}` on vertices (see `artifacts/certificate.json`).

This extends computational evidence (literature verifies much larger n) but **does not prove** the conjecture.

## Honest assessment

- **Null for discovery:** no refutation certificate.
- **Positive for methodology:** backtracking label search + reproducible bounded sweep.
- Prior-art risk: incremental extension of known computational verification.

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-008
python -m pytest tests/test_graceful_tree.py -q
```

## Open problem link

[Graceful labeling](https://www.openproblemgarden.org/op/graceful_labeling) · [`docs/ANTHEMIUM_NAMM_SYNERGY.md`](../../docs/ANTHEMIUM_NAMM_SYNERGY.md)

---

Roman Kuznetsov · NAMM research program
