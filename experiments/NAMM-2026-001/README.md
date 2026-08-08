# NAMM-2026-001 — Finite Graph Invariant Search

**Domain:** finite connected graphs, order ≤ 8  
**Status:** computationally supported (first complete NAMM cycle)

## Quick links

- **Full report:** [EXPERIMENT_REPORT.md](./EXPERIMENT_REPORT.md)
- **Human projection:** [artifacts/HUMAN_PROJECTION.md](./artifacts/HUMAN_PROJECTION.md)
- **Machine artifacts:** [artifacts/](./artifacts/)

## Best candidate

`2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering` — score 289.44, not equivalent to Wiener.

## Reproduction

```powershell
cd c:\Users\Public\NAMM
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m namm.cli run-experiment --id NAMM-2026-001
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe experiments\analyze_namm_2026_001.py
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m pytest -q
```
