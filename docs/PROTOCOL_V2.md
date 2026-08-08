# NAMM Protocol v2

Consolidated operational protocol for NAMM experiments. v2 strengthens rejection criteria, baseline comparison, and negative-result logging — motivated by **NAMM-2026-001**, which accepted a Wiener-dominated linear combination (Pearson \(r \approx 0.938\)) as a “candidate” because non-equivalence alone was too weak.

> **Philosophy (Tegmark / MUH):** see [`PHILOSOPHY.md`](PHILOSOPHY.md). This document is methodology only.

---

## Executable NAMM cycle checklist

Run every cycle in order. Do not skip steps; record pass/fail in the experiment artifact.

| Step | Action | Required output |
|------|--------|-----------------|
| **INPUT** | Select domain, base object, research question | Falsifiable question in experiment config |
| **ABSTRACT** | Extract objects, relations, transforms, invariants | Primitive data section |
| **META-LIFT** | Promote morphisms/rules/logic to next level | Meta-level origin (≥2 levels) |
| **GENERATE** | Construct candidate(s) machine-natively | Canonical serialization + representation metrics |
| **FORMALIZE** | Rigorous definitions, types, semantics | Claims table with status labels |
| **ATTACK** | Run [`ATTACK_CHECKLIST.md`](ATTACK_CHECKLIST.md) | Signed-off checklist; counterexamples logged |
| **VERIFY** | Exhaustive / computational / proof-assistant checks | Certificates in artifacts |
| **COMPARE** | Baselines + prior art + novelty ladder | [`NOVELTY_LADDER.md`](NOVELTY_LADDER.md) level N0–N5 |
| **PROJECT** | Human-readable projection separate from machine form | `HUMAN_PROJECTION.md` |

---

## v2 acceptance gates (hard)

A candidate **fails** the cycle unless all gates pass:

1. **Non-equivalence:** differs from primary baseline on ≥1 graph in the test universe.
2. **Correlation gate:** Pearson \(r \leq \tau\) vs every known baseline on the atlas graph set (default \(\tau = 0.95\), configurable). *NAMM-2026-001 would fail at \(r \approx 0.938\) only if threshold lowered; at 0.95 it passes correlation but fails novelty — see below.*
3. **Prior-art simplify gate:** expression must not sympy-simplify to a known baseline form (wiener, degree_sum, clustering, num_edges, avg_degree).
4. **Novelty floor:** assessed level must be ≥ **N2** (new combination) with honest justification; **N0–N1** are automatic rejections for publication-style claims.
5. **Representation logged:** \(K_A\) proxies recorded per [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md).
6. **Baselines table:** all required baselines from [`BASELINE_PROTOCOL.md`](BASELINE_PROTOCOL.md) run under the **same compute budget** as the candidate generator.
7. **Negative results:** every rejection written to `rejections.jsonl` with reason code.

Gate schema for multi-agent handoff: [`../schemas/gates.json`](../schemas/gates.json).

---

## Status labels (unchanged)

`DEFINITION` · `CONJECTURE` · `LEMMA` · `THEOREM` · `COMPUTATIONAL_EVIDENCE` · `PHILOSOPHICAL_INFERENCE` (philosophy doc only)

---

## Artifact layout

```
experiments/NAMM-YYYY-NNN/
  config.yaml
  EXPERIMENT_REPORT.md
  artifacts/
    candidates.jsonl
    rejections.jsonl      # MUST include correlation & simplify rejections
    result.json
    extended_analysis.json
    HUMAN_PROJECTION.md
```

---

## Quick activation (v2)

Activate **NAMM v2**. Select a formal domain; define primitives; meta-lift ≥2 levels; generate machine-native candidates; log representation metrics; run attack checklist; verify; compare against required baselines with correlation threshold; assign novelty level N0–N5; reject and log negative results; project for humans only after formal stabilization. Do not claim novelty below N3 without external confirmation.
