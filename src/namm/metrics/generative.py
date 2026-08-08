"""Generative holdout evaluation on structurally distinct graph families."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from namm.domains.graph.generator import enumerate_small_graphs


def _connected_only(graphs: list[nx.Graph]) -> list[nx.Graph]:
    """Keep only connected graphs with at least one edge."""
    return [g for g in graphs if g.number_of_nodes() > 0 and nx.is_connected(g)]


def generate_family_graphs(
    family: str,
    max_order: int,
    count: int = 10,
) -> list[nx.Graph]:
    """Generate graphs from a named held-out family."""
    graphs: list[nx.Graph] = []
    if family == "trees":
        for n in range(2, max_order + 1):
            if len(graphs) >= count:
                break
            graphs.append(nx.random_labeled_tree(n, seed=n * 17))
        while len(graphs) < count:
            n = min(max_order, 3 + len(graphs))
            graphs.append(nx.random_labeled_tree(n, seed=100 + len(graphs)))
    elif family == "bipartite":
        seed = 0
        while len(graphs) < count and seed < count * 20:
            a = 2 + (seed % max(1, max_order // 2))
            b = 2 + ((seed + 1) % max(1, max_order // 2))
            p = 0.35 + 0.08 * (seed % 5)
            g = nx.bipartite.random_graph(a, b, p, seed=seed * 31)
            if g.number_of_edges() > 0 and nx.is_connected(g):
                graphs.append(g)
            seed += 1
    elif family == "cubic":
        for n in range(4, max_order + 1):
            if n % 2 != 0:
                continue
            if len(graphs) >= count:
                break
            try:
                g = nx.random_regular_graph(3, n, seed=n * 13)
                if nx.is_connected(g):
                    graphs.append(g)
            except nx.NetworkXError:
                continue
        seed = 0
        while len(graphs) < count and seed < 50:
            n = 6 + (seed % (max_order - 3)) * 2
            if n <= max_order:
                try:
                    g = nx.random_regular_graph(3, n, seed=seed)
                    if nx.is_connected(g):
                        graphs.append(g)
                except nx.NetworkXError:
                    pass
            seed += 1
    else:
        raise ValueError(f"Unknown family: {family}")
    return _connected_only(graphs)[:count]


def generate_held_out_families(
    families: list[str],
    max_order: int = 8,
    per_family: int = 10,
) -> dict[str, list[nx.Graph]]:
    """Build held-out test sets keyed by family name."""
    return {f: generate_family_graphs(f, max_order, per_family) for f in families}


@dataclass
class GenerativeHoldoutResult:
    aggregate_score: float
    per_family_variance: dict[str, float]
    per_family_mean: dict[str, float]
    passed: bool
    min_variance_threshold: float


def generative_holdout_score(
    evaluate_fn,
    train_graphs: list[nx.Graph],
    held_out: dict[str, list[nx.Graph]],
    min_variance: float = 1e-6,
) -> GenerativeHoldoutResult:
    """
    Score generative power: mean per-family value range on held-out sets.

    Train/search uses train_graphs; test requires non-trivial spread on each family.
    """
    per_var: dict[str, float] = {}
    per_mean: dict[str, float] = {}

    for family, graphs in held_out.items():
        if not graphs:
            per_var[family] = 0.0
            per_mean[family] = 0.0
            continue
        vals = [evaluate_fn(g) for g in graphs]
        per_mean[family] = sum(vals) / len(vals)
        per_var[family] = max(vals) - min(vals) if vals else 0.0

    # Train-side reference range for normalization
    train_vals = [evaluate_fn(g) for g in train_graphs]
    train_range = max(train_vals) - min(train_vals) if train_vals else 1.0
    if train_range < 1e-9:
        train_range = 1.0

    family_scores = [per_var[f] / train_range for f in per_var]
    aggregate = sum(family_scores) / len(family_scores) if family_scores else 0.0
    passed = all(v >= min_variance for v in per_var.values()) and aggregate > 0.01

    return GenerativeHoldoutResult(
        aggregate_score=round(aggregate, 6),
        per_family_variance={k: round(v, 6) for k, v in per_var.items()},
        per_family_mean={k: round(v, 6) for k, v in per_mean.items()},
        passed=passed,
        min_variance_threshold=min_variance,
    )


def train_graph_set(max_order: int = 6) -> list[nx.Graph]:
    """Connected atlas graphs for training/search (order <= max_order)."""
    return enumerate_small_graphs(max_order)
