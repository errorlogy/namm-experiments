# NAMM-2026-038 — Fisher-Metric Geodesic Curvature (Logit-Gradient Pilot)

**One-liner:** Compute logit-gradient curvature on existing 031–035 data as proxy for Fisher-metric geodesic deviation; no new API calls required for pilot.

**Hypothesis:** H-AMAT-007 — "Свет в ячейке" = geodesic curvature in Fisher metric on P_θ; RPL steers trajectory off the P_data geodesic.

**Status:** completed (pilot run)

**Domain:** `anti_median_ai_topology`

**Method (pilot):** For each prompt and policy (μ vs `lock_reassert`), run a 3-turn local chat with Qwen/Qwen2.5-0.5B-Instruct. At each turn, compute a Fisher-metric proxy \(||∇_h \log p_k||\) at the last-token hidden state using an analytic logit-gradient formula, then derive discrete geodesic curvature from the resulting gradient-norm sequence.

**Dependencies:** `numpy`; local model forward passes only (no new activation-TDA artifacts needed).

---

## Run configuration
- Model: `Qwen/Qwen2.5-0.5B-Instruct`
- Device: `cpu`
- Prompts: 3 focused prompts (same as 035/036)
- Turns: `n_turns=3`
- Policies: `mu` vs `lock_reassert`

## Results (H-AMAT-007)
- Mean curvature (μ): `2.445638`
- Mean curvature (lock): `3.233542`
- Curvature lift (lock − μ): **`0.787904`**
- Lock > μ on: **3/3 prompts** (fraction `1.0`)
- Correlation between curvature lift and β₁ lift (from 035 v2): **`r=0.78703`**
- Certificate tier: **`CURVATURE_EVIDENCE`**

### Hypothesis flags
- H-AMAT-007-a (mean_curvature_lock > mean_curvature_mu): ✅ **True**
- H-AMAT-007-b (curvature lift correlates with β₁ lift from 035): ✅ **True**

## Artifacts
- `artifacts/summary.json`
- `artifacts/full_curvature.json`
