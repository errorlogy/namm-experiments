"""AST to lossy string for display and optional simplify checks."""

from __future__ import annotations

from namm.domains.program.ast import ProgramNode


def ast_to_expression(node: ProgramNode) -> str:
    """Lossy string projection of AST (not canonical)."""
    if node.is_leaf():
        return f"1*{node.name}"
    if node.op == "neg":
        return f"(-({ast_to_expression(node.child)}))"  # type: ignore[arg-type]
    sym = {"add": "+", "sub": "-", "mul": "*"}[node.op]
    return f"({ast_to_expression(node.left)} {sym} {ast_to_expression(node.right)})"


def collect_leaf_names(node: ProgramNode) -> list[str]:
    if node.is_leaf():
        return [node.name]  # type: ignore[list-item]
    if node.op == "neg":
        return collect_leaf_names(node.child)  # type: ignore[arg-type]
    return collect_leaf_names(node.left) + collect_leaf_names(node.right)  # type: ignore[arg-type]
