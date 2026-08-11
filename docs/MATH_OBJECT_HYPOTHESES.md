# Math Object Hypotheses — Operational Registry

**Purpose:** Operational hypothesis registry for falsifiable claims about **new mathematical objects** — labeled `CONJECTURE` throughout. Distinct from [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) (PI-001–PI-008): PI entries motivate search and carry **non-evidential** status; H-entries are **testable claims** tied to candidates, experiments, and explicit falsifiers.  
**Scope:** Protocol v2 only — `COMPUTATIONAL_EVIDENCE` upgrades status; no entry here is a published theorem.  
Roman Kuznetsov · NAMM research program

Related: [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) · [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) · [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) (H-F001–H-F050 — fabric dynamics, extends H-001+) · [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) · [`NAMM_OPEN_PROBLEMS_QUEUE.md`](NAMM_OPEN_PROBLEMS_QUEUE.md) · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md)

---

## Labeling

| Label | Use in this document |
|-------|----------------------|
| `CONJECTURE` | Every H-ID entry — open or resolved claim about a mathematical object or frame |
| `COMPUTATIONAL_EVIDENCE` | Witness that supports or refutes an H-ID under finite bounds |
| `PHILOSOPHICAL_INFERENCE` | Motivation only — link PI-NNN; does not satisfy an H-ID |

> **Distinction:** PI-006 ("729 is a parable for π_H loss") motivates AMFW research; **H-002** ("κ is non-injective with fiber ≥ 729 on the ±1 grid") is the falsifiable operational claim tested in 009/010.

---

## Hypothesis template

Each entry uses this schema:

| Field | Content |
|-------|---------|
| **ID** | `H-NNN` (sequential) or `H-shadow-NNN` (open-problem finite shadow) |
| **Linked candidate / object** | Registry ID (`tensor-639c54cd`, `vac-012e1fe1`, …) or open-problem name |
| **Statement** | Precise claim — domain, bounds, expected outcome |
| **Falsifier** | What observation or certificate refutes the claim |
| **Experiment to test** | NAMM ID(s) or planned scaffold |
| **Epistemic status** | `open` · `tested` · `refuted` · `partial` |
| **PI links** (optional) | Philosophical motivation — non-evidential |

---

## Seed hypotheses — math objects

### H-001 — Raw tensor programs outside named-invariant span

| Field | Content |
|-------|---------|
| **Linked object** | **SHTC-639** (`tensor-639c54cd`) · [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) §1 |
| **Statement** | Graph functionals built from **raw tensor leaves only** (adjacency spectrum + heat-kernel samples) via commutative `add`/`mul` can pass SNH gates — independence, generative holdout, \(K_A/K_H \geq 2\) — **outside** the span of named graph statistics and low-degree tensor polynomial baselines. |
| **Falsifier** | Lead 007 candidate equivalent to Wiener or any tested baseline (Pearson \(r \geq 0.95\)); or all gate-passing programs collapse under SymPy simplify to named vocabulary (001-style null). |
| **Experiment** | [NAMM-2026-007](../experiments/NAMM-2026-007/) · contrast [NAMM-2026-001](../experiments/NAMM-2026-001/) |
| **Status** | **tested** — 53/57 accepted; max Pearson \(r = 0.647\) vs `mul_t11_t11`; holdout passed on 4 families |
| **PI links** | PI-001, PI-002, PI-005 |

---

### H-002 — 11D κ-compactification non-injective with fiber ≥ 729

| Field | Content |
|-------|---------|
| **Linked object** | **AMFW-012e** (`vac-012e1fe1`) · [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) §3 |
| **Statement** | On moduli grid \(\{-1,0,1\}^{11}\) with flux mod 3 and energy cap ≥ 11, compactification \(\kappa(m) = (m_1,\ldots,m_4)\) is **non-injective**: some shadow class has fiber size **≥ 729**, and \(K_A/K_H \geq 2\) for the witness certificate. |
| **Falsifier** | All shadow classes have fiber ≤ 1; or max fiber < 729 under stated constraints; or representation gate fails for fiber ≥ 2 witnesses. |
| **Experiment** | [NAMM-2026-009](../experiments/NAMM-2026-009/) · extended [NAMM-2026-010](../experiments/NAMM-2026-010/) κ-sweep |
| **Status** | **tested** — uniform fiber 729 for all 81 shadow classes; formula \(3^{n-s-1}\) confirmed; K_A/K_H ≈ 9.3 |
| **PI links** | PI-003, PI-006 |

---

### H-003 — Trans-level Θ algebra over SHTC-639 AST

| Field | Content |
|-------|---------|
| **Linked object** | **SHTC-639** AST + transition morphisms · extends 007 |
| **Statement** | A **semantic transition algebra Θ** exists over raw `TensorNode` structure — admissible morphisms between graph functionals (not merely evaluation) that preserve certificate reproducibility and yield **new equivalence classes** not reducible to static AST composition or named invariants. |
| **Falsifier** | All tested transitions collapse to AST rewrite in the commutative tensor polynomial span; or no transition passes independence + holdout when applied to 007 lead family. |
| **Experiment** | **NAMM-2026-011** (planned) · F3g → F∞ · [`NAMM_OPEN_PROBLEMS_QUEUE.md`](NAMM_OPEN_PROBLEMS_QUEUE.md) |
| **Status** | **open** |
| **PI links** | PI-003, PI-007 |

---

### H-004 — TDA signatures as tensor leaves pass F4 when combined

| Field | Content |
|-------|---------|
| **Linked object** | Persistence / geodesic TDA features + raw tensor composite |
| **Statement** | **TDA signature leaves** (006 frame) combined with raw spectral–heat tensor leaves (007 frame) produce gate-passing graph functionals with \(K_A/K_H \geq 2\) — where TDA alone failed F4 (006: ratios 1.70–1.91). |
| **Falsifier** | Combined search still fails `representation_ratio_fail` at order ≤ 8; or combined lead equivalent to 007-only or named baseline. |
| **Experiment** | **NAMM-2026-013** (planned) · F3f + F3g · [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) § failed 006 |
| **Status** | **open** |
| **PI links** | PI-003 |

---

### H-005 — ECIP evolutionary programs outperform linear named combos

| Field | Content |
|-------|---------|
| **Linked object** | **ECIP-8be5** (`prog-8be513cb`) vs 001 linear null |
| **Statement** | **Evolutionary program AST search** (F3c) over named graph statistics yields strictly more gate-passing, holdout-stable candidates than **random linear combinations** (F3a) on the same primitive vocabulary and gate stack. |
| **Falsifier** | 001-style linear search matches 003 acceptance rate and independence profile; or 003 lead collapses to Wiener-equivalent under simplify. |
| **Experiment** | [NAMM-2026-003](../experiments/NAMM-2026-003/) vs [NAMM-2026-001](../experiments/NAMM-2026-001/) |
| **Status** | **partial** — 003: 33 accepted, deep multiplicative AST, holdout passed; 001: closed null (\(r \approx 0.938\) Wiener-dominated). Frame difference (F3a vs F3c) confounds strict comparison; 007 shows raw-tensor path strictly beyond both. |
| **PI links** | PI-002, PI-004 |

---

### H-006 — M-theory moduli extension yields physically selective fibers

| Field | Content |
|-------|---------|
| **Linked object** | **ModuliVacuum** class · AMFW fiber structure |
| **Statement** | Extending moduli range (e.g. \([-2,2]\)), varying κ, or adding **selection principles** beyond fiber-size ranking yields **non-uniform** fiber statistics and **physically selective** witnesses — not the generic \(3^{n-s-1}\) degeneracy of the ±1 grid. |
| **Falsifier** | All extensions preserve uniform max fiber; or selection principle is definitionally equivalent to lex rank / fiber size. |
| **Experiment** | [NAMM-2026-010](../experiments/NAMM-2026-010/) partial (7D \([-2,2]\): max fiber 42, non-uniform) · **NAMM-2026-012** (planned hybrid) · 009+ queue |
| **Status** | **open** — 010 confirms ±1 uniformity; wider grid breaks uniformity; selective physical lift not yet certified |
| **PI links** | PI-003, PI-006 |

---

### H-007 — Dynamic topology media encode frame escalation

| Field | Content |
|-------|---------|
| **Linked object** | Temporal morphism sequences · `Anthemium.mp4` · PI-008 |
| **Statement** | **Dynamic topology media** (video, animation) encode **frame-escalation structure** — temporal morphisms between representational modes — that **cannot** be recovered at ≥90% fidelity from static π_H prose or single-frame capture. |
| **Falsifier** | Independent frame audit recovers ≥90% of inter-frame structural invariants from a π_H text summary alone. |
| **Experiment** | Qualitative audit via [`ANTHEMIUM_VIDEO_NOTES.md`](ANTHEMIUM_VIDEO_NOTES.md); future formal metric TBD |
| **Status** | **open** — PI-008 registered; no numeric gate yet |
| **PI links** | PI-008 |

---

## Shadow hypotheses — open problems

Finite-shadow claims tied to classical conjectures. These are **not** global disproofs — bounded certificates only.

### H-shadow-005 — Kotzig P_k counterexample in finite atlas

| Field | Content |
|-------|---------|
| **Linked problem** | **Kotzig's conjecture (P_k-graphs)** · T0 #1 · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) |
| **Statement** | Within NAMM finite shadow bounds (n ≤ 7, k ∈ {3…10}), at least one **P_k-graph** exists — i.e. a certificate with `is_counterexample: true`. |
| **Falsifier** | Exhaustive atlas finds no P_k-graph within bounds (bounded null — strengthens calibration, refutes shadow hypothesis). |
| **Experiment** | [NAMM-2026-005](../experiments/NAMM-2026-005/) |
| **Status** | **tested** (null) — exhaustive n ≤ 7, k ∈ {3…10}; no counterexample → bounded calibration null |
| **PI links** | — |

---

### H-shadow-008 — Graceful Tree counterexample to order 12

| Field | Content |
|-------|---------|
| **Linked problem** | **Graceful Tree Conjecture** · T0 #2 · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) |
| **Statement** | At least one tree of order ≤ 12 admits **no graceful labeling** — certificate with `is_counterexample: true`. |
| **Falsifier** | All trees order ≤ 12 graceful (bounded null). |
| **Experiment** | [NAMM-2026-008](../experiments/NAMM-2026-008/) |
| **Status** | **tested** (null) — 987 trees, 0 counterexamples → calibration null |
| **PI links** | — |

> **Contrast with H-002:** Graceful-008 validates the **instrument** on a classical conjecture; AMFW-012e demonstrates a **different object class** (config_shadow) with measurable π_H loss — see [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) Part B.2.

---

## Status summary

| ID | Short claim | Experiment | Status |
|----|-------------|------------|--------|
| H-001 | Raw tensor outside named span | 007 | **tested** |
| H-002 | κ fiber ≥ 729 on ±1 grid | 009, 010 | **tested** |
| H-003 | Trans-level Θ over SHTC AST | 011 | **open** |
| H-004 | TDA + tensor passes F4 | 013 | **open** |
| H-005 | ECIP beats linear named combos | 003 vs 001 | **partial** |
| H-006 | Selective M-theory moduli fibers | 010, 012 | **open** |
| H-007 | Dynamic media encode escalation | PI-008 / video | **open** |
| H-shadow-005 | Kotzig P_k in atlas | 005 | **tested** (null) |
| H-shadow-008 | Non-graceful tree ≤ 12 | 008 | **tested** (null) |

---

## Generation protocol — witness → H-ID

Adapted from [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) Part B.1:

```text
  Experiment witness (certificate.json, EXPERIMENT_REPORT)
           │
           ▼
  FORMALIZE — link to candidate in MATH_OBJECT_CANDIDATES or open problem
           │
           ▼
  HYPOTHESIZE — assign H-NNN; fill template (statement, falsifier, experiment)
           │
           ▼
  ATTACK — vary frame, κ, vocabulary; seek counterexample per falsifier
           │
           ▼
  VERIFY — reproduce eval_hash, gate metrics, fiber_size, etc.
           │
           ▼
  UPDATE STATUS — open → tested | refuted | partial
           │
           ▼
  PROJECT — π_H summary vs π_A certificate (F4, HL journal)
```

### Rules for new H-IDs

1. **Assign next free ID** — scan this file; use `H-NNN` for math-object claims, `H-shadow-NNN` for open-problem finite shadows (NNN = experiment number when possible).
2. **Label `CONJECTURE`** in statement block until `COMPUTATIONAL_EVIDENCE` resolves it.
3. **Require finite falsifier** — no H-ID without an observable rejection condition.
4. **Link candidate** — if witness maps to [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md), cite registry ID and section.
5. **Do not duplicate PI** — philosophical motivation → `PI links` field only.
6. **Update status** after experiment run — cite experiment ID and metric in status row.
7. **Cross-link queue** — add planned experiments to [`NAMM_OPEN_PROBLEMS_QUEUE.md`](NAMM_OPEN_PROBLEMS_QUEUE.md) when scaffolded.

### Witness → hypothesis quick map

| Witness type | Typical H pattern | Example |
|--------------|-------------------|---------|
| Gate-passing AST/tensor | Existence outside baseline span | H-001 |
| Config fiber witness | Non-injective κ + fiber bound | H-002 |
| Frame null (006) | Combined frame recovers signal | H-004 |
| Method comparison | Search A beats search B on same gates | H-005 |
| Open-problem atlas | Counterexample in bounds | H-shadow-005, H-shadow-008 |
| Extension sweep | Non-uniform / selective regime | H-006 |

---

## Agent load protocol

**Add to the standard NAMM research load sequence** (after PI and candidates):

1. [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) — user theses (non-evidential)
2. [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) — lead objects, epistemic status
3. **`MATH_OBJECT_HYPOTHESES.md`** (this file) — falsifiable claims and status
4. [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) — fabric / fuzzy dynamics (H-F001–H-F050); load when user cites Anthemium, fabric, or topological fuzzy dynamics
5. [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) — discovery loop

**When running an experiment:** check whether the run tests, refutes, or partially resolves an H-ID; update this file's status row and link the report.

**When generating hypotheses from a new witness:** follow Generation protocol above; do not promote PI to H without a falsifier.

---

## Cross-reference index

| H-ID | Candidate / problem | Frame | Key metric | PI |
|------|---------------------|-------|------------|-----|
| H-001 | SHTC-639 | F3g | independence \(r\), holdout | 001, 002, 005 |
| H-002 | AMFW-012e | F3h | fiber 729, K_A/K_H | 003, 006 |
| H-003 | Θ algebra | F3g→F∞ | new transition classes | 003, 007 |
| H-004 | TDA + tensor | F3f+F3g | K_A/K_H ≥ 2 | 003 |
| H-005 | ECIP vs linear | F3c vs F3a | acceptance, depth | 002, 004 |
| H-006 | ModuliVacuum | F3h | selective fiber | 003, 006 |
| H-007 | Dynamic media | visual F∞ | morphism recovery | 008 |
| H-shadow-005 | Kotzig P_k | F3e | counterexample cert | — |
| H-shadow-008 | Graceful Tree | F3e₂ | counterexample cert | — |

---

Roman Kuznetsov · NAMM research program
