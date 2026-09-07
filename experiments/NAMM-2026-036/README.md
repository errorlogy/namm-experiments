# NAMM-2026-036 — AMAT Activation TDA v3: PCA-Reduced D_eff

## Motivation

Experiments 035-v1/v2 confirmed beta_1 lift (+0.67→+1.0 mean, chimera +4.0) but
D_eff lift = 0.0 both runs. Root cause: 24 points in 896-d space → only 2 PCs dominate,
making D_eff trivially = 1.0 in both policies (artifact, not signal).

## Fix

Project hidden-state point cloud to PCA d=8 **before** ripser. In reduced space
D_eff should meaningfully separate μ (compact, low-variance) vs lock_reassert
(dispersed, high-variance) trajectories.

## Design

### Sweep (chimera prompt only)
- `pca_dims` ∈ {4, 8, 16}
- `n_turns` ∈ {3, 6, 10}
- 9 cells → select best `pca_dim` by `lift_d_eff`

### Full focused-prompt run (best pca_dim)
- All 3 NAMM focused prompts
- `n_turns` = 6 (established best from 035)

## Certificate Tiers

| Tier | Condition |
|------|-----------|
| ACTIVATION_EVIDENCE | beta_1 AND d_eff both separate |
| D_EFF_PARTIAL | mean_lift_d_eff > 0.5 at best pca_dim |
| ACTIVATION_PILOT | any separation found |

## Model

Qwen2.5-0.5B-Instruct on CPU, last_n_layers=8, max_new_tokens=128

## Artifacts

- `artifacts/sweep_chimera.jsonl` — 9 sweep cells (pca_dims × n_turns)
- `artifacts/focused_loop.jsonl` — 3 focused-prompt cells at best pca_dim
- `artifacts/summary.json` — final certificate + joint 035+036 note
- `artifacts/full_pca_tda.json` — full result blob
