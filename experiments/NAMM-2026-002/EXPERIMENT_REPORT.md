# NAMM-2026-002 — Experiment Report

**Domain:** string rewriting (`rewriting`)  
**Date:** 2026-08-08  
**Seed:** 2026  
**Status:** honest null result

## Summary

| Metric | Value |
|--------|-------|
| Candidates | 0 |
| Rejections | 40 |
| Confluence threshold | 1.0 (full confluence) |
| Max string length | 6 |
| Representation gate | K_A/K_H ≥ 2.0 |

## Research question

Can search discover a confluent string rewriting system on bounded `{a,b}` strings that random rule generation cannot find?

## Result

**No candidates accepted.** All 40 generated systems (random rules + mutations of known confluent seeds) failed at least one gate:

| Rejection reason | Count |
|------------------|-------|
| `confluence_fail` | 20 |
| `does_not_exceed_random_baseline` | 11 |
| `normalization_fail` | 9 |

This is an **honest null**: under strict confluence + normalization + random-baseline comparison, novel confluent TRS were not discovered in this budget. Known confluent baseline (`ba→ab`) remains the reference.

## Methodology

- Generator: `src/namm/domains/rewriting/` (rules, evaluator, baseline, serializer)
- Search: ⅓ mutations of known confluent systems, ⅔ random rules
- Certificate-first: `certificate.json` written before human projection when candidates exist
- Gates: confluence score = 1.0, normalization, beats random baseline sample, not duplicate of known system hash

## Artifacts

- `artifacts/rejections.jsonl` — full rejection log
- `artifacts/candidates.jsonl` — empty
- `artifacts/result.json` — machine summary

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-002
```
