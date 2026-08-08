"""Known graph invariants and statistics."""

from __future__ import annotations

import networkx as nx
import numpy as np


def graph_statistics(g: nx.Graph) -> dict[str, float]:
    """Compute primitive statistics used in invariant formulas."""
    n = g.number_of_nodes()
    m = g.number_of_edges()
    stats: dict[str, float] = {
        "num_nodes": float(n),
        "num_edges": float(m),
        "avg_degree": float(2 * m / n) if n > 0 else 0.0,
        "diameter": float(nx.diameter(g)) if n > 1 else 0.0,
        "radius": float(nx.radius(g)) if n > 1 else 0.0,
        "clustering": float(nx.transitivity(g)),
        "wiener_index": float(wiener_index(g)),
        "algebraic_connectivity": float(algebraic_connectivity(g)),
    }
    return stats


def wiener_index(g: nx.Graph) -> float:
    """Sum of shortest-path distances between all unordered node pairs."""
    if g.number_of_nodes() <= 1:
        return 0.0
    return float(nx.wiener_index(g))


def algebraic_connectivity(g: nx.Graph) -> float:
    """Second-smallest Laplacian eigenvalue (Fiedler value)."""
    if g.number_of_nodes() <= 1:
        return 0.0
    lap = nx.laplacian_matrix(g).astype(float).toarray()
    eigenvalues = np.sort(np.linalg.eigvalsh(lap))
    return float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
