# NAMM-2026-031 — AMAT live loop (LLM API + embeddings)

**Domain:** `anti_median_ai_topology`  
**Protocol:** `amat-live-loop-v1`  
**Synthetic baseline:** NAMM-2026-030 (in-silico)  
**This experiment:** **live** chat completions + embedding typicality metrics

## Design

Grid: **5 prompts × 3 turn counts** × 3 policies:

| Policy | System prompt per turn |
|--------|------------------------|
| `mu` | median-helpful always |
| `lock_reassert` | RPL JSON every turn |
| `lock_decay` | RPL turn 0 only, then median-helpful |

Metrics on **completion embeddings** (not prompt-only):

- \(d(h, B_*)\) — typicality distance (legacy name `d_med`)
- lift = lock − μ
- persistence_gap = lock_reassert − lock_decay

## Run

```bash
namm llm loop --chat-provider groq --embed-provider openai
python experiments/NAMM-2026-031/run_experiment.py
python experiments/run_live_amat_loop.py
```

Requires keys in `.env.local` or `C:\ai_models\mas\research\.env`.

## Certificate tiers

| Tier | Condition |
|------|-----------|
| PROMPT_PILOT | prompt-only (`--skip-chat`) |
| LIVE_PARTIAL | completions embedded, lift>0 on majority cells |
| LIVE_EVIDENCE | H-CCT-020 & H-CCT-021 cell fractions ≥ 0.6 |
