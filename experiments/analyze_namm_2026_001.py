"""Extended analysis for NAMM-2026-001: verification and prior-art comparison."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.domains.graph.generator import enumerate_small_graphs
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

KNOWN_INVARIANTS = {
    "wiener_index": "1*wiener_index",
    "degree_sum_2x_edges": "2*num_edges",
    "avg_degree": "1*avg_degree",
    "clustering": "1*clustering",
    "algebraic_connectivity": "1*algebraic_connectivity",
    "wiener_plus_edges": "1*wiener_index + 1*num_edges",
    "wiener_plus_clustering": "1*wiener_index + 1*clustering",
    "2x_wiener": "2*wiener_index",
    "diameter": "1*diameter",
    "radius": "1*radius",
}


def load_best_candidate() -> tuple[str, str]:
    result = json.loads((ARTIFACTS / "result.json").read_text(encoding="utf-8"))
    best = result["best_candidate"]
    expr = best["formula"]["expression"]
    cid = best["candidate_id"]
    return cid, expr


def compare_to_known(expr: str, max_order: int = 6) -> dict:
    graphs = enumerate_small_graphs(max_order)
    comparisons = {}
    for name, baseline_expr in KNOWN_INVARIANTS.items():
        agrees = formulas_agree_on_graphs(expr, baseline_expr, graphs)
        comparisons[name] = {
            "baseline_expr": baseline_expr,
            "equivalent_on_order_leq": max_order,
            "equivalent": agrees,
        }
    return comparisons


def main() -> None:
    cid, expr = load_best_candidate()
    baseline = "1*wiener_index"

    verify_5 = exhaustive_equivalence_check(expr, baseline, max_order=5)
    graphs_atlas_6 = enumerate_atlas_connected(6)
    comparisons = compare_to_known(expr, max_order=6)

    # Full atlas exhaustive check (143 connected graphs, order <= 6)
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

    # Correlation with Wiener on full atlas order <= 6
    graphs = graphs_atlas_6
    wiener_vals = [evaluate_formula("1*wiener_index", g) for g in graphs]
    cand_vals = [evaluate_formula(expr, g) for g in graphs]
    n = len(graphs)
    mean_w = sum(wiener_vals) / n
    mean_c = sum(cand_vals) / n
    cov = sum((w - mean_w) * (c - mean_c) for w, c in zip(wiener_vals, cand_vals)) / n
    std_w = (sum((w - mean_w) ** 2 for w in wiener_vals) / n) ** 0.5
    std_c = (sum((c - mean_c) ** 2 for c in cand_vals) / n) ** 0.5
    correlation = cov / (std_w * std_c) if std_w > 0 and std_c > 0 else 0.0

    analysis = {
        "candidate_id": cid,
        "expression": expr,
        "baseline": baseline,
        "exhaustive_vs_wiener_order_5": verify_5,
        "exhaustive_vs_wiener_order_6_atlas": verify_6_atlas,
        "known_invariant_comparisons_order_6": comparisons,
        "correlation_with_wiener_order_6": {
            "graphs_checked": n,
            "pearson_r": correlation,
        },
        "equivalent_to_any_known": any(c["equivalent"] for c in comparisons.values()),
    }

    out_path = ARTIFACTS / "extended_analysis.json"
    out_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
