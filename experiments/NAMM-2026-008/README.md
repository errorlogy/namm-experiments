# NAMM-2026-008 — Graceful Tree Conjecture Shadow

**Domain:** `open_problem_shadow`  
**Problem:** Graceful Tree Conjecture (T0 tierlist)  
**Strategy:** [`docs/ANTHEMIUM_NAMM_SYNERGY.md`](../../docs/ANTHEMIUM_NAMM_SYNERGY.md)

## Run

```bash
python -m namm.cli run-experiment --id NAMM-2026-008
python -m pytest tests/test_graceful_tree.py -q
```

## Finite shadow

All non-isomorphic trees of order ≤12 must admit a graceful labeling, or one tree certificate refutes the conjecture in this bound.
