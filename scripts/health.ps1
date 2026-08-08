# NAMM health loop: pytest + smoke experiment
# Run from the repository root. Uses `python` on PATH (activate a venv first if needed).
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py -3.12" } else { "python" }

Invoke-Expression "$py -m pytest tests/ -q"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Invoke-Expression "$py -m namm.cli run-experiment --id NAMM-2026-001"
exit $LASTEXITCODE
