# NAMM-2026-007 — Experiment Report

**Domain:** raw tensor (`raw_tensor`)  
**Date:** 2026-08-11  
**Seed:** 2026007  
**Frame:** F3g — beyond homo-known vocabulary  
**Search:** evolutionary (pop 60, 8 generations)  
**Status:** tested-signal — 53 independent tensor invariants

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **53** |
| Rejections | 4 |
| Max Pearson r vs baselines | **0.647** (`mul_t11_t11`) |
| K_A/K_H (bytes/tokens proxy) | 2516/241 ≈ **10.4** |
| Generative holdout | **4/4 families passed** |
| Train order | ≤ 6 |
| Test order | ≤ 8 |

## Research question

Can evolutionary search over ADD/MUL/COMPOSE programs on raw adjacency-derived tensor leaves discover invariants independent of 20+ polynomial baselines, with K_A/K_H ≥ 2 and generative holdout on ≥2 graph families — without named human invariant vocabulary?

## Result

**Yes.** Evolutionary search produced 53 accepted candidates using only numeric tensor leaves (`t0`–`t11`: spectrum + heat-kernel samples). Best candidate `tensor-976e0a7a` has max baseline correlation **r = 0.647** (well below τ = 0.95), K_A/K_H ≈ 10.4, and generative holdout passed on all four held-out families (trees, bipartite, cubic, random_regular).

This directly addresses HL-005 (beyond named vocabulary) and HL-012 (automated independence from 20+ baselines): humans cannot visually detect r = 0.647 independence; the gate pipeline can.

## Best candidate

**ID:** `tensor-976e0a7a`  
**Score (value range):** 4.90×10¹²  
**Novelty:** N2  
**Certificate:** `artifacts/certificate.json`  
**eval_hash:** see certificate

## Rejection breakdown

| Reason | Count |
|--------|-------|
| `representation_ratio_fail` | 2 |
| `high_correlation_with_tensor_baseline` | 2 |

## Honest assessment

Strong **operational signal** for beyond-homo search: banning named invariants does not collapse discovery; independence and holdout gates are enforceable. Remaining risk: some accepted programs may be algebraically reducible beyond Pearson checks — attack checklist O2–O4 not yet signed off.

## Artifacts

- `config.yaml` — experiment parameters
- `artifacts/certificate.json` — primary ground truth
- `artifacts/candidates.jsonl` / `rejections.jsonl`
- `artifacts/human_projection.md` — lossy audit

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-007
python -m pytest tests/test_tensor_domain.py -q
```

## Strategy link

[`docs/BEYOND_HOMO_STRATEGY.md`](../../docs/BEYOND_HOMO_STRATEGY.md)

---

Roman Kuznetsov · NAMM research program
