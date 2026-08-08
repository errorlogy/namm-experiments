"""Random AST generation with depth and operator limits."""

from __future__ import annotations

import random
import uuid

from namm.domains.program.ast import LEAF_OPS, BINARY_OPS, ProgramNode, leaf


def random_program_ast(
    seed: int | None = None,
    max_depth: int = 3,
    max_leaves: int = 5,
) -> tuple[ProgramNode, str]:
    """Generate a random program AST. Returns (ast, candidate_id)."""
    rng = random.Random(seed)
    candidate_id = f"prog-{uuid.uuid4().hex[:8]}"
    leaves_used = [0]

    def _gen(depth: int) -> ProgramNode:
        leaves_used[0] += 1
        if depth >= max_depth or leaves_used[0] >= max_leaves or rng.random() < 0.35:
            return leaf(rng.choice(LEAF_OPS))
        op = rng.choice(BINARY_OPS)
        left = _gen(depth + 1)
        right = _gen(depth + 1)
        return ProgramNode(op=op, left=left, right=right)

    return _gen(0), candidate_id
