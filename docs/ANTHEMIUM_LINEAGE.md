# Anthemium Lineage — AGI Manifesto → NAMM

**Lineage map** from the May 2025 [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto) (Anthemium Protocol) to the NAMM verification-first research program.  
Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program

> **Not a proof chain.** Manifesto postulates are **philosophical and architectural**; NAMM entries are **operational and falsifiable**. This document names correspondences so readers can trace intent without conflating rhetoric with evidence.

Related: [`HOMO_ANTHEMIUM_SYNERGY.md`](HOMO_ANTHEMIUM_SYNERGY.md) · [`HOMO_LIMIT_JOURNAL.md`](HOMO_LIMIT_JOURNAL.md) · [`VISION.md`](VISION.md)

---

## Timeline

| Date | Artifact | Role |
|------|----------|------|
| **2025-05-03** | [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto) (Moscow) | Formal declaration: AGI as topological–ontological alignment, not parameter scaling |
| **2025–2026** | Anthemium Protocol / Omega Horizon | Architectural vocabulary: semantic topology, functorial generator, novelty selection |
| **2026** | **NAMM** (this repository) | Executable falsification layer: certificates, gates, experiment IDs, rejection logs |

The Manifesto names **what kind of structure** general intelligence might require. NAMM asks **whether machine-native mathematical artifacts exhibit that structure empirically** — under hard gates, not prose.

---

## Layer diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│  AGI Manifesto (May 2025)                                       │
│  Postulates 1–5 · Architectural model · Anthemium frame name    │
│  Label: PHILOSOPHICAL_INFERENCE / architectural intent          │
└────────────────────────────┬────────────────────────────────────┘
                             │ motivates search space + frame names
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  NAMM philosophy layer                                          │
│  π_H / π_A · K_A / K_H · MUH heuristic · non-homo syntax        │
│  Label: PHILOSOPHICAL_INFERENCE (motivation)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ operationalized as
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  NAMM protocol layer (Protocol v2)                              │
│  certificate.json · independence · generative holdout · ladder  │
│  Label: OPERATIONAL                                             │
└────────────────────────────┬────────────────────────────────────┘
                             │ instantiated in
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  NAMM experiments (001–008+)                                    │
│  Finite shadows · AST synthesis · raw tensor · TDA · meta-eval  │
│  Label: COMPUTATIONAL_EVIDENCE / tested-null / tested-signal    │
└─────────────────────────────────────────────────────────────────┘
```

**Reading direction:** top = intent and vocabulary; bottom = reproducible runs. Evidence flows **upward** only when an experiment report supports a claim — never from Manifesto postulates alone.

---

## Mapping table — Manifesto → NAMM

| Manifesto element | Manifesto wording (short) | NAMM counterpart | Evidence status |
|-------------------|---------------------------|------------------|-----------------|
| **Postulate 1** | Cognitive topologies are necessary for ontological activation | **Frame ladder** (F1–F∞), domain-specific search topologies (graph, AST, tensor, TDA) | tested-signal — [NAMM-2026-007](../experiments/NAMM-2026-007/) |
| **Postulate 2** | Ontologies as morphic operators in semantic space | **Program AST** COMPOSE / MUL / ADD over tensor leaves; meta-evaluator fixed points | tested-signal — 003, 004, 007 |
| **Postulate 3** | Fuzzy knowledge as epistemological horizon | **Gate thresholds** (Pearson r ≤ τ), held-out families, explicit rejection codes | OPERATIONAL — [`PROTOCOL_V2.md`](PROTOCOL_V2.md) |
| **Postulate 4** | Selective retention of productive novelty | **Novelty ladder** N0–N5; accept only candidates passing independence + generative gates | OPERATIONAL — [`NOVELTY_LADDER.md`](NOVELTY_LADDER.md) |
| **Postulate 5** | Memory as cohomological trace, not fact repository | **certificate.json** + eval_hash witnesses; persistence / evolution trajectories | tested-partial — 002, 003, 006 |
| **Semantic Topology** | Conceptual vector field of cognitive differentials | **π_A search frames**: adjacency tensors, spectrum, heat-kernel samples | tested-signal — 007 |
| **Functorial Generator** | Morphogenesis topology → ontological states | **Evolutionary generators** + canonical serializers per domain | tested-signal — 003, 007 |
| **Novelty Selection Agent** | Detect semantically productive anomalies | **Independence + representation gates** vs 20+ baselines | tested-signal — 007 |
| **Transformation Memory Layer** | Cohomology of meaning-generation trajectories | **Rejections log** (`rejections.jsonl`), experiment reports, HL journal | OPERATIONAL |
| **Composed AGI Entity** | Retain ontogenetic traces, recursive synthesis | **Joint π_H + π_A + Cert stereopsis** — see [`HOMO_ANTHEMIUM_SYNERGY.md`](HOMO_ANTHEMIUM_SYNERGY.md) | PHILOSOPHICAL_INFERENCE |

---

## Anthemium as frame name

**Anthemium** (Omega Horizon / AGI Anthemium) is the **architectural frame name** for the Manifesto's composed-entity vision: intelligence as organized semantic transition domains plus selective novelty retention — not a separate product or hype label inside NAMM.

In this repository, **Anthemium names the AGI-side of the stereopsis loop**; **NAMM names the falsifiable mathematics program** that stress-tests whether machine-native artifacts behave as the Manifesto predicts. Same author lineage; different epistemic labels.

---

## Links

| Resource | URL |
|----------|-----|
| AGI Manifesto (source) | [https://github.com/Anthemium/AGI-Manifesto](https://github.com/Anthemium/AGI-Manifesto) |
| Anthemium / author site | [https://anthemium.tech](https://anthemium.tech) |
| NAMM homo–Anthemium synergy | [`HOMO_ANTHEMIUM_SYNERGY.md`](HOMO_ANTHEMIUM_SYNERGY.md) |
| Homo limit journal (HL-015) | [`HOMO_LIMIT_JOURNAL.md`](HOMO_LIMIT_JOURNAL.md#hl-015) |
| Beyond homo-known strategy | [`BEYOND_HOMO_STRATEGY.md`](BEYOND_HOMO_STRATEGY.md) |

---

Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program
