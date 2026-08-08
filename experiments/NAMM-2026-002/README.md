# NAMM-2026-002 — String Rewriting Systems

**Domain:** `rewriting` (Phase 2)  
**Status:** null result — protocol exercised, 0 candidates passed all gates

## Quick links

- **Full report:** [EXPERIMENT_REPORT.md](./EXPERIMENT_REPORT.md)
- **Config:** [config.yaml](./config.yaml)
- **Certificate:** [artifacts/certificate.json](./artifacts/certificate.json)

## Research question

Can search discover a confluent string rewriting system on bounded `{a,b}` strings that random rule generation cannot find?

## Reproduction

```bash
python -m pip install -e ".[dev]"
python -m namm.cli run-experiment --id NAMM-2026-002
python -m pytest tests/test_rewriting.py -q
```

See [`docs/AI_NATIVE_NAMM.md`](../../docs/AI_NATIVE_NAMM.md) for certificate-first artifacts.
