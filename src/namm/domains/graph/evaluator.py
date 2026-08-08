"""Exact evaluation of invariant formulas on graphs."""

from __future__ import annotations

import ast
import operator

import networkx as nx

from namm.domains.graph.invariants import graph_statistics

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_ast(node: ast.AST, env: dict[str, float]) -> float:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise ValueError(f"Unknown primitive: {node.id}")
        return env[node.id]
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left, env)
        right = _eval_ast(node.right, env)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported operator: {op_type}")
        return _BIN_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand, env)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type}")
        return _UNARY_OPS[op_type](operand)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        args = [_eval_ast(a, env) for a in node.args]
        name = node.func.id
        if name == "max" and len(args) == 2:
            return max(args)
        if name == "min" and len(args) == 2:
            return min(args)
        raise ValueError(f"Unsupported function: {name}")
    raise ValueError(f"Unsupported expression node: {type(node)}")


def evaluate_formula(expression: str, g: nx.Graph) -> float:
    """Evaluate an invariant formula on a graph using networkx-derived stats."""
    env = graph_statistics(g)
    tree = ast.parse(expression, mode="eval")
    return _eval_ast(tree, env)


def formulas_agree_on_graphs(
    expr_a: str, expr_b: str, graphs: list[nx.Graph], tol: float = 1e-9
) -> bool:
    """Return True if two formulas yield identical values on all graphs."""
    for g in graphs:
        va = evaluate_formula(expr_a, g)
        vb = evaluate_formula(expr_b, g)
        if abs(va - vb) > tol:
            return False
    return True
