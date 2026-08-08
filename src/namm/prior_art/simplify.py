"""Sympy simplify checks against known baseline forms."""

from __future__ import annotations

import re
from typing import Any

import sympy as sp

from namm.metrics.baselines import KNOWN_BASELINE_EXPRESSIONS

_PRIMITIVE_SYMBOLS = {
    "num_nodes": sp.Symbol("num_nodes"),
    "num_edges": sp.Symbol("num_edges"),
    "avg_degree": sp.Symbol("avg_degree"),
    "diameter": sp.Symbol("diameter"),
    "radius": sp.Symbol("radius"),
    "clustering": sp.Symbol("clustering"),
    "algebraic_connectivity": sp.Symbol("algebraic_connectivity"),
    "wiener_index": sp.Symbol("wiener_index"),
}

_ATTACK_BASELINES = ("wiener_index", "degree_sum", "clustering", "num_edges", "avg_degree")


def _parse_linear_expression(expression: str) -> sp.Expr | None:
    """Parse linear combination of coefficient*primitive terms."""
    compact = expression.strip().replace(" ", "")
    if not compact:
        return None
    term_re = re.compile(r"([+-]?\d+)\*([a-z_]+)")
    matches = term_re.findall(compact)
    if not matches:
        return None
    sym_expr = sp.Integer(0)
    for coeff_s, prim in matches:
        if prim not in _PRIMITIVE_SYMBOLS:
            return None
        sym_expr += int(coeff_s) * _PRIMITIVE_SYMBOLS[prim]
    return sp.expand(sym_expr)


def _baseline_sympy(baseline_id: str) -> sp.Expr | None:
    expr_str = KNOWN_BASELINE_EXPRESSIONS.get(baseline_id)
    if expr_str is None:
        return None
    return _parse_linear_expression(expr_str)


def check_simplification(expression: str) -> dict[str, Any]:
    """Check whether expression simplifies to any known baseline form."""
    candidate = _parse_linear_expression(expression)
    if candidate is None:
        return {
            "parseable": False,
            "simplifies_to_known": False,
            "matches": [],
        }

    matches: list[dict[str, str]] = []
    for baseline_id in _ATTACK_BASELINES:
        baseline = _baseline_sympy(baseline_id)
        if baseline is None:
            continue
        if sp.simplify(candidate - baseline) == 0:
            matches.append({"baseline_id": baseline_id, "relationship": "equivalent"})

    redundancy_note = None
    if "avg_degree" in expression and "num_edges" in expression:
        redundancy_note = "avg_degree redundant with num_edges/num_nodes"

    return {
        "parseable": True,
        "simplifies_to_known": len(matches) > 0,
        "matches": matches,
        "redundancy_note": redundancy_note,
        "sympy_form": str(candidate),
    }


def simplifies_to_known_baseline(expression: str) -> bool:
    """Return True if expression is algebraically equivalent to a known baseline."""
    return bool(check_simplification(expression)["simplifies_to_known"])
