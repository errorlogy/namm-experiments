# Build a Zenodo-ready source tarball from the repository root.
# Excludes .git, experiment logs, artifacts/, scratch dirs, and local junk.
#
# Usage (from repo root):
#   pwsh -File scripts/build_zenodo_bundle.ps1
#   pwsh -File scripts/build_zenodo_bundle.ps1 -Version v0.1.0
#
param(
    [Parameter()]
    [string]$Version = "",

    [Parameter()]
    [string]$OutputDir = "dist"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (-not $Version) {
    $tag = git describe --tags --exact-match 2>$null
    if ($tag) {
        $Version = $tag
    }
    else {
        $Version = "snapshot"
    }
}

$Version = ($Version -replace '^v', '').Trim()
if (-not $Version) {
    $Version = "snapshot"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$bundleBase = "namm-experiments-$Version"
$tarPath = Join-Path $OutputDir "$bundleBase.tar.gz"

if (Test-Path $tarPath) {
    Remove-Item -Force $tarPath
}

$excludePatterns = @(
    ".git",
    ".git/*",
    "dist",
    "dist/*",
    "*.log",
    "run_*.log",
    "pytest_followup.txt",
    "experiments/REPO_AUDIT_DRAFT.md",
    "experiments/*/artifacts",
    "experiments/*/artifacts/*",
    "experiments/*/_scratch",
    "experiments/*/_scratch/*",
    "__pycache__",
    "**/__pycache__",
    "**/__pycache__/*",
    ".venv",
    ".venv/*",
    "venv",
    "venv/*",
    "external",
    "external/*",
    ".pytest_cache",
    ".pytest_cache/*",
    ".mypy_cache",
    ".mypy_cache/*",
    ".ruff_cache",
    ".ruff_cache/*",
    "*.egg-info",
    "**/*.egg-info",
    "**/*.egg-info/*",
    "Anthemium.mp4",
    "experiments/anthemium-video-extract",
    "experiments/anthemium-video-extract/*",
    "extracted",
    "extracted/*",
    "*.zip",
    ".env",
    ".env.*",
    "2310.20360v3.pdf"
)

$excludeArgs = foreach ($pattern in $excludePatterns) {
    @("--exclude=$pattern")
}

Write-Host "Building Zenodo bundle: $tarPath"
& tar -czf $tarPath @excludeArgs -C $repoRoot .

if ($LASTEXITCODE -ne 0) {
    throw "tar failed with exit code $LASTEXITCODE"
}

$sizeMb = [math]::Round((Get-Item $tarPath).Length / 1MB, 2)
Write-Host "OK: $tarPath ($sizeMb MB)"
