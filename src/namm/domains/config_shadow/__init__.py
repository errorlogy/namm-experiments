"""11D configuration shadow domain — finite moduli vacua enumeration (NAMM-2026-009)."""

from namm.domains.config_shadow.vacua import (
    ModuliVacuum,
    enumerate_admissible_vacua,
    fiber_map_from_vacua,
    project_shadow,
    project_shadow_4d,
    search_ambiguous_vacua,
    sweep_kappa_modes,
)

__all__ = [
    "ModuliVacuum",
    "enumerate_admissible_vacua",
    "fiber_map_from_vacua",
    "project_shadow",
    "project_shadow_4d",
    "search_ambiguous_vacua",
    "sweep_kappa_modes",
]
