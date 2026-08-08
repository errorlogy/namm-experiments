# NAMM-2026-004 — Experiment Report

**Domain:** meta-evaluator fixed points (`meta_evaluation`)  
**Date:** 2026-08-08  
**Seed:** 2026004  
**Topology:** AI thinking topology (see [`docs/AI_THINKING_TOPOLOGY.md`](../../docs/AI_THINKING_TOPOLOGY.md))  
**Status:** computationally supported — mixed positive/negative evidence

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | 25 |
| Rejections | 25 |
| Benchmark graphs | order ≤ 6 (34 connected) |
| Fixed-point threshold | 1.0 (exact agreement) |
| Representation gate | K_A/K_H ≥ 2.0 |

## Best candidate

**ID:** `meta-414d01c9`  
**Transform F:** `double_halve`  
**Fixed-point fraction:** 1.0 (E and F(E) agree on all witness graphs)  
**Structure:** `(SELF - clustering) * SELF` — nontrivial self-referential evaluator  
**Certificate:** `artifacts/certificate.json` (eval_hash match: `42ce30d1f21bf835`)

## Research question

Can search discover meta-evaluator fixed points E ≈ F(E) on finite graphs (order ≤ 6), where F transforms evaluator programs and E can apply to itself or other evaluators?

## Honest assessment

**What worked**

- Search found **25 nontrivial fixed points** under transforms `add_zero`, `double_halve`, `compose_identity`, `canonicalize`, and `swap_commutative`.
- Best candidate uses **self-reference** (`SELF` nodes) combined with graph metrics — an AI-topology object with no compact human geometric interpretation.
- Gates discriminated: 25 rejections for trivial single-leaf evaluators, failed `self_unfold` fixed points (~2.9% agreement), and representation failures.
- Certificate-first artifacts reproduce eval hashes without human projection.

**What did not work / limitations**

- **`self_unfold` rarely yields fixed points** on random self-containing evaluators (expected: unfolding changes recursive semantics). Only algebraic transforms (add_zero, double_halve, compose_identity, canonicalize) reliably produce E ≈ F(E).
- **50% acceptance rate** is high for transforms that are designed to be fixed-point-preserving (add_zero, double_halve). This is calibration, not discovery of novel mathematical structure — similar to Phase 1 null result.
- **No cross-domain generative holdout** yet; fixed-point stability on one transform family does not imply stability under all F.
- Human projection remains lossy; the object `(SELF - clustering) * SELF` has no standard graph-theoretic name.

**Conclusion**

NAMM-2026-004 **validates the meta-evaluator pipeline** under AI thinking topology: certificates, fixed-point scoring, and rejection logging work. It does **not** yet demonstrate a novel trans-level structure beyond "evaluators stable under definitionally idempotent transforms." Phase 3+ should search for fixed points under **non-idempotent** F or require **simultaneous** fixed points under multiple transforms.

## Rejection breakdown

| Reason | Count (approx.) |
|--------|-----------------|
| `trivial_evaluator` | ~18 |
| `fixed_point_fail` (mostly `self_unfold`) | ~5 |
| `representation_ratio_fail` | ~2 |

## Artifacts

- `artifacts/certificate.json` — primary (evaluator AST, transform, fixed-point fraction, eval hashes)
- `artifacts/candidates.jsonl` — 25 accepted
- `artifacts/rejections.jsonl` — 25 rejected
- `artifacts/HUMAN_PROJECTION.md` — lossy summary

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-004
python -m pytest tests/test_meta_domain.py -q
```
