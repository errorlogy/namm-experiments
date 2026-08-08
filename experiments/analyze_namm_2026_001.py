"""Extended analysis for NAMM-2026-001: verification and prior-art comparison."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula
from namm.metrics.baselines import compare_to_baselines, assess_novelty_level
from namm.metrics.representation import compute_representation_metrics
from namm.prior_art.simplify import check_simplification, simplifies_to_known_baseline
from namm.verifiers import exhaustive_equivalence_check


def enumerate_atlas_connected(max_order: int) -> list[nx.Graph]:
    """All connected graphs in the NetworkX atlas up to max_order."""
    atlas = nx.graph_atlas_g()
    graphs: list[nx.Graph] = []
    for n in range(1, max_order + 1):
        for g in atlas:
            if g.number_of_nodes() == n and nx.is_connected(g):
                graphs.append(g.copy())
    return graphs


WORKSPACE = Path(__file__).resolve().parents[1]
ARTIFACTS = WORKSPACE / "experiments" / "NAMM-2026-001" / "artifacts"


def load_best_candidate() -> tuple[str, str]:
    result = json.loads((ARTIFACTS / "result.json").read_text(encoding="utf-8"))
    best = result["best_candidate"]
    if best is None:
        raise SystemExit("No best candidate in result.json — run may have rejected all under v2 gates")
    expr = best["formula"]["expression"]
    cid = best["candidate_id"]
    return cid, expr


def main() -> None:
    cid, expr = load_best_candidate()
    baseline = "1*wiener_index"

    verify_5 = exhaustive_equivalence_check(expr, baseline, max_order=5)
    graphs_atlas_6 = enumerate_atlas_connected(6)
    baseline_results = compare_to_baselines(expr, graphs_atlas_6)
    simplify_info = check_simplification(expr)
    novelty = assess_novelty_level(
        baseline_results,
        simplifies_to_known=simplifies_to_known_baseline(expr),
        correlation_threshold=0.95,
    )
    rep_metrics = compute_representation_metrics(expr, reference_graphs=graphs_atlas_6[:5])

    verify_6_atlas: dict = {"equivalent": True, "graphs_checked": len(graphs_atlas_6)}
    for g in graphs_atlas_6:
        va = evaluate_formula(expr, g)
        vb = evaluate_formula(baseline, g)
        if abs(va - vb) > 1e-9:
            verify_6_atlas = {
                "equivalent": False,
                "graphs_checked": len(graphs_atlas_6),
                "counterexample": {
                    "order": g.number_of_nodes(),
                    "edges": list(g.edges()),
                    "value_a": va,
                    "value_b": vb,
                },
            }
            break

    wiener_comp = next(
        (c for c in baseline_results.comparisons if c.baseline_id == "wiener_index"),
        None,
    )

    analysis = {
        "protocol_version": "v2",
        "candidate_id": cid,
        "expression": expr,
        "baseline": baseline,
        "exhaustive_vs_wiener_order_5": verify_5,
        "exhaustive_vs_wiener_order_6_atlas": verify_6_atlas,
        "baseline_results": baseline_results.model_dump(),
        "prior_art_simplify": simplify_info,
        "novelty_level": novelty.value,
        "representation_metrics": rep_metrics.model_dump(),
        "correlation_with_wiener_order_6": {
            "graphs_checked": len(graphs_atlas_6),
            "pearson_r": wiener_comp.pearson_r if wiener_comp else None,
        },
        "equivalent_to_any_known": any(c.equivalent for c in baseline_results.comparisons),
        "v2_would_reject_at_threshold_0.90": abs(baseline_results.max_correlation or 0) > 0.90,
    }

    out_path = ARTIFACTS / "extended_analysis.json"
    out_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
