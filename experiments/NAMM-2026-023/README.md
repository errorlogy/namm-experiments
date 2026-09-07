# NAMM-2026-023 — Class separation in embedding topology

**Domain:** `cognitive_class_taxonomy` + TDA proxy  
**Hypotheses:** H-CCT-001, H-CCT-004, H-CCT-012  
**Doc:** [`docs/COGNITIVE_CLASS_TAXONOMY.md`](../../docs/COGNITIVE_CLASS_TAXONOMY.md) §11

## Design

Synthetic class-proxy embeddings for K1/K3/K5/K6; measure median distance \(d\),
effective dimension \(D_{\mathrm{eff}}\), and Betti proxies \(\beta_0, \beta_1\) on k-NN graphs.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-023
```

## Results (round 3 — sci-flow, 10 seeds)

| Metric | Value |
|--------|-------|
| non-1D score | 81.79 |
| K1 vs K6 separation | 5.19 |
| H-CCT-001, H-CCT-004, H-CCT-012 | **supported** |
| Certificate | PARTIAL_EVIDENCE |

## Results (latest run)

| Metric | Value |
|--------|-------|
| non-1D score | 102.03 |
| K1 vs K5 separation | 4.11 |
| K1 d_median | 0.085 |
| K5 d_median | 1.662 |
| H-CCT-001, H-CCT-004, H-CCT-012 | **supported** |
| Certificate | PARTIAL_EVIDENCE |
