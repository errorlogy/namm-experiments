# NAMM-2026-010 — Experiment Report

**Domain:** configuration shadow (`config_shadow`) — κ-projection sensitivity  
**Date:** 2026-08-11  
**Seed:** 2026010  
**Frame:** F3h extension  
**Status:** **50 candidates accepted** — **tested-signal**

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **50** |
| Rejections | **0** |
| κ modes swept | **4** (`first_4`, `last_4`, `middle_4`, `flux_blocks_4`) |
| Vacua scanned (each mode) | **59,049** |
| Max fiber (all modes) | **729** |
| Ambiguous shadows (all modes) | **81** |
| Selected κ for ranking | `first_4` (tie) |
| Lead witness | `vac-012e1fe1` (same as 009) |

## κ-sweep results

| κ mode | vacua | shadows | max fiber |
|--------|-------|---------|-----------|
| first_4 | 59,049 | 81 | 729 |
| last_4 | 59,049 | 81 | 729 |
| middle_4 | 59,049 | 81 | 729 |
| flux_blocks_4 | 59,049 | 81 | 729 |

## Research question

How does compactification ambiguity vary under alternate κ projections vs NAMM-2026-009 baseline?

## Result

**No variation at ±1 grid.** All four κ maps yield identical fiber statistics. Degeneracy is driven by **(11−4−1) free flux coordinates** with inactive energy bound, not by κ choice alone.

**Extension signal (script):** 7D moduli in \([-2,2]\) → 23,745 vacua, max fiber **42**, 625 shadows — wider grid breaks uniform 729.

## Honest assessment

- Confirms 009 fiber formula \(3^{n-s-1}\) is κ-robust for symmetric grids.
- Does **not** select a canonical compactification — all tested κ equally lossy here.
- Next: NAMM-2026-012 graceful-moduli hybrid; energy-active regimes at higher \(n\) or tighter Σm² cap.

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-010
python scripts/analyze_fiber_009.py
```

## Related

[`docs/AMFW_11D_HYPOTHESIS_RESEARCH.md`](../../docs/AMFW_11D_HYPOTHESIS_RESEARCH.md) · [`experiments/NAMM-2026-009/`](../NAMM-2026-009/)

---

Roman Kuznetsov · NAMM research program
