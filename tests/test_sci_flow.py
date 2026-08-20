"""Tests for NAMM Sci Flow routing and module selection."""

from __future__ import annotations

import pytest

from namm.sci_flow import SciFlowRunner, load_registry, resolve_modules, resolve_route
from namm.sci_flow.adapters import check_dependencies, module_catalog
from namm.sci_flow.registry import get_module_meta


def test_registry_loads():
    reg = load_registry()
    assert reg["schema_version"] == 1
    assert "entropy" in reg["modules"]
    assert "NAMM-2026-030" in reg["experiment_routes"]


def test_resolve_modules_from_experiment():
    modules = resolve_modules(experiment_id="NAMM-2026-021")
    assert "consensus" in modules
    assert "entropy" in modules
    assert "fuzzy" in modules
    # kuramoto requires consensus — both should appear
    assert "kuramoto" in modules


def test_resolve_modules_from_hypothesis():
    modules = resolve_modules(hypothesis_id="H-MCG-005")
    assert "catastrophe" in modules
    assert "cognitive_class" in modules


def test_resolve_modules_explicit_override():
    modules = resolve_modules(
        experiment_id="NAMM-2026-021",
        sci_modules=["entropy", "fuzzy"],
    )
    assert modules == ["entropy", "fuzzy", "consensus", "kuramoto"]


def test_resolve_modules_unknown_raises():
    with pytest.raises(ValueError, match="Cannot resolve sci modules"):
        resolve_modules()


def test_experiment_route_metadata():
    route = resolve_route("NAMM-2026-028")
    assert route["branch"] == "MCG"
    assert route["handler"] == "run_028"
    assert "catastrophe" in route["modules"]


def test_module_meta():
    meta = get_module_meta("tda")
    assert meta["namm_extra"] == "nd"
    assert "tda_frame" in meta["domains"]


def test_dependency_check_core_modules_available():
    modules = resolve_modules(experiment_id="NAMM-2026-021")
    result = check_dependencies(modules)
    assert result["all_available"] is True
    assert "entropy" in result["available"]


def test_describe_modules_dry_run():
    runner = SciFlowRunner()
    desc = runner.describe_modules("NAMM-2026-026")
    ids = [d["module_id"] for d in desc]
    assert "consensus" in ids
    assert "cognitive_class" in ids
    assert all("available" in d for d in desc)


def test_module_catalog_non_empty():
    catalog = module_catalog()
    assert len(catalog) >= 8
    assert any(entry["module_id"] == "game_theory_2_0" for entry in catalog)


def test_sci_flow_run_021_smoke():
    """End-to-end smoke test for sci-flow on NAMM-2026-021."""
    runner = SciFlowRunner()
    result = runner.run("NAMM-2026-021", skip_dependency_check=False)
    assert result.experiment_id == "NAMM-2026-021"
    assert "load_config" in result.stages_completed
    assert "certificate_check" in result.stages_completed
    assert result.certificate["sci_modules"]
    assert "hypothesis_support" in result.experiment_result
