"""AST over raw numeric tensor leaves — ADD/MUL/COMPOSE only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from namm.domains.tensor.features import (
    DEFAULT_HEAT_TIMES,
    DEFAULT_SPECTRUM_SIZE,
    tensor_leaf_count,
)

BINARY_OPS = ("add", "mul")
COMMUTATIVE_OPS = ("add", "mul")


def leaf_names(
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> tuple[str, ...]:
    count = tensor_leaf_count(spectrum_size=spectrum_size, heat_times=heat_times)
    return tuple(f"t{i}" for i in range(count))


@dataclass(frozen=True)
class TensorNode:
    """Program tree over numeric tensor leaves."""

    op: str
    name: str | None = None
    left: TensorNode | None = None
    right: TensorNode | None = None

    def is_leaf(self) -> bool:
        return self.op == "leaf"


def tensor_leaf(
    name: str,
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> TensorNode:
    allowed = leaf_names(spectrum_size=spectrum_size, heat_times=heat_times)
    if name not in allowed:
        raise ValueError(f"Unknown tensor leaf: {name}")
    return TensorNode(op="leaf", name=name)


def ast_to_dict(node: TensorNode) -> dict[str, Any]:
    if node.is_leaf():
        return {"op": "leaf", "name": node.name}
    return {
        "op": node.op,
        "left": ast_to_dict(node.left),  # type: ignore[arg-type]
        "right": ast_to_dict(node.right),  # type: ignore[arg-type]
    }


def parse_ast_dict(data: dict[str, Any]) -> TensorNode:
    op = data["op"]
    if op == "leaf":
        return TensorNode(op="leaf", name=data["name"])
    if op in BINARY_OPS:
        return TensorNode(
            op=op,
            left=parse_ast_dict(data["left"]),
            right=parse_ast_dict(data["right"]),
        )
    raise ValueError(f"Unknown op: {op}")
