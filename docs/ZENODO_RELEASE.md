# Zenodo release checklist

**Deposit:** [Zenodo record 22646895](https://zenodo.org/records/22646895) (sibling EIA concept record; NAMM uploads new versions here per [`CITATION.cff`](../CITATION.cff))  
**Concept DOI:** `10.5281/zenodo.22646895`  
**Citation source of truth:** [`CITATION.cff`](../CITATION.cff) (currently `version: 0.2.0`, `date-released: 2026-09-07`)  
**Article outline:** [`NAMM_ARTICLE_OUTLINE.md`](NAMM_ARTICLE_OUTLINE.md)

This document describes how to cut a versioned release aligned with Zenodo and `.github/workflows/release.yml`.

---

## Metadata alignment (CITATION.cff ↔ Zenodo)

Before uploading a new Zenodo version, verify these fields match between [`CITATION.cff`](../CITATION.cff) and the deposit form:

| Field | CITATION.cff key | Zenodo form |
|-------|------------------|-------------|
| Title | `title` | Title |
| Version | `version` | Version |
| Release date | `date-released` | Publication date |
| Authors | `authors` | Creators |
| Abstract | `abstract` | Description |
| Keywords | `keywords` | Keywords |
| License | `license` | License (CC-BY-4.0) |
| Code repository | `repository-code` / `url` | Related identifiers → URL |
| Resource type | `type: software` | Upload type → Software |

After publish, cite the **version-specific** DOI Zenodo mints (e.g. `10.5281/zenodo.22646895.v2`) in papers; keep the concept DOI in `identifiers` / `references`.

---

## Pre-release (local)

- [ ] Changes merged on target branch (`hypothesis/cognitive-antigravity` or `main`).
- [ ] `pytest tests/ -v` passes (`pip install -e ".[dev]"`).
- [ ] [`CITATION.cff`](../CITATION.cff) `version` and `date-released` updated.
- [ ] [`pyproject.toml`](../pyproject.toml) `version` aligned (e.g. `0.2.0`).
- [ ] [`NAMM_ARTICLE_OUTLINE.md`](NAMM_ARTICLE_OUTLINE.md) §10 Zenodo items reviewed.

Build the source bundle (Windows):

```powershell
pwsh -ExecutionPolicy Bypass -File scripts\build_zenodo_bundle.ps1 -Version v0.2.0
```

Linux/macOS (same exclusions, zip output):

```bash
bash scripts/build_zenodo_bundle.sh 0.2.0
```

CI on tag push uses the PowerShell script and produces `dist/namm-experiments-0.2.0.tar.gz`.

Spot-check (no logs or artifacts):

```powershell
tar -tzf dist\namm-experiments-0.2.0.tar.gz | Select-String "\.log|/artifacts/"
# Expect no matches
```

---

## Git tag + GitHub Release (CI/CD)

1. Commit metadata updates.
2. Tag and push (`v*` pattern):

   ```powershell
   git tag -a v0.2.0 -m "NAMM 0.2.0 — AMAT pilots + release bundle"
   git push origin v0.2.0
   ```

3. **Release** workflow (`.github/workflows/release.yml`):
   - `pytest tests/ -v`
   - `scripts/build_zenodo_bundle.ps1`
   - 90-day CI artifact + GitHub Release with tarball

4. Download the bundle from GitHub Release for Zenodo upload (keeps CI and deposit identical).

---

## Zenodo new version upload

1. Open [22646895](https://zenodo.org/records/22646895) → **New version**.
2. Upload `namm-experiments-<version>.tar.gz` from the GitHub Release.
3. Copy metadata from [`CITATION.cff`](../CITATION.cff).
4. Related identifiers: GitHub repo URL; arXiv DOI when available.
5. Publish → record version DOI for README and paper.

---

## Post-release

- [ ] Tag, GitHub Release, Zenodo version, and `CITATION.cff` agree.
- [ ] README cites Zenodo DOI.
- [ ] [`NAMM_ARTICLE_OUTLINE.md`](NAMM_ARTICLE_OUTLINE.md) §10 checkbox done.

---

## Troubleshooting

| Issue | Action |
|-------|--------|
| Release workflow did not run | Tag must be `v*` (e.g. `v0.2.0`). |
| pytest fails on tag | Fix on branch; retag only if Zenodo not yet uploaded. |
| Tarball contains `.log` or `artifacts/` | Re-run bundle script; file a bug if exclusion missed. |
| Metadata drift | Re-read `CITATION.cff`; edit Zenodo deposit fields. |