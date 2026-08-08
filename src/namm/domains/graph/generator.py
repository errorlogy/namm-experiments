"""Random graph and invariant formula generation."""

from __future__ import annotations

import random
import uuid

import networkx as nx

from namm.schemas.experiment import InvariantFormula

PRIMITIVES = [
    "num_nodes",
    "num_edges",
    "avg_degree",
    "diameter",
    "radius",
    "clustering",
    "algebraic_connectivity",
    "wiener_index",
]

OPERATORS = ["+", "-", "*", "max", "min"]


def random_graph(n: int, p: float, seed: int | None = None) -> nx.Graph:
    """Generate a connected random graph on n nodes if possible."""
    rng = random.Random(seed)
    for _ in range(20):
        g = nx.erdos_renyi_graph(n, p, seed=rng.randint(0, 2**31 - 1))
        if nx.is_connected(g):
            return g
    # fallback: path graph is always connected
    return nx.path_graph(n)


def enumerate_small_graphs(max_order: int) -> list[nx.Graph]:
    """Enumerate connected graphs up to max_order (atlas for n<=5, sample above)."""
    graphs: list[nx.Graph] = []
    atlas = nx.graph_atlas_g()
    for n in range(1, max_order + 1):
        if n <= 5:
            for g in atlas:
                if g.number_of_nodes() == n and nx.is_connected(g):
                    graphs.append(g.copy())
        else:
            for seed in range(3):
                graphs.append(random_graph(n, 0.4, seed=seed + n * 10))
    return graphs


def random_invariant_formula(seed: int | None = None) -> InvariantFormula:
    """Generate a random linear combination of graph statistics."""
    rng = random.Random(seed)
    chosen = rng.sample(PRIMITIVES, k=rng.randint(2, 4))
    coeffs = [rng.randint(1, 5) for _ in chosen]
    terms = [f"{c}*{p}" for c, p in zip(coeffs, chosen)]
    op = rng.choice(["+", "-"])
    expression = f" {op} ".join(terms)
    return InvariantFormula(
        id=f"inv-{uuid.uuid4().hex[:8]}",
        expression=expression,
        primitives=chosen,
        meta_origin="random_composition_of_graph_statistics",
    )
