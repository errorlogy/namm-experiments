"""AST node types for small graph-invariant programs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

LeafName = Literal[
    "num_nodes",
    "num_edges",
    "degree_sum",
    "avg_degree",
    "wiener_index",
    "clustering",
    "algebraic_connectivity",
    "diameter",
    "radius",
]

LEAF_OPS: tuple[str, ...] = (
    "num_nodes",
    "num_edges",
    "degree_sum",
    "avg_degree",
    "wiener_index",
    "clustering",
    "algebraic_connectivity",
    "diameter",
    "radius",
)

BINARY_OPS = ("add", "sub", "mul")
COMMUTATIVE_OPS = ("add", "mul")


@dataclass(frozen=True)
class ProgramNode:
    """Small program tree: leaf primitives or binary ops."""

    op: str
    name: str | None = None
    left: ProgramNode | None = None
    right: ProgramNode | None = None
    child: ProgramNode | None = None

    def is_leaf(self) -> bool:
        return self.op == "leaf"


def leaf(name: str) -> ProgramNode:
    if name not in LEAF_OPS:
        raise ValueError(f"Unknown leaf: {name}")
    return ProgramNode(op="leaf", name=name)


def ast_to_dict(node: ProgramNode) -> dict[str, Any]:
    if node.is_leaf():
        return {"op": "leaf", "name": node.name}
    if node.op == "neg":
        return {"op": "neg", "child": ast_to_dict(node.child)}  # type: ignore[arg-type]
    return {
        "op": node.op,
        "left": ast_to_dict(node.left),  # type: ignore[arg-type]
        "right": ast_to_dict(node.right),  # type: ignore[arg-type]
    }


def parse_ast_dict(data: dict[str, Any]) -> ProgramNode:
    op = data["op"]
    if op == "leaf":
        return leaf(data["name"])
    if op == "neg":
        return ProgramNode(op="neg", child=parse_ast_dict(data["child"]))
    if op in BINARY_OPS:
        return ProgramNode(
            op=op,
            left=parse_ast_dict(data["left"]),
            right=parse_ast_dict(data["right"]),
        )
    raise ValueError(f"Unknown op: {op}")
