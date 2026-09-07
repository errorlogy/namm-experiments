"""SciFlowRunner — load config, route modules, run experiment, aggregate certificate."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from namm.sci_flow.adapters import build_adapters, check_dependencies
from namm.sci_flow.handlers import get_handler
from namm.sci_flow.registry import load_registry, resolve_modules, resolve_route

WORKSPACE = Path(__file__).resolve().parents[3]


@dataclass
class SciFlowResult:
    """Aggregated sci-flow run output."""

    experiment_id: str
    modules_used: list[str]
    branch: str | None
    handler: str | None
    dependency_check: dict[str, Any]
    experiment_result: dict[str, Any]
    certificate: dict[str, Any]
    stages_completed: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "modules_used": self.modules_used,
            "branch": self.branch,
            "handler": self.handler,
            "dependency_check": self.dependency_check,
            "experiment_result": self.experiment_result,
            "certificate": self.certificate,
            "stages_completed": self.stages_completed,
            "timestamp": self.timestamp,
        }


class SciFlowRunner:
    """Pipeline: load config → select modules → check deps → run handler → certificate."""

    def __init__(self, registry_path: Path | None = None) -> None:
        self.registry_path = registry_path

    def load_config(self, experiment_id: str, config_path: Path | None = None, variant: str | None = None) -> dict[str, Any]:
        if config_path is None:
            exp_dir = WORKSPACE / "experiments" / experiment_id
            path = exp_dir / "config.yaml"
            if variant:
                alt = exp_dir / f"config-{variant}.yaml"
                if alt.exists():
                    path = alt
        else:
            path = config_path
        if not path.exists():
            raise FileNotFoundError(f"Experiment config not found: {path}")
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        data.setdefault("experiment_id", experiment_id)
        if variant:
            data.setdefault("variant", variant)
        return data

    def run(
        self,
        experiment_id: str,
        *,
        config_path: Path | None = None,
        variant: str | None = None,
        skip_dependency_check: bool = False,
    ) -> SciFlowResult:
        stages: list[str] = []
        config = self.load_config(experiment_id, config_path, variant=variant)
        stages.append("load_config")

        registry = load_registry(self.registry_path)
        route = resolve_route(experiment_id, registry)
        modules = resolve_modules(
            experiment_id=experiment_id,
            hypothesis_id=config.get("hypothesis_id"),
            sci_modules=config.get("sci_modules"),
            registry=registry,
        )
        stages.append("select_modules")

        dep_check = check_dependencies(modules)
        if not skip_dependency_check and not dep_check["all_available"]:
            missing = ", ".join(m["module_id"] for m in dep_check["missing"])
            raise RuntimeError(f"Sci-flow dependency check failed for: {missing}")
        stages.append("check_dependencies")

        handler_name = route.get("handler")
        if not handler_name:
            raise ValueError(f"No handler registered for {experiment_id}")
        handler = get_handler(handler_name)
        experiment_result = handler(config, variant=variant)
        stages.append("run_modules")

        certificate = self._build_certificate(experiment_id, config, experiment_result, modules)
        stages.append("aggregate")
        stages.append("certificate_check")

        result = SciFlowResult(
            experiment_id=experiment_id,
            modules_used=modules,
            branch=route.get("branch"),
            handler=handler_name,
            dependency_check=dep_check,
            experiment_result=experiment_result,
            certificate=certificate,
            stages_completed=stages,
        )

        artifacts = WORKSPACE / "experiments" / experiment_id / "artifacts"
        artifacts.mkdir(parents=True, exist_ok=True)
        (artifacts / "sci_flow.json").write_text(
            json.dumps(result.to_dict(), indent=2),
            encoding="utf-8",
        )
        (artifacts / "certificate.json").write_text(
            json.dumps(certificate, indent=2),
            encoding="utf-8",
        )
        return result

    def describe_modules(self, experiment_id: str, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Dry-run module selection without executing handler."""
        cfg = config or self.load_config(experiment_id)
        registry = load_registry(self.registry_path)
        modules = resolve_modules(
            experiment_id=experiment_id,
            hypothesis_id=cfg.get("hypothesis_id"),
            sci_modules=cfg.get("sci_modules"),
            registry=registry,
        )
        return [a.describe() for a in build_adapters(modules)]

    @staticmethod
    def _build_certificate(
        experiment_id: str,
        config: dict[str, Any],
        experiment_result: dict[str, Any],
        modules: list[str],
    ) -> dict[str, Any]:
        confirmed = experiment_result.get("hypothesis_confirmed", False)
        support = experiment_result.get("hypothesis_support", {})
        falsifiers = experiment_result.get("falsifiers_triggered", {})
        status = "PARTIAL_EVIDENCE" if confirmed else "INCONCLUSIVE"
        if falsifiers and any(falsifiers.values()):
            status = "FALSIFIER_TRIGGERED"
        return {
            "experiment_id": experiment_id,
            "protocol": config.get("protocol_version", "sci-flow-v1"),
            "sci_modules": modules,
            "hypothesis_id": config.get("hypothesis_id"),
            "hypotheses": config.get("hypotheses", []),
            "falsifiers": config.get("falsifiers", []),
            "status": status,
            "hypothesis_confirmed": confirmed,
            "hypothesis_support": support,
            "falsifiers_triggered": falsifiers,
            "metrics": experiment_result.get("metrics", {}),
            "sci_flow_version": 1,
        }


def run_sci_flow(
    experiment_id: str,
    *,
    config_path: Path | str | None = None,
    variant: str | None = None,
    skip_dependency_check: bool = False,
) -> SciFlowResult:
    """Convenience entry point for sci-flow execution."""
    path = Path(config_path) if config_path else None
    return SciFlowRunner().run(
        experiment_id,
        config_path=path,
        variant=variant,
        skip_dependency_check=skip_dependency_check,
    )
