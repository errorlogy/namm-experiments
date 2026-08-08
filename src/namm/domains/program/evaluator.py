"""Execute program AST on networkx graphs."""

from __future__ import annotations

import networkx as nx

from namm.domains.program.ast import ProgramNode


def _leaf_value(name: str, g: nx.Graph) -> float:
    n = g.number_of_nodes()
    m = g.number_of_edges()
    if name == "num_nodes":
        return float(n)
    if name == "num_edges":
        return float(m)
    if name == "degree_sum":
        return 2.0 * m
    if name == "avg_degree":
        return float(2 * m / n) if n > 0 else 0.0
    if name == "wiener_index":
        return float(nx.wiener_index(g)) if n > 1 else 0.0
    if name == "clustering":
        return float(nx.transitivity(g))
    if name == "algebraic_connectivity":
        from namm.domains.graph.invariants import algebraic_connectivity

        return algebraic_connectivity(g)
    if name == "diameter":
        return float(nx.diameter(g)) if n > 1 and nx.is_connected(g) else 0.0
    if name == "radius":
        return float(nx.radius(g)) if n > 1 and nx.is_connected(g) else 0.0
    raise ValueError(f"Unknown leaf: {name}")


def evaluate_ast(node: ProgramNode, g: nx.Graph) -> float:
    """Evaluate a program AST on a graph."""
    if node.is_leaf():
        return _leaf_value(node.name, g)  # type: ignore[arg-type]
    if node.op == "neg":
        return -evaluate_ast(node.child, g)  # type: ignore[arg-type]
    left = evaluate_ast(node.left, g)  # type: ignore[arg-type]
    right = evaluate_ast(node.right, g)  # type: ignore[arg-type]
    if node.op == "add":
        return left + right
    if node.op == "sub":
        return left - right
    if node.op == "mul":
        return left * right
    raise ValueError(f"Unknown op: {node.op}")


def ast_agrees_on_graphs(
    ast_a: ProgramNode,
    ast_b: ProgramNode,
    graphs: list[nx.Graph],
    tol: float = 1e-9,
) -> bool:
    """Return True if two ASTs yield identical values on all graphs."""
    for g in graphs:
        va = evaluate_ast(ast_a, g)
        vb = evaluate_ast(ast_b, g)
        if abs(va - vb) > tol:
            return False
    return True
