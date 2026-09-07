Non-Anthropic Mathematics Mode (NAMM) — Zenodo source bundle
================================================================

Version: 0.2.0
Date: 2026-09-07
License: CC-BY-4.0
Repository: https://github.com/errorlogy/namm-experiments

What this deposit is
--------------------
This archive is a clean, reproducible source snapshot of the NAMM research
program: verification-first machine-native mathematical discovery with
certificates, frame escalation, compression asymmetry (K_A/K_H), and AMAT
topology pilots (experiments NAMM-2026-037 through NAMM-2026-041).

Included: src/, docs/, schemas/, experiment scaffolds (config + runners),
tests, LICENSE, CITATION.cff, README.

Excluded: .git history, local run logs, experiment artifacts/, scratch
directories (_scratch), virtual environments, build outputs, secrets (.env),
and ad-hoc downloads.

Relationship to EIA (Endogenous Initiative Architecture)
----------------------------------------------------------
NAMM and EIA are sibling Anthemium research programs with different goals:

  NAMM — Can machines certify mathematical structure before compact human
         projection exists? (this deposit)

  EIA  — Proactive AI with endogenous initiative; code at
         https://github.com/errorlogy/eia

They share verification-first methodology but are separate software deposits.
When citing NAMM, use the DOI assigned to this Zenodo record (concept
10.5281/zenodo.22646895 or its version-specific child DOI after upload).

How to reproduce
----------------
  python -m pip install -e .
  python -m pytest tests/test_amat_041_037_040.py -v

See docs/ZENODO_RELEASE.md in the repository for the full release checklist.
