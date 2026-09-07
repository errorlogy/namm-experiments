#!/usr/bin/env bash
# Build a Zenodo-ready source bundle for NAMM (CI + Linux/macOS).
# Excludes .git, logs, experiment artifacts, scratch dirs, and local cruft.
#
# Usage: bash scripts/build_zenodo_bundle.sh [version]
# Output: dist/namm-experiments-v<version>-zenodo.zip

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  VERSION="$(grep -E '^version = ' pyproject.toml | head -1 | sed -E 's/version = "(.*)"/\1/')"
fi

OUT_DIR="$ROOT/dist"
STAGING="$(mktemp -d)"
BUNDLE="$OUT_DIR/namm-experiments-v${VERSION}-zenodo.zip"

mkdir -p "$OUT_DIR"

echo "Staging Zenodo bundle v${VERSION} -> ${BUNDLE}"

tar \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='venv' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.pytest_cache' \
  --exclude='.mypy_cache' \
  --exclude='dist' \
  --exclude='*.log' \
  --exclude='run.log' \
  --exclude='run_*.log' \
  --exclude='*_scratch' \
  --exclude='*/artifacts/*' \
  --exclude='2310.20360v3.pdf' \
  --exclude='pytest_followup.txt' \
  --exclude='experiments/REPO_AUDIT_DRAFT.md' \
  --exclude='README(4).md' \
  -cf - . | tar -xf - -C "$STAGING"

rm -f "$BUNDLE"
(cd "$STAGING" && zip -rq "$BUNDLE" .)

rm -rf "$STAGING"

echo "Created ${BUNDLE} ($(du -h "$BUNDLE" | cut -f1))"
