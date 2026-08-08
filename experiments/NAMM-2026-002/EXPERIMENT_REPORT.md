# NAMM-2026-002 — Full Experiment Report

**Status:** computationally supported  
**Cycle:** INPUT → ABSTRACT → META-LIFT → GENERATE → FORMALIZE → ATTACK → VERIFY → COMPARE → PROJECT  
**Date:** 2026-08-08  
**Protocol:** v2 AI-native (certificate-first)

---

## NAMM Research Cycle

### INPUT

- **Domain:** program AST over finite connected simple graphs, order \(n \leq 8\)
- **Train set:** connected atlas graphs, order \(\leq 6\)
- **Held-out families:** trees, bipartite, cubic (order \(\leq 8\))
- **Baseline:** Wiener index (AST leaf `wiener_index`)
- **Seed:** 2026; **Candidates generated:** 80

### ABSTRACT

Objects: connected graphs \(G=(V,E)\), \(|V|\leq 8\).  
Relations: graph isomorphism.  
Transformations: random AST composition of graph-statistic leaves with `add`, `sub`, `mul`, `neg`.  
Invariants: verified program trees evaluated by structured interpreter.  
Constraints: reject Wiener-equivalent programs; independence gate (\(r \leq 0.95\)); generative holdout on unseen families.

### META-LIFT

| Level | Object |
|-------|--------|
| L0 | Graph statistics as AST leaves |
| L1 | `evaluate_ast` as graph → ℝ interpreter |
| L2 | `random_program_ast` generator (depth ≤ 3, leaves ≤ 5) |
| L3 | Gates: independence, prior-art simplify, generative holdout |

The generator operates on **program structure**, not human-motivated formula strings. Canonical form is the sorted AST in `certificate.json`.

### GENERATE

Machine-native generator: `random_program_ast(seed)` → binary tree over statistic leaves.

**Best candidate (by variance score):**

```
prog-17644c1d: ((num_edges * num_edges) - algebraic_connectivity) * degree_sum
```

- **Score:** 5447.50 (max − min over 40 test graphs)
- **Meta-origin:** `random_ast_composition`
- **AST hash:** `db4d26320d0d5f29`
- **Eval hash:** `4d6db98eb49aa164`

### FORMALIZE

**Definition (COMPUTATIONAL_EVIDENCE).** For connected graph \(G\),

\[
I(G) = \bigl(|E(G)|^2 - \lambda_2(G)\bigr) \cdot \sum_{v \in V} \deg(v)
\]

where \(\lambda_2\) is algebraic connectivity (Fiedler value) and \(\sum \deg(v) = 2|E|\).

Program is stored as canonical JSON AST in `artifacts/certificate.json`.

### ATTACK

| Step | Check | Result |
|------|-------|--------|
| A1 | Non-equivalence vs Wiener on test set | **passed** |
| A3 | Independence (\(r \leq 0.95\) vs baselines on atlas \(n\leq 6\)) | **passed** (max \(r=0.912\) vs degree_sum) |
| A4 | Prior-art simplify | **passed** |
| G1 | Generative holdout (trees, bipartite, cubic) | **passed** (aggregate score 7.82) |

**Rejection breakdown (57 total):**

- Wiener-equivalent or evaluation errors
- High correlation with baselines (\(r > 0.95\))
- Generative holdout failure (flat on held-out family)
- Prior-art simplify matches

### VERIFY

| Check | Result |
|-------|--------|
| Certificate AST hash | `db4d26320d0d5f29` |
| Eval witness hash (20 reference graphs) | `4d6db98eb49aa164` |
| Attack checklist signed off | Yes |
| Generative holdout per-family variance | trees 5624, bipartite 9020, cubic 2464 |

### COMPARE

| Baseline | Pearson \(r\) |
|----------|---------------|
| wiener_index | −0.068 |
| degree_sum | 0.912 |
| avg_degree | 0.904 |
| clustering | 0.619 |
| algebraic_connectivity | 0.716 |

**Novelty level:** N2 — passes independence gate but structurally related to degree_sum (\(r \approx 0.91\)). Not Wiener-dominated (unlike NAMM-2026-001).

### PROJECT

**Representation metrics (K_A proxies):**

| Metric | Value |
|--------|-------|
| JSON bytes | 277 |
| Gzip bytes | 147 |
| Eval time | 0.46 ms/graph |
| Projection tokens | ≈11 |

**K_A/K_H proxy:** 277 bytes / 132 tokens ≈ **2.1** — machine certificate is compact; human projection is longer and lossy (includes protocol context, witness notes).

Human projection is secondary; `certificate.json` is the primary reproducible artifact.

---

## Summary

NAMM-2026-002 demonstrates the AI-native pipeline: random AST synthesis with certificate-first artifacts, independence gates, and generative holdout on structurally distinct graph families. Of 80 candidates, **23 passed all gates**. Best candidate is a non-Wiener program at novelty N2 with strong generative spread on held-out families.

**Honest assessment:** Positive computational result for the *protocol* (certificate, holdout, independence machinery works). The discovered invariant is not mathematically novel — it correlates with degree_sum — but shows the AI-native search can find structurally distinct programs that generalize beyond the training atlas.

---

## Artifacts

| File | Role |
|------|------|
| `artifacts/certificate.json` | Primary machine artifact |
| `artifacts/result.json` | Experiment summary |
| `artifacts/candidates.jsonl` | Accepted candidates |
| `artifacts/rejections.jsonl` | Rejected candidates with reasons |
| `artifacts/HUMAN_PROJECTION.md` | Lossy human-readable projection |
