# NAMM-2026-001 — Finite Graph Invariant Search

**Domain:** finite connected graphs, order ≤ 8  
**Research question:** Can search find a nontrivial graph invariant candidate?

## Claims

| ID | Statement | Status |
|----|-----------|--------|
| C1 | Random linear combinations of graph statistics may differ from Wiener index | CONJECTURE |
| C2 | Exhaustive check on n≤5 detects equivalence to baseline | COMPUTATIONAL_EVIDENCE |

## Reproduction

From workspace root (`c:\Users\Public\NAMM`):

```powershell
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m namm.cli run-experiment --id NAMM-2026-001
```

Artifacts are written to `experiments/NAMM-2026-001/artifacts/`.
