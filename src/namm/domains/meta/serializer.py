"""Certificate and projection for meta-evaluator fixed points."""

from __future__ import annotations

import gzip
import hashlib
import time
from typing import Any

import networkx as nx
import orjson

from namm.domains.meta.ast import MetaEvaluatorNode, meta_to_dict
from namm.domains.meta.canonical import canonicalize_meta, meta_hash
from namm.domains.meta.evaluator import evaluate_meta_on_graph, fixed_point_score


def eval_hash_meta(node: MetaEvaluatorNode, graphs: list[nx.Graph]) -> str:
    """Digest of evaluated values on reference graphs."""
    parts: list[str] = []
    for g in graphs:
        v = evaluate_meta_on_graph(node, g)
        parts.append(f"{g.number_of_nodes()}:{g.number_of_edges()}:{v:.9f}")
    payload = "|".join(parts)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def human_projection_from_meta(
    node: MetaEvaluatorNode,
    *,
    candidate_id: str,
    transform_name: str,
    fixed_point_fraction: float,
    trust_certificate: bool = True,
) -> str:
    """Lossy human-readable projection."""

    def _proj(n: MetaEvaluatorNode) -> str:
        if n.is_leaf():
            return n.name or "?"
        if n.op == "self":
            return "SELF"
        if n.op == "target":
            return "TARGET"
        sym = {"add": "+", "sub": "-", "mul": "*", "delta": "Δ", "ratio": "/"}[n.op]
        return f"({_proj(n.left)} {sym} {_proj(n.right)})"  # type: ignore[arg-type]

    lines = [
        f"**Candidate:** `{candidate_id}`",
        f"**Transform F:** `{transform_name}`",
        f"**Fixed-point score:** {fixed_point_fraction:.4f}",
        f"**Approximate form:** `{_proj(node)}`",
    ]
    if trust_certificate:
        lines.append(
            "\n> Trust certificate; full object in certificate.json. "
            "Meta-evaluator fixed points are AI-topology objects — "
            "human projection is intentionally lossy."
        )
    return "\n".join(lines)


def compute_meta_representation_metrics(
    node: MetaEvaluatorNode,
    reference_graphs: list[nx.Graph] | None = None,
) -> dict[str, Any]:
    """K_A proxies for meta certificate payload."""
    canonical = canonicalize_meta(node)
    payload = {"canonical_ast": meta_to_dict(canonical), "meta_hash": meta_hash(canonical)}
    raw = orjson.dumps(payload)
    json_bytes = len(raw)
    gzip_bytes = len(gzip.compress(raw))

    if reference_graphs:
        start = time.perf_counter()
        for g in reference_graphs:
            evaluate_meta_on_graph(node, g)
        eval_time_ms = (time.perf_counter() - start) / len(reference_graphs) * 1000.0
    else:
        eval_time_ms = 0.0

    projection = human_projection_from_meta(
        node,
        candidate_id="tmp",
        transform_name="identity",
        fixed_point_fraction=1.0,
        trust_certificate=False,
    )
    projection_token_estimate = max(1, len(projection.split()))

    return {
        "json_bytes": json_bytes,
        "gzip_bytes": gzip_bytes,
        "eval_time_ms": round(eval_time_ms, 6),
        "projection_token_estimate": projection_token_estimate,
        "token_count_estimate": projection_token_estimate,
    }


def build_meta_certificate(
    *,
    candidate_id: str,
    evaluator: MetaEvaluatorNode,
    transformed: MetaEvaluatorNode,
    transform_name: str,
    seed: int,
    reference_graphs: list[nx.Graph],
    witness_bounds: dict[str, Any],
    fixed_point_fraction: float,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build primary certificate.json for meta fixed-point candidate."""
    canonical = canonicalize_meta(evaluator)
    transformed_canonical = canonicalize_meta(transformed)
    cert: dict[str, Any] = {
        "candidate_id": candidate_id,
        "domain": "meta_evaluation",
        "canonical_ast": meta_to_dict(canonical),
        "meta_hash": meta_hash(canonical),
        "transform": transform_name,
        "transformed_ast": meta_to_dict(transformed_canonical),
        "transformed_hash": meta_hash(transformed_canonical),
        "fixed_point_fraction": fixed_point_fraction,
        "eval_hash": eval_hash_meta(canonical, reference_graphs),
        "transformed_eval_hash": eval_hash_meta(transformed_canonical, reference_graphs),
        "witness_bounds": witness_bounds,
        "seeds": {"experiment": seed, "generator": seed},
        "representation_metrics": compute_meta_representation_metrics(
            canonical, reference_graphs
        ),
    }
    if extra:
        cert.update(extra)
    return cert
