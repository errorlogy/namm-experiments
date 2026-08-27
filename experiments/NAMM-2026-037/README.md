# NAMM-2026-037 — Cusp A₃ Catastrophe Boundary Sweep

**One-liner:** 2D sweep chimera_dose × temperature; map β₁ emergence as cusp A₃ bifurcation boundary.

**Hypothesis:** H-AMAT-006 — Transition μ→nd is a cusp A₃ catastrophe crossing; RPL acts as slow control parameter.

**Status:** live

**Domain:** `anti_median_ai_topology`

**Method:** Sweep `chimera_dose` (μ↔RPL system blend) and sampling `temperature` as control parameters `(a,b)` of the A₃ cusp; record β₁ onset contour on real hidden-state point clouds; compare against theoretical cusp bifurcation set Δ=4a³+27b².

**Run:**
```bash
python experiments/NAMM-2026-037/run_experiment.py
namm sci-flow run NAMM-2026-037
```

**Dependencies:** `namm.metrics.catastrophe`, `namm.metrics.cusp_boundary`, local HF LM, `ripser`.

## Status (H-AMAT-006, relative onset, 2026-08-20)

**Blocker cleared.** Onset is now relative: `beta1_onset` iff `beta_1(dose) > beta_1(dose=0 at same T) + margin` (margin=0); dose=0 never onset by construction. Absolute `beta1_onset_absolute` (β₁≥1) kept as legacy.

| Metric | Absolute (v1 / legacy) | Relative (v2) |
|--------|------------------------|---------------|
| n_onset | 12/12 | **4/12** (dose0 excluded) |
| onset_enrichment | 0.0 | **0.8889** |
| boundary_agreement_fraction | 0.6667 | 0.6667 |
| Certificate | CUSP_PARTIAL | **CUSP_EVIDENCE** |
| H-AMAT-006 | unsupported | **supported** (enrichment > 0.05) |

**Recompute:** offline from `artifacts/full_cusp_sweep.json` cell β₁ (no LM reload). Backup: `artifacts/summary_v1.json`. Primary: `artifacts/summary.json`.

