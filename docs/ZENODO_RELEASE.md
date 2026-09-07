# Zenodo release checklist

This repository publishes software snapshots to [Zenodo](https://zenodo.org). GitHub Actions validates code and builds Python packages; **you upload the Zenodo bundle manually**.

**Sibling deposit (EIA, already published):** [https://zenodo.org/records/22646895](https://zenodo.org/records/22646895) — Endogenous Initiative Architecture  
**NAMM deposit:** create a **new upload** (separate concept DOI); link to EIA via *related identifier* (`is related to`)

---

## Current bundle (ready to upload)

| Field | Value |
|-------|-------|
| **File** | `dist/namm-experiments-0.2.0.tar.gz` |
| **Version** | 0.2.0 |
| **Size** | 560 371 bytes (0.53 MB) |
| **SHA256** | `5F7A811DB1D49D422D2FD7C0826A37565BEF326A22858256C5654E0A74BCBC18` |
| **Entries** | 527 paths |
| **Built on** | 2026-09-07 |
| **Branch** | `hypothesis/cognitive-antigravity` |

Verify locally:

```powershell
Get-FileHash dist/namm-experiments-0.2.0.tar.gz -Algorithm SHA256
```

Manifest of included paths (generated at build time): `dist/ZENODO_FILES.txt`.

Inside the archive: `ZENODO_README.txt` explains what this deposit is vs. the sibling EIA program.

---

## Before you release

1. Merge to `main` with green CI (`pytest`, AMAT smoke, smoke search) — optional for a branch snapshot but recommended before publishing a versioned DOI.
2. Update version in `pyproject.toml` and `CITATION.cff` (keep them aligned).
3. Set `date-released` in `CITATION.cff` to the publication date.
4. After Zenodo assigns a **version-specific** DOI, add it under `identifiers` in `CITATION.cff` and the badge/link in `README.md`.
5. Commit version bumps on your release branch.

---

## Build the Zenodo source bundle

The bundle is a **clean source tarball** (no `.git`, logs, or experiment artifacts).

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_zenodo_bundle.ps1 -Version v0.2.0
```

### Linux / macOS

```bash
bash scripts/build_zenodo_bundle.sh 0.2.0
```

**Output (Windows / primary):** `dist/namm-experiments-<version>.tar.gz`  
**Output (Linux/macOS script):** `dist/namm-experiments-v<version>-zenodo.zip`

After building, regenerate the path manifest:

```powershell
tar -tzf dist/namm-experiments-0.2.0.tar.gz | Out-File -Encoding utf8 dist/ZENODO_FILES.txt
Get-FileHash dist/namm-experiments-0.2.0.tar.gz -Algorithm SHA256
```

### What is included

| Path | Contents |
|------|----------|
| `src/` | NAMM Python package |
| `docs/` | Protocol and research documentation |
| `schemas/` | JSON schemas for certificates and results |
| `experiments/NAMM-*/` | Experiment scaffolds (`config.yaml`, `run_experiment.py`, `README.md`) |
| `tests/` | Test suite |
| `LICENSE`, `CITATION.cff`, `README.md` | Legal, citation, overview |
| `ZENODO_README.txt` | Deposit description (NAMM vs EIA) |
| `.zenodo.json` | Zenodo metadata template |

### What is excluded

| Pattern | Reason |
|---------|--------|
| `.git/` | Not part of the archive |
| `experiments/*/artifacts/` | Generated experiment outputs |
| `experiments/**/*.log`, `run_*.log` | Local run logs |
| `experiments/**/_scratch/` | Scratch workspaces |
| `.venv/`, `venv/`, `__pycache__/` | Local environment |
| `dist/`, `build/`, `*.egg-info/` | Build products |
| `.env`, `.env.*` | Secrets |
| `external/` | Vendored upstream clones |
| `*.pdf` (repo root), `README(4).md` | Ad-hoc downloads / accidental duplicates |
| `pytest_followup.txt`, `experiments/REPO_AUDIT_DRAFT.md` | Local scratch notes |

Re-run the script after changing the version string in `pyproject.toml`.

---

## Upload to Zenodo (recommended: new NAMM deposit)

**Do not** use *New version* on [22646895](https://zenodo.org/records/22646895) unless that record is explicitly the NAMM concept deposit. If 22646895 is the **EIA** release (as published today), NAMM needs its **own** upload.

1. Sign in at [zenodo.org](https://zenodo.org) → **Upload** → **New upload**.
2. **Upload** `dist/namm-experiments-0.2.0.tar.gz`.
3. Metadata (or sync from `.zenodo.json`):
   - **Title:** Non-Anthropic Mathematics Mode (NAMM) — verification-first machine-native math discovery
   - **Version:** 0.2.0
   - **Authors:** Roman Kuznetsov (Anthemium)
   - **Description:** Protocol v2 tooling, Sci Flow, experiment scaffolds, AMAT pilots 037–041 with tiered certificates and documented falsifications (incl. D_eff null). See `ZENODO_README.txt` inside the archive.
   - **License:** CC-BY-4.0
   - **Related identifier:** `10.5281/zenodo.22646895` (EIA sibling program; relation: *is related to*)
   - **Related identifier:** `https://github.com/errorlogy/namm-experiments` (relation: *is supplement to*)
4. **Publish** → copy the new **concept DOI** and **version DOI** into `CITATION.cff` and `README.md`.

### New version (only if NAMM already has its own concept DOI)

If you already created a separate NAMM concept record: open that deposit → **New version** → upload the same tarball → publish → update version-specific DOI in `CITATION.cff`.

---

## Verify the bundle

```powershell
# List contents
tar -tzf dist/namm-experiments-0.2.0.tar.gz | Select-Object -First 20

# Confirm exclusions (should return nothing)
tar -tzf dist/namm-experiments-0.2.0.tar.gz | Select-String '\.git/|artifacts/|_scratch|\.env|run\.log'

# Smoke test (extract first)
tar -xzf dist/namm-experiments-0.2.0.tar.gz -C $env:TEMP\namm-zenodo-test
cd $env:TEMP\namm-zenodo-test
python -m pip install -e .
python -m pytest tests/test_amat_041_037_040.py -v
```

---

## Cut a Git tag (optional)

Tags trigger `.github/workflows/release.yml`, which builds `sdist` + `wheel` and attaches them to a GitHub Release. **Not required** for Zenodo upload.

```bash
git tag -a v0.2.0 -m "NAMM 0.2.0 — AMAT pilots 037–041"
git push origin v0.2.0
```

---

## GitHub ↔ Zenodo (optional automation)

Enable [Zenodo–GitHub integration](https://docs.zenodo.org/guides/github-release-zenodo/) on the repository to auto-archive GitHub Releases. This repo still documents the manual bundle for reproducibility when you need to exclude logs and artifacts explicitly.

Metadata template: [`.zenodo.json`](../.zenodo.json) at the repository root.
