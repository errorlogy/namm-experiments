"""Tests for 11D configuration shadow domain."""

from namm.domains.config_shadow.serializer import compute_config_representation_metrics
from namm.domains.config_shadow.vacua import (
    enumerate_admissible_vacua,
    fiber_map_from_vacua,
    project_shadow_4d,
    search_ambiguous_vacua,
)


def test_project_shadow_4d():
    moduli = tuple(range(11))
    assert project_shadow_4d(moduli) == (0, 1, 2, 3)


def test_enumerate_admissible_vacua_bounded():
    vacua = enumerate_admissible_vacua(
        config_dim=5,
        moduli_min=-1,
        moduli_max=1,
        max_energy=8.0,
        flux_modulus=3,
    )
    assert len(vacua) > 0
    for v in vacua:
        assert len(v.moduli) == 5
        assert v.shadow_4d == project_shadow_4d(v.moduli)
        assert v.stability_score <= 8.0


def test_fiber_map_non_injective_exists():
    moduli_list = [
        (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0),
    ]
    fibers = fiber_map_from_vacua(moduli_list)
    shadow = (0, 0, 0, 0)
    assert len(fibers[shadow]) == 2


def test_search_ambiguous_vacua_11d():
    result = search_ambiguous_vacua(
        config_dim=11,
        moduli_min=-1,
        moduli_max=1,
        max_energy=20.0,
        flux_modulus=3,
        min_fiber_size=2,
        limit=10,
        seed=2026009,
    )
    assert result.vacua_scanned > 0
    assert result.ambiguous_fibers > 0
    assert result.max_fiber_size >= 2
    assert len(result.candidates) > 0


def test_representation_asymmetry():
    result = search_ambiguous_vacua(
        config_dim=7,
        moduli_min=-1,
        moduli_max=1,
        limit=1,
        seed=1,
    )
    vacuum = result.candidates[0]
    metrics = compute_config_representation_metrics(vacuum)
    ratio = metrics["gzip_bytes"] / metrics["projection_token_estimate"]
    assert ratio >= 1.0
