# NAMM-2026-034 — AMAT multi-embedder gate stability (v1)

**Protocol:** `amat-multi-embedder-v1`  
**Prior:** NAMM-2026-033 (single-embedder gate calibration)

Compare calibrated RPL gate stability across embedding providers on **shared live chat completions**:
OpenAI (required), OpenRouter (if key present). Jina skipped without key.

Per embedder: μ-null distribution → P95/z/lift-ratio thresholds → lift & calibrated pass fraction.  
Cross-embedder: Spearman rank correlation of per-cell lift; agreement fraction (≥2 embedders with lift > 0.03).

**Run:** `python experiments/NAMM-2026-034/run_experiment.py`  
**Sci-flow:** `run_034` in `src/namm/sci_flow/handlers.py`

Roadmap: 033 (calibration) → **034** (multi-embedder) → 035 (activation TDA).
