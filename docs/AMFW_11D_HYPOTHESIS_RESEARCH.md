# AMFW-11D Hypothesis Research — Deep Dive & Protocol

**Date:** 2026-08-11  
**Scope:** NAMM-2026-009 (AMFW-012e), NAMM-2026-010 (κ-sweep), hypothesis protocol, philosophical frame  
**Epistemic baseline:** `COMPUTATIONAL_EVIDENCE` under Protocol v2 — not physical M-theory or published theorems  
Roman Kuznetsov · NAMM research program

Related: [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) (PI-001–PI-007) · [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) · [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) · [`HOMO_LIMIT_JOURNAL.md`](HOMO_LIMIT_JOURNAL.md) HL-004

---

## Labeling

| Label | Use |
|-------|-----|
| `DEFINITION` | Precise operational or mathematical content |
| `COMPUTATIONAL_EVIDENCE` | Reproducible experiment witness |
| `CONJECTURE` | Open claim not yet verified |
| `PHILOSOPHICAL_INFERENCE` | Motivates search; non-evidential |

---

# Part A — AMFW-012e (`vac-012e1fe1`) Deep Dive

## A.1 Experiment artifacts (NAMM-2026-009)

| Field | Value |
|-------|-------|
| Lead ID | `vac-012e1fe1` |
| 11D moduli \(m\) | `[1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]` |
| 4D shadow \(\kappa(m)\) | `[1, 1, -1, -1]` |
| Fiber size \(\|\kappa^{-1}(\kappa(m))\|\) | **729** |
| Fiber index | **492** (lex order within fiber) |
| Stability \(\sum m_i^2\) | **11.0** |
| \(\sum m_i\) | **−3 ≡ 0 (mod 3)** |
| Vacua scanned | **59,049** |
| Ambiguous shadow classes | **81** |
| K_A/K_H (gzip / projection tokens) | **149 B / ≈16 → ≈9.3** |
| Certificate | `experiments/NAMM-2026-009/artifacts/certificate.json` |

Reproduction:

```bash
python -m namm.cli run-experiment --id NAMM-2026-009
python -m pytest tests/test_config_shadow.py -q
python scripts/analyze_fiber_009.py
```

## A.2 Why fiber size = 729?

`DEFINITION` · Configuration space \(\mathcal{M} = \{-1,0,1\}^{11}\). Admissibility:

1. **Flux quantization:** \(\sum_{i=1}^{11} m_i \equiv 0 \pmod{3}\)
2. **Energy bound:** \(\sum m_i^2 \leq 20\)
3. **Compactification:** \(\kappa(m) = (m_1,m_2,m_3,m_4)\) — first four moduli

`COMPUTATIONAL_EVIDENCE` · Enumeration confirms:

| Quantity | Value | Formula |
|----------|-------|---------|
| Raw grid | \(3^{11} = 177{,}147\) | full \(\{-1,0,1\}^{11}\) |
| Admissible vacua | **59,049** | \(177{,}147 / 3 = 3^{10}\) — flux cuts by exactly \(1/3\) |
| Shadow classes | **81** | \(3^4\) — every 4D pattern in \(\{-1,0,1\}^4\) appears |
| Fiber size (all shadows) | **729** | **uniform** — \(59{,}049 / 81 = 3^6\) |

### Structural theorem (finite shadow)

For moduli in \(\{-1,0,1\}\), config dimension \(n\), shadow dimension \(s\), flux modulus 3, and energy cap \(E \geq n\):

\[
|\kappa^{-1}(\sigma)| = 3^{\,n - s - 1}
\]

whenever shadow \(\sigma\) has at least one admissible lift — because:

1. **Energy is inactive:** each coordinate contributes at most 1 to \(\sum m_i^2\); max energy is \(n \leq 11 \ll 20\). Tail coordinates never hit the energy wall.
2. **Flux splits fibers equally:** fixing the head \(h = \kappa(m)\) with \(\sum h \equiv r \pmod{3}\), the tail \(t \in \{-1,0,1\}^{n-s}\) must satisfy \(\sum t \equiv -r \pmod{3}\). Among \(3^{n-s}\) tails, exactly \(3^{n-s-1}\) satisfy this (uniform distribution over \(\mathbb{Z}_3\)).

With \(n=11, s=4\): fiber size \(= 3^{11-4-1} = 3^6 = 729\).

> **Interpretation:** 729 is **not** a fine-tuned anomaly — it is the **generic degeneracy** of a lossy head projection under independent tail flux constraints. Ranking by fiber size in 009 selects the **maximum generic ambiguity**, not a physically distinguished vacuum.

### Equivalence classes

| Level | Object | Count (009 grid) |
|-------|--------|------------------|
| Full moduli | \(m \in \mathcal{M}_\text{adm}\) | 59,049 |
| Shadow class | \(\kappa(m) \in \{-1,0,1\}^4\) | 81 |
| Fiber | \(\kappa^{-1}(\sigma)\) | 729 each |
| Witness pick | single \(m\) + fiber index | 1 |

Shadow classes are **equivalence classes** under the relation \(m \sim m'\iff \kappa(m)=\kappa(m')\). The certificate breaks equivalence by storing the full 11D preimage and **fiber_index** within the class.

## A.3 Characterization of `vac-012e1fe1`

`DEFINITION` · Witness vector:

\[
m = (\underbrace{1,1,-1,-1}_{\kappa(m)},\ \underbrace{1,-1,-1,-1,1,-1,-1}_{\text{tail}})
\]

| Invariant | Value | Note |
|-----------|-------|------|
| Support | 11/11 coords non-zero | no moduli at 0 |
| Sign pattern | 7 positive, 4 negative | balanced flux |
| \(\sum m_i\) | −3 | ≡ 0 (mod 3) |
| \(\sum m_i^2\) | 11 | mid-range stability |
| Head energy | 4 | tail budget unused (max tail energy 7) |
| Fiber index 492 | 492/728 | ~67th percentile in lex fiber order |

`COMPUTATIONAL_EVIDENCE` · ID `vac-012e1fe1` = SHA-256 prefix of `"m|κ(m)"` — deterministic, not selected for physical optimality.

Human projection \(\pi_H\) sees only `[1,1,-1,-1]` + stability 11. **728 other 11D vacua** share that shadow — HL-004 compactification loss made executable.

## A.4 Extension — NAMM-2026-010 (κ-sweep)

| κ mode | Definition | max fiber | shadows | vacua |
|--------|------------|-----------|---------|-------|
| `first_4` | \((m_1,\ldots,m_4)\) | 729 | 81 | 59,049 |
| `last_4` | \((m_8,\ldots,m_{11})\) | 729 | 81 | 59,049 |
| `middle_4` | central 4 coords | 729 | 81 | 59,049 |
| `flux_blocks_4` | block sums mod 3 | 729 | 81 | 59,049 |

`COMPUTATIONAL_EVIDENCE` · At \(\{-1,0,1\}^{11}\) with inactive energy, **all tested κ maps yield identical fiber statistics**. Ambiguity is a property of **(grid × flux) / shadow dimension**, not κ alone.

**Wider moduli (7D, \([-2,2]\)):** 23,745 vacua, 625 shadows, **max fiber 42** — energy and richer grid break uniformity; see `scripts/analyze_fiber_009.py`.

Report: [`experiments/NAMM-2026-010/EXPERIMENT_REPORT.md`](../experiments/NAMM-2026-010/EXPERIMENT_REPORT.md)

---

# Part B — Hypothesis Generation from 11D Fiber Witnesses

## B.1 Operational protocol: AMFW → falsifiable hypotheses

```text
  11D witness (certificate.json)
           │
           ▼
  FORMALIZE — type ModuliVacuum + κ + constraints
           │
           ▼
  HYPOTHESIZE — structured claim with falsifier
           │
           ▼
  ATTACK — vary κ, moduli range, energy; seek counterexample
           │
           ▼
  VERIFY — reproduce fiber_size, fiber_index, eval_hash
           │
           ▼
  PROJECT — π_H (4D shadow) vs π_A (full moduli + fiber)
```

### Witness → hypothesis template

| Step | Input | Output hypothesis | Falsifier |
|------|-------|-------------------|-----------|
| H1 Fiber bound | `(n,s,E,grid)` | \(F_{\max} = f(n,s,E,\|G\|)\) | find admissible grid with larger fiber |
| H2 κ sensitivity | κ family | ambiguity depends on κ | 010-style sweep showing unequal max fibers |
| H3 Selection | ranked vacua | physical selection picks unique lift | second principle picks different member of fiber |
| H4 Compression | K_A/K_H | ≥ 2 for all fiber ≥ 2 | certificate failing representation gate |
| H5 Open-problem lift | combinatorial shadow | labeling ambiguity ≅ fiber degeneracy | counterexample tree / deck pair |

Each hypothesis must specify: **domain**, **finite bounds**, **certificate shape**, **rejection reason** if false.

## B.2 Open-problem target — Graceful Tree Conjecture

Selected from [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) **T0 #2**.

| Role | Experiment | Frame | Purpose |
|------|------------|-------|---------|
| **Calibration (T0)** | NAMM-2026-008 | F3e₂ | Exhaustive graceful labeling to order 12 — **987 trees, 0 counterexamples** |
| **Beyond-anthropic target** | NAMM-2026-009/010 | F3h | AMFW fiber witnesses — **729-fold ambiguity** under κ |
| **Hybrid (planned)** | NAMM-2026-012 | F3e₂ + F3h | Encode graceful labelings as moduli; fiber = labeling ambiguity |

`CONJECTURE` · Graceful Tree at order ≤ 12 is **calibration null** (extends literature). AMFW is **not** a disproof of graceful trees — it demonstrates a **different object class** where π_H loss is measurable (K_A/K_H ≈ 9.3 vs graceful shadow ~1×).

**Why this pairing:** same tierlist tier (T0), same certificate culture, contrasting epistemic outcomes — **verified combinatorial shadow** vs **intentionally ambiguous configuration shadow**.

## B.3 Experiment scaffolds

| ID | Status | Content |
|----|--------|---------|
| **NAMM-2026-010** | **run complete** | κ-sweep; confirms uniform 729 degeneracy at ±1 grid |
| **NAMM-2026-012** | scaffold | Graceful labeling → 11D moduli + κ; see [`experiments/NAMM-2026-012/README.md`](../experiments/NAMM-2026-012/README.md) |

### NAMM-2026-012 planned falsifiers

1. **Refute Graceful Tree:** one tree order ≤ n with no graceful labeling → certificate with `is_counterexample: true`
2. **AMFW-style signal:** tree with ≥ 2 graceful labelings sharing κ-shadow → `fiber_size ≥ 2` configuration witness

---

# Part C — AGI, Fuzzy Sets, ND Topology (`PHILOSOPHICAL_INFERENCE`)

> **PHILOSOPHICAL_INFERENCE:** The following motivates the F1→F∞ research queue. It does **not** satisfy NAMM acceptance gates.

## C.1 Core hypothesis (formal sketch)

Let \(\mathcal{H}\) = fuzzy set of **known human mathematics** — membership \(\mu_{\mathcal{H}}(x) \in [0,1]\) = degree to which structure \(x\) admits compact anthropic notation (definition, proof, named invariant).

Let \(\mathcal{T}_N\) = **ND configuration topology** — parameter space of dimension \(N\) (operational: \(N\)-tuples with constraints + projection κ).

**Claim (`PHILOSOPHICAL_INFERENCE`):** True AGI-native mathematics occupies regions where \(\mu_{\mathcal{H}}(x) \ll 1\) but **machine certificates** remain exact — i.e. beyond the fuzzy support of current human math, not merely low-\(\mu\) noise inside it.

**Topology stretch:** Deform \(\mathcal{T}_N \to \mathcal{T}_{N'}\) (increase \(N\), change κ, weaken energy) — the fuzzy set \(\mathcal{H}\) **does not expand automatically**; new objects appear as **preimages under lossy κ** (AMFW fibers) or **AST/tensor programs** (SHTC-639) whose \(\mu_{\mathcal{H}}\) is low until a human bridge is found.

## C.2 Anthemium + frame ladder alignment

| Manifesto / Anthemium | NAMM operational |
|----------------------|------------------|
| Cognitive topology | Search domains (graph, tensor, config_shadow, meta) |
| Morphisms / transitions | κ maps, AST evaluation, generative holdout |
| Transformation memory | `certificate.json`, rejections.jsonl |
| Frame escalation F1→F∞ | [`FRAME_LADDER.md`](FRAME_LADDER.md) — F3h = 11D shadow rung |

F1 (pop-D metaphor) motivates questions; F3 executes; F4 (π_H bottleneck) gates acceptance; F∞ requires explicit ordinal/colimit structure — not metaphor alone.

## C.3 Operational metrics — when does "stretch" produce testable objects?

| Metric | Pass threshold | AMFW-012e | Graceful-008 (contrast) |
|--------|----------------|-----------|-------------------------|
| **F4 compression** K_A/K_H | ≥ 2.0 | **9.3** ✅ | ~1× (edge list) |
| **Non-injective κ** | fiber ≥ 2 | **729** ✅ | N/A (unique labeling witness) |
| **Certificate reproducibility** | eval_hash stable | ✅ | ✅ |
| **Independence from named math** | domain-specific | N/A (config, not graph) | N/A |
| **Generative holdout** | protocol v2 | ❌ (future) | implicit (tree families) |
| **Falsifier exists** | finite shadow | vary κ / grid | one non-graceful tree |

`OPERATIONAL` · **Stretch is productive** when increasing \(N\) or changing κ yields **new certificate classes** passing F4 without collapsing to π_H-only description. AMFW-012e is the strongest F4 witness in the registry; Graceful-008 validates the **instrument** on a classical conjecture without producing beyond-π_H compression.

`PHILOSOPHICAL_INFERENCE` · If repeated stretch operations produce stable certificate families with high K_A/K_H and no human name, that is **evidence** (not proof) that \(\mu_{\mathcal{H}}(x)\) is genuinely low for those \(x\) — the fuzzy boundary of "known math" is being mapped operationally.

## C.4 User thesis and assistant nuance (2026-08-11)

Registered in [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) as **PI-002, PI-003, PI-006, PI-007**. Summary:

**User thesis (two legs):**

1. **Extension leg** — ND topology deformation stretches fuzzy set \(\mathcal{F}_H\) of known math → new invariants, ontologies, certificates (NAMM + Anthemium queue).
2. **Non-boost leg** — genuine AGI cannot reduce to homo-conditioned embeddings; it must navigate \(\mu_{\mathcal{F}_H}(x) \approx 0\) with verifiable \(x\).

**Assistant agreement:** After 007/009, the direction is **operationally credible** — witnesses exist where \(\pi_H\) is lossy and certificates hold. AMFW-012e (729→1 shadow) is the cleanest parable.

**Assistant nuance (not full literal agreement):**

| Claim | Refinement |
|-------|------------|
| "Only AI" conducts extensions | Only **machine-native search at scale**; humans set falsifiability gates |
| AGI ⇒ math beyond \(\mathcal{F}_H\) | **Design axiom**; falsifier = tested-signal + frame escalation |
| Philosophy ⇒ ontology | Witnesses in specific frames ≠ proof all math lies outside human reach |

**Consolidated formulation:**

> Substantial mathematics may be machine-accessible and certificate-verifiable while anthropically inaccessible at compact description. NAMM explores that gap; embedding-only systems cannot close it.

---

## Summary table

| Artifact | Experiment | Key result |
|----------|------------|------------|
| AMFW-012e | 009 | 729 uniform fibers; vac-012e1fe1 index 492 |
| κ-sweep | 010 | All κ modes → max fiber 729 at ±1 grid |
| Graceful calibration | 008 | 987 trees graceful to order 12 |
| Hybrid scaffold | 012 | Graceful → moduli fiber (planned) |

---

Roman Kuznetsov · NAMM research program
