# NAMM Open Problems Queue

**As of:** 2026-08-11  
**Purpose:** Single operational map — which open problems NAMM **attacks** vs **calibrates**, what is running, and what is planned next.  
Roman Kuznetsov · NAMM research program

Related: [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) · [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) · [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) · [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md)

---

## Epistemic baseline

NAMM produces **finite shadows** — bounded, exact, falsifiable claims with `certificate.json` witnesses. It does **not** claim to resolve Millennium problems or full conjectures outright. Positive results extend verified bounds; negative results (counterexamples) are certificates; null results calibrate the instrument.

Label: `COMPUTATIONAL_EVIDENCE` under Protocol v2 unless promoted externally.

---

## Tier roles (attack vs calibration)

| Tier | Role in NAMM | Examples |
|------|--------------|----------|
| **T0 — attack target** | Direct finite shadow search; counterexample = certificate | Kotzig (005), Graceful Tree (008), Graph Reconstruction (planned), Sombor max, total domination |
| **T1 — methodology only** | Closed or refuted; Lean/SAT replay as reference | Unit vector flows, WOWII-200 |
| **T2 — future attack** | Shadow defined; adapter or search cost not in repo yet | Hedetniemi product, vertex-transitive Hamiltonian, Turán C₄, OEIS gnu |
| **T3 — motivation only** | No crisp bounded falsifier | Riemann Hypothesis, P vs NP |

**Calibration shadows (T0):** classical conjectures where NAMM validates the pipeline (honest null, reproducible bounds) — e.g. Graceful Tree 008 to order 12 (987 trees, 0 counterexamples).

**Beyond-anthropic targets (not tierlist disproof):** config_shadow frame (009/010) — AMFW fibers measure π_H loss (K_A/K_H ≈ 9.3), not a refutation of Graceful Tree or Kotzig.

---

## Running / complete (open-problem & config track)

| ID | Problem / frame | Status | Result (summary) |
|----|-----------------|--------|------------------|
| **005** | Kotzig P_k-graphs (T0 #1) | implemented / run | Exhaustive atlas n≤7, k∈{3…10}; no counterexample → bounded null |
| **008** | Graceful Tree (T0 #2) | run | 987 trees order ≤12; all graceful → calibration null |
| **009** | 11D moduli / M-theory **metaphor** (F3h) | run | 59,049 vacua; uniform fiber 729; AMFW-012e witness |
| **010** | κ-sweep extension of 009 | run | All κ modes → max fiber 729 at ±1 grid |
| **012** | Graceful → moduli hybrid (F3e₂ + F3h) | **scaffold only** | Encode labelings as moduli; fiber = labeling ambiguity |

M-theory in docs = **operational metaphor** (integer moduli, flux mod 3, lossy κ) — not physical M-theory or Calabi–Yau results.

---

## Planned queue (proposed IDs — not all scaffolded)

| Proposed ID | Focus | Frame | Source |
|-------------|-------|-------|--------|
| **011** | Trans-level **Θ** — semantic transition algebra over raw structure (extends SHTC-639 / 007) | F3g → F∞ | [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md), [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) |
| **012** | Graceful labeling moduli shadow (hybrid) | F3e₂ + F3h | [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) Part B |
| **013** | TDA + raw tensor composite (006 lesson + 007 signal) | F3f + F3g | [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) § failed 006 |
| **014** | Graph Reconstruction Conjecture deck shadow (T0 #3) | F3e | [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) |
| **009+** | Extended M-theory moduli shadows (wider grid, selection principles) | F3h | Synergy roadmap |

Additional T0 backlog (no ID yet): Sombor index maximum on trees; total domination vs matching.

---

## 11D / config_shadow — which problems fit

| Amenable via config_shadow | Mechanism | Experiment |
|----------------------------|-----------|------------|
| Graceful Tree (labeling ambiguity) | Multiple labelings → same κ shadow → fiber ≥ 2 | 012 (planned) |
| Kotzig / deck / extremal graphs | **Not** primary config_shadow domain — use graph atlas (005, 014) | — |
| Fiber bound hypotheses H1–H4 | Vary (n, s, E, grid, κ); seek unequal fibers or K_A/K_H fail | 009, 010 |
| M-theory landscape metaphor | Enumerate admissible moduli; rank by fiber degeneracy | 009, future 009+ |

Part B of [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) pairs **Graceful Tree** as T0 calibration with **AMFW** as beyond-π_H target — same certificate culture, contrasting outcomes.

---

## What NAMM does **not** claim

- Disproving Kotzig, Graceful Tree, or Reconstruction **globally** from bounded nulls
- Proving M-theory, 11D supergravity, or AGI from fiber enumeration
- Resolving RH, P vs NP, or other T3 items without new finite reformulation

---

Roman Kuznetsov · NAMM research program
