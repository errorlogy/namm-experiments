"""Verification stubs: z3 and exhaustive checks."""

from __future__ import annotations

from typing import Any

import networkx as nx
from z3 import Int, Solver, sat

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.domains.graph.generator import enumerate_small_graphs
from namm.metrics.antigravity_embedding import compute_antigravity_scores
from namm.prior_art.arxiv import check_prior_art



def exhaustive_equivalence_check(
    expr_a: str, expr_b: str, max_order: int = 5
) -> dict[str, Any]:
    """Exhaustively check formula equivalence on small connected graphs."""
    graphs = enumerate_small_graphs(max_order)
    for g in graphs:
        va = evaluate_formula(expr_a, g)
        vb = evaluate_formula(expr_b, g)
        if abs(va - vb) > 1e-9:
            return {
                "equivalent": False,
                "counterexample": {
                    "order": g.number_of_nodes(),
                    "edges": list(g.edges()),
                    "value_a": va,
                    "value_b": vb,
                },
            }
    return {"equivalent": True, "graphs_checked": len(graphs)}


def z3_stub_check(expr: str) -> dict[str, Any]:
    """Stub z3 verification — proves trivial integer constraint satisfiability."""
    x = Int("x")
    solver = Solver()
    solver.add(x > 0)
    result = solver.check()
    return {
        "expr": expr,
        "z3_available": True,
        "stub_result": str(result),
        "satisfiable": result == sat,
        "note": "Full invariant encoding not yet implemented; stub confirms z3 import.",
    }


def verify_candidate(
    candidate_expr: str, baseline_expr: str, max_order: int = 5
) -> dict[str, Any]:
    """Run verifiers on a candidate against a baseline, including Antigravity & Prior Art gates."""
    exhaustive = exhaustive_equivalence_check(candidate_expr, baseline_expr, max_order)
    z3_result = z3_stub_check(candidate_expr)
    graphs = enumerate_small_graphs(max_order)
    agrees = formulas_agree_on_graphs(candidate_expr, baseline_expr, graphs)

    # Antigravity embedding metrics vs baseline
    antigravity_metrics = compute_antigravity_scores(
        response_text=candidate_expr,
        median_text=baseline_expr,
    )

    # Prior Art check on arXiv
    prior_art_check = check_prior_art(
        query=candidate_expr.replace("*", " ").replace("+", " "),
        max_results=3,
    )

    is_novel = not agrees and antigravity_metrics.distance_from_median >= 0.15

    return {
        "candidate_expr": candidate_expr,
        "baseline_expr": baseline_expr,
        "is_novel_candidate": is_novel,
        "exhaustive": exhaustive,
        "z3_stub": z3_result,
        "agrees_with_baseline": agrees,
        "antigravity_metrics": antigravity_metrics.to_dict(),
        "prior_art_summary": {
            "query": prior_art_check.query,
            "arxiv_matches_found": prior_art_check.total_found,
            "has_prior_art_match": prior_art_check.has_prior_art_match,
        },
    }

