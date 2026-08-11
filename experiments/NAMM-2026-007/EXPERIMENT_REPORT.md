# NAMM-2026-007 — Experiment Report

**Domain:** raw tensor (`raw_tensor`)  
**Date:** 2026-08-11  
**Seed:** 2026007  
**Frame:** F3g — beyond named-invariant vocabulary  
**Status:** **53 candidates accepted**

## Summary

| Metric | Value |
|--------|-------|
| Candidates accepted | **53** |
| Rejections | **4** |
| Search | evolutionary (60×8 pop, 120 returned) |
| Tensor leaves | 12 (8 spectrum + 4 heat-kernel) |
| Baseline polynomials | 20+ (degree ≤4) |
| Representation gate | K_A/K_H ≥ 2.0 |

## Best candidate

**ID:** `tensor-639c54cd`  
**AST hash:** see `artifacts/certificate.json`  
**Score (value range):** 4.90×10¹²  
**Novelty:** **N2** (independent of tensor polynomial baselines)  
**Max Pearson r vs baselines:** 0.647 (`mul_t11_t11`)  
**K_A/K_H proxy:** gzip **213 B** / projection **≈97 tokens** → ratio **≈2.2**  
**Generative holdout:** **passed** — all 4 families (trees, bipartite, cubic, random_regular)  
**Certificate:** `artifacts/certificate.json`

## Rejection breakdown (4)

| Reason | Count |
|--------|-------|
| `high_correlation_with_tensor_baseline` | 2 |
| `generative_holdout_fail` | 2 |

## Novelty assessment

The best candidate is a **deep ADD/MUL composition** over raw tensor indices (`t0`, `t3`, `t6`, `t8`–`t11`) with **no named human invariants** in the search vocabulary. It is **not** in the span of degree-≤4 tensor polynomial baselines (max |r| = 0.65 ≪ 0.95 threshold) and passes generative holdout on all four families.

**Caveat:** Large numeric range suggests sensitivity to spectrum/heat scale — certificate is ground truth; human projection is lossy. **COMPUTATIONAL_EVIDENCE** only; not a published graph invariant theorem.

## Reproduction

```bash
python -m namm.cli run-experiment --id NAMM-2026-007
python -m pytest tests/test_tensor_domain.py -q
```

## Strategy link

[`docs/ANTHEMIUM_NAMM_SYNERGY.md`](../../docs/ANTHEMIUM_NAMM_SYNERGY.md)

---

Roman Kuznetsov · NAMM research program
