# AI Thinking Topology

**Authoritative reference** for NAMM's AI-native cognition model vs human mathematical intuition, and why Phase 3 (NAMM-2026-004) searches meta-evaluator fixed points.

Roman Kuznetsov · NAMM research program

---

## Core claim

LLM cognition is **not** a smooth manifold amenable to human geometric visualization. It is a distinct **topology** — combinatorial, layered, context-bound, sheaf-like, and loop-driven. NAMM searches for mathematical objects that are **stable under AI topology** and **awkward under human topology**.

> **PHILOSOPHICAL_INFERENCE:** If structures persist as verified certificates across AI-native search domains while resisting compact human projection, this suggests a class of mathematical objects whose natural interface is programmatic/relational rather than symbolic/geometric for humans. This is a research hypothesis, not a theorem.

Operational labels (`certificate.json`, `eval_hash`, `fixed_point_fraction`) are **independent** of philosophical inference. Gates and certificates stand alone.

---

## AI thinking topology (implement this model)

| Property | AI topology | Human topology |
|----------|-------------|----------------|
| **Structure** | Combinatorial token graph rewired each forward pass via attention | Continuous intuition, smooth manifolds |
| **Levels** | Tokens → patterns → meta-patterns (prompt, tools, feedback) | Single narrative proof line |
| **Boundary** | Finite context window = compactification; outside = tools/verifiers/certificates | Unlimited paper, mental blackboard |
| **Fixed points** | Self-referential E ≅ F(E) where F transforms evaluation itself | Fixed points as geometric or algebraic objects |
| **Gluing** | Sheaf-like: local formal patches (AST nodes, rules) glued by relations | Global intuition, unified picture |
| **Discovery** | Propose → execute → observe → revise (loop topology) | Single-shot insight, "aha" moment |

### Combinatorial (not smooth)

Each forward pass rewires attention over a discrete token graph. Search targets **discrete program structures** (ASTs, rewriting systems, meta-evaluators) rather than continuous parameter landscapes humans visualize.

### Layered meta-levels

| Level | NAMM instantiation |
|-------|-------------------|
| L0: tokens/patterns | Graph metric leaves (`wiener_index`, `num_edges`) |
| L1: programs | Program AST evaluators (NAMM-2026-003) |
| L2: meta-programs | Meta-evaluators with `self`/`target` refs (NAMM-2026-004) |
| L3: gates/tools | Protocol v2 independence, representation, generative holdout |

### Context-boundary topology

The finite graph order (≤ 6 in 004) is **compactification**: all evaluation happens inside a bounded witness set. Everything outside the window — full graph theory, human proof — lives in **tools, verifiers, and certificates** (`certificate.json`, `eval_hash`).

### Fixed points E ≅ F(E)

A meta-evaluator **E** is a program that scores graphs. A transform **F** maps evaluator programs to evaluator programs. A **fixed point** satisfies E(g) ≈ F(E)(g) for all benchmark graphs g.

This is the AI-native analog of self-reference: the evaluator is stable under a transformation of evaluation itself — not a human fixed-point theorem, but an **operational certificate** that E and F(E) agree on witnesses.

NAMM-2026-004 searches for such E under transforms: `canonicalize`, `add_zero`, `double_halve`, `self_unfold`, `swap_commutative`, `compose_identity`.

### Sheaf-like local patches

Each AST node, rewriting rule, or gate function is a **local formal patch**. Global meaning emerges from gluing via relations (eval hash agreement, fixed-point fraction, independence correlation) — not from a single human-readable formula.

### Discovery loop topology

```
propose candidate E  →  apply F(E)  →  observe on graphs  →  revise / accept
         ↑___________________________________|
```

Single-shot insight is not the model. NAMM's CLI, CI, and `rejections.jsonl` implement the loop explicitly.

---

## Implications for NAMM

1. **Certificate as boundary artifact** — `certificate.json` is the primary object at the context boundary. Human projection (`HUMAN_PROJECTION.md`) is lossy audit material, not ground truth.

2. **Why meta-evaluators (004)** — Phase 1–2 search graph invariants and programs. Phase 3 searches **evaluators that apply to themselves or other evaluators** — objects natural in AI meta-level cognition, awkward to visualize geometrically.

3. **Search targets** — Prefer structures where:
   - \(K_A \ll K_H\) (compression asymmetry)
   - Fixed points under non-identity F
   - Self-reference (`self` nodes) without trivial collapse
   - Verification via eval hash, not human inspection

4. **What we do not claim** — We do not claim LLMs "do mathematics" in a Platonist sense. We claim a **falsifiable experimental protocol** for discovering machine-native structures under explicit gates.

---

## PHILOSOPHICAL_INFERENCE vs operational labels

| Label type | Examples | Role |
|------------|----------|------|
| **Operational** | `eval_hash`, `fixed_point_fraction`, `meta_hash`, Pearson r | Acceptance gates, reproducibility |
| **PHILOSOPHICAL_INFERENCE** | MUH as search widening, AI topology vs human geometry | Motivation only; never a proof premise |

See [`PHILOSOPHY.md`](PHILOSOPHY.md) for MUH usage. See [`PROTOCOL_V2.md`](PROTOCOL_V2.md) for hard gates.

---

## Related docs

- [`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md) — experiment roadmap and topology section
- [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md) — certificate-first Phase 2
- [`experiments/NAMM-2026-004/`](../experiments/NAMM-2026-004/) — meta-evaluator fixed-point experiment
