"""Evolutionary search over tensor ASTs."""

from __future__ import annotations

import random
import uuid

from namm.domains.tensor.ast import BINARY_OPS, TensorNode, leaf_names, tensor_leaf
from namm.domains.tensor.canonical import canonicalize
from namm.domains.tensor.features import DEFAULT_HEAT_TIMES, DEFAULT_SPECTRUM_SIZE
from namm.domains.tensor.generator import random_tensor_ast


def _clone(node: TensorNode) -> TensorNode:
    if node.is_leaf():
        return tensor_leaf(node.name)  # type: ignore[arg-type]
    return TensorNode(
        op=node.op,
        left=_clone(node.left),  # type: ignore[arg-type]
        right=_clone(node.right),  # type: ignore[arg-type]
    )


def _collect_nodes(node: TensorNode) -> list[TensorNode]:
    if node.is_leaf():
        return [node]
    return [node] + _collect_nodes(node.left) + _collect_nodes(node.right)  # type: ignore[arg-type]


def _replace_subtree(
    root: TensorNode, target: TensorNode, replacement: TensorNode
) -> TensorNode:
    if root is target:
        return _clone(replacement)
    if root.is_leaf():
        return root
    return TensorNode(
        op=root.op,
        left=_replace_subtree(root.left, target, replacement),  # type: ignore[arg-type]
        right=_replace_subtree(root.right, target, replacement),  # type: ignore[arg-type]
    )


def _mutate(
    node: TensorNode,
    rng: random.Random,
    *,
    max_depth: int,
    max_leaves: int,
    spectrum_size: int,
    heat_times: tuple[float, ...],
) -> TensorNode:
    nodes = _collect_nodes(node)
    target = rng.choice(nodes)
    if target.is_leaf() and rng.random() < 0.5:
        leaves = list(leaf_names(spectrum_size=spectrum_size, heat_times=heat_times))
        replacement = tensor_leaf(
            rng.choice(leaves), spectrum_size=spectrum_size, heat_times=heat_times
        )
    else:
        replacement, _ = random_tensor_ast(
            seed=rng.randint(0, 2**31 - 1),
            max_depth=max(1, max_depth - 1),
            max_leaves=max(2, max_leaves // 2),
            spectrum_size=spectrum_size,
            heat_times=heat_times,
        )
    return canonicalize(_replace_subtree(node, target, replacement))


def _crossover(a: TensorNode, b: TensorNode, rng: random.Random) -> TensorNode:
    nodes_a = _collect_nodes(a)
    nodes_b = _collect_nodes(b)
    if not nodes_a or not nodes_b:
        return canonicalize(_clone(a))
    sub_a = rng.choice(nodes_a)
    sub_b = rng.choice(nodes_b)
    return canonicalize(_replace_subtree(a, sub_a, sub_b))


def evolutionary_tensor_population(
    seed: int,
    *,
    population_size: int = 20,
    generations: int = 5,
    max_depth: int = 3,
    max_leaves: int = 5,
    fitness_fn=None,
    return_count: int | None = None,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> list[tuple[TensorNode, str]]:
    rng = random.Random(seed)
    count = return_count or population_size
    population: list[tuple[TensorNode, str, float]] = []

    for i in range(population_size):
        ast, _ = random_tensor_ast(
            seed=seed + i,
            max_depth=max_depth,
            max_leaves=max_leaves,
            spectrum_size=spectrum_size,
            heat_times=heat_times,
        )
        fitness = fitness_fn(ast) if fitness_fn else rng.random()
        population.append((ast, f"tensor-{uuid.uuid4().hex[:8]}", fitness))

    for _gen in range(generations):
        population.sort(key=lambda x: x[2], reverse=True)
        elites = population[: max(2, population_size // 4)]
        next_gen = [(canonicalize(_clone(e[0])), e[1], e[2]) for e in elites]

        while len(next_gen) < population_size:
            p1 = rng.choice(elites)[0]
            p2 = rng.choice(elites)[0]
            if rng.random() < 0.7:
                child = _crossover(p1, p2, rng)
            else:
                child = _mutate(
                    p1,
                    rng,
                    max_depth=max_depth,
                    max_leaves=max_leaves,
                    spectrum_size=spectrum_size,
                    heat_times=heat_times,
                )
            cid = f"tensor-{uuid.uuid4().hex[:8]}"
            fitness = fitness_fn(child) if fitness_fn else rng.random()
            next_gen.append((child, cid, fitness))
        population = next_gen

    population.sort(key=lambda x: x[2], reverse=True)
    seen: set[str] = set()
    results: list[tuple[TensorNode, str]] = []
    for ast, cid, _ in population:
        key = str(canonicalize(ast))
        if key in seen:
            continue
        seen.add(key)
        results.append((canonicalize(ast), cid))
        if len(results) >= count:
            break
    return results
