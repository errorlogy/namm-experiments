# NAMM-2026-003 — Experiment Report

**Domain:** program AST synthesis (`program_ast`, Graph → Int)  
**Date:** 2026-08-08  
**Seed:** 2026  
**Search:** evolutionary (population 40, 5 generations)  
**Status:** computationally supported

## Summary

| Metric | Value |
|--------|-------|
| Candidates | 33 |
| Rejections | 6 |
| Search strategy | `evolutionary` |
| Representation gate | K_A/K_H ≥ 2.0 |
| Held-out families | trees, bipartite, cubic |

## Best candidate

**ID:** `prog-8be513cb`  
**Score:** high value-range on test graphs (see `result.json`)  
**Certificate:** `artifacts/certificate.json` (primary artifact)

Sympy is used **only** for equivalence checking against baselines (`namm.domains.program.equivalence`).

## Research question

Can evolutionary AST program synthesis discover a graph invariant whose canonical representation is a verified program tree, passes independence gates vs known baselines, and shows generative power on held-out graph families?

## Result

**33 candidates accepted** out of 40 evolutionary individuals. Six rejected for: Wiener equivalence, high correlation, generative holdout failure, or representation ratio.

Evolutionary search (single population run, deduplicated to 40 individuals) outperformed pure random AST generation for finding diverse invariant programs passing v2 gates.

## Gates passed (best candidate)

- Non-equivalence vs Wiener (exact eval + sympy)
- Independence: Pearson r ≤ 0.95 vs baselines
- Generative holdout on trees / bipartite / cubic
- Representation asymmetry K_A/K_H ≥ 2

## Artifacts

- `artifacts/certificate.json` — canonical AST, eval hash, witness bounds
- `artifacts/candidates.jsonl` — 33 accepted candidates
- `artifacts/rejections.jsonl` — 6 rejections
- `artifacts/HUMAN_PROJECTION.md` — lossy human summary

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-003
python -m pytest tests/test_program_search.py tests/test_program_equivalence.py -q
```
