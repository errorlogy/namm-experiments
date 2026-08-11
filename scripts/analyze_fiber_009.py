"""One-off fiber analysis for AMFW-012e / NAMM-2026-009."""
from __future__ import annotations

from itertools import product

from namm.domains.config_shadow.vacua import (
    fiber_map_from_vacua,
    project_shadow_4d,
)


def _admissible_raw(
    *,
    config_dim: int,
    moduli_min: int,
    moduli_max: int,
    max_energy: float,
    flux_modulus: int,
) -> list[tuple[int, ...]]:
    values = range(moduli_min, moduli_max + 1)
    raw: list[tuple[int, ...]] = []
    for m in product(values, repeat=config_dim):
        energy = sum(x * x for x in m)
        if energy > max_energy:
            continue
        if flux_modulus > 0 and sum(m) % flux_modulus != 0:
            continue
        raw.append(m)
    return raw


def main() -> None:
    raw = _admissible_raw(
        config_dim=11,
        moduli_min=-1,
        moduli_max=1,
        max_energy=20.0,
        flux_modulus=3,
    )
    print("Total admissible vacua:", len(raw))

    fibers = fiber_map_from_vacua(raw, shadow_dim=4, kappa_mode="first_4")
    fiber_sizes = [len(f) for f in fibers.values()]
    print("Distinct 4D shadows:", len(fibers))
    print("Max fiber size:", max(fiber_sizes))
    print("Uniform fiber check:", len(set(fiber_sizes)) == 1, set(fiber_sizes))

    target = (1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1)
    shadow = project_shadow_4d(target)
    fiber = fibers[shadow]
    idx = fiber.index(target)
    print("vac-012e1fe1 shadow:", shadow, "fiber_size:", len(fiber), "fiber_index:", idx)
    print("Sum m_i:", sum(target), "Sum m_i^2:", sum(x * x for x in target))

    head = shadow
    head_energy = sum(x * x for x in head)
    tails = [m[4:] for m in fiber]
    tail_energies = [sum(x * x for x in t) for t in tails]
    print("Head energy:", head_energy, "tail energy max:", max(tail_energies))

    count = sum(
        1
        for t in product([-1, 0, 1], repeat=7)
        if sum(t) % 3 == 0 and sum(x * x for x in t) <= 20 - head_energy
    )
    print("Tail count (flux+energy given head):", count, "(expect 729 = 3^6)")

    print("\n--- kappa mode comparison (11D, moduli +/-1) ---")
    for mode in ("first_4", "last_4", "middle_4", "flux_blocks_4"):
        fm = fiber_map_from_vacua(raw, shadow_dim=4, kappa_mode=mode)
        sizes = [len(v) for v in fm.values()]
        print(
            mode,
            "shadows=",
            len(fm),
            "max_fiber=",
            max(sizes),
            "min_fiber=",
            min(sizes),
        )

    print("\n--- 7D moduli range [-2,2] sample ---")
    raw7 = _admissible_raw(
        config_dim=7,
        moduli_min=-2,
        moduli_max=2,
        max_energy=20.0,
        flux_modulus=3,
    )
    fm7 = fiber_map_from_vacua(raw7, shadow_dim=4, kappa_mode="first_4")
    sizes7 = [len(v) for v in fm7.values()]
    print("vacua=", len(raw7), "max_fiber=", max(sizes7), "shadows=", len(fm7))


if __name__ == "__main__":
    main()
