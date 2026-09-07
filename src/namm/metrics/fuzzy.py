"""Fuzzy membership functions for CNS socio-political contours.

Pure ``numpy`` / ``networkx`` implementations. Optional ``scikit-fuzzy`` helpers
are exposed via :func:`try_import_skfuzzy` for future defuzzification pipelines.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

import networkx as nx
import numpy as np


class MembershipKind(str, Enum):
    TRIANGULAR = "triangular"
    TRAPEZOIDAL = "trapezoidal"
    GAUSSIAN = "gaussian"
    GAUSSIAN_CENTROID = "gaussian_centroid"
    RAMP = "ramp"
    SPATIAL_SOFT = "spatial_soft"
    ISSUE_TAG = "issue_tag"


def triangular(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership on [a, c] with peak at b."""
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / max(b - a, 1e-12)
    return (c - x) / max(c - b, 1e-12)


def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
    """Trapezoidal membership on [a, d] with plateau [b, c]."""
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return (x - a) / max(b - a, 1e-12)
    return (d - x) / max(d - c, 1e-12)


def gaussian(x: float, center: float, sigma: float) -> float:
    """1-D Gaussian membership."""
    return float(np.exp(-0.5 * ((x - center) / max(sigma, 1e-6)) ** 2))


def gaussian_centroid(
    opinion: np.ndarray,
    centroid: np.ndarray,
    sigma: float,
) -> float:
    """Gaussian membership from Euclidean distance to centroid."""
    centroid = np.asarray(centroid, dtype=float)
    opinion = np.asarray(opinion, dtype=float)
    dim = min(len(centroid), len(opinion))
    dist = float(np.linalg.norm(opinion[:dim] - centroid[:dim]))
    return float(np.exp(-0.5 * (dist / max(sigma, 1e-6)) ** 2))


def ramp(x: float, x0: float, x1: float) -> float:
    """Linear ramp from 0 at x0 to 1 at x1."""
    if x <= x0:
        return 0.0
    if x >= x1:
        return 1.0
    return (x - x0) / max(x1 - x0, 1e-12)


def spatial_soft(
    agent_idx: int,
    center_node: int,
    graph: nx.Graph,
    decay_length: float = 2.5,
) -> float:
    """Graph-distance soft membership exp(-d / decay_length)."""
    if center_node not in graph:
        center_node = list(graph.nodes())[0]
    try:
        dist = nx.shortest_path_length(graph, agent_idx, center_node)
    except nx.NetworkXNoPath:
        dist = graph.number_of_nodes()
    return float(np.exp(-dist / max(decay_length, 1e-6)))


def issue_tag_membership(
    agent_tags: set[str],
    contour_tags: list[str],
    agent_expertise_weight: float = 0.6,
) -> float:
    """Tag-overlap membership for issue-based contours."""
    if not contour_tags:
        return 0.0
    overlap = len(agent_tags.intersection(set(contour_tags)))
    raw = overlap / len(contour_tags)
    return float(min(1.0, raw * agent_expertise_weight + (1 - agent_expertise_weight) * 0.5))


def try_import_skfuzzy() -> Any | None:
    """Return ``skfuzzy`` if ``namm[science]`` extra is installed, else None."""
    try:
        import skfuzzy  # type: ignore[import-untyped]

        return skfuzzy
    except ImportError:
        return None
