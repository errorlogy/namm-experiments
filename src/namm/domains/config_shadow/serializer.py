"""Certificate serialization for 11D configuration shadow domain."""

from __future__ import annotations

import gzip
import hashlib
import json
from typing import Any

from namm.domains.config_shadow.vacua import ModuliVacuum


def build_config_shadow_certificate(
    *,
    candidate_id: str,
    vacuum: ModuliVacuum,
    seed: int,
    witness_bounds: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build certificate.json for ambiguous compactification witness."""
    payload = {
        "candidate_id": candidate_id,
        "domain": "config_shadow",
        "protocol_version": "v2-11d-config-shadow",
        "frame": "F3h_11d_configuration_shadow",
        "seed": seed,
        "vacuum": vacuum.to_dict(),
        "witness_bounds": witness_bounds,
        "compactification": {
            "kappa": extra.get("kappa_mode", "first_4") if extra else "first_4",
            "non_injective": vacuum.fiber_size >= 2,
            "fiber_size": vacuum.fiber_size,
        },
    }
    if extra:
        payload.update(extra)

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["eval_hash"] = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return payload


def compute_config_representation_metrics(vacuum: ModuliVacuum) -> dict[str, float | int]:
    """K_A vs K_H: full 11D certificate vs 4D-only human projection."""
    full = json.dumps(vacuum.to_dict(), sort_keys=True).encode()
    gz = gzip.compress(full)
    shadow_only = (
        f"4D shadow κ(m) = {list(vacuum.shadow_4d)} "
        f"(effective couplings; fiber degeneracy unknown without full moduli)"
    )
    return {
        "json_bytes": len(full),
        "gzip_bytes": len(gz),
        "eval_time_ms": 0.0,
        "token_count_estimate": len(full) // 4,
        "projection_token_estimate": max(12, len(shadow_only.split())),
    }


def human_projection_from_config(
    vacuum: ModuliVacuum,
    *,
    candidate_id: str,
) -> str:
    """Lossy 4D-only projection — fiber data omitted (HL-004)."""
    return (
        f"**Config shadow `{candidate_id}`** — 4D effective theory only\n"
        f"- κ projection (first 4 moduli): {list(vacuum.shadow_4d)}\n"
        f"- Stability score Σmᵢ²: {vacuum.stability_score:.1f}\n"
        f"- Full 11D preimage and fiber index **not** specified in π_H\n"
        f"\n> Trust certificate.json for full moduli vector and fiber metadata."
    )
