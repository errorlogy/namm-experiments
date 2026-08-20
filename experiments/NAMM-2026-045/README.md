# NAMM-2026-045 — Real Hidden States @ 1.5B (D_eff separation)

**Hypothesis:** H-AMAT-004  
**Protocol:** `amat-activation-tda-v2`  
**Question:** Does D_eff finally resolve on real activations at Qwen2.5-1.5B after 035 (0.5B, β₁↑ D_eff=0) and 043/044 (nomic hybrid NULL)?

## Protocol (044 sweet spot on real HS)

| Parameter | Value |
|---|---|
| Model | `Qwen/Qwen2.5-1.5B-Instruct` (fallback 0.5B) |
| Space | Last-token **hidden states** (not embeddings, not logprobs) |
| Policies | `mu`, `lock_reassert` |
| n_turns | 6 |
| last_n_layers | 4 → 24 points/policy |
| pca_dims | 8 |
| ripser metric | cosine |
| Prompts | 3 focused AMAT prompts |

## Run

```bash
pip install torch transformers accelerate ripser
python experiments/NAMM-2026-045/run_experiment.py
namm sci-flow run NAMM-2026-045
```

## Certificate tiers (035/043 style)

| Tier | Condition |
|---|---|
| `D_EFF_RESOLVED` | `mean_lift_d_eff > 0.3` |
| `HYBRID_EVIDENCE` | `β₁ lift > 0.05` AND `D_eff lift > 0.3` |
| `HYBRID_PILOT` | either lift > threshold (0.05 / 0.1) |
| `NULL` | else |

## Cross-experiment comparison

| Exp | Space | Model | n_turns | lift β₁ | lift D_eff | cert |
|---|---|---|---|---|---|---|
| 035 | real HS | Qwen 0.5B | 3 | +0.78 | 0.0 | LIVE_EVIDENCE |
| 044 | nomic hybrid | llama3.2+nomic | 6 | 0.0 | +0.33* | NULL |
| **045** | real HS | Qwen 1.5B | 6 | *run* | *run* | *run* |

\*044 n=6 sweet spot only; aggregate cert NULL.

## Artifacts

- `artifacts/summary.json` — metrics, certificate, comparison table
- `artifacts/full_activation_tda.json` — per-prompt batches
- `artifacts/activation_cells.jsonl` — streaming cells
- `run.log` — execution summary
