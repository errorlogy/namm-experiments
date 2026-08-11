"""Raw adjacency-derived tensor features — no named graph invariants."""

from __future__ import annotations

import networkx as nx
import numpy as np

DEFAULT_SPECTRUM_SIZE = 8
DEFAULT_HEAT_TIMES = (0.25, 0.5, 1.0, 2.0)


def graph_tensor_vector(
    g: nx.Graph,
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> list[float]:
    """
    Build fixed-length numeric feature vector from adjacency spectrum and
    heat-kernel diagonal sums. Indices map to AST leaves t0, t1, …
    """
    n = g.number_of_nodes()
    if n == 0:
        return [0.0] * (spectrum_size + len(heat_times))

    adj = nx.adjacency_matrix(g, nodelist=sorted(g.nodes())).astype(float).toarray()
    eigenvalues = np.sort(np.linalg.eigvalsh(adj))[::-1]
    spec = [float(v) for v in eigenvalues[:spectrum_size]]
    while len(spec) < spectrum_size:
        spec.append(0.0)

    lap = nx.laplacian_matrix(g, nodelist=sorted(g.nodes())).astype(float).toarray()
    eigvals, eigvecs = np.linalg.eigh(lap)
    heat: list[float] = []
    for t in heat_times:
        exp_e = np.exp(-t * eigvals)
        kernel = eigvecs @ np.diag(exp_e) @ eigvecs.T
        heat.append(float(np.trace(kernel)))

    return spec + heat


def tensor_leaf_count(
    *,
    spectrum_size: int = DEFAULT_SPECTRUM_SIZE,
    heat_times: tuple[float, ...] = DEFAULT_HEAT_TIMES,
) -> int:
    return spectrum_size + len(heat_times)
