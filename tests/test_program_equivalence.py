"""Tests for sympy equivalence on program AST."""

from namm.domains.program.ast import leaf, parse_ast_dict
from namm.domains.program.canonical import canonicalize
from namm.domains.program.equivalence import ast_equivalent_sympy, ast_equivalent_to_baseline_sympy


def test_wiener_leaf_equivalent():
    a = leaf("wiener_index")
    b = leaf("wiener_index")
    assert ast_equivalent_sympy(a, b)


def test_different_leaves_not_equivalent():
    a = leaf("wiener_index")
    b = leaf("num_edges")
    assert not ast_equivalent_sympy(a, b)


def test_commutative_ast_equivalent():
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
    assert ast_equivalent_sympy(canonicalize(a), canonicalize(b))


def test_baseline_sympy_check():
    w = leaf("wiener_index")
    assert ast_equivalent_to_baseline_sympy(w, "wiener_index")
    assert not ast_equivalent_to_baseline_sympy(leaf("num_edges"), "wiener_index")
