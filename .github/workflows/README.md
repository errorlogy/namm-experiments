# GitHub Actions for NAMM

This folder defines **CI/CD** for the NAMM experiments project. For a research codebase, **CI is the quality gate**; there is no production deployment pipeline.

## Workflows

| Workflow | File | When it runs | What it does |
|----------|------|--------------|--------------|
| **CI** | `ci.yml` | Every push and pull request to `main` | Installs the package, runs `pytest`, runs a lightweight smoke search (10 candidates), uploads experiment template artifact on `main` |
| **Scheduled health** | `health.yml` | Weekly (Mon 09:00 UTC) + manual | Runs `pytest` to catch dependency drift |

## What CI does on each push/PR

1. Checks out your code on Ubuntu with Python 3.12.
2. Installs the project in editable mode: `pip install -e ".[dev]"`.
3. Runs the full test suite: `pytest tests/ -v`.
4. Runs a **smoke test** — a tiny random search (10 candidates, max order 5) to verify the experiment pipeline without running the full 50-candidate experiment.
5. On pushes to `main` only: uploads `experiments/NAMM-2026-001/config.yaml` and `README.md` as a downloadable artifact (30-day retention).

## How to read failed checks

1. Open the pull request or commit on GitHub.
2. Click the red **X** or **Details** next to the failing check (e.g. "Test (Python 3.12)").
3. Expand the failed step in the log — pytest failures show file, test name, and assertion.
4. Reproduce locally (see below), fix, commit, and push.

Common failures:

- **Import errors** — missing dependency in `pyproject.toml` or wrong `pythonpath`.
- **pytest failures** — logic or schema change broke a test; update code or test intentionally.
- **Smoke test assertion** — experiment config or `random_search` behavior changed.

## Run CI locally (mimic GitHub Actions)

```powershell
cd c:\Users\Public\NAMM
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

Smoke step (same as CI):

```powershell
python -c "from namm.baselines import random_search; from namm.schemas.experiment import ExperimentConfig; c=ExperimentConfig(experiment_id='ci-smoke', max_order=5, num_candidates=10, seed=1); r=random_search(c); assert len(r.candidates)+len(r.rejections)==10; print('Smoke OK')"
```

Or use the full local health script (pytest + full experiment):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\health.ps1
```

## Adding new tests

1. Add a file under `tests/` named `test_*.py`.
2. Use pytest conventions (`def test_...()`).
3. Run `pytest tests/ -v` locally before pushing.
4. CI picks up new tests automatically — no workflow change needed.

## Branch protection (recommended for private repo)

In GitHub: **Settings → Branches → Add branch protection rule** for `main`:

- Require a pull request before merging (optional for solo work).
- **Require status checks to pass** — select `Test (Python 3.12)` from CI.
- Do not allow force pushes to `main`.

This ensures every merge keeps tests green.

## Why no full CD?

NAMM is a **research / experiment** project. Outputs are artifacts under `experiments/*/artifacts/`, not a deployed service. CI validates code quality; you run experiments locally or via scheduled health. Full CD (deploy to production) does not apply here.
