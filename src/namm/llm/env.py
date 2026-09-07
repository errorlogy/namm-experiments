"""Load API keys from .env files without committing secrets."""

from __future__ import annotations

import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]

DEFAULT_EXTERNAL_ENV = Path(r"C:\ai_models\mas\research\.env")


def parse_dotenv(path: Path) -> dict[str, str]:
    """Minimal KEY=VALUE parser (no variable expansion)."""
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            out[key] = value
    return out


def env_search_paths() -> list[Path]:
    paths: list[Path] = []
    explicit = os.environ.get("NAMM_ENV_FILE")
    if explicit:
        paths.append(Path(explicit))
    paths.extend([WORKSPACE / ".env.local", WORKSPACE / ".env"])
    if DEFAULT_EXTERNAL_ENV.is_file():
        paths.append(DEFAULT_EXTERNAL_ENV)
    return paths


def load_env(*, override: bool = False) -> dict[str, str]:
    """Merge dotenv files into os.environ. Later files do not override earlier unless override=True."""
    merged: dict[str, str] = {}
    for path in env_search_paths():
        for key, value in parse_dotenv(path).items():
            if override or key not in merged:
                merged[key] = value
    for key, value in merged.items():
        if override or key not in os.environ:
            os.environ[key] = value
    return merged


def get_secret(*keys: str) -> str | None:
    """Return first non-empty env value among key aliases."""
    for key in keys:
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None
