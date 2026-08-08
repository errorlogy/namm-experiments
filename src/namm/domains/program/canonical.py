"""AST canonicalization and stable hashing."""

from __future__ import annotations

import hashlib
import json

from namm.domains.program.ast import COMMUTATIVE_OPS, ProgramNode, ast_to_dict


def canonicalize(node: ProgramNode) -> ProgramNode:
    """Sort commutative ops; produce stable tree shape."""
    if node.is_leaf():
        return node
    if node.op == "neg":
        return ProgramNode(op="neg", child=canonicalize(node.child))  # type: ignore[arg-type]
    left = canonicalize(node.left)  # type: ignore[arg-type]
    right = canonicalize(node.right)  # type: ignore[arg-type]
    if node.op in COMMUTATIVE_OPS:
        left_key = _sort_key(left)
        right_key = _sort_key(right)
        if right_key < left_key:
            left, right = right, left
    return ProgramNode(op=node.op, left=left, right=right)


def _sort_key(node: ProgramNode) -> str:
    return json.dumps(ast_to_dict(canonicalize(node)), sort_keys=True)


def ast_hash(node: ProgramNode) -> str:
    """Stable SHA-256 hash of canonical AST JSON."""
    canonical = canonicalize(node)
    payload = json.dumps(ast_to_dict(canonical), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
