"""Tests for finite category domain stub."""

import networkx as nx
import pytest

from namm.domains.category.finite import (
    count_homomorphisms,
    graph_category_shadow,
)


def test_path_to_path_homomorphisms():
    p3 = nx.path_graph(3)
    p2 = nx.path_graph(2)
    count = count_homomorphisms(p2, p3)
    assert count >= 1


def test_self_endomorphisms():
    k3 = nx.complete_graph(3)
    assert count_homomorphisms(k3, k3) >= 6  # permutations preserve edges


def test_category_shadow():
    graphs = [nx.path_graph(3), nx.cycle_graph(4), nx.complete_graph(3)]
    shadow = graph_category_shadow(graphs)
    assert shadow.object_count == 3
    assert len(shadow.morphism_counts) == 9
    assert shadow.shadow_hash


def test_order_limit():
    big = nx.complete_graph(8)
    small = nx.path_graph(3)
    with pytest.raises(ValueError, match="order"):
        count_homomorphisms(big, small)
