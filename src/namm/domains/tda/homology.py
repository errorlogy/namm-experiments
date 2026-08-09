"""Persistent homology on graph shortest-path metric via Gudhi."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import networkx as nx
import numpy as np

MAX_TDA_ORDER = 20


@dataclass(frozen=True)
class PersistenceSignature:
    """Machine-native persistence summary for a graph metric space."""

    betti_0: int
    betti_1: int
    total_persistence_h1: float
    persistence_entropy_h1: float
    max_order: int
    filtration_steps: int
    signature_hash: str

    def to_dict(self) -> dict:
        return {
            "betti_0": self.betti_0,
            "betti_1": self.betti_1,
            "total_persistence_h1": self.total_persistence_h1,
            "persistence_entropy_h1": self.persistence_entropy_h1,
            "max_order": self.max_order,
            "filtration_steps": self.filtration_steps,
            "signature_hash": self.signature_hash,
        }


def _shortest_path_matrix(g: nx.Graph) -> np.ndarray:
    n = g.number_of_nodes()
    dist = np.full((n, n), np.inf, dtype=float)
    for i in range(n):
        dist[i, i] = 0.0
    for u, v in g.edges():
        dist[u, v] = 1.0
        dist[v, u] = 1.0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                via = dist[i, k] + dist[k, j]
                if via < dist[i, j]:
                    dist[i, j] = via
    max_finite = np.max(dist[np.isfinite(dist)])
    dist[~np.isfinite(dist)] = max_finite + 1.0
    return dist


def _persistence_entropy(lifetimes: list[float]) -> float:
    if not lifetimes:
        return 0.0
    total = sum(lifetimes)
    if total <= 0:
        return 0.0
    probs = [lt / total for lt in lifetimes if lt > 0]
    return float(-sum(p * np.log(p + 1e-12) for p in probs))


def graph_persistence_signature(
    g: nx.Graph,
    *,
    max_edge_length: float = 3.0,
    filtration_steps: int = 10,
) -> PersistenceSignature:
    """Compute H0/H1 persistence signature from graph geodesic metric.

    Uses Gudhi Rips complex on shortest-path distances. Graphs with order > 20
    raise ValueError to keep computation tractable.
    """
    gudhi = __import__("gudhi")

    n = g.number_of_nodes()
    if n == 0:
        raise ValueError("empty graph")
    if n > MAX_TDA_ORDER:
        raise ValueError(f"graph order {n} exceeds TDA limit {MAX_TDA_ORDER}")

    dist = _shortest_path_matrix(g)
    rips = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=max_edge_length)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()

    pairs = st.persistence()
    h0_lives: list[float] = []
    h1_lives: list[float] = []
    for dim, (birth, death) in pairs:
        life = death - birth if np.isfinite(death) else max_edge_length - birth
        if life <= 0:
            continue
        if dim == 0:
            h0_lives.append(float(life))
        elif dim == 1:
            h1_lives.append(float(life))

    betti_0 = len(h0_lives) if h0_lives else 1
    betti_1 = len(h1_lives)
    total_h1 = float(sum(h1_lives))
    entropy_h1 = _persistence_entropy(h1_lives)

    payload = f"{betti_0}:{betti_1}:{total_h1:.6f}:{entropy_h1:.6f}:{n}"
    sig_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]

    return PersistenceSignature(
        betti_0=betti_0,
        betti_1=betti_1,
        total_persistence_h1=total_h1,
        persistence_entropy_h1=entropy_h1,
        max_order=n,
        filtration_steps=filtration_steps,
        signature_hash=sig_hash,
    )


def persistence_distance(a: PersistenceSignature, b: PersistenceSignature) -> float:
    """L1 distance on normalized persistence feature vector."""
    va = np.array(
        [a.betti_0, a.betti_1, a.total_persistence_h1, a.persistence_entropy_h1],
        dtype=float,
    )
    vb = np.array(
        [b.betti_0, b.betti_1, b.total_persistence_h1, b.persistence_entropy_h1],
        dtype=float,
    )
    scale = np.maximum(np.abs(va), np.abs(vb))
    scale[scale == 0] = 1.0
    return float(np.sum(np.abs(va - vb) / scale))
