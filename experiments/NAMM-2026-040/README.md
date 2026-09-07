# NAMM-2026-040 — Multi-Session Lyapunov Proxy + TDA (Strange Attractor Detection)

**One-liner:** Estimate Lyapunov exponent proxy across multi-session nd-phase trajectories; combine with TDA to test positive λ₁ and non-trivial topology vs μ-phase fixed-point.

**Hypothesis:** H-AMAT-009 — nd-phase is a chaotic attractor with λ₁>0; μ-phase is periodic/fixed-point.

**Status:** live (v2 expanded)

**Domain:** `anti_median_ai_topology`

**Run:**
```bash
python experiments/NAMM-2026-040/run_experiment.py
namm sci-flow run NAMM-2026-040
```

## Result (v2b-rosenstein)

- Model: Qwen2.5-0.5B-Instruct CPU
- Grid: 2 prompts × 3 sessions × 8 turns × max_new_tokens=24
- Protocol: \mat-lyapunov-multisession-v2b-rosenstein- mean_lift_lambda1 (pair) ≈ **+0.030**; lock_pos=2, mu_pos=2
- Rosenstein: **finite** (mean_μ ≈ −0.23, mean_lock ≈ −0.26, lift_ros ≈ −0.025)
- Certificate: **\CHAOS_PARTIAL\** (lock λ₁>0 on pair; not lock_pos>mu_pos)
- H-AMAT-009 support: false
- Lean pilot archived: \rtifacts/summary_lean.json- Expanded artifacts: \rtifacts/summary.json\, \rtifacts/expanded/