# NAMM-2026-005 — Experiment Report

**Domain:** open problem shadow (`open_problem_shadow`, Kotzig P_k)  
**Date:** 2026-08-08  
**Seed:** 2026005  
**Search:** exhaustive NetworkX atlas scan  
**Status:** computationally supported (negative shadow)

## Summary

| Metric | Value |
|--------|-------|
| Graphs scanned | 995 (connected, order 2–7) |
| k range | 3–10 |
| Counterexamples | **0** |
| Near-miss candidates | 1 (best score 0.762) |
| Rejections logged | 5 |

## Research question

Does exhaustive atlas search up to order 7 find a finite P_k-graph (k≥3) counterexample to Kotzig's conjecture, or certify absence in this finite shadow?

## Result

**No counterexample** in the bounded shadow. Kotzig's conjecture survives for all 995 connected atlas graphs of order ≤7 and all k ∈ {3,…,10}.

Best near-miss: order-7 graph at k=4 with pair-fraction score **0.762** (76.2% of vertex pairs have exactly one length-4 path). Sample violations include pairs with 0, 2, or 3 paths instead of 1.

This extends computational evidence in the spirit of Kostochka (k≤20) but does **not** prove the conjecture.

## Certificate

Primary artifact: `artifacts/certificate.json`  
`eval_hash`: `db9a4190138fb0d8`

## Artifacts

- `artifacts/certificate.json` — bounded-search witness
- `artifacts/candidates.jsonl` — near-miss record
- `artifacts/rejections.jsonl` — non–P_k graphs
- `artifacts/HUMAN_PROJECTION.md` — lossy summary

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-005
python -m pytest tests/test_open_problem_pk.py -q
```

## Open problem link

[Kotzig's conjecture](https://en.wikipedia.org/wiki/Kotzig%27s_conjecture) · tierlist: [`docs/OPEN_PROBLEMS_TIERLIST.md`](../../docs/OPEN_PROBLEMS_TIERLIST.md)
