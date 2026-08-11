"""Random tensor AST generation — numeric leaves only."""

from __future__ import annotations

import random
import uuid

from namm.domains.tensor.ast import (
    BINARY_OPS,
    TensorNode,
    leaf_names,
    tensor_leaf,
)
from namm.domains.tensor.features import DEFAULT_HEAT_TIMES, DEFAULT_SPECTRUM_SIZE


def random_tensor_ast(
    seed: int | None = None,
    *,
    max_depth: int = 3,
    max_leaves: int = 5,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> tuple[TensorNode, str]:
    rng = random.Random(seed)
    candidate_id = f"tensor-{uuid.uuid4().hex[:8]}"
    leaves = list(leaf_names(spectrum_size=spectrum_size, heat_times=heat_times))
    leaves_used = [0]

    def _gen(depth: int) -> TensorNode:
        leaves_used[0] += 1
        if depth >= max_depth or leaves_used[0] >= max_leaves or rng.random() < 0.35:
            return tensor_leaf(
                rng.choice(leaves),
                spectrum_size=spectrum_size,
                heat_times=heat_times,
            )
        op = rng.choice(BINARY_OPS)
        left = _gen(depth + 1)
        right = _gen(depth + 1)
        return TensorNode(op=op, left=left, right=right)

    return _gen(0), candidate_id
