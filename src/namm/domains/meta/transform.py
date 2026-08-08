"""F(E): meta-transformations on evaluator programs."""

from __future__ import annotations

from typing import Callable

from namm.domains.meta.ast import MetaEvaluatorNode, meta_leaf, meta_self
from namm.domains.meta.canonical import canonicalize_meta

TransformFn = Callable[[MetaEvaluatorNode], MetaEvaluatorNode]

TRANSFORM_REGISTRY: dict[str, TransformFn] = {}


def _register(name: str):
    def decorator(fn: TransformFn) -> TransformFn:
        TRANSFORM_REGISTRY[name] = fn
        return fn
    return decorator


@_register("identity")
def transform_identity(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = E."""
    return node


@_register("canonicalize")
def transform_canonicalize(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = canonical form of E."""
    return canonicalize_meta(node)


@_register("add_zero")
def transform_add_zero(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = E + 0 via mul(num_nodes, 0)."""
    zero = MetaEvaluatorNode(
        op="mul",
        left=meta_leaf("num_nodes"),
        right=meta_leaf("num_nodes"),
    )
    zero = MetaEvaluatorNode(
        op="sub",
        left=zero,
        right=zero,
    )
    return MetaEvaluatorNode(op="add", left=node, right=zero)


@_register("double_halve")
def transform_double_halve(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = (E + E) * n/(2n) = E on graphs with n > 0."""
    doubled = MetaEvaluatorNode(op="add", left=node, right=_clone(node))
    n = meta_leaf("num_nodes")
    two_n = MetaEvaluatorNode(op="add", left=n, right=_clone(n))
    half = MetaEvaluatorNode(op="ratio", left=n, right=two_n)
    return MetaEvaluatorNode(op="mul", left=doubled, right=half)


@_register("self_unfold")
def transform_self_unfold(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = E with self nodes replaced by E (one unfold)."""
    return _replace_self(node, node)


@_register("swap_commutative")
def transform_swap_commutative(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = E with commutative operands swapped where applicable."""
    return _swap_commutative(node)


@_register("compose_identity")
def transform_compose_identity(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """F(E) = E composed with identity leaf (wiener_index * 0 + E)."""
    zero_w = MetaEvaluatorNode(
        op="mul",
        left=meta_leaf("wiener_index"),
        right=MetaEvaluatorNode(
            op="sub",
            left=meta_leaf("num_nodes"),
            right=meta_leaf("num_nodes"),
        ),
    )
    return MetaEvaluatorNode(op="add", left=zero_w, right=_clone(node))


def apply_transform(name: str, node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """Apply named transform F to evaluator E."""
    if name not in TRANSFORM_REGISTRY:
        raise ValueError(f"Unknown transform: {name}")
    return TRANSFORM_REGISTRY[name](node)


def list_transforms() -> list[str]:
    return sorted(TRANSFORM_REGISTRY.keys())


def _clone(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    if node.is_leaf() or node.op in ("self", "target"):
        return MetaEvaluatorNode(op=node.op, name=node.name)
    return MetaEvaluatorNode(
        op=node.op,
        left=_clone(node.left),  # type: ignore[arg-type]
        right=_clone(node.right),  # type: ignore[arg-type]
    )


def _replace_self(
    node: MetaEvaluatorNode,
    replacement: MetaEvaluatorNode,
) -> MetaEvaluatorNode:
    if node.op == "self":
        return _clone(replacement)
    if node.is_leaf() or node.op == "target":
        return MetaEvaluatorNode(op=node.op, name=node.name)
    return MetaEvaluatorNode(
        op=node.op,
        left=_replace_self(node.left, replacement),  # type: ignore[arg-type]
        right=_replace_self(node.right, replacement),  # type: ignore[arg-type]
    )


def _swap_commutative(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    if node.is_leaf() or node.op in ("self", "target"):
        return MetaEvaluatorNode(op=node.op, name=node.name)
    left = _swap_commutative(node.left)  # type: ignore[arg-type]
    right = _swap_commutative(node.right)  # type: ignore[arg-type]
    if node.op in ("add", "mul"):
        return MetaEvaluatorNode(op=node.op, left=right, right=left)
    return MetaEvaluatorNode(op=node.op, left=left, right=right)
