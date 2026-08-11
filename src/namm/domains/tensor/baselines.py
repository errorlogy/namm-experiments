"""Polynomial baseline programs (degree ≤4) over tensor leaves only."""

from __future__ import annotations

import itertools

from namm.domains.tensor.ast import TensorNode, leaf_names, tensor_leaf
from namm.domains.tensor.features import DEFAULT_HEAT_TIMES, DEFAULT_SPECTRUM_SIZE


def _mul_chain(nodes: list[TensorNode]) -> TensorNode:
    acc = nodes[0]
    for n in nodes[1:]:
        acc = TensorNode(op="mul", left=acc, right=n)
    return acc


def _add_chain(nodes: list[TensorNode]) -> TensorNode:
    acc = nodes[0]
    for n in nodes[1:]:
        acc = TensorNode(op="add", left=acc, right=n)
    return acc


def generate_tensor_baselines(
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
    max_degree: int = 4,
) -> dict[str, TensorNode]:
    """Return 20+ baseline ASTs built only from ADD/MUL on tensor leaves."""
    names = list(leaf_names(spectrum_size=spectrum_size, heat_times=heat_times))
    leaves = {
        n: tensor_leaf(n, spectrum_size=spectrum_size, heat_times=heat_times)
        for n in names
    }
    baselines: dict[str, TensorNode] = {}

    for n, node in leaves.items():
        baselines[f"leaf_{n}"] = node

    for i, j in itertools.combinations_with_replacement(names, 2):
        baselines[f"add_{i}_{j}"] = TensorNode(
            op="add", left=leaves[i], right=leaves[j]
        )
        baselines[f"mul_{i}_{j}"] = TensorNode(
            op="mul", left=leaves[i], right=leaves[j]
        )

    for i, j, k in itertools.combinations(names[: min(6, len(names))], 3):
        baselines[f"mul3_{i}_{j}_{k}"] = _mul_chain([leaves[i], leaves[j], leaves[k]])
        baselines[f"add_mul_{i}_{j}_{k}"] = TensorNode(
            op="add",
            left=leaves[i],
            right=TensorNode(op="mul", left=leaves[j], right=leaves[k]),
        )

    if max_degree >= 4 and len(names) >= 4:
        for quad in itertools.combinations(names[:4], 4):
            baselines[f"mul4_{'_'.join(quad)}"] = _mul_chain([leaves[q] for q in quad])

    if len(names) >= 3:
        baselines["sum_first3"] = _add_chain([leaves[names[0]], leaves[names[1]], leaves[names[2]]])

    return baselines
