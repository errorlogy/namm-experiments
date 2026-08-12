"""Load classical mathematics library base (YAML)."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

import yaml

_FILENAME = "mathematics_library_base.yaml"
_REPO_ROOT = Path(__file__).resolve().parents[3]
_REPO_DATA_PATH = _REPO_ROOT / "data" / _FILENAME


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at root of {_FILENAME}, got {type(data).__name__}")
    if "sections" not in data or not isinstance(data["sections"], list):
        raise ValueError(f"Expected 'sections' list in {_FILENAME}")
    return data


def _package_data_path() -> Path | None:
    try:
        ref = resources.files("namm.matlib.data") / _FILENAME
    except (ModuleNotFoundError, TypeError, FileNotFoundError):
        return None
    with resources.as_file(ref) as path:
        return path


def default_mathematics_library_path() -> Path:
    """Return the preferred on-disk path to the library YAML."""
    packaged = _package_data_path()
    if packaged is not None and packaged.is_file():
        return packaged
    if _REPO_DATA_PATH.is_file():
        return _REPO_DATA_PATH
    raise FileNotFoundError(
        f"Could not locate {_FILENAME} in namm.matlib.data or {_REPO_DATA_PATH}"
    )


def load_mathematics_sections(path: str | Path | None = None) -> dict[str, Any]:
    """Read mathematics library base YAML and return parsed document."""
    if path is None:
        resolved = default_mathematics_library_path()
    else:
        resolved = Path(path)
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
    return _load_yaml(resolved)
