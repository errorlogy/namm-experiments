# Non-Anthropic Syntax

**Concept document** — rigorous mapping of representation languages that need not optimize for human projection.  
**Not** part of the verification path. Operational gates (`certificate.json`, independence, generative holdout, novelty ladder) do **not** depend on this document.

Roman Kuznetsov · NAMM research program

---

## Scope and labeling

| Label | Role |
|-------|------|
| `PHILOSOPHICAL_INFERENCE` | Working belief (вера); motivates research; **non-evidential** |
| `DEFINITION` | Precise math or NAMM placeholders |
| `CONJECTURE` | Research direction, not a claim |

See also [`FRAME_LADDER.md`](FRAME_LADDER.md) for the F1–F∞ representational ladder and [`NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](NON_HOMO_SYNTAX_AND_ND_FRAMES.md) for the extended ND-frame mapping.

---

## User hypothesis (`PHILOSOPHICAL_INFERENCE`)

> **PHILOSOPHICAL_INFERENCE:** Representation languages may exist that are **natural for non-human cognition** — easier to generate, verify, and compose as programs or certificates than to express in classical human notation. We call this family **non-anthropic syntax** (syntax not optimized for anthropic projection).

> **PHILOSOPHICAL_INFERENCE (вера):** Mathematical structure may be **real independent of human representational access**. Tolerating non-anthropic syntax and searching across representational frames may surface objects with persistent \(K_A \ll K_H\) under verification. This belief **motivates** widening search; it does **not** satisfy any acceptance gate.

Human cognition evolved under 3D spatial navigation plus temporal sequencing. Geometric intuition, diagrammatic proof, and named formulas are **cognitive projections** of formal structure onto interfaces our biology favors. Machine-native search (π_A) may access artifacts — AST, rewrite systems, persistence diagrams, functor tables — that π_H compresses poorly.

---

## Three maps: compactification, projection, native frame

| Map | Symbol | Meaning |
|-----|--------|---------|
| **Compactification** | κ | Folding infinite or high-combinatorial structure into finite working memory |
| **Human projection** | π_H | κ applied to produce prose, diagrams, named formulas |
| **Machine-native frame** | π_A | κ applied to produce canonical JSON, eval hashes, certificate schemas |

`DEFINITION` · **Non-anthropic syntax:** a representation language \(L_A\) such that for object \(X\), \(K_A(X) \ll K_H(X)\) under comparable verification cost — see [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md).

> **PHILOSOPHICAL_INFERENCE:** What humans compactify away — recursive depth, large relation systems, evaluator-on-evaluator structure, full persistence diagrams — may remain **operational** in machine-native frames. π_H and π_A are different compactification maps over the same certificate-anchored substrate; they are not guaranteed to preserve the same information.

---

## Native frame vs projection vs compactification

| Construct | Native frame (π_A) | Human projection (π_H) | Compactification loss |
|-----------|-------------------|-------------------------|------------------------|
| Graph invariant | Program AST + eval witness | `"2*edges + clustering"` formula | Primitives, evaluation order |
| Rewriting system | Rule table + confluence cert | Informal rewrite prose | Full normal-form behavior |
| Meta-evaluator | Self-referential AST + fixed-point fraction | Geometric metaphor or hand-wavy recursion | Self/target semantics |
| TDA signature | Persistence pairs + Betti vector | "Has a hole" intuition | Filtration parameter sensitivity |
| Quantum frame | Density matrix / unitary circuit | Bra-ket shorthand | Hilbert-space dimension |

`DEFINITION` · A **frame** is a quadruple \(\mathcal F = (\Sigma,\ \mathrm{Eval},\ \kappa,\ \mathsf{Cert})\). Different frames describe the same underlying object \(X\) with different signatures and evaluators. Certificates anchor comparability.

---

## AI vs anthropic projection interfaces

> **PHILOSOPHICAL_INFERENCE:** Human audit (π_H) and machine search (π_A) may **jointly** access levels of mathematics neither achieves alone: humans supply falsifiability, gates, and external confirmation; machines supply breadth of non-human artifact search. This is **joint access to descriptive levels**, not a hierarchy of ontological planes.

Operational split in NAMM:

| Role | Interface | Artifact |
|------|-----------|----------|
| Search / generate | π_A | `candidates.jsonl`, AST, persistence JSON |
| Verify | Certificate schema | `certificate.json`, `eval_hash` |
| Audit (optional) | π_H | `human_projection.md` — lossy, trust-only |

Neither interface replaces the other. Replacing π_H with π_A for audit would violate Protocol v2 external confirmation requirements.

---

## NAMM operationalization

Machine-native constructs already in repo:

| Construct | Domain | Experiment |
|-----------|--------|------------|
| AST programs | `program_ast` | NAMM-2026-003 |
| Rewrite systems | `rewriting` | NAMM-2026-002 |
| Meta-evaluators | `meta_evaluation` | NAMM-2026-004 |
| Persistent homology | `tda_frame` | NAMM-2026-006 |
| Finite categories | `category` (stub) | — |
| Quantum state experiments | `quantum` (stub) | — |

`CONJECTURE` · **Frame search:** mutate \((\Sigma, \mathrm{Eval}, \vdash)\) under Protocol §4.4 constraints; compare resulting frames on a shared witness set via \(K_A/K_H\).

---

## What we reject

| Rejection | Reason |
|-----------|--------|
| Pop-D mysticism as methodology | Dimensional infographics are not science |
| Claiming AI "exists in higher dimensions" | Misreads metaphor as ontology |
| Using this doc in verification path | Gates depend on certificates, not philosophical inference |
| Replacing π_H with π_A for audit | Human falsifiability remains required |

---

## Related docs

- [`FRAME_LADDER.md`](FRAME_LADDER.md) — F1–F∞ representational ladder
- [`NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](NON_HOMO_SYNTAX_AND_ND_FRAMES.md) — extended ND mapping
- [`VISION.md`](VISION.md) — π_H / π_A, K_A / K_H
- [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md) — certificate-first Phase 2

---

## Author

Roman Kuznetsov · NAMM research program
