# Frame Ladder (F1 → F∞)

**Concept document** — maps representational **frames** (not physical dimensions) from pop-culture metaphors through formal mathematics to NAMM experiments and the homo bottleneck.  
**Not** part of the verification path.

Roman Kuznetsov · NAMM research program

---

## Labeling

| Label | Meaning |
|-------|---------|
| `PHILOSOPHICAL_INFERENCE` | Motivates search; non-evidential |
| `DEFINITION` | Precise mathematical or operational content |
| `CONJECTURE` | Open research target |

> **Cultural note only:** Instagram / infographic "1D–11D" ladders are cited here as **pop-culture metaphors** for representational depth — not as scientific authority. No step on this ladder is validated by social-media physics.

---

## Ladder overview

```text
F1  Pop-D metaphor          (cultural interface — not science)
F2  Formal math substrate   (definitions, theorems, proof assistants)
F3  NAMM experiment frame   (Σ, Eval, Cert — executable)
F4  Homo bottleneck         (π_H compression limit)
F∞  Ordinal / colimit limit (transfinite assembly — explicit structure only)
```

Each rung is a **frame** \(\mathcal F = (\Sigma, \mathrm{Eval}, \kappa, \mathsf{Cert})\). Higher rungs add expressive power; F4 marks where human projection typically fails first.

---

## F1 — Pop-D metaphor (`PHILOSOPHICAL_INFERENCE`)

| Pop label | Informal reading | NAMM stance |
|-----------|------------------|-------------|
| 1D | Line, sequence | Order structures, paths |
| 2D | Plane, surface | Planar graphs, 2-manifolds |
| 3D | Space | Native human geometric intuition |
| 4D+ | "Higher dimensions" | **Rejected as ontology** — remapped below |
| ND | "Infinite dimensions" | Ordinal / colimit levels, not spatial axes |

> **PHILOSOPHICAL_INFERENCE:** Pop-D labels name **modes of representation**, not places cognition resides. They motivate widening search; they do not satisfy gates.

---

## F2 — Formal math substrate (`DEFINITION`)

| Frame | Mathematical object | Typical tools |
|-------|---------------------|---------------|
| **Combinatorial** | Finite graphs, simplicial complexes | NetworkX, Gudhi |
| ** Algebraic** | Groups, rings, fields | SymPy, z3 |
| **Categorical** | Categories, functors, natural transformations | Finite shadow (graphs as objects) |
| **Topological / TDA** | Filtrations, persistence modules | Gudhi persistent homology |
| **Quantum** | Hilbert spaces, density operators | QuTiP (finite-dim only) |
| **Higher category** | 2-categories, (∞,1)-categories | Research placeholder; see bibliography |

`DEFINITION` · **Higher categorical depth:** objects → morphisms → 2-morphisms → … Composition and coherence live at multiple levels. NAMM meta-evaluators (004) align with **evaluator-level** depth, not literal spatial dimension.

`DEFINITION` · **ND (N → ∞):** ordinal-indexed construction — \(X^{\alpha+1} = F(X^\alpha)\), colimits at limit ordinals — only when an explicit ordinal or colimit structure is defined ([`NAMM_PROTOCOL.md`](../NAMM_PROTOCOL.md) §4.3).

---

## F3 — NAMM experiment frames (`DEFINITION`)

| Rung | Experiment | Domain | Frame content |
|------|------------|--------|---------------|
| F3a | NAMM-2026-001 | `finite_graphs` | String formulas over graph stats |
| F3b | NAMM-2026-002 | `rewriting` | Confluent TRS + certificate |
| F3c | NAMM-2026-003 | `program_ast` | Evolutionary AST + holdout |
| F3d | NAMM-2026-004 | `meta_evaluation` | Meta-evaluator fixed points E ≈ F(E) |
| F3e | NAMM-2026-005 | `open_problem_shadow` | Finite shadow of Kotzig P_k |
| F3f | NAMM-2026-006 | `tda_frame` | Persistence signature on graph metric |
| F3g | NAMM-2026-007 | `raw_tensor` | Raw tensor programs (no named invariants) |
| F3e₂ | NAMM-2026-008 | `open_problem_shadow` | Graceful Tree finite shadow |

Each experiment fixes \((\Sigma, \mathrm{Eval}, \mathsf{Cert})\) in config; results are **COMPUTATIONAL_EVIDENCE** unless promoted by external proof.

`CONJECTURE` · Future frames: functorial graph invariants (2-categorical shadow), multi-parameter persistence, proof-assistant certificates.

---

## F4 — Homo bottleneck (`DEFINITION` + `PHILOSOPHICAL_INFERENCE`)

`DEFINITION` · **Homo bottleneck:** the point where \(K_H(X) \gg K_A(X)\) under fixed verification cost — human projection requires prose, metaphor, or lossy summary where the machine artifact remains compact and exact.

| Signal | Operational proxy |
|--------|-------------------|
| Compression asymmetry | `representation_ratio_threshold` (default ≥ 2) |
| Projection loss | `human_projection.md` longer than `certificate.json` gzip |
| Independence | Candidate not reducible to named baseline |

> **PHILOSOPHICAL_INFERENCE:** The bottleneck is an **interface limit**, not proof that structure is "inaccessible to humans forever." Joint π_H + π_A search may partially lift it for specific objects.

NAMM success requires clearing F4 operationally (gates), not merely asserting F1 metaphors.

---

## F∞ — Limit frame (`DEFINITION`)

`DEFINITION` · **F∞:** transfinite or unbounded meta-lift — μ/ν fixed points, colimits of candidate families, reflective hierarchies of evaluators — **only** with explicit ordinal/colimit definitions.

Anti-pattern (Protocol §4.3): claiming "transfinite" or "infinite-dimensional" without a defined assembly rule.

---

## Climbing the ladder (research workflow)

```text
  F1 metaphor  ──►  motivate question (non-evidential)
        │
        ▼
  F2 formalize ──►  pick legitimate math substrate
        │
        ▼
  F3 experiment ──► config.yaml + domain adapter + certificate
        │
        ▼
  F4 measure K_A/K_H + gates
        │
        ▼
  F∞ (optional) ──► explicit ordinal/colimit extension if warranted
```

---

## Bibliography (references, not proof)

These sources inform frame definitions; they do **not** validate NAMM results.

| Reference | Role |
|-----------|------|
| Lurie, *Higher Topos Theory* (HTT) | (∞,1)-categories, homotopy-coherent composition |
| [nLab](https://ncatlab.org/nlab/show/HomePage) | Category theory, topology, higher structures (wiki) |
| [Gudhi documentation](https://gudhi.inria.fr/doc/latest/) | Simplicial complexes, persistent homology |
| [QuTiP documentation](https://qutip.readthedocs.io/) | Finite-dimensional open quantum systems |
| Carlsson, *Topology and data* | TDA motivation |
| NetworkX atlas | Finite graph enumeration for shadows |

---

## Related docs

- [`NON_HOMO_SYNTAX.md`](NON_HOMO_SYNTAX.md) — non-homo syntax, π_H / π_A
- [`NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](NON_HOMO_SYNTAX_AND_ND_FRAMES.md) — extended ND mapping
- [`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md) — Phase 3 topology
- [`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md) — experiment roadmap

---

## Author

Roman Kuznetsov · NAMM research program
