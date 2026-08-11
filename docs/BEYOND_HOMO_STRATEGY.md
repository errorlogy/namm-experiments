# Beyond Homo-Known Strategy

**Operational definition** for NAMM experiments that search outside the span of human-named mathematical vocabulary.  
Roman Kuznetsov · NAMM research program

---

## What “beyond homo-known” means (operationally)

A candidate clears the **beyond homo-known** bar only when **all** of the following hold:

| Gate | Criterion |
|------|-----------|
| **Vocabulary** | No named human invariants in search generators (ban `wiener`, `degree_sum`, etc.). Only **ADD / MUL / COMPOSE** on raw adjacency-derived numeric tensors. |
| **Independence** | Not in the span of **20+ known baselines** built from the same raw leaves, with polynomial degree **≤ 4** (Pearson r ≤ threshold). |
| **Compression** | **K_A / K_H ≥ 2** (prefer ≥ 5): certificate gzip bytes vs human projection token estimate. |
| **Generative holdout** | Non-trivial spread on **≥ 2** held-out families among: trees, bipartite, cubic, random regular. |
| **Frame escalation** | If a single frame fails all gates, combine domains per ladder below before declaring null. |

This is **not** a claim that humans can never understand the result — only that the **discovery path** did not start from named textbook invariants.

---

## Frame escalation ladder (F1 → F∞)

| Rung | Frame | Experiment(s) | When to use |
|------|-------|---------------|-------------|
| F1 | Pop metaphor | — | Motivation only |
| F2 | Formal math substrate | — | Definitions, not search |
| F3a | String formulas over stats | NAMM-2026-001 | Baseline (homo-known) |
| F3b | Rewriting systems | NAMM-2026-002 | Symbolic, non-graph |
| F3c | Named-leaf program AST | NAMM-2026-003 | AI-native but **uses** named stats |
| F3d | Meta-evaluator | NAMM-2026-004 | Topology-of-evaluator |
| F3e | Open-problem shadow | NAMM-2026-005, **008** | Falsifiable finite bounds |
| F3f | TDA persistence | NAMM-2026-006 | Metric topology frame |
| **F3g** | **Raw tensor programs** | **NAMM-2026-007** | **Beyond named math** |
| F4 | Homo bottleneck | All gated experiments | Interface limit (K_A ≪ K_H) |
| F∞ | Ordinal / colimit | Future | Explicit structure only |

**Escalation rule:** If F3c fails independence (too correlated with wiener/degree_sum), escalate to **F3g** (007). If F3g fails generative holdout, combine with **F3f** (006) in a joint certificate. If single-frame search returns null after combined frames, log **honest null** — not a conjecture refutation.

---

## Success vs null

### Success (beyond homo-known candidate)

- Passes all five operational gates above
- Novelty level **N2+** vs tensor polynomial baselines
- Reproducible certificate in `artifacts/certificate.json`
- `EXPERIMENT_REPORT.md` states **COMPUTATIONAL_EVIDENCE** only

### Null result (still valuable)

- High rejection rate with documented reasons (`representation_ratio_fail`, `high_correlation_with_tensor_baseline`, `generative_holdout_fail`)
- Confirms **bounded shadow** for open problems (005, 008) without counterexample
- Calibrates frame (e.g. TDA 006 accepts only graphs far from path baseline)

Null results must be reported honestly — they bound search, they do not prove theorems.

---

## Linked experiments

| ID | Domain | Beyond-homo role |
|----|--------|------------------|
| [NAMM-2026-006](../experiments/NAMM-2026-006/) | `tda_frame` | Frame escalation partner (persistence vs path) |
| [NAMM-2026-007](../experiments/NAMM-2026-007/) | `raw_tensor` | **Primary** beyond-named-math search |
| [NAMM-2026-008](../experiments/NAMM-2026-008/) | `open_problem_shadow` | Graceful Tree finite shadow (T0 tierlist #2) |

See also: [`FRAME_LADDER.md`](FRAME_LADDER.md), [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md), [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md).

---

Roman Kuznetsov · NAMM research program
