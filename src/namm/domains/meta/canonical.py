"""Canonical form and hashing for meta-evaluator ASTs."""

from __future__ import annotations

import hashlib
import json

from namm.domains.meta.ast import (
    COMMUTATIVE_OPS,
    MetaEvaluatorNode,
    meta_to_dict,
)


def canonicalize_meta(node: MetaEvaluatorNode) -> MetaEvaluatorNode:
    """Sort commutative operands; normalize structure."""
    if node.is_leaf() or node.op in ("self", "target"):
        return node
    left = canonicalize_meta(node.left)  # type: ignore[arg-type]
    right = canonicalize_meta(node.right)  # type: ignore[arg-type]
    if node.op in COMMUTATIVE_OPS:
        lk = _sort_key(left)
        rk = _sort_key(right)
        if lk > rk:
            left, right = right, left
    return MetaEvaluatorNode(op=node.op, left=left, right=right)


def _sort_key(node: MetaEvaluatorNode) -> str:
    return json.dumps(meta_to_dict(node), sort_keys=True)


def meta_hash(node: MetaEvaluatorNode) -> str:
    canonical = canonicalize_meta(node)
    payload = json.dumps(meta_to_dict(canonical), sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
