"""Module adapters — thin wrappers over namm.metrics and domain modules."""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any, Protocol

from namm.sci_flow.registry import get_module_meta, load_registry


class SciModuleAdapter(Protocol):
    """Common interface for sci-flow module adapters."""

    module_id: str

    def check_available(self) -> tuple[bool, str | None]: ...

    def describe(self) -> dict[str, Any]: ...


@dataclass
class RegistryAdapter:
    """Adapter backed by sci_flow_registry.yaml module entry."""

    module_id: str
    _meta: dict[str, Any] = field(repr=False)
    _imported: Any | None = field(default=None, repr=False)

    @classmethod
    def from_registry(cls, module_id: str) -> RegistryAdapter:
        return cls(module_id=module_id, _meta=get_module_meta(module_id))

    @property
    def import_path(self) -> str:
        return str(self._meta["import_path"])

    @property
    def namm_extra(self) -> str | None:
        return self._meta.get("namm_extra")

    @property
    def domains(self) -> list[str]:
        return list(self._meta.get("domains", []))

    def load(self) -> Any:
        if self._imported is None:
            self._imported = importlib.import_module(self.import_path)
        return self._imported

    def check_available(self) -> tuple[bool, str | None]:
        try:
            self.load()
        except ImportError as exc:
            extra = self.namm_extra
            hint = f'pip install -e ".[{extra}]"' if extra else "core dependency missing"
            return False, f"{self.import_path}: {exc} ({hint})"
        return True, None

    def describe(self) -> dict[str, Any]:
        ok, err = self.check_available()
        return {
            "module_id": self.module_id,
            "import_path": self.import_path,
            "namm_extra": self.namm_extra,
            "domains": self.domains,
            "available": ok,
            "error": err,
            "description": self._meta.get("description"),
        }


def build_adapters(module_ids: list[str]) -> list[RegistryAdapter]:
    """Instantiate adapters for resolved module IDs."""
    return [RegistryAdapter.from_registry(mid) for mid in module_ids]


def check_dependencies(module_ids: list[str]) -> dict[str, Any]:
    """Verify all required modules import successfully."""
    adapters = build_adapters(module_ids)
    missing: list[dict[str, Any]] = []
    available: list[str] = []
    for adapter in adapters:
        ok, err = adapter.check_available()
        if ok:
            available.append(adapter.module_id)
        else:
            missing.append({"module_id": adapter.module_id, "error": err})
    return {
        "all_available": len(missing) == 0,
        "available": available,
        "missing": missing,
    }


def module_catalog(registry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Describe all registered modules."""
    reg = registry or load_registry()
    return [
        RegistryAdapter.from_registry(mid).describe()
        for mid in reg.get("modules", {})
    ]
