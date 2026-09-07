# PROACTIVE AI × NAMM Integration

**Author:** Roman Kuznetsov · [Anthemium](https://anthemium.tech) · [NAMM research program](https://github.com/errorlogy/namm-experiments)

Related: [`ANTHEMIUM_NAMM_SYNERGY.md`](../ANTHEMIUM_NAMM_SYNERGY.md) · [`proactive-ai/README.md`](../../proactive-ai/README.md)

---

## What Is NAMM?

**NAMM** (Non-Anthropic Mathematics Mode) is a verification-first research program at `c:\Users\Public\NAMM` (remote: `https://github.com/errorlogy/namm-experiments.git`).

It tests whether machine-native artifacts can certify mathematical structure before compact human projection exists — via certificates, independence gates, and generative holdout under Protocol v2.

## What Is PROACTIVE AI?

**PROACTIVE AI** is a research platform for AI systems with **endogenous initiative** (P4–P5 proactivity): internal motives that produce questions and bounded actions without a current human request, with causal trace and dual-controller governance.

## Why Integrate?

Both programs share the **Anthemium** cognitive frame (AGI Manifesto lineage):

| Leg | Program | Focus |
|---|---|---|
| Cognitive frame | Anthemium | Search topology, novelty, frame escalation |
| Verification instrument | NAMM | Certificate-gated mathematical discovery |
| Agency instrument | PROACTIVE AI | Endogenous initiative, contact/action governance |

PROACTIVE AI MVP-0 (digital-only endogenous questioner) can reuse NAMM infrastructure:

- Python package layout (`src/namm/` pattern → future `src/proactive_ai/`)
- Experiment manifests and reproducibility discipline
- CI (pytest, smoke runs)
- Research governance (falsifiability gates, negative results)

---

## Repository Layout

**Canonical repo (planned):** [`errorlogy/eia`](https://github.com/errorlogy/eia) — Endogenous Initiative Architecture (EIA)

Until `errorlogy/eia` is published, bootstrap from `c:\Users\Public\PROACTIVE_AI` or this mirror:

```text
namm-experiments/
├── src/namm/              # NAMM core library
├── experiments/           # NAMM-2026-00x runs
├── docs/
│   ├── ANTHEMIUM_NAMM_SYNERGY.md
│   └── proactive-ai/
│       └── INTEGRATION.md   # this file
└── proactive-ai/          # EIA spec mirror (deprecated as implementation root)
    ├── README.md
    ├── docs/IMPLEMENTATION_PLAN.md
    ├── PROACTIVE_AI_Endogenous_Initiative_Architecture_EN_v0.1.md
    ├── PROACTIVE_AI_Endogenous_Initiative_Architecture_RU_v0.1.md
    ├── .env.example
    └── .gitignore
```

Standalone workspace: `c:\Users\Public\PROACTIVE_AI`

---

## Development Workflow

1. **Primary work** in `NAMM/proactive-ai/` (or sync from `PROACTIVE_AI` workspace).
2. **Architecture changes** update both EN and RU specs; version bump in filename when breaking.
3. **Implementation** (MVP-0+) will add `src/proactive_ai/` at NAMM root or under `proactive-ai/services/` per Section 25 of the architecture spec.
4. **Experiments** follow NAMM-style manifests: `experiments/PAI-E0-001/` with `experiment.yaml`, traces, and results.

### Sync from standalone folder

```powershell
Copy-Item -Recurse -Force "c:\Users\Public\PROACTIVE_AI\*" "c:\Users\Public\NAMM\proactive-ai\"
```

### Git (NAMM repository)

```bash
cd c:\Users\Public\NAMM
git status
git add proactive-ai/ docs/proactive-ai/
git commit -m "Update PROACTIVE AI architecture and integration docs"
git push origin HEAD
```

Do **not** force-push. NAMM currently tracks `origin` at `errorlogy/namm-experiments`.

---

## Roadmap Alignment

| PROACTIVE AI phase | NAMM synergy |
|---|---|
| R0–R1 (definitions, simulator) | Reuse experiment harness patterns from NAMM-2026-004 (meta-evaluator) |
| R2–R4 (drives, EOI benchmark) | PAI-EI benchmark as new experiment track |
| R5+ (security, sensors) | NAMM certificate/provenance patterns → causal trace audit |

---

## Next Steps

1. Commit `proactive-ai/` and `docs/proactive-ai/` to NAMM (user push with credentials).
2. Scaffold MVP-0: `simulator/`, `drive-engine/`, `contact-governor/` under `proactive-ai/`.
3. Add `experiments/PAI-E0-001/` with Twin World Test from architecture Section 31.
4. Extend NAMM CI to run proactive-ai tests when `src/proactive_ai/` appears.

---

## Author

**Roman Kuznetsov** — [anthemium.tech](https://anthemium.tech) · [X @AGIminister](https://x.com/AGIminister)
