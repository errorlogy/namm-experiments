"""Random graph generation for TDA frame search."""

from __future__ import annotations

import random
import uuid

import networkx as nx

from namm.domains.graph.generator import enumerate_small_graphs


def random_tda_graph(
    seed: int,
    *,
    max_order: int = 8,
) -> tuple[nx.Graph, str]:
    """Sample a connected graph for TDA signature search."""
    rng = random.Random(seed)
    pool = [g for g in enumerate_small_graphs(max_order) if g.number_of_nodes() >= 3]
    if not pool:
        pool = list(enumerate_small_graphs(max_order))
    base = rng.choice(pool).copy()
    # light mutation: add/remove one edge if possible
    nodes = list(base.nodes())
    u, v = rng.sample(nodes, 2)
    if base.has_edge(u, v) and base.number_of_edges() > base.number_of_nodes() - 1:
        base.remove_edge(u, v)
        if not nx.is_connected(base):
            base.add_edge(u, v)
    elif not base.has_edge(u, v):
        base.add_edge(u, v)
    candidate_id = f"tda-{uuid.uuid4().hex[:8]}"
    return base, candidate_id
