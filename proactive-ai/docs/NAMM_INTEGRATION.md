# PROACTIVE AI ↔ NAMM Integration

**Status:** v0.1 integration path (documentation + scaffold)  
**Author:** Roman Kuznetsov — [anthemium.tech](https://anthemium.tech) · [X @AGIminister](https://x.com/AGIminister)

---

## Relationship

| Program | Role | Repository |
|---------|------|------------|
| **Anthemium** | AGI cognitive frame — search topology, novelty selection, frame escalation | [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto) |
| **NAMM** | Verification-first machine-native math discovery (Protocol v2, certificates) | [errorlogy/namm-experiments](https://github.com/errorlogy/namm-experiments) |
| **PROACTIVE AI** | Endogenous initiative architecture — drives, goal genesis, contact/action governance | this repository |

PROACTIVE AI and NAMM are sibling research programs under the Anthemium lineage:

- **NAMM** tests whether machine-native artifacts certify mathematical structure before compact human projection exists.
- **PROACTIVE AI** tests whether an agent can form **endogenous motives** (P4–P5) and initiate bounded epistemic contact without a current user prompt.

Shared principles: falsifiable gates, causal traces, rejection logging, dual-controller governance, and experiment manifests.

See NAMM: [`docs/ANTHEMIUM_NAMM_SYNERGY.md`](https://github.com/errorlogy/namm-experiments/blob/main/docs/ANTHEMIUM_NAMM_SYNERGY.md).

---

## Development setup

### Option A — Side-by-side clone (recommended for now)

```powershell
# PROACTIVE AI (this repo)
cd c:\Users\Public\PROACTIVE_AI

# NAMM (sibling directory)
git clone https://github.com/errorlogy/namm-experiments.git ..\namm-experiments
cd ..\namm-experiments
python -m pip install -e ".[dev,nd]"
python -m pytest tests/ -v
```

### Option B — Git remote in PROACTIVE AI

If this directory is initialized as a git repository:

```powershell
cd c:\Users\Public\PROACTIVE_AI
git remote add namm https://github.com/errorlogy/namm-experiments.git
git fetch namm main
```

Use `git subtree` or `git submodule` only when code sharing is required — not needed at v0.1 (spec-only).

### Option C — Submodule (when shared schemas land)

```powershell
git submodule add https://github.com/errorlogy/namm-experiments.git vendor/namm-experiments
```

---

## Folder alignment

PROACTIVE AI adopts NAMM-compatible conventions where experiments are first-class:

```text
PROACTIVE_AI/
├── docs/                          # Architecture + integration (this file)
├── schemas/                       # Typed contracts (observation, motivation, …)
├── experiments/                   # PAI-EI-* experiment manifests (NAMM-style IDs)
│   └── PAI-EI-E0-001/
│       ├── config.yaml
│       ├── README.md
│       └── EXPERIMENT_REPORT.md
├── harnesses/                     # Component harnesses (see spec §18)
├── evals/                         # PAI-EI benchmark suites
└── services/                      # Future implementation (MVP-0+)
```

NAMM reference layout:

```text
namm-experiments/
├── src/namm/                      # Core library + CLI
├── experiments/NAMM-2026-NNN/     # Per-experiment config + reports
├── schemas/                       # Protocol v2 gates
├── prompts/                       # Discovery protocol prompts
└── docs/                          # Protocol, vision, synergy docs
```

**ID convention:** PROACTIVE AI experiments use prefix `PAI-EI-` (Endogenous Initiative); NAMM uses `NAMM-YYYY-NNN`. Both follow `config.yaml` + `EXPERIMENT_REPORT.md` pattern.

---

## Cross-program experiment hooks

| PROACTIVE AI artifact | NAMM analogue | Integration point |
|----------------------|---------------|-------------------|
| `motivation_signal` (§10.2) | drive / research question | Epistemic curiosity → NAMM domain queue |
| `initiative_proposal` (§10.3) | experiment candidate | Internal experiment governor → `namm.cli run-experiment` |
| `causal_trace_ref` | `certificate.json` lineage | Audit plane links PAI episode → NAMM certificate |
| `experiment manifest` (§23.1) | `experiments/*/config.yaml` | Shared fields: `hypotheses`, `code_version`, `primary_metrics` |
| Contact Governor | Protocol v2 attack checklist | Human-set falsifiability gates before external contact |
| Class mode / session policy (Ring 3) | CCT proto-subject projection \(\pi\) | User directive *operate as K4* → [`docs/COGNITIVE_CLASS_TAXONOMY.md`](../../docs/COGNITIVE_CLASS_TAXONOMY.md) §4.1–4.3 (H-CCT-011–014) |
| `AgentState` \(X_t\) (Ring 2) | CCT 3D class scale proxies | Belief/drive dynamics vs K_AI_μ collapse — H-CCT-014 |

Future MVP-0 may call NAMM as an **internal sandbox experiment** when `proposal.kind == "internal_experiment"` (spec §13.1).

---

## NAMM quick reference

```powershell
# From namm-experiments root
python -m pip install -e ".[dev,nd]"
python -m pytest tests/ -v
python -m namm.cli run-experiment --id NAMM-2026-003
```

Priority experiments (NAMM queue): 003 (P1), 007 (first signal), 002/005/008 (P2).

---

## AMAT loop → EIA governor (interim, 2026-08)

Anti-Median AI Topology (AMAT) tests whether **off-typical phase** ($K_{AI_{nd}}$) is measurable in live LLM geometry when steered by Representation Phase Lock (RPL). Terminology: **typicality / high-density** is primary; geometric median is a named robust proxy only ([`docs/ANTI_MEDIAN_AI_TOPOLOGY.md`](../../docs/ANTI_MEDIAN_AI_TOPOLOGY.md) §0).

| NAMM experiment | Certificate (interim) | EIA mapping |
|-----------------|----------------------|-------------|
| **037** cusp / relative β₁ onset | `CUSP_EVIDENCE` | **Initiative dose gate** — onset vs μ-baseline at same $T$, not absolute β₁≥1 (037 blocker lesson) |
| **038** Fisher geodesic κ | `CURVATURE_EVIDENCE` | **Trajectory monitor** — lock path curvature > μ; good runtime scalar for antigravity restart |
| **039** layer-wise fractal $d_f$ | `FRACTAL_EVIDENCE` (0.5B agg.) / `FRACTAL_PILOT` (cells) | **Layer profile** — nd-phase non-integer gap; per-layer, not pooled |
| **040** Lyapunov λ₁ | `CHAOS_PARTIAL` | **Not** primary nd-signature — both policies compressive; do not use λ₁>0 alone for contact trigger |
| **041** attention H¹ proxy | `H1_PARTIAL` | **Weak** head-disagreement lift; sign ok, below pilot threshold — not sole governor input |
| **042–045** pooled $D_{eff}$ | collapse / skipped | **Do not use pooled D_eff** as runtime gate for proactive contact |

**EIA recommendations (Ring 2–3):**

1. **Contact Governor** — prefer **relative / calibrated gates** (033-style null + 037-style μ-baseline), not fixed absolute topology thresholds.
2. **Antigravity restart** — trigger on κ rise + fractal non-integer gap + $d(h(y), B_*)$ lift, not $D_{eff}$ or Rosenstein λ₁ alone.
3. **Proactive risk** — initiative that stays in $K_{AI_\mu}$ looks safe but epistemically collapsed; initiative in $K_{AI_{nd}}$ needs certificate-backed trace before external contact (spec §13, Contact Governor).
4. **Runtime stack** — κ + relative cusp onset + typicality distance; **defer D_eff and Rosenstein λ₁** until per-layer protocol matures (039 path).

See also: [`docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](../../docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md), RPL [`data/prompts/k_ai_nd_phase_lock.v1.json`](../../data/prompts/k_ai_nd_phase_lock.v1.json).


---

## Links

- NAMM repository: https://github.com/errorlogy/namm-experiments
- NAMM Protocol v2: https://github.com/errorlogy/namm-experiments/blob/main/docs/PROTOCOL_V2.md
- PROACTIVE AI architecture: [`PROACTIVE_AI_Endogenous_Initiative_Architecture_EN_v0.1.md`](../PROACTIVE_AI_Endogenous_Initiative_Architecture_EN_v0.1.md)
