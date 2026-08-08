"""Program AST domain for AI-native graph invariant synthesis."""

from namm.domains.program.ast import ProgramNode, leaf, parse_ast_dict, ast_to_dict
from namm.domains.program.canonical import canonicalize, ast_hash
from namm.domains.program.evaluator import evaluate_ast, ast_agrees_on_graphs
from namm.domains.program.generator import random_program_ast
from namm.domains.program.project import ast_to_expression, collect_leaf_names
from namm.domains.program.serializer import (
    build_certificate,
    human_projection_from_ast,
)

__all__ = [
    "ProgramNode",
    "leaf",
    "parse_ast_dict",
    "ast_to_dict",
    "canonicalize",
    "ast_hash",
    "evaluate_ast",
    "ast_agrees_on_graphs",
    "random_program_ast",
    "build_certificate",
    "human_projection_from_ast",
    "ast_to_expression",
    "collect_leaf_names",
]
