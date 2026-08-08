# NAMM Experiments

Minimal runnable prototype for **NAMM Phase 1** — finite graph invariant search.

## Prerequisites

- Python **3.12** at `C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe`

## Setup

```powershell
cd c:\Users\Public\NAMM
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m pip install -e ".[dev]"
```

## Run tests

```powershell
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/ -v
```

## Run first experiment (NAMM-2026-001)

```powershell
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m namm.cli run-experiment --id NAMM-2026-001
```

Or after install, using the console script:

```powershell
namm run-experiment --id NAMM-2026-001
```

Artifacts are written to `experiments/NAMM-2026-001/artifacts/`:

- `candidates.jsonl` — promising invariant candidates
- `rejections.jsonl` — rejected candidates with reasons
- `result.json` — machine-native summary
- `HUMAN_PROJECTION.md` — human-readable summary

## Health loop (Cursor)

Re-run tests + smoke experiment on a schedule:

```text
/loop 30m Run scripts/health.ps1 in c:\Users\Public\NAMM; fix any failures.
```

Or manually:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\health.ps1
```

## Verify a candidate

```powershell
namm verify --expr "2*num_edges + 1*clustering" --baseline "1*wiener_index"
```

## Project layout

```
src/namm/           Core library (schemas, graph domain, verifiers, baselines, CLI)
experiments/        Per-experiment config and artifacts
tests/              pytest suite
prompts/            NAMM protocol prompts (from research repo)
```

See `NAMM_PROTOCOL.md` and `prompts/` for the full discovery protocol.

## CI/CD (GitHub Actions)

Every push and pull request to `main` runs CI:

- `pip install -e ".[dev]"`
- `pytest tests/ -v`
- Lightweight smoke search (10 candidates)

A weekly scheduled workflow re-runs pytest on `main`. There is no production deployment — CI is the quality gate before merge.

**Run the same checks locally:**

```powershell
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

Details: [`.github/workflows/README.md`](.github/workflows/README.md)
