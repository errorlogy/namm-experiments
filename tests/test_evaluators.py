"""Tests for graph evaluators."""

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.domains.graph.generator import enumerate_small_graphs, random_invariant_formula
from namm.domains.graph.invariants import wiener_index


def test_wiener_index_path():
    g = nx.path_graph(4)
    w = wiener_index(g)
    assert w == 10.0  # pairs: (0,1)=1,(0,2)=2,(0,3)=3,(1,2)=1,(1,3)=2,(2,3)=1


def test_evaluate_wiener_formula():
    g = nx.path_graph(3)
    val = evaluate_formula("1*wiener_index", g)
    assert val == wiener_index(g)


def test_formula_agreement_detects_difference():
    graphs = enumerate_small_graphs(4)
    assert formulas_agree_on_graphs("1*wiener_index", "1*num_edges", graphs) is False


def test_random_formula_evaluates():
    formula = random_invariant_formula(seed=0)
    g = nx.cycle_graph(5)
    val = evaluate_formula(formula.expression, g)
    assert isinstance(val, float)
