# GitHub Actions for NAMM

This folder defines **CI/CD** for the NAMM experiments project. For a research codebase, **CI is the quality gate**; there is no production deployment pipeline. Zenodo archives are uploaded manually — see [`docs/ZENODO_RELEASE.md`](../../docs/ZENODO_RELEASE.md).

## Workflows

| Workflow | File | When it runs | What it does |
|----------|------|--------------|--------------|
| **CI** | `ci.yml` | Every push and pull request to `main` | Installs the package, runs AMAT tests, runs fast pytest (`not llm and not slow`), smoke search, optional ND tests; uploads experiment template artifact on `main` |
| **Scheduled health** | `health.yml` | Weekly (Mon 09:00 UTC) + manual | Same fast pytest + AMAT checks to catch dependency drift |
| **Release** | `release.yml` | Push of tags matching `v*` | Builds sdist/wheel, uploads artifacts, creates GitHub Release |

## What CI does on each push/PR

1. Checks out your code on Ubuntu with Python 3.12.
2. Installs the project in editable mode: `pip install -e ".[dev]"`.
3. Runs **AMAT topology unit tests**: `pytest tests/test_amat_041_037_040.py -m amat`.
4. Runs the **fast test suite**: `pytest tests/ -m "not llm and not slow"`.
5. Runs a **smoke test** — a tiny random search (10 candidates, max order 5).
6. Optional (non-blocking): ND-frame tests with `pip install -e ".[dev,nd]"`.
7. On pushes to `main` only: uploads `experiments/NAMM-2026-001/config.yaml` and `README.md` as a downloadable artifact (30-day retention).

## Pytest markers

Defined in `pyproject.toml`:

| Marker | Meaning | CI default |
|--------|---------|------------|
| `amat` | AMAT pilots 037/040/041 helper tests | **Always run** (explicit step) |
| `llm` | Needs torch/transformers | Skipped |
| `slow` | Long-running searches | Skipped |
| `nd` | Needs gudhi/qutip | Optional job |

Run everything locally (including LLM mock test):

```bash
pip install -e ".[dev,nd,llm-local]"
pytest tests/ -v
```

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

```bash
# From the repository root (after clone)
python -m pip install -e ".[dev]"
python -m pytest tests/test_amat_041_037_040.py -v -m amat
python -m pytest tests/ -v -m "not llm and not slow"
```

Smoke step (same as CI):

```powershell
python -c "from namm.baselines import random_search; from namm.schemas.experiment import ExperimentConfig; c=ExperimentConfig(experiment_id='ci-smoke', max_order=5, num_candidates=10, seed=1); r=random_search(c); assert len(r.candidates)+len(r.rejections)==10; print('Smoke OK')"
```

Or use the full local health script (pytest + full experiment):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\health.ps1
```

## Cutting a release

```bash
git tag -a v0.1.0 -m "NAMM 0.1.0"
git push origin v0.1.0
```

This triggers `release.yml` (sdist + wheel on GitHub Releases). For Zenodo, build the source bundle:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_zenodo_bundle.ps1
```

See [`docs/ZENODO_RELEASE.md`](../../docs/ZENODO_RELEASE.md).

## Adding new tests

1. Add a file under `tests/` named `test_*.py`.
2. Use pytest conventions (`def test_...()`).
3. Add `@pytest.mark.slow`, `@pytest.mark.llm`, or `@pytest.mark.nd` when appropriate.
4. Run `pytest tests/ -v -m "not llm and not slow"` locally before pushing.
5. CI picks up new tests automatically — no workflow change needed unless you add a new marker category.

## Branch protection (recommended for private repo)

In GitHub: **Settings → Branches → Add branch protection rule** for `main`:

- Require a pull request before merging (optional for solo work).
- **Require status checks to pass** — select `Test (Python 3.12)` from CI.
- Do not allow force pushes to `main`.

This ensures every merge keeps tests green.

## Why no full CD?

NAMM is a **research / experiment** project. Outputs are artifacts under `experiments/*/artifacts/`, not a deployed service. CI validates code quality; you run experiments locally or via scheduled health. Full CD (deploy to production) does not apply here.
