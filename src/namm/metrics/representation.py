"""Operational K_A proxies: serialization size, gzip, eval time, token estimate."""

from __future__ import annotations

import gzip
import time
from typing import Any

import networkx as nx
import orjson

from namm.domains.graph.evaluator import evaluate_formula
from namm.domains.graph.generator import enumerate_small_graphs
from namm.schemas.experiment import InvariantFormula, RepresentationMetrics


def _canonical_payload(
    expression: str,
    formula: InvariantFormula | None = None,
) -> dict[str, Any]:
    if formula is not None:
        return {
            "expression": formula.expression,
            "primitives": formula.primitives,
            "meta_origin": formula.meta_origin,
        }
    return {"expression": expression}


def compute_representation_metrics(
    expression: str,
    formula: InvariantFormula | None = None,
    reference_graphs: list[nx.Graph] | None = None,
    max_order: int = 5,
) -> RepresentationMetrics:
    """Compute K_A proxy metrics for a candidate expression."""
    payload = _canonical_payload(expression, formula)
    raw = orjson.dumps(payload)
    json_bytes = len(raw)
    gzip_bytes = len(gzip.compress(raw))

    if reference_graphs is None:
        reference_graphs = enumerate_small_graphs(max_order)[:5]

    if reference_graphs:
        start = time.perf_counter()
        for g in reference_graphs:
            evaluate_formula(expression, g)
        elapsed_ms = (time.perf_counter() - start) / len(reference_graphs) * 1000.0
    else:
        elapsed_ms = 0.0

    tokens = [t for t in expression.replace("*", " ").replace("+", " ").replace("-", " ").split() if t]
    token_count = len(tokens) if tokens else max(1, len(expression) // 4)

    return RepresentationMetrics(
        json_bytes=json_bytes,
        gzip_bytes=gzip_bytes,
        eval_time_ms=round(elapsed_ms, 6),
        token_count_estimate=token_count,
        projection_token_estimate=token_count,
    )
