"""YAML registry loader and module routing for Sci Flow."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY_PATH = WORKSPACE / "data" / "sci_flow_registry.yaml"


@lru_cache(maxsize=1)
def load_registry(path: Path | None = None) -> dict[str, Any]:
    """Load sci_flow_registry.yaml (cached)."""
    registry_path = path or DEFAULT_REGISTRY_PATH
    with registry_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid registry format: {registry_path}")
    return data


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _expand_requires(modules: list[str], registry: dict[str, Any]) -> list[str]:
    module_defs = registry.get("modules", {})
    expanded: list[str] = []
    for name in modules:
        expanded.append(name)
        requires = module_defs.get(name, {}).get("requires", [])
        expanded.extend(requires)
    return _dedupe_preserve_order(expanded)


def resolve_modules(
    *,
    experiment_id: str | None = None,
    hypothesis_id: str | None = None,
    sci_modules: list[str] | None = None,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    """Resolve required sci modules from explicit list, experiment, or hypothesis."""
    reg = registry or load_registry()
    modules: list[str] = []

    if sci_modules:
        modules.extend(sci_modules)

    exp_routes = reg.get("experiment_routes", {})
    hyp_routes = reg.get("hypothesis_routes", {})

    if experiment_id and experiment_id in exp_routes:
        modules.extend(exp_routes[experiment_id].get("modules", []))

    if hypothesis_id and hypothesis_id in hyp_routes:
        modules.extend(hyp_routes[hypothesis_id].get("modules", []))

    if not modules and hypothesis_id:
        prefix = hypothesis_id.rsplit("-", 1)[0]  # H-CNS, H-CCT, H-MCG
        for branch in reg.get("branches", {}).values():
            if branch.get("hypothesis_prefix") == prefix:
                modules.extend(branch.get("default_modules", []))
                break

    if not modules:
        raise ValueError(
            f"Cannot resolve sci modules for experiment={experiment_id!r} "
            f"hypothesis={hypothesis_id!r}; set sci_modules in config or add registry route"
        )

    return _expand_requires(_dedupe_preserve_order(modules), reg)


def resolve_route(
    experiment_id: str,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return experiment route metadata from registry."""
    reg = registry or load_registry()
    routes = reg.get("experiment_routes", {})
    if experiment_id not in routes:
        raise KeyError(f"No sci_flow route for experiment {experiment_id!r}")
    return routes[experiment_id]


def get_module_meta(module_id: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return module metadata from registry."""
    reg = registry or load_registry()
    modules = reg.get("modules", {})
    if module_id not in modules:
        raise KeyError(f"Unknown sci module {module_id!r}")
    return modules[module_id]
