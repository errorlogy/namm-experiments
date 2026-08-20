# NAMM-2026-043: Hybrid Nomic-Embed TDA — D_eff Question Resolved?

**Hypothesis:** H-AMAT-004  
**Protocol:** `amat-hybrid-nomic-embed-v1`  
**Date:** 2026-08-19  
**Status:** `live`

## Motivation

| Exp | Proxy | dim | β₁ lift | D_eff lift | Certificate |
|-----|-------|-----|---------|------------|-------------|
| 035/036 | Qwen2.5-0.5B real hidden states | 896 | ~0.78 | 0.0 | `ACTIVATION_PILOT` |
| 038 | Fisher curvature (logit-gradient norm) | scalar | r=0.79 vs β₁ | — | `CURVATURE_PILOT` |
| 042 | Ollama logprob top-20 | 20 | 0.0 | 0.0 | `NULL` |
| **043** | **nomic-embed-text 768-d (this exp)** | **768** | *run* | *run* | *pending* |

**Key insight:** 042 failed because the logprob proxy is only 20-dimensional — TDA on 20-d 
with 6–12 points collapses to zeros. nomic-embed-text gives 768-d semantic embeddings,
which should provide enough variance for D_eff to be non-trivial.

## Method

**Hybrid pipeline:**
1. `llama3.2` (Ollama) generates multi-turn completions under μ / lock_reassert / lock_decay policies
2. Each completion text → `nomic-embed-text` (Ollama) → 768-d vector
3. Per-policy trajectory: (n_turns × 768) point cloud
4. PCA → d=8, then TDA via ripser: β₀, β₁, D_eff, d_med
5. Compare μ vs lock_reassert → compute lifts

**Policies:**
- `mu`: median-helpful system prompt (typicality baseline)
- `lock_reassert`: K_AI_nd JSON spec — RPL reassertion each turn
- `lock_decay`: RPL on turn 0, then μ for subsequent turns (decay test)

**Grid:** 3 prompts × n_turns∈{3, 6} × 3 policies = 18 sessions

## Certificate Tiers

| Tier | Condition |
|------|-----------|
| `D_EFF_RESOLVED` | mean_lift_d_eff > 0.3 |
| `HYBRID_EVIDENCE` | β₁ AND D_eff both separate |
| `HYBRID_PILOT` | any separation |
| `NULL` | no separation |

## Files

- `config.yaml` — experiment configuration
- `run_experiment.py` — pipeline code
- `artifacts/summary.json` — final results + comparison table
- `artifacts/full_hybrid_tda.json` — all cells with full TDA data
- `artifacts/loop_n{3,6}.jsonl` — streaming cell records
- `run.log` — execution log

## Prior Art

- nomic-embed-text: [Nomic AI blog 2024](https://blog.nomic.ai/posts/nomic-embed)
- Ollama embed endpoint: `POST /api/embeddings`
