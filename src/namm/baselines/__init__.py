"""Baseline search strategies."""

from __future__ import annotations

import random
from dataclasses import dataclass

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.domains.graph.generator import enumerate_small_graphs, random_invariant_formula
from namm.schemas.experiment import CandidateRecord, ExperimentConfig, RejectionRecord


@dataclass
class SearchResult:
    candidates: list[CandidateRecord]
    rejections: list[RejectionRecord]


def wiener_baseline_expression() -> str:
    return "1*wiener_index"


def random_search(
    config: ExperimentConfig,
    graphs: list | None = None,
) -> SearchResult:
    """Random search for invariant candidates differing from Wiener baseline."""
    rng = random.Random(config.seed)
    if graphs is None:
        graphs = enumerate_small_graphs(config.max_order)

    baseline = wiener_baseline_expression()
    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []

    for i in range(config.num_candidates):
        formula = random_invariant_formula(seed=rng.randint(0, 2**31 - 1))
        try:
            agrees = formulas_agree_on_graphs(formula.expression, baseline, graphs)
        except (ValueError, ZeroDivisionError, FloatingPointError) as exc:
            rejections.append(
                RejectionRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    reason=f"evaluation_error: {exc}",
                )
            )
            continue

        if agrees:
            rejections.append(
                RejectionRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    reason="equivalent_to_wiener_baseline",
                )
            )
            continue

        # score: variance of candidate values across test graphs
        values = [evaluate_formula(formula.expression, g) for g in graphs]
        score = float(max(values) - min(values)) if values else 0.0

        candidates.append(
            CandidateRecord(
                candidate_id=formula.id,
                formula=formula,
                score=score,
                agrees_with_baseline=False,
                graphs_tested=len(graphs),
                status="candidate",
            )
        )

    return SearchResult(candidates=candidates, rejections=rejections)
