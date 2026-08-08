# NAMM Experiments

Minimal runnable prototype for **NAMM Phase 1** — finite graph invariant search.

**Protocol v2:** operational methodology, acceptance gates, and novelty ladder are in [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md). Philosophy (MUH/Tegmark) is isolated in [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md).

**AI-native Phase 2:** program AST domain, certificates, and independence/generative gates — see [`docs/AI_NATIVE_NAMM.md`](docs/AI_NATIVE_NAMM.md).

## Clone and run

Requires **Python 3.12+**. From the project root (after cloning):

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

On Windows you can use `py -3.12` instead of `python` if multiple versions are installed.

## Run first experiment (NAMM-2026-001)

```bash
python -m namm.cli run-experiment --id NAMM-2026-001
```

Or after install, using the console script:

```bash
namm run-experiment --id NAMM-2026-001
```

Artifacts are written to `experiments/NAMM-2026-001/artifacts/`:

- `candidates.jsonl` — promising invariant candidates
- `rejections.jsonl` — rejected candidates with reasons
- `result.json` — machine-native summary
- `HUMAN_PROJECTION.md` — human-readable summary

## Run AI-native experiment (NAMM-2026-002)

```bash
python -m namm.cli run-experiment --id NAMM-2026-002
```

Produces `certificate.json` plus human projection (see AI-native docs).

## Health loop (Cursor)

Re-run tests + smoke experiment on a schedule:

```text
/loop 30m Run scripts/health.ps1 from the project root; fix any failures.
```

Or manually (Windows PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/health.ps1
```

Cross-platform equivalent:

```bash
python -m pytest tests/ -q
python -m namm.cli run-experiment --id NAMM-2026-001
```

## Verify a candidate

```bash
namm verify --expr "2*num_edges + 1*clustering" --baseline "1*wiener_index"
```

## Project layout

```
src/namm/           Core library (schemas, graph domain, verifiers, baselines, CLI)
experiments/        Per-experiment config and artifacts
tests/              pytest suite
prompts/            NAMM protocol prompts (from research repo)
```

See `NAMM_PROTOCOL.md`, [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md), and `prompts/` for the discovery protocol.

## CI/CD (GitHub Actions)

Every push and pull request to `main` runs CI:

- `pip install -e ".[dev]"`
- `pytest tests/ -v`
- Lightweight smoke search (10 candidates)

A weekly scheduled workflow re-runs pytest on `main`. There is no production deployment — CI is the quality gate before merge.

**Run the same checks locally:**

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

Details: [`.github/workflows/README.md`](.github/workflows/README.md)
