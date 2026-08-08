# Representation Metrics (K_A / K_H proxies)

Operational proxies for representational complexity from NAMM §2. Full Kolmogorov complexity is uncomputable; use these ** reproducible** metrics on every candidate.

## Machine complexity \(K_A\) proxies

Computed by `namm.metrics.representation.compute_representation_metrics`:

| Metric | Definition | Use |
|--------|------------|-----|
| `json_bytes` | Byte length of canonical orjson serialization | Structural size |
| `gzip_bytes` | gzip(orjson(payload)) | Compressibility / effective complexity |
| `eval_time_ms` | Mean evaluation time over reference graphs | Computational cost |
| `token_count_estimate` | Heuristic word-split count on expression string | Rough human-token proxy |

## Human complexity \(K_H\) projection

For Phase 1, estimate human load as:

\[
K_H^{\mathrm{proxy}} \approx \texttt{token\_count\_estimate} \times c_{\mathrm{human}}
\]

where \(c_{\mathrm{human}}\) is documented per experiment (default: interpret each token as one primitive or operator the reader must hold in working memory).

**Non-anthropic signal:** candidates where `gzip_bytes` is small but `eval_time_ms` is large, or where \(K_H^{\mathrm{proxy}} \gg K_A\) via gzip, warrant explicit discussion in the human projection.

---

## Canonical payload

```json
{
  "expression": "2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering",
  "primitives": ["avg_degree", "wiener_index", "num_edges", "clustering"],
  "meta_origin": "random_composition_of_graph_statistics"
}
```

---

## Example (NAMM-2026-001 best candidate)

Typical values (order ≤ 6 atlas, 5 reference graphs):

- `json_bytes`: ~180–220
- `gzip_bytes`: ~140–180
- `eval_time_ms`: < 1 ms per graph (Python AST)
- `token_count_estimate`: ~15–20

These do **not** alone establish novelty; they document machine-native compactness vs human reading cost.
