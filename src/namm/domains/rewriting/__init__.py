"""String rewriting systems domain for NAMM-2026-002."""

from namm.domains.rewriting.evaluator import (
    check_confluence,
    check_normalization,
    confluence_score,
    normalize,
)
from namm.domains.rewriting.generator import random_rewriting_system
from namm.domains.rewriting.rules import RewriteRule, RewritingSystem, rules_to_dict
from namm.domains.rewriting.serializer import (
    build_rewriting_certificate,
    compute_rewriting_representation_metrics,
)

__all__ = [
    "RewriteRule",
    "RewritingSystem",
    "build_rewriting_certificate",
    "check_confluence",
    "check_normalization",
    "compute_rewriting_representation_metrics",
    "confluence_score",
    "normalize",
    "random_rewriting_system",
    "rules_to_dict",
]
