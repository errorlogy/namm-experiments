# Baseline Protocol

Required baselines and the **same budget rule** for fair comparison.

## Same budget rule

Every baseline strategy must receive the **same** compute budget as the candidate generator:

| Resource | Must match |
|----------|------------|
| `num_candidates` | Equal trial count |
| `max_order` | Same graph universe |
| `seed` | Documented; vary seeds for robustness checks |
| Wall-clock cap | Document in reproduction section |
| Graph enumeration | Same `enumerate_small_graphs` / atlas policy |

Do not compare a 50-candidate random search against a single hand-tuned formula without equalizing trials.

---

## Required baselines (graph domain, Phase 1)

| ID | Expression / method | Role |
|----|---------------------|------|
| `wiener_index` | `1*wiener_index` | Primary non-equivalence target |
| `degree_sum` | `2*num_edges` | Degree redundancy check |
| `avg_degree` | `1*avg_degree` | Redundancy with num_edges |
| `clustering` | `1*clustering` | Transitivity baseline |
| `algebraic_connectivity` | `1*algebraic_connectivity` | Spectral family |
| `wiener_plus_edges` | `1*wiener_index + 1*num_edges` | Simple combo |
| `wiener_plus_clustering` | `1*wiener_index + 1*clustering` | Simple combo |
| `2x_wiener` | `2*wiener_index` | Scalar multiple |
| `diameter` | `1*diameter` | Distance family |
| `radius` | `1*radius` | Distance family |
| `random_search` | `random_invariant_formula` × N | Generator baseline |

---

## Reporting

Populate the **Baselines table** in `EXPERIMENT_TEMPLATE.md`:

| Baseline | Equivalent? | Pearson r | Same budget? |
|----------|-------------|-----------|--------------|
| wiener_index | no | 0.938 | yes |

Store structured results in `baseline_results` on each candidate record and in `extended_analysis.json`.

---

## Correlation threshold

Default rejection: Pearson \(r > 0.95\) vs any row in the table on the **atlas graph set** (connected graphs, order ≤ `correlation_atlas_order`, default 6).

Configure per experiment in `config.yaml`:

```yaml
correlation_threshold: 0.95
correlation_atlas_order: 6
```
