"""Certificate serialization for TDA frame domain."""

from __future__ import annotations

import gzip
import hashlib
import json
from typing import Any

import networkx as nx

from namm.domains.tda.homology import PersistenceSignature, graph_persistence_signature


def build_tda_certificate(
    *,
    candidate_id: str,
    graph: nx.Graph,
    seed: int,
    baseline_signature: PersistenceSignature,
    witness_bounds: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build certificate.json payload for TDA frame candidate."""
    sig = graph_persistence_signature(graph)
    payload = {
        "candidate_id": candidate_id,
        "domain": "tda_frame",
        "protocol_version": "v2-tda-frame",
        "seed": seed,
        "signature": sig.to_dict(),
        "baseline_signature": baseline_signature.to_dict(),
        "witness_bounds": witness_bounds,
        "graph": {
            "order": graph.number_of_nodes(),
            "size": graph.number_of_edges(),
            "edges": [[int(u), int(v)] for u, v in graph.edges()],
        },
    }
    if extra:
        payload.update(extra)

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["eval_hash"] = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return payload


def compute_tda_representation_metrics(
    graph: nx.Graph,
    *,
    projection_estimate: int = 80,
) -> dict[str, float | int]:
    """K_A proxies for persistence signature."""
    sig = graph_persistence_signature(graph)
    raw = json.dumps(sig.to_dict(), sort_keys=True).encode()
    gz = gzip.compress(raw)
    return {
        "json_bytes": len(raw),
        "gzip_bytes": len(gz),
        "eval_time_ms": 0.0,
        "token_count_estimate": len(raw) // 4,
        "projection_token_estimate": projection_estimate,
    }


def human_projection_from_tda(
    sig: PersistenceSignature,
    *,
    candidate_id: str,
    graph_order: int,
    distance_to_baseline: float,
) -> str:
    """Lossy human projection for TDA candidate."""
    return (
        f"**TDA candidate `{candidate_id}`** (order {graph_order})\n"
        f"- Betti: β₀={sig.betti_0}, β₁={sig.betti_1}\n"
        f"- H¹ total persistence: {sig.total_persistence_h1:.4f}\n"
        f"- H¹ persistence entropy: {sig.persistence_entropy_h1:.4f}\n"
        f"- L1 distance to path baseline: {distance_to_baseline:.4f}\n"
        f"- Signature hash: `{sig.signature_hash}`\n"
        f"\n> Trust certificate; full persistence summary in certificate.json."
    )
