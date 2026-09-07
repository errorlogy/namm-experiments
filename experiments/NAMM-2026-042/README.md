# NAMM-2026-042 · amat-activation-tda-1.5B

**Status:** live  
**Branch:** AMAT  
**Hypotheses:** H-AMAT-004, H-CCT-020, H-CCT-021  
**Protocol:** amat-activation-tda-1.5B-v1  

## Motivation

Experiments 035 and 036 on Qwen2.5-0.5B confirmed β₁ lift (two-phase structure in
activation space) but found D\_eff = 0 across all tested pca\_dims. Root cause: the
0.5B model's hidden geometry is too isotropic — after PCA both μ and lock\_reassert
point clouds collapse to the same effective rank, yielding D\_eff lift = 0.

**Hypothesis for 042:** a ≥1.5B model with a richer, more anisotropic hidden space
will produce D\_eff > 1 for the lock\_reassert policy but not for μ, resolving D\_eff
separation and upgrading the certificate from `ACTIVATION_PILOT` to `D_EFF_RESOLVED`.

## Design

| Parameter | Value |
|-----------|-------|
| Model candidates | Qwen2.5-1.5B-Instruct → 0.5B-Instruct → Llama-3.2-1B |
| last\_n\_layers | 4 (best from 036) |
| pca\_dims | 8 (best from 036) |
| n\_turns | 3, 6 |
| prompts | 3 focused (consensus, chimera, cognitive capitalism) |
| policies | μ (median\_helpful), lock\_reassert (RPL rendered\_system\_prompt) |
| total cells | 3 prompts × 2 n\_turns = 6 cells per policy |

## Certificate tiers

| Tier | Condition |
|------|-----------|
| `D_EFF_RESOLVED` | mean\_lift\_d\_eff > 0.3 |
| `ACTIVATION_EVIDENCE` | β₁ AND D\_eff both separate |
| `ACTIVATION_PILOT` | β₁ only (as in 035/036) |
| `NULL` | no separation |

## Artifacts

- `artifacts/summary.json` — full payload with certificate, per-cell metrics, model comparison
- `artifacts/full_activation_tda.json` — raw cell data for both n\_turns sweeps
- `run.log` — human-readable run log

## Comparison table (035/036 vs 042)

See `artifacts/summary.json` → `model_comparison` field.

## Relation to prior experiments

- **035:** β₁ lift live on 0.5B CPU; D\_eff=0 (rank collapse artifact)
- **036:** PCA sweep confirms D\_eff collapse at all pca\_dims for 0.5B
- **042 (this):** same protocol on ≥1.5B → expect D\_eff separation
