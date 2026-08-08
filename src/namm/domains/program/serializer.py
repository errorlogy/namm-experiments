"""Machine-native JSON certificate format for program AST candidates."""

from __future__ import annotations

import gzip
import hashlib
import time
from typing import Any

import networkx as nx
import orjson

from namm.domains.program.ast import ProgramNode, ast_to_dict
from namm.domains.program.canonical import ast_hash, canonicalize
from namm.domains.program.evaluator import evaluate_ast


def eval_hash(node: ProgramNode, graphs: list[nx.Graph]) -> str:
    """Digest of evaluated values on reference graphs."""
    parts: list[str] = []
    for g in graphs:
        v = evaluate_ast(node, g)
        parts.append(f"{g.number_of_nodes()}:{g.number_of_edges()}:{v:.9f}")
    payload = "|".join(parts)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def human_projection_from_ast(
    node: ProgramNode,
    *,
    candidate_id: str,
    trust_certificate: bool = True,
) -> str:
    """Lossy human-readable projection from AST."""

    def _proj(n: ProgramNode) -> str:
        if n.is_leaf():
            return n.name or "?"
        if n.op == "neg":
            return f"(- {_proj(n.child)})"  # type: ignore[arg-type]
        sym = {"add": "+", "sub": "-", "mul": "*"}[n.op]
        return f"({_proj(n.left)} {sym} {_proj(n.right)})"

    lines = [
        f"**Candidate:** `{candidate_id}`",
        f"**Approximate form:** `{_proj(node)}`",
    ]
    if trust_certificate:
        lines.append(
            "\n> Trust certificate; full object in certificate.json. "
            "Projection omits canonical sort order and witness bounds."
        )
    return "\n".join(lines)


def compute_ast_representation_metrics(
    node: ProgramNode,
    reference_graphs: list[nx.Graph] | None = None,
) -> dict[str, Any]:
    """K_A proxies for AST certificate payload."""
    canonical = canonicalize(node)
    payload = {"canonical_ast": ast_to_dict(canonical), "ast_hash": ast_hash(canonical)}
    raw = orjson.dumps(payload)
    json_bytes = len(raw)
    gzip_bytes = len(gzip.compress(raw))

    if reference_graphs:
        start = time.perf_counter()
        for g in reference_graphs:
            evaluate_ast(node, g)
        eval_time_ms = (time.perf_counter() - start) / len(reference_graphs) * 1000.0
    else:
        eval_time_ms = 0.0

    projection = human_projection_from_ast(node, candidate_id="tmp", trust_certificate=False)
    projection_token_estimate = max(1, len(projection.split()))

    return {
        "json_bytes": json_bytes,
        "gzip_bytes": gzip_bytes,
        "eval_time_ms": round(eval_time_ms, 6),
        "projection_token_estimate": projection_token_estimate,
        "token_count_estimate": projection_token_estimate,
    }


def build_certificate(
    *,
    candidate_id: str,
    node: ProgramNode,
    seed: int,
    reference_graphs: list[nx.Graph],
    witness_bounds: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build primary certificate.json payload."""
    canonical = canonicalize(node)
    cert: dict[str, Any] = {
        "candidate_id": candidate_id,
        "canonical_ast": ast_to_dict(canonical),
        "ast_hash": ast_hash(canonical),
        "eval_hash": eval_hash(canonical, reference_graphs),
        "witness_bounds": witness_bounds,
        "seeds": {"experiment": seed, "generator": seed},
        "representation_metrics": compute_ast_representation_metrics(
            canonical, reference_graphs
        ),
    }
    if extra:
        cert.update(extra)
    return cert
