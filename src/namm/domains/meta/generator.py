"""Random meta-evaluator AST generation."""

from __future__ import annotations

import random
import uuid

from namm.domains.meta.ast import (
    MetaEvaluatorNode,
    meta_leaf,
    meta_self,
    meta_target,
)
from namm.domains.program.ast import LEAF_OPS


def random_meta_evaluator(
    seed: int,
    *,
    max_depth: int = 3,
    include_self: bool = True,
    include_target: bool = False,
) -> tuple[MetaEvaluatorNode, str]:
    """Generate a random meta-evaluator AST."""
    rng = random.Random(seed)
    node = _gen_node(rng, depth=0, max_depth=max_depth, include_self=include_self, include_target=include_target)
    candidate_id = f"meta-{uuid.uuid4().hex[:8]}"
    return node, candidate_id


def _gen_node(
    rng: random.Random,
    *,
    depth: int,
    max_depth: int,
    include_self: bool,
    include_target: bool,
) -> MetaEvaluatorNode:
    if depth >= max_depth:
        return meta_leaf(rng.choice(LEAF_OPS))

    choices: list[str] = ["leaf", "binary"]
    if include_self and depth > 0:
        choices.append("self")
    if include_target and depth > 0:
        choices.append("target")

    kind = rng.choice(choices)
    if kind == "leaf":
        return meta_leaf(rng.choice(LEAF_OPS))
    if kind == "self":
        return meta_self()
    if kind == "target":
        return meta_target()

    op = rng.choice(["add", "sub", "mul"])
    left = _gen_node(rng, depth=depth + 1, max_depth=max_depth, include_self=include_self, include_target=include_target)
    right = _gen_node(rng, depth=depth + 1, max_depth=max_depth, include_self=include_self, include_target=include_target)
    return MetaEvaluatorNode(op=op, left=left, right=right)
