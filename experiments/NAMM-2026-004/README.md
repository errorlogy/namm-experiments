# NAMM-2026-004 — Trans-Level Meta-Evaluators (Scaffold)

**Status:** documentation only — not yet implemented  
**Domain:** `meta_evaluation` (proposed)

---

## Research question

Can we build **evaluators that score other evaluators** — measuring whether a discovery pipeline's gates (independence, representation ratio, generative holdout) discriminate signal from noise across domains, without human judgment in the loop?

This is a **trans-level** experiment: the object of study is not graph invariants or rewriting systems, but the **meta-metrics** that accept or reject candidates in NAMM-2026-001 through 003.

---

## Proposed design (future)

| Component | Role |
|-----------|------|
| **Evaluator registry** | Catalog of gate functions (`reject_if_correlated`, `reject_if_low_compression_asymmetry`, `generative_holdout_score`) |
| **Synthetic candidates** | Known-positive and known-negative fixtures per domain |
| **Meta-score** | True-positive rate, false-positive rate, calibration vs held-out synthetic set |
| **Certificate** | `meta_certificate.json` with gate ROC-style summary and seed |

---

## Dependencies

- Stable artifacts from NAMM-2026-001 (null baseline), 002 (rewriting), 003 (program AST)
- [`docs/RESEARCH_DIRECTION.md`](../../docs/RESEARCH_DIRECTION.md) — Phase 4 roadmap

---

## Not in scope (this scaffold)

- No `config.yaml` or CLI runner yet
- No production code under `src/namm/domains/meta/`

When implemented, this experiment will **not** replace domain experiments; it audits whether our gates generalize.

---

## Author

Roman Kuznetsov · NAMM research program
