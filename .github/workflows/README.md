# GitHub Actions for NAMM

This folder defines **CI/CD** for the NAMM experiments project. For a research codebase, **CI is the quality gate**; there is no production deployment pipeline.

## Workflows

| Workflow | File | When it runs | What it does |
|----------|------|--------------|--------------|
| **CI** | `ci.yml` | Every push and pull request to `main` | Installs the package, runs full `pytest`, runs AMAT unit tests explicitly, smoke search (10 candidates), uploads experiment template artifact on `main` |
| **Scheduled health** | `health.yml` | Weekly (Mon 09:00 UTC) + manual | Runs `pytest` to catch dependency drift |
| **Release** | `release.yml` | Push tag `v*` (e.g. `v0.2.0`) | Full pytest, Zenodo tarball via `build_zenodo_bundle.ps1`, CI artifact, GitHub Release |

## What CI does on each push/PR

1. Checks out your code on Ubuntu with Python 3.12.
2. Installs the project in editable mode: `pip install -e ".[dev]"`.
3. Runs the full test suite: `pytest tests/ -v`.
4. Runs **AMAT unit tests** explicitly (cusp, Lyapunov, H¹, fractal TDA, information geometry) — no GPU or live LLM keys required.
5. Runs a **smoke test** — a tiny random search (10 candidates, max order 5) to verify the experiment pipeline without running the full 50-candidate experiment.
6. On pushes to `main` only: uploads `experiments/NAMM-2026-001/config.yaml` and `README.md` as a downloadable artifact (30-day retention).

## Release workflow (tags)

When you push a version tag:

```bash
git tag -a v0.2.0 -m "NAMM 0.2.0"
git push origin v0.2.0
```

The release job:

1. Runs the full pytest suite.
2. Builds `dist/namm-experiments-0.2.0.tar.gz` via `scripts/build_zenodo_bundle.ps1` (excludes `.git`, logs, `artifacts/`, scratch).
3. Uploads the tarball as a 90-day Actions artifact.
4. Creates a GitHub Release with the tarball attached.

**Zenodo upload is manual.** Follow [`docs/ZENODO_RELEASE.md`](../docs/ZENODO_RELEASE.md). Deposit: [22646895](https://zenodo.org/records/22646895).

## Pytest markers

Defined in `pyproject.toml`:

| Marker | Use |
|--------|-----|
| `slow` | Long-running tests — skip in quick loops with `pytest -m "not slow"` |
| `llm` | Tests needing live LLM keys or local GPU models |

CI runs the default suite (AMAT helpers are pure unit tests and always run).

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
python -m pytest tests/ -v
pytest tests/test_amat_041_037_040.py tests/test_catastrophe.py -v
```

Smoke step (same as CI):

```powershell
python -c "from namm.baselines import random_search; from namm.schemas.experiment import ExperimentConfig; c=ExperimentConfig(experiment_id='ci-smoke', max_order=5, num_candidates=10, seed=1); r=random_search(c); assert len(r.candidates)+len(r.rejections)==10; print('Smoke OK')"
```

Or use the full local health script (pytest + full experiment):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\health.ps1
```

Zenodo bundle (local):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_zenodo_bundle.ps1
```

## Adding new tests

1. Add a file under `tests/` named `test_*.py`.
2. Use pytest conventions (`def test_...()`).
3. Mark slow or LLM-dependent tests with `@pytest.mark.slow` or `@pytest.mark.llm`.
4. Run `pytest tests/ -v` locally before pushing.
5. CI picks up new tests automatically — no workflow change needed unless they require secrets.

## Branch protection (recommended for private repo)

In GitHub: **Settings → Branches → Add branch protection rule** for `main`:

- Require a pull request before merging (optional for solo work).
- **Require status checks to pass** — select `Test (Python 3.12)` from CI.
- Do not allow force pushes to `main`.

This ensures every merge keeps tests green.

## Why no deploy CD?

NAMM is a **research / experiment** project. Outputs are artifacts under `experiments/*/artifacts/`, not a deployed service. CI validates code quality; release CD publishes a source bundle for Zenodo and GitHub Releases, not a running service.
