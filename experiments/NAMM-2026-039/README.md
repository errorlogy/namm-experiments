# NAMM-2026-039 — Layer-Wise TDA + Box-Counting Fractal Dimension Sweep

**One-liner:** Layer-wise TDA and box-counting sweep across transformer layers to detect non-integer fractal dimension in nd-phase hidden-state trajectories.

**Hypothesis:** H-AMAT-008 — Hidden-state trajectories in nd-phase have non-integer box-counting dimension d_f across transformer layers; μ-phase collapses to integer dimension.

**Status:** completed (certificate=FRACTAL_EVIDENCE; H-AMAT-008-a=false)

**Domain:** `anti_median_ai_topology`

**Method:** Extract per-layer hidden states across multi-turn trajectories (μ vs lock_reassert); estimate box-counting fractal dimension d_f per layer; compare mean d_f and non-integer gap (|d_f - round(d_f)|); inspect layer variance profile.

**Dependencies:** `transformers`, `torch`, `numpy` (CPU); `pytest` (tests). No persistent-homology backend required for this experiment.

## Run parameters

- Model: `Qwen/Qwen2.5-0.5B-Instruct` (CPU)
- n_turns: 3
- Policies: `mu` vs `lock_reassert`
- Prompts:
  - chimera synchronization / partial vs full consensus
  - consensus permanently suboptimal
- d_f estimator: box-counting slope of `log N_boxes` vs `log(1/ε)`
- Settings: `pca_dim=3`, `epsilon_range=[0.02, 0.5]`, `n_epsilons=14`, `layer_variance_threshold=0.01`

## Results (from `artifacts/summary.json`)

- mean lift of d_f (lock − mu): **-0.02569** (lock mean d_f is lower)
- mean lift of non-integer gap: **+0.01963** (lock has more non-integer behavior)
- H-AMAT-008-a (mean d_f lock>mu on both prompts): **false**
- H-AMAT-008-b (non-integer gap lock>mu on both prompts): **true**
- H-AMAT-008-c (layer-wise profile non-flat on both prompts): **true**
- Certificate tier: **FRACTAL_EVIDENCE**
- `hypothesis_confirmed`: **false** (because H-AMAT-008-a is false)

### Most informative layers (highest |d_f(lock) − d_f(mu)| mass)

- Layers: **19, 17, 4, 20, 3**

## Russian summary (task #10)

Разделение по **нецелому** измерению найдено: для `lock_reassert` наблюдается устойчиво больший non-integer gap (H-AMAT-008-b=true) и заметная неодномерность профиля по слоям (H-AMAT-008-c=true), что соответствует tier **FRACTAL_EVIDENCE**. При этом разделения по **среднему** d_f (H-AMAT-008-a) нет: средний d_f в lock_reassert оказался ниже, чем в μ-phase, поэтому конъектура H-AMAT-008 целиком **не подтверждена**. Наиболее информативные слои: **19, 17, 4, 20, 3**.
