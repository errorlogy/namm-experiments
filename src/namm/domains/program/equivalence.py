"""Sympy equivalence check for program AST expressions (Graph → Int)."""

from __future__ import annotations

import sympy as sp

from namm.domains.program.ast import ProgramNode
from namm.domains.program.project import ast_to_expression


def ast_to_sympy(node: ProgramNode) -> sp.Expr:
    """Map AST leaves to sympy symbols; binary ops to sympy expressions."""
    if node.is_leaf():
        return sp.Symbol(node.name)  # type: ignore[arg-type]
    if node.op == "neg":
        return -ast_to_sympy(node.child)  # type: ignore[arg-type]
    left = ast_to_sympy(node.left)  # type: ignore[arg-type]
    right = ast_to_sympy(node.right)  # type: ignore[arg-type]
    if node.op == "add":
        return left + right
    if node.op == "sub":
        return left - right
    if node.op == "mul":
        return left * right
    raise ValueError(f"Unknown op: {node.op}")


def ast_equivalent_sympy(a: ProgramNode, b: ProgramNode) -> bool:
    """Return True if two ASTs are sympy-equivalent."""
    try:
        diff = sp.simplify(ast_to_sympy(a) - ast_to_sympy(b))
        return diff == 0
    except (TypeError, ValueError, sp.SympifyError):
        return False


def ast_equivalent_to_baseline_sympy(ast: ProgramNode, baseline_id: str) -> bool:
    """Check sympy equivalence to a named baseline expression."""
    baseline_map = {
        "wiener_index": "wiener_index",
        "degree_sum": "degree_sum",
        "clustering": "clustering",
        "algebraic_connectivity": "algebraic_connectivity",
        "num_edges": "num_edges",
    }
    if baseline_id not in baseline_map:
        return False
    baseline = ProgramNode(op="leaf", name=baseline_map[baseline_id])
    return ast_equivalent_sympy(ast, baseline)
