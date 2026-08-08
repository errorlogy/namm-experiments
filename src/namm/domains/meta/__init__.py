"""Meta-evaluator domain for NAMM-2026-004 fixed-point search."""

from namm.domains.meta.ast import MetaEvaluatorNode, meta_to_dict, parse_meta_dict
from namm.domains.meta.canonical import canonicalize_meta, meta_hash
from namm.domains.meta.evaluator import (
    evaluate_meta_on_graph,
    fixed_point_score,
    meta_agrees_on_graphs,
)
from namm.domains.meta.generator import random_meta_evaluator
from namm.domains.meta.transform import apply_transform, list_transforms
from namm.domains.meta.serializer import build_meta_certificate

__all__ = [
    "MetaEvaluatorNode",
    "apply_transform",
    "build_meta_certificate",
    "canonicalize_meta",
    "evaluate_meta_on_graph",
    "fixed_point_score",
    "list_transforms",
    "meta_agrees_on_graphs",
    "meta_hash",
    "meta_to_dict",
    "parse_meta_dict",
    "random_meta_evaluator",
]
