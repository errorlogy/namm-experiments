# NAMM-2026-035 — AMAT Activation TDA (local 7B-8B + ripser)

**Decisive test:** Is AMAT live AI-science on **hidden-state topology**, or only RPL text-embedding engineering?

## Protocol

- **Model:** local causal LM via `transformers` (auto-fallback: Qwen2.5-0.5B → 1.5B → Llama-3.2-1B → 3B)
- **Policies:** `mu` (median helpful system) vs `lock_reassert` (RPL `rendered_system_prompt`)
- **Prompts:** same 3 focused prompts as NAMM-2026-032/033
- **Turns:** `n_turns=3`, zero API cost
- **Point cloud:** last-token hidden states, `turns × last_n_layers` (default 4)
- **Metrics:** `d_med`, `D_eff`, `beta_0/β₁` (ripser if installed, else k-NN proxy)
- **Falsifier:** **F-AMAT-4** — no two-phase structure vs μ controls on activations

## Run

```bash
pip install torch transformers accelerate
pip install ripser  # optional, science extra
python experiments/NAMM-2026-035/run_experiment.py
```

Sci-flow:

```bash
namm sci-flow run NAMM-2026-035
```

## Certificate tiers

| Tier | Condition |
|------|-----------|
| `ACTIVATION_PILOT` | Model loaded, activations extracted |
| `TDA_PARTIAL` | `mean_lift_beta_1 > 0.05` OR `two_phase_fraction ≥ 0.5` |
| `LIVE_EVIDENCE` | F-AMAT-4 **not** triggered + positive `mean_lift_d_med` |

## Artifacts

- `artifacts/summary.json` — certificate, lifts, F-AMAT-4 status
- `artifacts/full_activation_tda.json` — full loop payload
- `artifacts/activation_cells.jsonl` — per-prompt cells (append/resume)

## Hardware notes

If GPU/RAM insufficient, the runner auto-falls back to the smallest model in the candidate list. Document actual `model_id` and `device` in `summary.json`.
