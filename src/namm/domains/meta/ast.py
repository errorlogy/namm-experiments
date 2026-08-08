"""Meta-evaluator AST: programs that evaluate graphs and reference self/target."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from namm.domains.program.ast import LEAF_OPS

META_OPS = ("leaf", "add", "sub", "mul", "self", "target", "delta", "ratio")
BINARY_OPS = ("add", "sub", "mul")
COMMUTATIVE_OPS = ("add", "mul")


@dataclass(frozen=True)
class MetaEvaluatorNode:
    """Evaluator program tree with self/target meta references."""

    op: str
    name: str | None = None
    left: MetaEvaluatorNode | None = None
    right: MetaEvaluatorNode | None = None

    def is_leaf(self) -> bool:
        return self.op == "leaf"


def meta_leaf(name: str) -> MetaEvaluatorNode:
    if name not in LEAF_OPS:
        raise ValueError(f"Unknown leaf: {name}")
    return MetaEvaluatorNode(op="leaf", name=name)


def meta_self() -> MetaEvaluatorNode:
    return MetaEvaluatorNode(op="self")


def meta_target() -> MetaEvaluatorNode:
    return MetaEvaluatorNode(op="target")


def meta_to_dict(node: MetaEvaluatorNode) -> dict[str, Any]:
    if node.is_leaf():
        return {"op": "leaf", "name": node.name}
    if node.op in ("self", "target"):
        return {"op": node.op}
    return {
        "op": node.op,
        "left": meta_to_dict(node.left),  # type: ignore[arg-type]
        "right": meta_to_dict(node.right),  # type: ignore[arg-type]
    }


def parse_meta_dict(data: dict[str, Any]) -> MetaEvaluatorNode:
    op = data["op"]
    if op == "leaf":
        return meta_leaf(data["name"])
    if op == "self":
        return meta_self()
    if op == "target":
        return meta_target()
    if op in BINARY_OPS:
        return MetaEvaluatorNode(
            op=op,
            left=parse_meta_dict(data["left"]),
            right=parse_meta_dict(data["right"]),
        )
    if op in ("delta", "ratio"):
        return MetaEvaluatorNode(
            op=op,
            left=parse_meta_dict(data["left"]),
            right=parse_meta_dict(data["right"]),
        )
    raise ValueError(f"Unknown meta op: {op}")
