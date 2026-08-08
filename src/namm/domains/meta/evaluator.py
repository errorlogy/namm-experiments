"""Execute meta-evaluator AST on graphs with self/target context."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from namm.domains.meta.ast import MetaEvaluatorNode
from namm.domains.program.evaluator import evaluate_ast
from namm.domains.program.ast import ProgramNode, leaf as prog_leaf


@dataclass
class MetaEvalContext:
    """Evaluation context for meta-evaluators."""

    root: MetaEvaluatorNode
    target: MetaEvaluatorNode | None
    graph: nx.Graph
    depth: int = 0
    max_depth: int = 8
    _root_cache: dict[int, float] | None = None

    def __post_init__(self) -> None:
        if self._root_cache is None:
            self._root_cache = {}


def _leaf_to_program(node: MetaEvaluatorNode) -> ProgramNode:
    """Convert a meta leaf to program AST for graph metric evaluation."""
    if not node.is_leaf():
        raise ValueError("Expected leaf node")
    return prog_leaf(node.name)  # type: ignore[arg-type]


def evaluate_meta(
    node: MetaEvaluatorNode,
    ctx: MetaEvalContext,
) -> float:
    """Evaluate meta-evaluator on graph with optional self/target references."""
    if node.is_leaf():
        prog = _leaf_to_program(node)
        return evaluate_ast(prog, ctx.graph)

    if node.op == "self":
        if ctx.depth >= ctx.max_depth:
            return 0.0
        next_depth = ctx.depth + 1
        cache = ctx._root_cache
        assert cache is not None
        if next_depth not in cache:
            child_ctx = MetaEvalContext(
                root=ctx.root,
                target=ctx.target,
                graph=ctx.graph,
                depth=next_depth,
                max_depth=ctx.max_depth,
                _root_cache=cache,
            )
            cache[next_depth] = evaluate_meta(ctx.root, child_ctx)
        return cache[next_depth]

    if node.op == "target":
        if ctx.target is None:
            return 0.0
        if ctx.depth >= ctx.max_depth:
            return 0.0
        child_ctx = MetaEvalContext(
            root=ctx.target,
            target=ctx.root,
            graph=ctx.graph,
            depth=ctx.depth + 1,
            max_depth=ctx.max_depth,
            _root_cache={},
        )
        return evaluate_meta(ctx.target, child_ctx)

    left = evaluate_meta(node.left, ctx)  # type: ignore[arg-type]
    right = evaluate_meta(node.right, ctx)  # type: ignore[arg-type]

    if node.op == "add":
        return left + right
    if node.op == "sub":
        return left - right
    if node.op == "mul":
        return left * right
    if node.op == "delta":
        return abs(left - right)
    if node.op == "ratio":
        denom = right if abs(right) > 1e-12 else 1e-12
        return left / denom
    raise ValueError(f"Unknown meta op: {node.op}")


def evaluate_meta_on_graph(
    node: MetaEvaluatorNode,
    graph: nx.Graph,
    *,
    target: MetaEvaluatorNode | None = None,
    max_depth: int = 8,
) -> float:
    """Convenience wrapper for single-graph evaluation."""
    ctx = MetaEvalContext(
        root=node,
        target=target,
        graph=graph,
        depth=0,
        max_depth=max_depth,
    )
    return evaluate_meta(node, ctx)


def meta_agrees_on_graphs(
    ast_a: MetaEvaluatorNode,
    ast_b: MetaEvaluatorNode,
    graphs: list[nx.Graph],
    tol: float = 1e-6,
) -> bool:
    """Return True if two meta-evaluators yield identical values on all graphs."""
    for g in graphs:
        va = evaluate_meta_on_graph(ast_a, g)
        vb = evaluate_meta_on_graph(ast_b, g)
        if abs(va - vb) > tol:
            return False
    return True


def fixed_point_score(
    evaluator: MetaEvaluatorNode,
    transformed: MetaEvaluatorNode,
    graphs: list[nx.Graph],
    tol: float = 1e-6,
) -> float:
    """Fraction of benchmark graphs where E(g) ≈ F(E)(g)."""
    if not graphs:
        return 0.0
    matches = 0
    for g in graphs:
        ve = evaluate_meta_on_graph(evaluator, g)
        vf = evaluate_meta_on_graph(transformed, g)
        if abs(ve - vf) <= tol:
            matches += 1
    return matches / len(graphs)
