# NAMM-2026-007 — Raw Tensor Invariants (Beyond Named Math)

**Domain:** `raw_tensor`  
**Frame:** F3g — beyond named-invariant vocabulary  
**Strategy:** [`docs/ANTHEMIUM_NAMM_SYNERGY.md`](../../docs/ANTHEMIUM_NAMM_SYNERGY.md)

## Run

```bash
python -m namm.cli run-experiment --id NAMM-2026-007
python -m pytest tests/test_tensor_domain.py -q
```

## Gates

- No named invariants (wiener, degree_sum, etc.) in search vocabulary
- Independence vs 20+ tensor polynomial baselines (degree ≤4)
- K_A/K_H ≥ 2 (representation gate)
- Generative holdout on ≥2 of: trees, bipartite, cubic, random_regular
