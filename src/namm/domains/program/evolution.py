"""Evolutionary search over program ASTs (Graph → Int invariants)."""

from __future__ import annotations

import random
import uuid
from copy import deepcopy

from namm.domains.program.ast import BINARY_OPS, LEAF_OPS, ProgramNode, leaf
from namm.domains.program.canonical import canonicalize
from namm.domains.program.generator import random_program_ast


def _clone(node: ProgramNode) -> ProgramNode:
    if node.is_leaf():
        return leaf(node.name)  # type: ignore[arg-type]
    if node.op == "neg":
        return ProgramNode(op="neg", child=_clone(node.child))  # type: ignore[arg-type]
    return ProgramNode(
        op=node.op,
        left=_clone(node.left),  # type: ignore[arg-type]
        right=_clone(node.right),  # type: ignore[arg-type]
    )


def _collect_nodes(node: ProgramNode) -> list[ProgramNode]:
    if node.is_leaf():
        return [node]
    if node.op == "neg":
        return [node] + _collect_nodes(node.child)  # type: ignore[arg-type]
    return [node] + _collect_nodes(node.left) + _collect_nodes(node.right)  # type: ignore[arg-type]


def _replace_subtree(root: ProgramNode, target: ProgramNode, replacement: ProgramNode) -> ProgramNode:
    if root is target:
        return _clone(replacement)
    if root.is_leaf():
        return root
    if root.op == "neg":
        return ProgramNode(op="neg", child=_replace_subtree(root.child, target, replacement))  # type: ignore[arg-type]
    return ProgramNode(
        op=root.op,
        left=_replace_subtree(root.left, target, replacement),  # type: ignore[arg-type]
        right=_replace_subtree(root.right, target, replacement),  # type: ignore[arg-type]
    )


def _mutate(node: ProgramNode, rng: random.Random, max_depth: int, max_leaves: int) -> ProgramNode:
    nodes = _collect_nodes(node)
    target = rng.choice(nodes)
    if target.is_leaf() and rng.random() < 0.5:
        replacement = leaf(rng.choice(LEAF_OPS))
    else:
        replacement, _ = random_program_ast(
            seed=rng.randint(0, 2**31 - 1),
            max_depth=max(1, max_depth - 1),
            max_leaves=max(2, max_leaves // 2),
        )
    return canonicalize(_replace_subtree(node, target, replacement))


def _crossover(a: ProgramNode, b: ProgramNode, rng: random.Random) -> ProgramNode:
    nodes_a = _collect_nodes(a)
    nodes_b = _collect_nodes(b)
    if not nodes_a or not nodes_b:
        return canonicalize(_clone(a))
    sub_a = rng.choice(nodes_a)
    sub_b = rng.choice(nodes_b)
    child = _replace_subtree(a, sub_a, sub_b)
    return canonicalize(child)


def evolutionary_program_ast(
    seed: int,
    *,
    population_size: int = 20,
    generations: int = 5,
    max_depth: int = 3,
    max_leaves: int = 5,
    fitness_fn=None,
) -> tuple[ProgramNode, str]:
    """
    Simple genetic search over ASTs.

    fitness_fn(node) -> float; higher is better. If None, returns best random individual.
    """
    rng = random.Random(seed)
    population: list[tuple[ProgramNode, str, float]] = []

    for i in range(population_size):
        ast, _ = random_program_ast(
            seed=seed + i,
            max_depth=max_depth,
            max_leaves=max_leaves,
        )
        fitness = fitness_fn(ast) if fitness_fn else rng.random()
        population.append((ast, f"prog-{uuid.uuid4().hex[:8]}", fitness))

    for gen in range(generations):
        population.sort(key=lambda x: x[2], reverse=True)
        elites = population[: max(2, population_size // 4)]
        next_gen = [(canonicalize(_clone(e[0])), e[1], e[2]) for e in elites]

        while len(next_gen) < population_size:
            p1 = rng.choice(elites)[0]
            p2 = rng.choice(elites)[0]
            if rng.random() < 0.7:
                child = _crossover(p1, p2, rng)
            else:
                child = _mutate(p1, rng, max_depth, max_leaves)
            cid = f"prog-{uuid.uuid4().hex[:8]}"
            fitness = fitness_fn(child) if fitness_fn else rng.random()
            next_gen.append((child, cid, fitness))
        population = next_gen

    population.sort(key=lambda x: x[2], reverse=True)
    best_ast, best_id, _ = population[0]
    return canonicalize(best_ast), best_id


def evolutionary_program_population(
    seed: int,
    *,
    population_size: int = 20,
    generations: int = 5,
    max_depth: int = 3,
    max_leaves: int = 5,
    fitness_fn=None,
    return_count: int | None = None,
) -> list[tuple[ProgramNode, str]]:
    """
    Run genetic search once; return top individuals from final population.

    return_count defaults to population_size.
    """
    rng = random.Random(seed)
    count = return_count or population_size
    population: list[tuple[ProgramNode, str, float]] = []

    for i in range(population_size):
        ast, _ = random_program_ast(
            seed=seed + i,
            max_depth=max_depth,
            max_leaves=max_leaves,
        )
        fitness = fitness_fn(ast) if fitness_fn else rng.random()
        population.append((ast, f"prog-{uuid.uuid4().hex[:8]}", fitness))

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
                child = _mutate(p1, rng, max_depth, max_leaves)
            cid = f"prog-{uuid.uuid4().hex[:8]}"
            fitness = fitness_fn(child) if fitness_fn else rng.random()
            next_gen.append((child, cid, fitness))
        population = next_gen

    population.sort(key=lambda x: x[2], reverse=True)
    seen: set[str] = set()
    results: list[tuple[ProgramNode, str]] = []
    for ast, cid, _ in population:
        key = str(canonicalize(ast))
        if key in seen:
            continue
        seen.add(key)
        results.append((canonicalize(ast), cid))
        if len(results) >= count:
            break
    return results
