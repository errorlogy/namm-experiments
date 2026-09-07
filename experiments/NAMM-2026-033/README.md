# NAMM-2026-033 — AMAT gate calibration (planned)

**Protocol:** `amat-gate-calibration-v1`  
**Prior:** 030 (synthetic gates), 031/032 (live lift without absolute gate pass)

Recalibrate `d_med` gates using μ-policy null distribution on live embeddings; compare percentile / z-score / lift-ratio vs legacy `d_med_min: 1.2`.

**Status:** implemented — `run_033` wired in sci-flow; run via `python experiments/NAMM-2026-033/run_experiment.py`.
See AMAT loop roadmap (033→034→035 sequence): gate calibration → multi-embedder → activation TDA.
