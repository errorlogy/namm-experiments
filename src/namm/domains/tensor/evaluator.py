"""Evaluate tensor AST programs on graphs."""

from __future__ import annotations

import networkx as nx

from namm.domains.tensor.ast import TensorNode
from namm.domains.tensor.features import (
    DEFAULT_HEAT_TIMES,
    DEFAULT_SPECTRUM_SIZE,
    graph_tensor_vector,
)


def evaluate_tensor_ast(
    node: TensorNode,
    g: nx.Graph,
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> float:
    if node.is_leaf():
        idx = int(node.name[1:])  # type: ignore[union-attr,index]
        vec = graph_tensor_vector(
            g, spectrum_size=spectrum_size, heat_times=heat_times
        )
        return vec[idx] if idx < len(vec) else 0.0
    left = evaluate_tensor_ast(
        node.left, g, spectrum_size=spectrum_size, heat_times=heat_times  # type: ignore[arg-type]
    )
    right = evaluate_tensor_ast(
        node.right, g, spectrum_size=spectrum_size, heat_times=heat_times  # type: ignore[arg-type]
    )
    if node.op == "add":
        return left + right
    if node.op == "mul":
        return left * right
    raise ValueError(f"Unknown op: {node.op}")


def tensor_ast_agrees_on_graphs(
    ast_a: TensorNode,
    ast_b: TensorNode,
    graphs: list[nx.Graph],
    tol: float = 1e-9,
    **kwargs,
) -> bool:
    for g in graphs:
        va = evaluate_tensor_ast(ast_a, g, **kwargs)
        vb = evaluate_tensor_ast(ast_b, g, **kwargs)
        if abs(va - vb) > tol:
            return False
    return True
