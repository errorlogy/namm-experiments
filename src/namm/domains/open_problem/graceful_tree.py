"""Graceful Tree Conjecture finite shadow — backtracking label search."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


def is_graceful_labeling(g: nx.Graph, labeling: dict[int, int]) -> bool:
    """True if vertex labels yield distinct edge sums."""
    if g.number_of_edges() == 0:
        return True
    seen: set[int] = set()
    for u, v in g.edges():
        s = labeling[int(u)] + labeling[int(v)]
        if s in seen:
            return False
        seen.add(s)
    return len(seen) == g.number_of_edges()


def find_graceful_labeling(g: nx.Graph) -> dict[int, int] | None:
    """Backtracking search for a graceful labeling; None if none found."""
    gc = nx.convert_node_labels_to_integers(g, first_label=0)
    nodes = sorted(int(v) for v in gc.nodes())
    m = gc.number_of_edges()
    if not nodes:
        return {}
    if m == 0:
        return {nodes[0]: 0}

    edges = [(int(u), int(v)) for u, v in gc.edges()]
    assignment: dict[int, int | None] = {v: None for v in nodes}

    def partial_valid() -> bool:
        sums: list[int] = []
        for u, w in edges:
            lu, lw = assignment[u], assignment[w]
            if lu is not None and lw is not None:
                s = lu + lw
                if s in sums:
                    return False
                sums.append(s)
        return True

    def backtrack(idx: int) -> bool:
        if idx == len(nodes):
            sums: list[int] = []
            for u, w in edges:
                s = assignment[u] + assignment[w]  # type: ignore[operator]
                if s in sums:
                    return False
                sums.append(s)
            return len(sums) == m

        v = nodes[idx]
        used = {assignment[x] for x in nodes if assignment[x] is not None}
        for lab in range(m + 1):
            if lab in used:
                continue
            assignment[v] = lab
            if partial_valid() and backtrack(idx + 1):
                return True
            assignment[v] = None
        return False

    if backtrack(0):
        return {v: int(assignment[v]) for v in nodes}  # type: ignore[arg-type]
    return None


def has_graceful_labeling(g: nx.Graph) -> bool:
    return find_graceful_labeling(g) is not None


@dataclass
class GracefulTreeHit:
    tree_order: int
    tree_index: int
    is_counterexample: bool
    edge_list: list[tuple[int, int]]
    labeling: dict[int, int] | None


@dataclass
class GracefulTreeSearchResult:
    max_order: int
    trees_scanned: int
    counterexamples: list[GracefulTreeHit]
    verified_trees: list[GracefulTreeHit]


def _tree_signature(g: nx.Graph) -> tuple[int, list[tuple[int, int]]]:
    gc = nx.convert_node_labels_to_integers(g, first_label=0)
    edges = sorted((min(u, v), max(u, v)) for u, v in gc.edges())
    return gc.number_of_nodes(), edges


def search_graceful_tree_counterexamples(
    *,
    max_order: int,
    top_verified: int = 5,
) -> GracefulTreeSearchResult:
    """Enumerate non-isomorphic trees up to max_order; find non-graceful trees."""
    counterexamples: list[GracefulTreeHit] = []
    verified: list[GracefulTreeHit] = []
    scanned = 0

    for n in range(1, max_order + 1):
        idx = 0
        for tree in nx.nonisomorphic_trees(n):
            scanned += 1
            gc = nx.convert_node_labels_to_integers(tree, first_label=0)
            order, edges = _tree_signature(gc)
            labeling = find_graceful_labeling(gc)
            hit = GracefulTreeHit(
                tree_order=order,
                tree_index=idx,
                is_counterexample=labeling is None,
                edge_list=edges,
                labeling=labeling,
            )
            if hit.is_counterexample:
                counterexamples.append(hit)
            else:
                verified.append(hit)
            idx += 1

    verified.sort(key=lambda h: (-h.tree_order, h.tree_index))
    return GracefulTreeSearchResult(
        max_order=max_order,
        trees_scanned=scanned,
        counterexamples=counterexamples,
        verified_trees=verified[:top_verified],
    )
