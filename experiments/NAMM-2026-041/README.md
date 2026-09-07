# NAMM-2026-041 — Attention Head Disagreement Proxy for Sheaf Cohomology H¹

**One-liner:** Compute attention head disagreement across layers as proxy for sheaf cohomology obstruction H¹≠0; test whether β₁ correlates with inconsistency of local sections.

**Hypothesis:** H-AMAT-010 — β₁ reflects inconsistency of local sections across attention heads; "свет в ячейке" = sheaf cohomology obstruction H¹≠0 (PHILOSOPHICAL_INFERENCE→CONJECTURE).

**Status:** live

**Domain:** `anti_median_ai_topology`

**Method:** Extract per-head attention distributions via `output_attentions`; measure pairwise Jensen–Shannon disagreement across heads as H¹ approximation; correlate with β₁ from activation TDA; compare μ vs `lock_reassert`.

**Run:**
```bash
python experiments/NAMM-2026-041/run_experiment.py
namm sci-flow run NAMM-2026-041
```

**Certificate tiers:** `H1_EVIDENCE` / `H1_PILOT` / `H1_PARTIAL` / `NULL`

**Dependencies:** local HF transformers; `numpy`; `ripser` for β₁; `namm.metrics.attention_h1`.

**Epistemic note:** H-AMAT-010 is PHILOSOPHICAL_INFERENCE→CONJECTURE. This experiment provides the first operational proxy, not a formal sheaf construction.

## Status (pilot + deepen, 2026-08-26)

- **Pilot (2026-08-20):** certificate **`H1_PARTIAL`** — `artifacts/summary.json`; lock>μ H₁ proxy on 2/2 prompts; mean_lift_h1≈0.006 (below `H1_PILOT` 0.01 threshold).
- **Deepen (8841567e):** certificate **`H1_PILOT`** — `artifacts/summary_deepen.json`; Qwen2.5-0.5B, `n_turns=6`, `last_n_layers=2`, 2 prompts; lock>μ on 2/2; **mean_lift_h1≈0.047**; H-AMAT-010-a supported, H-AMAT-010-b false (β₁ lift=0). Usable as pilot signal for EIA crosswalk; expand prompts/layers for `H1_EVIDENCE` (see [`docs/ANTI_MEDIAN_AI_TOPOLOGY.md`](../../docs/ANTI_MEDIAN_AI_TOPOLOGY.md) §5).
