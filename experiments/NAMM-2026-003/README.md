# NAMM-2026-003 — Program Synthesis (Graph → Int AST)

**Domain:** `program_ast` with evolutionary search  
**Status:** computationally supported

## Quick links

- **Full report:** [EXPERIMENT_REPORT.md](./EXPERIMENT_REPORT.md)
- **Config:** [config.yaml](./config.yaml)
- **Certificate:** [artifacts/certificate.json](./artifacts/certificate.json)

## Research question

Can evolutionary AST program synthesis discover a graph invariant whose canonical representation is a verified program tree, passes independence gates, and shows generative power on held-out graph families?

## Reproduction

```bash
python -m pip install -e ".[dev]"
python -m namm.cli run-experiment --id NAMM-2026-003
python -m pytest tests/test_program_search.py tests/test_generative.py -q
```

Sympy is used **only** for equivalence checking against baselines. See [`docs/AI_NATIVE_NAMM.md`](../../docs/AI_NATIVE_NAMM.md).
