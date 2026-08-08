# NAMM-2026-002 — AI-Native Program AST Search

**Domain:** `program_ast` (Phase 2)  
**Status:** computationally supported (first AI-native NAMM cycle)

## Quick links

- **Full report:** [EXPERIMENT_REPORT.md](./EXPERIMENT_REPORT.md)
- **Config:** [config.yaml](./config.yaml)
- **Certificate:** [artifacts/certificate.json](./artifacts/certificate.json)
- **Human projection:** [artifacts/HUMAN_PROJECTION.md](./artifacts/HUMAN_PROJECTION.md)

## Best candidate

`prog-17644c1d` — `((num_edges² − algebraic_connectivity) × degree_sum)`  
Score 5447.50, novelty N2, generative holdout passed (trees/bipartite/cubic). K_A/K_H proxy ≈ 277/132.

## Research question

Can random AST program synthesis discover a graph invariant whose canonical representation is a verified program tree, passes independence gates vs known baselines, and shows generative power on held-out graph families (trees, bipartite, cubic)?

## Reproduction

```bash
# From the repository root
python -m pip install -e ".[dev]"
python -m namm.cli run-experiment --id NAMM-2026-002
python -m pytest tests/test_program_search.py tests/test_generative.py -q
```

See [`docs/AI_NATIVE_NAMM.md`](../../docs/AI_NATIVE_NAMM.md) for certificate-first artifacts and Phase 2 methodology.
