# NAMM-2026-009 — Experiment Report

**Domain:** configuration shadow (`config_shadow`)  
**Date:** 2026-08-11  
**Seed:** 2026009  
**Frame:** F3h — 11D moduli / 4D compactification shadow (ND config-space)  
**Status:** **50 candidates accepted** — **tested-signal**

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **50** |
| Rejections | **0** |
| Vacua scanned | **59,049** (11D, moduli ∈ {-1,0,1}) |
| Ambiguous 4D shadows (fiber ≥ 2) | **81** |
| Max fiber size | **729** |
| Representation gate | K_A/K_H ≥ 2.0 |

## Best candidate

**ID:** `vac-012e1fe1`  
**11D moduli:** `[1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]`  
**4D shadow κ(m):** `[1, 1, -1, -1]`  
**Fiber size:** **729** (729 distinct 11D vacua share this 4D shadow)  
**Fiber index:** 492  
**Stability:** Σmᵢ² = 11.0  
**Novelty:** **N2**  
**K_A/K_H proxy:** gzip **149 B** / projection **≈16 tokens** → ratio **≈9.3**  
**Certificate:** `artifacts/certificate.json`

## Research question

Can finite enumeration of 11-parameter moduli vacua find witnesses where compactification κ (first 4 moduli → 4D effective theory) is **non-injective**, with compression asymmetry K_A/K_H ≥ 2 between full certificate and 4D-only human projection?

## Result

**Yes.** All 50 top ambiguous vacua pass gates. The best witness demonstrates **HL-004 compactification loss** operationally: human π_H sees only the 4D shadow `[1,1,-1,-1]`, while the certificate preserves the full 11D moduli vector and records **fiber_size = 729**.

This is **COMPUTATIONAL_EVIDENCE** for non-anthropic configuration objects — not a physical M-theory or Calabi–Yau result.

## Honest assessment

**What worked**

- Explicit κ map (first 4 moduli) with measurable fiber degeneracy.
- Large compression gap: certificate gzip 149 B vs ~16-token 4D-only projection.
- 59k admissible vacua enumerated under flux (mod 3) and energy (Σm² ≤ 20) constraints.

**Limitations**

- Moduli range bounded to {-1,0,1}; not a literal 11D supergravity landscape.
- No generative holdout or independence vs named baselines (frame differs from 007 tensor).
- Fiber size ranking selects maximal ambiguity, not physical vacuum selection.

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-009
python -m pytest tests/test_config_shadow.py -q
```

## Strategy link

[`docs/ANTHEMIUM_NAMM_SYNERGY.md`](../../docs/ANTHEMIUM_NAMM_SYNERGY.md) · [`docs/HOMO_LIMIT_JOURNAL.md`](../../docs/HOMO_LIMIT_JOURNAL.md) HL-004

---

Roman Kuznetsov · NAMM research program
