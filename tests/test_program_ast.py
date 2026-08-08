"""Tests for program AST domain."""

import networkx as nx

from namm.domains.program.ast import leaf, parse_ast_dict, ast_to_dict
from namm.domains.program.canonical import canonicalize, ast_hash
from namm.domains.program.evaluator import evaluate_ast, ast_agrees_on_graphs
from namm.domains.program.generator import random_program_ast
from namm.domains.graph.invariants import wiener_index


def test_leaf_eval_wiener():
    g = nx.path_graph(4)
    ast = leaf("wiener_index")
    assert evaluate_ast(ast, g) == wiener_index(g)


def test_binary_ast_evaluates():
    ast = parse_ast_dict(
        {
            "op": "add",
            "left": {"op": "leaf", "name": "num_edges"},
            "right": {"op": "leaf", "name": "clustering"},
        }
    )
    g = nx.cycle_graph(5)
    val = evaluate_ast(ast, g)
    assert isinstance(val, float)


def test_canonicalization_sorts_commutative():
    a = parse_ast_dict(
        {
            "op": "add",
            "left": {"op": "leaf", "name": "num_edges"},
            "right": {"op": "leaf", "name": "wiener_index"},
        }
    )
    b = parse_ast_dict(
        {
            "op": "add",
            "left": {"op": "leaf", "name": "wiener_index"},
            "right": {"op": "leaf", "name": "num_edges"},
        }
    )
    ca = canonicalize(a)
    cb = canonicalize(b)
    assert ast_to_dict(ca) == ast_to_dict(cb)
    assert ast_hash(ca) == ast_hash(cb)


def test_random_ast_generates_and_evaluates():
    ast, cid = random_program_ast(seed=42)
    g = nx.karate_club_graph()
    val = evaluate_ast(ast, g)
    assert isinstance(val, float)
    assert cid.startswith("prog-")


def test_ast_agreement_detects_difference():
    wiener = leaf("wiener_index")
    edges = leaf("num_edges")
    graphs = [nx.path_graph(3), nx.cycle_graph(4)]
    assert ast_agrees_on_graphs(wiener, edges, graphs) is False
