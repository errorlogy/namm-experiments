# NAMM-2026-014 — Brainwave / Ω_c Covariate Bridge (scaffold)

**Domain:** cross-cutting — `raw_tensor` + `meta_evaluation` covariates for 013  
**Status:** **scaffold only** — not yet implemented  
**Hypothesis:** [`docs/BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](../../docs/BRAINWAVE_OSCILLATION_HYPOTHESIS.md) · H-BW-003 · [`docs/KURAMOTO_MIOC_SYNTHESIS.md`](../../docs/KURAMOTO_MIOC_SYNTHESIS.md) · H-KM-001, H-KM-003  
**Primary experiment:** [`NAMM-2026-013`](../NAMM-2026-013/) (H-CA-001)  
**Branch:** `hypothesis/cognitive-antigravity`

## Planned research question

Do **inter-layer coherence proxies** (Ω_c, Kuramoto order parameter, band-power ratios) covary with **cognitive antigravity** outcomes (\(D_{\mathrm{med}}\), \(S_{\mathrm{fals}}\)) across 013 arms — and do they add predictive power beyond prompt condition alone?

## Planned design

| Input | Source |
|-------|--------|
| 013 arms + task battery | Shared with NAMM-2026-013 |
| Hidden-state traces | Same model forward passes as 013 |
| Band decomposition | delta→high-gamma per BRAINWAVE doc §2 |

**Covariates (planned):**

- Ω_c \((i,j)\) — Kraskov MI between selected layer pairs  
- Kuramoto \(r(t)\) — single-band order parameter  
- \(R_{\mathrm{multi}}(t)\) — weighted sum over delta→high-gamma bands  
- Theta–gamma nesting index (cross-frequency coupling surrogate)  
- Per-band power ratios (alpha/gamma as homo-binding probe)  
- Dead synchrony flag: \(R > R_{\max}\) with flat \(S_{\mathrm{fals}}\)  
- Optional: MIOC Φ / \(d_\sigma\) stub from hidden-state graph signatures  

**Guard windows** (from `omega_horizon_formal.md`): \(R \in (0.2, 0.85)\), \(\Omega_c \in (0.15, 0.75)\).

**Primary correlation targets:** \(D_{\mathrm{med}}\), pipeline compliance, task accuracy (from 013).

## Falsifiers

1. Ω_c proxy uncorrelated with 013 primary metrics (F-BW-1).
2. Covariates significant but **not** arm-specific — same under control (F-BW-4).
3. High coherence without ↑ \(S_{\mathrm{fals}}\) — decorative oscillation (F-BW-3).

## Dependencies

- NAMM-2026-013 task battery and rubric  
- Activation logging hook (mechanistic interpretability layer)  
- Reference implementation hints: `anthemium_kuramoto_uat_research.py` (local ANTHEMIUM tree — not in NAMM repo)

## Not run in this session

Implementation deferred; see [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](../../docs/BRAINWAVE_OSCILLATION_HYPOTHESIS.md) §10.

---

Roman Kuznetsov · NAMM research program
