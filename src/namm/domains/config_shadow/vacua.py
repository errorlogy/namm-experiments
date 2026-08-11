"""Finite 11D moduli vacua with explicit 4D compactification shadow κ."""

from __future__ import annotations

import hashlib
import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class ModuliVacuum:
    """Admissible moduli configuration with 4D shadow and fiber metadata."""

    moduli: tuple[int, ...]
    shadow_4d: tuple[int, ...]
    fiber_size: int
    fiber_index: int
    stability_score: float
    vacuum_id: str

    def to_dict(self) -> dict:
        return {
            "moduli": list(self.moduli),
            "shadow_4d": list(self.shadow_4d),
            "fiber_size": self.fiber_size,
            "fiber_index": self.fiber_index,
            "stability_score": self.stability_score,
            "vacuum_id": self.vacuum_id,
            "config_dim": len(self.moduli),
            "shadow_dim": len(self.shadow_4d),
        }


def project_shadow_4d(moduli: tuple[int, ...], shadow_dim: int = 4) -> tuple[int, ...]:
    """κ projection: first shadow_dim moduli as 4D effective shadow."""
    return tuple(moduli[:shadow_dim])


def _stability_score(moduli: tuple[int, ...]) -> float:
    return float(sum(m * m for m in moduli))


def _is_admissible(
    moduli: tuple[int, ...],
    *,
    max_energy: float,
    flux_modulus: int,
) -> bool:
    if _stability_score(moduli) > max_energy:
        return False
    if flux_modulus > 0 and sum(moduli) % flux_modulus != 0:
        return False
    return True


def enumerate_admissible_vacua(
    *,
    config_dim: int = 11,
    moduli_min: int = -1,
    moduli_max: int = 1,
    max_energy: float = 20.0,
    flux_modulus: int = 3,
) -> list[ModuliVacuum]:
    """Enumerate all admissible moduli vectors in bounded range."""
    values = range(moduli_min, moduli_max + 1)
    raw: list[tuple[int, ...]] = []
    for m in itertools.product(values, repeat=config_dim):
        if _is_admissible(m, max_energy=max_energy, flux_modulus=flux_modulus):
            raw.append(m)
    fibers = fiber_map_from_vacua(raw, shadow_dim=4)
    vacua: list[ModuliVacuum] = []
    for moduli in raw:
        shadow = project_shadow_4d(moduli, shadow_dim=4)
        fiber = fibers[shadow]
        idx = fiber.index(moduli)
        vid = _vacuum_id(moduli, shadow)
        vacua.append(
            ModuliVacuum(
                moduli=moduli,
                shadow_4d=shadow,
                fiber_size=len(fiber),
                fiber_index=idx,
                stability_score=_stability_score(moduli),
                vacuum_id=vid,
            )
        )
    return vacua


def fiber_map_from_vacua(
    moduli_list: list[tuple[int, ...]],
    *,
    shadow_dim: int = 4,
) -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    """Group full configs by 4D shadow — measures non-injectivity of κ."""
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for moduli in moduli_list:
        shadow = project_shadow_4d(moduli, shadow_dim=shadow_dim)
        fibers.setdefault(shadow, []).append(moduli)
    return fibers


def _vacuum_id(moduli: tuple[int, ...], shadow: tuple[int, ...]) -> str:
    payload = f"{moduli}|{shadow}"
    return "vac-" + hashlib.sha256(payload.encode()).hexdigest()[:8]


@dataclass(frozen=True)
class AmbiguousVacuaSearchResult:
    """Search output for ambiguous compactification witnesses."""

    vacua_scanned: int
    ambiguous_fibers: int
    candidates: list[ModuliVacuum]
    max_fiber_size: int


def search_ambiguous_vacua(
    *,
    config_dim: int = 11,
    moduli_min: int = -1,
    moduli_max: int = 1,
    max_energy: float = 20.0,
    flux_modulus: int = 3,
    min_fiber_size: int = 2,
    limit: int = 50,
    seed: int = 0,
) -> AmbiguousVacuaSearchResult:
    """Find vacua in fibers where κ is non-injective (fiber size ≥ min_fiber_size)."""
    import random

    all_vacua = enumerate_admissible_vacua(
        config_dim=config_dim,
        moduli_min=moduli_min,
        moduli_max=moduli_max,
        max_energy=max_energy,
        flux_modulus=flux_modulus,
    )
    ambiguous = [v for v in all_vacua if v.fiber_size >= min_fiber_size]
    ambiguous.sort(key=lambda v: (-v.fiber_size, -v.stability_score, v.vacuum_id))

    rng = random.Random(seed)
    if len(ambiguous) > limit:
        top = ambiguous[: limit * 2]
        rng.shuffle(top)
        selected = top[:limit]
        selected.sort(key=lambda v: (-v.fiber_size, v.vacuum_id))
    else:
        selected = ambiguous

    fibers = {v.shadow_4d for v in ambiguous}
    max_fiber = max((v.fiber_size for v in ambiguous), default=0)

    return AmbiguousVacuaSearchResult(
        vacua_scanned=len(all_vacua),
        ambiguous_fibers=len(fibers),
        candidates=selected,
        max_fiber_size=max_fiber,
    )
