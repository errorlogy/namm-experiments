# AI-Native NAMM

AI-first discovery principles for NAMM Phase 2. This document extends [Protocol v2](PROTOCOL_V2.md); it does not replace baseline or novelty gates.

## North star

> Discover structures whose canonical representation is a verified program, not a formula; whose human explanation is longer and lossier than the machine artifact; and which predict behavior on families no named invariant spans.

Success is measured by **compression asymmetry** \(K_A \ll K_H\): the machine-native certificate is smaller and more precise than any human projection; **independence** from known baselines (Pearson \(r \leq \tau\)); and **generative power** on held-out graph families not used during search.

---

## What changed from human-adjacent graph formulas

| Aspect | Phase 1 (graph string) | Phase 2 (program AST) |
|--------|------------------------|------------------------|
| Canonical artifact | Linear expression string (`2*wiener_index + …`) | Verified program tree (JSON AST) |
| Generator | Coefficient × primitive strings | Random AST with depth/operator limits |
| Evaluation | Python `ast.parse` on strings | Structured interpreter over AST nodes |
| Human form | Often shorter than machine (misleading) | Explicitly secondary, lossy projection |
| Certificate | `result.json` summary | `certificate.json` (AST hash, eval witness, seeds) |

Phase 1 remains supported as `domain: graph_string` (alias `finite_graphs`) for reproducibility of NAMM-2026-001.

---

## Certificate-first artifacts

Primary artifact for AI-native runs:

```
artifacts/certificate.json
```

Contains:

- `canonical_ast` — sorted commutative ops, stable hash
- `eval_hash` — digest of values on reference graph set
- `witness_bounds` — order range, graph count, family coverage
- `seeds` — generator and experiment seeds
- `representation_metrics` — json_bytes, gzip_bytes, eval_time_ms, projection_token_estimate

Secondary artifact:

```
artifacts/human_projection.md
```

Auto-generated lossy description. May include: *"Trust certificate; full object in certificate.json."*

Human projection is **optional** for machine-to-machine handoff and **trust-only** for humans auditing results without re-running the evaluator.

---

## When human projection is optional / trust-only

1. **Multi-agent pipelines:** agents consume `certificate.json` and re-evaluate; projection is not parsed.
2. **Verification:** eval hash and canonical AST hash are the ground truth.
3. **Publication:** human projection may appear in reports but must not be the only reproducible artifact.
4. **Lossy by design:** projection omits node IDs, sort order, and witness details present in the certificate.

---

## Independence and generative power

- **Representation gate:** reject candidates with \(K_A/K_H < \tau\) (default \(\tau = 2\); gzip bytes / projection tokens). Configurable via `representation_ratio_threshold` in experiment config. See `namm.metrics.representation.reject_if_low_compression_asymmetry`.
- **Independence:** reject candidates with Pearson \(r > \tau\) vs any baseline on the atlas (default \(\tau = 0.95\)). See `namm.metrics.independence`.
- **Generative power:** search on connected graphs order \(\leq 6\); require non-trivial score on held-out families (trees, bipartite, cubic). See `namm.metrics.generative`.

---

## Experiment domains

| Config value | Description |
|--------------|-------------|
| `graph_string` / `finite_graphs` | Phase 1 string formulas (NAMM-2026-001) |
| `rewriting` | Phase 2a string rewriting systems (NAMM-2026-002) |
| `program_ast` | Phase 2b AST programs with evolutionary search (NAMM-2026-003) |
| `meta_evaluation` | Phase 3 meta-evaluator fixed points E ≈ F(E) (NAMM-2026-004) |

---

## Related docs

- [PROTOCOL_V2.md](PROTOCOL_V2.md) — acceptance gates
- [REPRESENTATION_METRICS.md](REPRESENTATION_METRICS.md) — \(K_A\) proxies
- [NOVELTY_LADDER.md](NOVELTY_LADDER.md) — N0–N5 assignment
