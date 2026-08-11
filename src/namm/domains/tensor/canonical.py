"""Canonical sort for commutative tensor AST nodes."""

from __future__ import annotations

import hashlib
import json

from namm.domains.tensor.ast import COMMUTATIVE_OPS, TensorNode, ast_to_dict


def canonicalize(node: TensorNode) -> TensorNode:
    if node.is_leaf():
        return node
    left = canonicalize(node.left)  # type: ignore[arg-type]
    right = canonicalize(node.right)  # type: ignore[arg-type]
    if node.op in COMMUTATIVE_OPS:
        left_key = _sort_key(left)
        right_key = _sort_key(right)
        if right_key < left_key:
            left, right = right, left
    return TensorNode(op=node.op, left=left, right=right)


def _sort_key(node: TensorNode) -> str:
    return json.dumps(ast_to_dict(node), sort_keys=True)


def ast_hash(node: TensorNode) -> str:
    payload = json.dumps(ast_to_dict(canonicalize(node)), sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
