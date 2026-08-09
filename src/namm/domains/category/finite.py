"""Finite category shadow: objects = graphs, morphisms = homomorphisms."""

from __future__ import annotations

import hashlib
import itertools
from dataclasses import dataclass

import networkx as nx

MAX_CATEGORY_ORDER = 6


@dataclass(frozen=True)
class FiniteCategoryShadow:
    """Hom-set counts for a finite family of graphs (category shadow)."""

    object_count: int
    morphism_counts: dict[str, int]
    self_endomorphisms: dict[str, int]
    shadow_hash: str

    def to_dict(self) -> dict:
        return {
            "object_count": self.object_count,
            "morphism_counts": self.morphism_counts,
            "self_endomorphisms": self.self_endomorphisms,
            "shadow_hash": self.shadow_hash,
        }


def _graph_label(g: nx.Graph) -> str:
    edges = tuple(sorted((min(u, v), max(u, v)) for u, v in g.edges()))
    return f"n{g.number_of_nodes()}_m{g.number_of_edges()}_e{hash(edges) % 10_000:04d}"


def count_homomorphisms(source: nx.Graph, target: nx.Graph) -> int:
    """Count graph homomorphisms source → target (edge-preserving maps)."""
    if source.number_of_nodes() > MAX_CATEGORY_ORDER or target.number_of_nodes() > MAX_CATEGORY_ORDER:
        raise ValueError(f"graphs must have order ≤ {MAX_CATEGORY_ORDER}")

    n_s = source.number_of_nodes()
    n_t = target.number_of_nodes()
    s_nodes = list(source.nodes())
    t_nodes = list(target.nodes())

    count = 0
    for assignment in itertools.product(t_nodes, repeat=n_s):
        mapping = dict(zip(s_nodes, assignment))
        ok = True
        for u, v in source.edges():
            if not target.has_edge(mapping[u], mapping[v]):
                ok = False
                break
        if ok:
            count += 1
    return count


def graph_category_shadow(graphs: list[nx.Graph]) -> FiniteCategoryShadow:
    """Build hom-set counts for all pairs in a finite graph family."""
    filtered = [g.copy() for g in graphs if g.number_of_nodes() <= MAX_CATEGORY_ORDER]
    labels = [_graph_label(g) for g in filtered]

    morphism_counts: dict[str, int] = {}
    self_endo: dict[str, int] = {}

    for i, g_src in enumerate(filtered):
        for j, g_tgt in enumerate(filtered):
            key = f"{labels[i]}->{labels[j]}"
            cnt = count_homomorphisms(g_src, g_tgt)
            morphism_counts[key] = cnt
            if i == j:
                self_endo[labels[i]] = cnt

    payload = "|".join(f"{k}:{v}" for k, v in sorted(morphism_counts.items()))
    shadow_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]

    return FiniteCategoryShadow(
        object_count=len(filtered),
        morphism_counts=morphism_counts,
        self_endomorphisms=self_endo,
        shadow_hash=shadow_hash,
    )
