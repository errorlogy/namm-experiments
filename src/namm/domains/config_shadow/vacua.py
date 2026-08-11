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


KAPPA_MODES = ("first_4", "last_4", "middle_4", "flux_blocks_4")


def project_shadow(
    moduli: tuple[int, ...],
    *,
    shadow_dim: int = 4,
    mode: str = "first_4",
) -> tuple[int, ...]:
    """κ compactification map: full moduli → shadow_dim effective coordinates."""
    n = len(moduli)
    if mode == "first_4":
        return tuple(moduli[:shadow_dim])
    if mode == "last_4":
        return tuple(moduli[-shadow_dim:])
    if mode == "middle_4":
        start = max(0, (n - shadow_dim) // 2)
        return tuple(moduli[start : start + shadow_dim])
    if mode == "flux_blocks_4":
        if n < shadow_dim:
            raise ValueError(f"config_dim {n} < shadow_dim {shadow_dim}")
        block = max(1, n // shadow_dim)
        coords: list[int] = []
        for i in range(shadow_dim):
            chunk = moduli[i * block : (i + 1) * block]
            if not chunk:
                chunk = (moduli[i % n],)
            coords.append(sum(chunk) % 3)
        return tuple(coords)
    raise ValueError(f"unknown kappa mode: {mode}")


def project_shadow_4d(moduli: tuple[int, ...], shadow_dim: int = 4) -> tuple[int, ...]:
    """κ projection: first shadow_dim moduli as 4D effective shadow."""
    return project_shadow(moduli, shadow_dim=shadow_dim, mode="first_4")


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
    shadow_dim: int = 4,
    kappa_mode: str = "first_4",
) -> list[ModuliVacuum]:
    """Enumerate all admissible moduli vectors in bounded range."""
    values = range(moduli_min, moduli_max + 1)
    raw: list[tuple[int, ...]] = []
    for m in itertools.product(values, repeat=config_dim):
        if _is_admissible(m, max_energy=max_energy, flux_modulus=flux_modulus):
            raw.append(m)
    fibers = fiber_map_from_vacua(
        raw,
        shadow_dim=shadow_dim,
        kappa_mode=kappa_mode,
    )
    vacua: list[ModuliVacuum] = []
    for moduli in raw:
        shadow = project_shadow(moduli, shadow_dim=shadow_dim, mode=kappa_mode)
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
    kappa_mode: str = "first_4",
) -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    """Group full configs by shadow — measures non-injectivity of κ."""
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for moduli in moduli_list:
        shadow = project_shadow(moduli, shadow_dim=shadow_dim, mode=kappa_mode)
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
    shadow_dim: int = 4,
    kappa_mode: str = "first_4",
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
        shadow_dim=shadow_dim,
        kappa_mode=kappa_mode,
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


@dataclass(frozen=True)
class KappaSweepRow:
    """One κ projection mode in a sensitivity sweep."""

    kappa_mode: str
    vacua_scanned: int
    ambiguous_fibers: int
    max_fiber_size: int
    best_vacuum: ModuliVacuum | None


def sweep_kappa_modes(
    *,
    modes: list[str],
    config_dim: int = 11,
    moduli_min: int = -1,
    moduli_max: int = 1,
    max_energy: float = 20.0,
    flux_modulus: int = 3,
    shadow_dim: int = 4,
) -> list[KappaSweepRow]:
    """Compare fiber degeneracy across κ projection modes."""
    rows: list[KappaSweepRow] = []
    for mode in modes:
        result = search_ambiguous_vacua(
            config_dim=config_dim,
            moduli_min=moduli_min,
            moduli_max=moduli_max,
            max_energy=max_energy,
            flux_modulus=flux_modulus,
            shadow_dim=shadow_dim,
            kappa_mode=mode,
            min_fiber_size=1,
            limit=1,
            seed=0,
        )
        best = result.candidates[0] if result.candidates else None
        rows.append(
            KappaSweepRow(
                kappa_mode=mode,
                vacua_scanned=result.vacua_scanned,
                ambiguous_fibers=result.ambiguous_fibers,
                max_fiber_size=result.max_fiber_size,
                best_vacuum=best,
            )
        )
    return rows
