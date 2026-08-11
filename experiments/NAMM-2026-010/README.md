# NAMM-2026-010 — κ-Projection Sensitivity (AMFW extension)

**Domain:** `config_shadow` (F3h extension)  
**Parent:** [NAMM-2026-009](../NAMM-2026-009/) · AMFW-012e / `vac-012e1fe1`  
**Epistemic label:** `COMPUTATIONAL_EVIDENCE` only

## Research question

Does compactification ambiguity depend materially on the choice of κ map? Sweep four κ modes at fixed 11D moduli grid and compare max fiber size and shadow-class counts to the 009 baseline (`first_4`).

## κ modes

| Mode | Definition |
|------|------------|
| `first_4` | κ(m) = (m₁,…,m₄) — 009 baseline |
| `last_4` | κ(m) = (m₈,…,m₁₁) |
| `middle_4` | κ(m) = central 4 coordinates |
| `flux_blocks_4` | block sums mod 3 → 4D |

## Run

```bash
python -m namm.cli run-experiment --id NAMM-2026-010
python -m pytest tests/test_config_shadow.py -q
```

## Open-problem link

Graceful Tree Conjecture ([NAMM-2026-008](../NAMM-2026-008/)) serves as **T0 calibration**; AMFW fibers are the **beyond-anthropic target** (see `docs/AMFW_11D_HYPOTHESIS_RESEARCH.md`).

---

Roman Kuznetsov · NAMM research program
