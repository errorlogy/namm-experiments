"""Certificates and representation metrics for tensor AST programs."""

from __future__ import annotations

import gzip
import hashlib
import time
from typing import Any

import networkx as nx
import orjson

from namm.domains.tensor.ast import TensorNode, ast_to_dict
from namm.domains.tensor.canonical import ast_hash, canonicalize
from namm.domains.tensor.evaluator import evaluate_tensor_ast
from namm.domains.tensor.features import DEFAULT_HEAT_TIMES, DEFAULT_SPECTRUM_SIZE


def eval_hash(
    node: TensorNode,
    graphs: list[nx.Graph],
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> str:
    parts: list[str] = []
    for g in graphs:
        v = evaluate_tensor_ast(
            node, g, spectrum_size=spectrum_size, heat_times=heat_times
        )
        parts.append(f"{g.number_of_nodes()}:{g.number_of_edges()}:{v:.9f}")
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def human_projection_from_tensor(
    node: TensorNode,
    *,
    candidate_id: str,
    trust_certificate: bool = True,
) -> str:
    def _proj(n: TensorNode) -> str:
        if n.is_leaf():
            return n.name or "?"
        sym = {"add": "+", "mul": "*"}[n.op]
        return f"({_proj(n.left)} {sym} {_proj(n.right)})"

    lines = [
        f"**Candidate:** `{candidate_id}`",
        f"**Tensor program (numeric leaves):** `{_proj(node)}`",
    ]
    if trust_certificate:
        lines.append(
            "\n> Trust certificate; raw tensor indices in certificate.json. "
            "No named human invariants in search vocabulary."
        )
    return "\n".join(lines)


def compute_tensor_representation_metrics(
    node: TensorNode,
    reference_graphs: list[nx.Graph] | None = None,
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> dict[str, Any]:
    canonical = canonicalize(node)
    payload = {"canonical_ast": ast_to_dict(canonical), "ast_hash": ast_hash(canonical)}
    raw = orjson.dumps(payload)
    json_bytes = len(raw)
    gzip_bytes = len(gzip.compress(raw))

    if reference_graphs:
        start = time.perf_counter()
        for g in reference_graphs:
            evaluate_tensor_ast(
                node, g, spectrum_size=spectrum_size, heat_times=heat_times
            )
        eval_time_ms = (time.perf_counter() - start) / len(reference_graphs) * 1000.0
    else:
        eval_time_ms = 0.0

    projection = human_projection_from_tensor(
        node, candidate_id="tmp", trust_certificate=False
    )
    return {
        "json_bytes": json_bytes,
        "gzip_bytes": gzip_bytes,
        "eval_time_ms": eval_time_ms,
        "token_count_estimate": max(1, len(str(ast_to_dict(canonical)).split())),
        "projection_token_estimate": max(1, len(projection.split())),
    }


def build_tensor_certificate(
    *,
    candidate_id: str,
    node: TensorNode,
    seed: int,
    reference_graphs: list[nx.Graph],
    witness_bounds: dict[str, Any],
    extra: dict[str, Any] | None = None,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> dict[str, Any]:
    canonical = canonicalize(node)
    cert: dict[str, Any] = {
        "candidate_id": candidate_id,
        "canonical_ast": ast_to_dict(canonical),
        "ast_hash": ast_hash(canonical),
        "eval_hash": eval_hash(
            canonical,
            reference_graphs,
            spectrum_size=spectrum_size,
            heat_times=heat_times,
        ),
        "seed": seed,
        "witness_bounds": witness_bounds,
        "frame": "raw_tensor_beyond_named",
    }
    if extra:
        cert.update(extra)
    return cert
