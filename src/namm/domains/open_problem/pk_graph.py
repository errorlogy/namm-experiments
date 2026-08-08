"""Kotzig P_k-graph finite shadow — counterexample search on small graphs."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


def count_paths_length_k(g: nx.Graph, source: int, target: int, k: int) -> int:
    """Count simple paths of exactly length k between distinct vertices."""
    if source == target:
        return 0
    if k < 1:
        return 0

    nodes = list(g.nodes())
    index = {v: i for i, v in enumerate(nodes)}
    adj: list[list[int]] = [[] for _ in nodes]
    for u, v in g.edges():
        ui, vi = index[u], index[v]
        adj[ui].append(vi)
        adj[vi].append(ui)

    si, ti = index[source], index[target]
    count = 0

    def dfs(cur: int, remaining: int, visited: int) -> None:
        nonlocal count
        if remaining == 0:
            if cur == ti:
                count += 1
            return
        for nxt in adj[cur]:
            bit = 1 << nxt
            if visited & bit:
                continue
            dfs(nxt, remaining - 1, visited | bit)

    dfs(si, k, 1 << si)
    return count


def pk_graph_violations(g: nx.Graph, k: int) -> list[tuple[int, int, int]]:
    """Return (u, v, path_count) for pairs violating the P_k-graph condition."""
    if g.number_of_nodes() < 2:
        return []
    nodes = list(g.nodes())
    bad: list[tuple[int, int, int]] = []
    for i, u in enumerate(nodes):
        for v in nodes[i + 1 :]:
            c = count_paths_length_k(g, u, v, k)
            if c != 1:
                bad.append((u, v, c))
    return bad


def is_pk_graph(g: nx.Graph, k: int) -> bool:
    """True iff every pair of distinct vertices has exactly one path of length k."""
    return g.number_of_nodes() >= 2 and not pk_graph_violations(g, k)


def pk_graph_score(g: nx.Graph, k: int) -> float:
    """Fraction of distinct vertex pairs with exactly one length-k path."""
    n = g.number_of_nodes()
    if n < 2:
        return 0.0
    total_pairs = n * (n - 1) // 2
    bad = pk_graph_violations(g, k)
    return (total_pairs - len(bad)) / total_pairs


@dataclass
class PkSearchHit:
    """Atlas graph that satisfies or nearly satisfies P_k structure."""

    graph_order: int
    graph_index: int
    k: int
    score: float
    is_counterexample: bool
    edge_list: list[tuple[int, int]]
    violations: list[tuple[int, int, int]]


@dataclass
class PkSearchResult:
    """Exhaustive bounded search outcome."""

    k_min: int
    k_max: int
    max_order: int
    graphs_scanned: int
    counterexamples: list[PkSearchHit]
    best_near_misses: list[PkSearchHit]


def _graph_signature(g: nx.Graph) -> tuple[int, list[tuple[int, int]]]:
    edges = sorted((min(u, v), max(u, v)) for u, v in g.edges())
    return g.number_of_nodes(), edges


def search_pk_counterexamples(
    *,
    max_order: int,
    k_min: int = 3,
    k_max: int = 8,
    top_near_misses: int = 5,
) -> PkSearchResult:
    """Scan NetworkX atlas connected graphs for Kotzig counterexamples."""
    atlas = nx.graph_atlas_g()
    counterexamples: list[PkSearchHit] = []
    near: list[PkSearchHit] = []
    scanned = 0

    for n in range(2, max_order + 1):
        idx = 0
        for g in atlas:
            if g.number_of_nodes() != n or not nx.is_connected(g):
                continue
            scanned += 1
            gc = g.copy()
            gc = nx.convert_node_labels_to_integers(gc, first_label=0)
            order, edges = _graph_signature(gc)
            for k in range(k_min, k_max + 1):
                violations = pk_graph_violations(gc, k)
                score = pk_graph_score(gc, k)
                hit = PkSearchHit(
                    graph_order=order,
                    graph_index=idx,
                    k=k,
                    score=score,
                    is_counterexample=score == 1.0,
                    edge_list=edges,
                    violations=violations[:10],
                )
                if hit.is_counterexample:
                    counterexamples.append(hit)
                elif score > 0.0:
                    near.append(hit)
            idx += 1

    near.sort(key=lambda h: (-h.score, h.k, h.graph_order))
    return PkSearchResult(
        k_min=k_min,
        k_max=k_max,
        max_order=max_order,
        graphs_scanned=scanned,
        counterexamples=counterexamples,
        best_near_misses=near[:top_near_misses],
    )
