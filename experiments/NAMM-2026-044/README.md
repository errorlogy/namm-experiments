# NAMM-2026-044: D_eff Stability Sensitivity (vs 043)

**Hypothesis:** H-AMAT-004  
**Protocol:** `amat-hybrid-nomic-embed-v2`  
**Date:** 2026-08-19  
**Status:** complete — certificate `NULL`

## Protocol change (single bundled improvement)

043 used short trajectories (`n_turns ∈ {3, 6}`, 1 embed/turn → 3–6 points) with silent PCA cap and euclidean ripser. TDA collapsed: β₁=0, two_phase=0, D_eff lift negative.

044 stabilizes sampling + logs diagnostics:

| Parameter | 043 | 044 |
|---|---|---|
| n_turns | {3, 6} | {6, 9, 12} |
| points per policy | 3–6 | **12–24** (2 samples/turn) |
| PCA k (effective) | 2–5 (capped) | **8** (capped at min(8, n−1)) |
| effective rank | unlogged | **6–23** logged |
| ripser metric | euclidean | **cosine** |
| diagnostics | none | n_points, pca_k, eff_rank, ripser settings |

## Results vs 043

| Metric | 043 | 044 | Δ |
|---|---|---|---|
| mean_lift_d_eff | −0.50 | **−0.11** | +0.39 |
| mean_lift_beta_1 | 0.00 | **−0.22** | −0.22 |
| mean_lift_d_med | +2.42 | +1.53 | −0.89 |
| two_phase_fraction | 0.00 | **1.00** | +1.00 |
| certificate | NULL | NULL | — |

**Per n_turns (044):**

| n_turns | n_points | pca_k | eff_rank (μ/lock) | lift_d_eff | lift_β₁ | two_phase |
|---|---|---|---|---|---|---|
| 6 | 12 | 8 | 9.3 / 11.0 | **+0.33** | 0.00 | 1.0 |
| 9 | 18 | 8 | 14.7 / 16.7 | 0.00 | **+0.33** | 1.0 |
| 12 | 24 | 8 | 19.7 / 20.7 | **−0.67** | −1.00 | 1.0 |

## Diagnosis

1. **043 β₁=0 was sampling collapse** — confirmed. With ≥12 points, full PCA k=8, and cosine ripser, homology is non-trivial and two_phase_fraction=1.0.
2. **D_eff aggregate still NULL** — mean lift −0.11; sign flips across n_turns (+0.33 at n=6, 0 at n=9, −0.67 at n=12). Longer clouds increase rank but also variance; lock and μ both develop rich topology, so *relative* D_eff lift is unstable.
3. **Sweet spot at n_turns=6** — only regime with positive mean D_eff lift; n=12 over-samples and inverts separation.

## Run

```bash
python experiments/NAMM-2026-044/run_experiment.py
namm sci-flow run NAMM-2026-044
```

## Artifacts

- `artifacts/summary.json` — aggregate + `comparison_vs_043`
- `artifacts/full_hybrid_tda.json` — all cells with per-policy PCA/TDA diagnostics
- `artifacts/loop_n{6,9,12}.jsonl` — streaming records
- `run.log` — execution summary
