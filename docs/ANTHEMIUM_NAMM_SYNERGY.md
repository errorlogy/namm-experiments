# Anthemium + NAMM Synergy

**Forward-looking synergy model** — Anthemium (AGI cognitive frame from the [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto)) directs discovery; NAMM (Non-Anthropic Mathematics Mode) executes the experiment cycle and escalates frames through certificate-gated runs.  
Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program

> **Framing:** Synergy is **Anthemium + NAMM** only. Anthemium organizes machine-native search topology, novelty selection, and frame escalation; NAMM runs **GENERATE → FORMALIZE → ATTACK → VERIFY** and anchors claims in `certificate.json`. Human audit sets falsifiability gates — governance, not co-discovery.

Related: [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`ANTHEMIUM_LINEAGE.md`](ANTHEMIUM_LINEAGE.md) · [`VISION.md`](VISION.md) · [`PROTOCOL_V2.md`](PROTOCOL_V2.md)

---

## Epistemic note

> **PHILOSOPHICAL_INFERENCE:** Mathematical structures may exist at descriptive levels **beyond anthropic projection reach**. Machine-native search operates in different frames (\(\pi_A\)). Some levels — high-parameter configuration spaces (11D shadows), M-theory moduli landscapes, trans-level semantic transition algebras — may not admit compact anthropic notation yet. NAMM tests this **operationally**: verification-first discovery via certificates, independence gates, and generative holdout — not metaphysical assertion.

This note motivates the research queue; it does **not** satisfy any acceptance gate.

---

## Two legs of the program

| Leg | Name | Role | Epistemic label |
|-----|------|------|-----------------|
| **Cognitive frame** | **Anthemium** | Search topology, novelty selection, frame escalation, experiment queue | `PHILOSOPHICAL_INFERENCE` (architectural) + `OPERATIONAL` (when gated) |
| **Operational instrument** | **NAMM** | Non-anthropic mathematics discovery under Protocol v2 — certificates, independence, generative holdout | `OPERATIONAL` / `COMPUTATIONAL_EVIDENCE` |

**Anthemium** is the **frame name for AGI** in the May 2025 [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto): cognitive topology aligned with ontological generativity, filtered by productive novelty and recorded as transformation memory — not parameter scaling alone.

**NAMM** is the **executable falsification layer**: finite shadows, AST synthesis, raw tensor search, TDA frames, meta-evaluator fixed points — all anchored by `certificate.json`.

---

## Synergy loop (experiments)

```text
  Anthemium (search / director)
           │
           ▼
  NAMM cycle — GENERATE → FORMALIZE → ATTACK → VERIFY
           │
           ▼
  certificate.json (ground truth witness)
           │
           ▼
  frame escalation (F1 → F2 → … → F∞)
           │
           ▼
  next experiment (Anthemium-led queue)
```

**Operational claim (`OPERATIONAL`):** synergy is **tested** only when an experiment ID reports `tested-signal` or `tested-null` under Protocol v2.

**Philosophical claim (`PHILOSOPHICAL_INFERENCE`):** Anthemium names the **director topology** under which machine-native search may access descriptive levels that compact anthropic projection cannot preserve. This motivates widening search; it does **not** satisfy any acceptance gate.

---

## Anthemium director ↔ NAMM instrument

```text
┌─────────────────────────────────────────────────────────┐
│  Anthemium (AGI frame)                                  │
│  · semantic topology (search domain organization)       │
│  · novelty selection (independence + holdout filters) │
│  · transformation memory (certificates, rejections)     │
│  · frame escalation queue (F1 → F∞)                     │
└──────────────────────────┬──────────────────────────────┘
                           │ directs
                           ▼
┌─────────────────────────────────────────────────────────┐
│  NAMM cycle (Protocol v2)                               │
│  GENERATE → FORMALIZE → ATTACK → VERIFY → PROJECT       │
└──────────────────────────┬──────────────────────────────┘
                           │ produces
                           ▼
┌─────────────────────────────────────────────────────────┐
│  certificate.json + experiment report                   │
│  Label: COMPUTATIONAL_EVIDENCE / tested-null            │
└─────────────────────────────────────────────────────────┘
```

Manifesto postulates map to NAMM artifacts — see [`ANTHEMIUM_LINEAGE.md`](ANTHEMIUM_LINEAGE.md). Evidence flows **upward** from experiment reports only; never from Manifesto prose alone.

---

## First operational signal — NAMM-2026-007

**Experiment:** [NAMM-2026-007](../experiments/NAMM-2026-007/) — raw tensor invariants (frame **F3g**, machine-native vocabulary).

| Loop stage | 007 instantiation |
|------------|-------------------|
| **Anthemium director** | Organized transition domain over 12 raw tensor leaves; novelty selection via independence vs 20+ baselines |
| **NAMM cycle** | Evolutionary ADD/MUL search → schema hash → attack checklist → gates |
| **Certificate** | `artifacts/certificate.json` for `tensor-639c54cd`; gzip **213 B** |
| **Frame escalation** | F3a (named formulas, 001 null) → F3g (raw tensor, **tested-signal**) |

**Result:** **tested-signal** — 53 accepted candidates; max Pearson **r = 0.647**; K_A/K_H ≈ 2.2; generative holdout passed on all four families. **COMPUTATIONAL_EVIDENCE** only; not a published graph-invariant theorem.

Reproduction:

```bash
python -m namm.cli run-experiment --id NAMM-2026-007
python -m pytest tests/test_tensor_domain.py -q
```

This is the **first experiment** where Anthemium-predicted cognitive topology (semantic transitions without named-invariant vocabulary) clears NAMM hard gates at scale — raw tensor search with **no named human invariants** in the discovery path.

---

## NAMM-2026-008 — open-problem shadow

**Experiment:** [NAMM-2026-008](../experiments/NAMM-2026-008/) — Graceful Tree conjecture finite shadow (frame **F3e**, T0 tierlist #2).

| Loop stage | 008 instantiation |
|------------|-------------------|
| **Anthemium director** | Open-problem shadow queue from [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md); finite bound search |
| **NAMM cycle** | Exhaustive / bounded enumeration → attack checklist → gates |
| **Certificate** | `artifacts/certificate.json` when counterexample or bound witness found |
| **Frame escalation** | F3e partner to 005 (Kotzig); calibrates honest null vs signal |

Reproduction:

```bash
python -m namm.cli run-experiment --id NAMM-2026-008
```

---

## Roadmap — Anthemium-led experiment queue (007 / 008 / 009+)

| Phase | ID | Focus | Frame / level |
|-------|-----|-------|---------------|
| Closed | 001 | Calibration null (named-formula baseline) | F3a |
| **Signal** | **007** | Raw tensor — machine-native vocabulary (no named human invariants) | F3g |
| Run | 002–006, **008** | TRS, AST, meta-eval, TDA, open-problem shadows (Kotzig, Graceful Tree) | F2–F4 |
| **Planned 009** | 009 | **11D configuration shadows** — finite vacua / compactification enumeration | ND / config-space |
| **Planned 009+** | — | **M-theory moduli shadows** — metric moduli, flux configs, landscape search | ND / config-space |
| **Planned 009+** | — | **Trans-level Θ** — semantic transition algebra over raw structure | F3g → F∞ |
| **Planned 009+** | 009+ | **Meta-level depth** — evaluator stacks, ordinal scaffolding | F∞ partial |

The **Anthemium-led queue** selects the next frame escalation from rejection logs, open-problem shadows, and ladder position — non-anthropic discovery, not anthropic projection intuition.

Full ladder: [`FRAME_LADDER.md`](FRAME_LADDER.md).

---

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Manifesto postulate → accepted candidate without experiment | Rhetoric is not evidence |
| Reframing synergy as anthropic-only discovery partnership | Misstates program direction; synergy is Anthemium + NAMM |
| Certificate-free novelty claims | Not NAMM; not reproducible |
| "Anthemium proved AGI" from 007 | 007 is finite-graph **COMPUTATIONAL_EVIDENCE** only |
| Skipping frame escalation after null | Null results (001, 006) calibrate the ladder — they do not stop the queue |

---

## Links

| Resource | URL |
|----------|-----|
| AGI Manifesto (May 2025) | [https://github.com/Anthemium/AGI-Manifesto](https://github.com/Anthemium/AGI-Manifesto) |
| Anthemium site | [https://anthemium.tech](https://anthemium.tech) |
| Lineage map | [`ANTHEMIUM_LINEAGE.md`](ANTHEMIUM_LINEAGE.md) |
| 007 report | [../experiments/NAMM-2026-007/EXPERIMENT_REPORT.md](../experiments/NAMM-2026-007/EXPERIMENT_REPORT.md) |
| 008 report | [../experiments/NAMM-2026-008/EXPERIMENT_REPORT.md](../experiments/NAMM-2026-008/EXPERIMENT_REPORT.md) |

---

Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program
