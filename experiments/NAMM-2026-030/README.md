# NAMM-2026-030 — AMAT / RPL: K_AI_nd JSON phase-lock

**Domain:** `anti_median_ai_topology` (CCT Axis B labels only)  
**Terminology:** compact phase = **typicality / high-density** basin \(B_*\) (barycenter). Metric `d_med` is a **legacy name** for distance from that location; geometric median only if an experiment names \(B_{\mathrm{gmed}}\). See [`ANTI_MEDIAN_AI_TOPOLOGY.md`](../../docs/ANTI_MEDIAN_AI_TOPOLOGY.md) **§0**.  
**Prompt:** [`data/prompts/k_ai_nd_phase_lock.v1.json`](../../data/prompts/k_ai_nd_phase_lock.v1.json)  
**Schema:** [`schemas/k_ai_nd_phase_lock.json`](../../schemas/k_ai_nd_phase_lock.json)  
**Hypotheses:** H-AMAT-001/003/004, H-CCT-001B, H-CCT-013, H-CCT-020, H-CCT-021

## Design

Two synthetic embedding policies, same seeds:

| Policy | Meaning |
|--------|---------|
| `K_AI_mu` | typicality / high-density attractor (no phase lock) |
| `lock_reassert` | apply JSON spec as steering each turn |
| `lock_decay` | apply once then decay toward \(B_*\) (code: \(B_{\mathrm{med}}\) as typicality location) |

This is an **in-silico proxy** of LLM embedding-level phase, not a live API call. The JSON `rendered_system_prompt` is the artifact to load as a real system prompt; the sweep tests whether the **gates encoded in that JSON** separate μ vs nd geometry.

## Run

```bash
namm sci-flow run --experiment NAMM-2026-030
python experiments/NAMM-2026-030/run_experiment.py
```

**Live API pilot** (real embeddings, optional chat):

```bash
namm llm status
namm llm probe --skip-chat --embed-provider openai   # or gemini, openrouter, jina
namm llm probe --embed-provider openai --chat-provider groq   # full μ vs RPL completions
```

See [`docs/LLM_PROVIDERS.md`](../../docs/LLM_PROVIDERS.md). Keys: `.env.local` or `C:\ai_models\mas\research\.env`.

Default config enables **loop mode**: grid `gain × decay × n_turns` (45 cells × 10 seeds).

## Results — loop grid (45 cells)

Grid: gain ∈ {0.35, 0.55, 0.75, 0.85, 1.0} × decay ∈ {0.35, 0.55, 0.80} × turns ∈ {3, 6, 12}.

| Metric | Value |
|--------|-------|
| cells | **45** |
| mean lift \(d_{\mathrm{lock}}-d_{\mathrm{\mu}}\) | **1.431** |
| min / max lift | 1.039 / **1.508** |
| mean persistence gap (reassert − decay) | **1.364** |
| H-CCT-020 cell fraction | **1.0** |
| H-CCT-021 cell fraction | **1.0** |
| best cell | gain=**1.0**, decay=0.35, turns=6, \(d_{\mathrm{med}}\)=1.589 |
| prompt vs median-helpful | 0.642 |

**H-CCT-020:** lift > 0.5 on every cell — even weak gain 0.35 still leaves the median attractor.  
**H-CCT-021:** without per-turn reassert, decay returns near μ on every cell (persistence_gap ≈ 1.36). Stronger gain helps; **reassert is mandatory** for phase lock.

Single-point baseline (gain=0.85, turns=6) remains in the table below for comparison.

## Results (single cell, 10 seeds)

| Metric | μ baseline | lock + reassert | lock decay |
|--------|------------|-----------------|------------|
| mean \(d_{\mathrm{med}}\) | 0.082 | **1.574** | 0.057 |
| gate pass fraction | 0.0 | **0.5** | 0.0 |

| Hypothesis | Verdict |
|------------|---------|
| H-CCT-001B | supported |
| H-CCT-013 | supported |
| H-CCT-020 | supported (100% of loop cells) |
| H-CCT-021 | supported (100% of loop cells) |
| Certificate | PARTIAL_EVIDENCE — embedding proxy, not live LLM API |
