"""Baseline search strategies with Protocol v2 rejection gates."""

from __future__ import annotations

import random
from dataclasses import dataclass

import networkx as nx

from namm.domains.graph.evaluator import evaluate_formula, formulas_agree_on_graphs
from namm.domains.graph.generator import enumerate_small_graphs, random_invariant_formula
from namm.domains.program.ast import ast_to_dict, leaf
from namm.domains.program.canonical import ast_hash, canonicalize
from namm.domains.program.evaluator import ast_agrees_on_graphs, evaluate_ast
from namm.domains.program.generator import random_program_ast
from namm.domains.program.project import ast_to_expression, collect_leaf_names
from namm.domains.program.serializer import compute_ast_representation_metrics
from namm.metrics.baselines import (
    BaselineComparison,
    BaselineResults,
    assess_novelty_level,
    compare_to_baselines,
)
from namm.metrics.generative import (
    generate_held_out_families,
    generative_holdout_score,
    train_graph_set,
)
from namm.metrics.independence import reject_if_correlated
from namm.metrics.representation import (
    compute_representation_metrics,
    reject_if_low_compression_asymmetry,
)
from namm.prior_art.simplify import check_simplification, simplifies_to_known_baseline
from namm.schemas.experiment import (
    AttackChecklist,
    AttackChecklistItem,
    CandidateRecord,
    ExperimentConfig,
    InvariantFormula,
    RejectionRecord,
    RepresentationMetrics,
)


@dataclass
class SearchResult:
    candidates: list[CandidateRecord]
    rejections: list[RejectionRecord]
    best_generative: dict | None = None


def run_search(config: ExperimentConfig, graphs: list | None = None) -> SearchResult:
    """Dispatch search by experiment domain."""
    if config.is_rewriting_domain:
        return rewriting_search(config)
    if config.is_program_domain:
        return program_search(config, graphs=graphs)
    return random_search(config, graphs=graphs)


def wiener_baseline_expression() -> str:
    return "1*wiener_index"


def _atlas_connected_graphs(max_order: int) -> list[nx.Graph]:
    """Connected graphs from NetworkX atlas up to max_order."""
    atlas = nx.graph_atlas_g()
    graphs: list[nx.Graph] = []
    for n in range(1, max_order + 1):
        for g in atlas:
            if g.number_of_nodes() == n and nx.is_connected(g):
                graphs.append(g.copy())
    return graphs


def _build_attack_checklist(
    *,
    non_equiv_pass: bool,
    correlation_pass: bool,
    simplify_pass: bool,
    max_r: float | None,
    correlated_baseline: str | None,
    simplify_info: dict,
) -> AttackChecklist:
    items = [
        AttackChecklistItem(
            step="A1",
            passed=non_equiv_pass,
            notes="Baseline non-equivalence on test graph set",
        ),
        AttackChecklistItem(
            step="A3",
            passed=correlation_pass,
            notes=(
                f"max r={max_r} vs {correlated_baseline}"
                if max_r is not None
                else "correlation check"
            ),
        ),
        AttackChecklistItem(
            step="A4",
            passed=simplify_pass,
            notes=simplify_info.get("redundancy_note") or "prior-art simplify",
        ),
    ]
    signed_off = all(i.passed for i in items)
    return AttackChecklist(items=items, signed_off=signed_off)


def random_search(
    config: ExperimentConfig,
    graphs: list | None = None,
) -> SearchResult:
    """Random search with v2 correlation and simplify rejection gates."""
    rng = random.Random(config.seed)
    if graphs is None:
        graphs = enumerate_small_graphs(config.max_order)

    atlas_graphs = _atlas_connected_graphs(config.correlation_atlas_order)
    baseline = wiener_baseline_expression()
    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []

    for _ in range(config.num_candidates):
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

        baseline_results = compare_to_baselines(formula.expression, atlas_graphs)
        simplify_info = check_simplification(formula.expression)
        simplifies = simplifies_to_known_baseline(formula.expression)
        max_r = abs(baseline_results.max_correlation or 0.0)
        threshold = config.effective_correlation_threshold
        correlation_fail = max_r > threshold

        attack = _build_attack_checklist(
            non_equiv_pass=True,
            correlation_pass=not correlation_fail,
            simplify_pass=not simplifies,
            max_r=baseline_results.max_correlation,
            correlated_baseline=baseline_results.correlated_baseline,
            simplify_info=simplify_info,
        )
        novelty = assess_novelty_level(
            baseline_results,
            simplifies_to_known=simplifies,
            correlation_threshold=threshold,
        )
        rep_metrics = compute_representation_metrics(
            formula.expression, formula=formula, reference_graphs=graphs[:5]
        )
        ratio_threshold = config.effective_representation_ratio_threshold
        if ratio_threshold is not None:
            rep_gate = reject_if_low_compression_asymmetry(
                rep_metrics, threshold=ratio_threshold
            )
            if not rep_gate.passed:
                rejections.append(
                    RejectionRecord(
                        candidate_id=formula.id,
                        formula=formula,
                        reason=(
                            f"representation_ratio_fail:"
                            f"ratio={rep_gate.ratio:.4f}<{ratio_threshold}"
                        ),
                        baseline_results=baseline_results,
                        novelty_level=novelty,
                    )
                )
                continue

        if simplifies:
            baseline_results.rejected_for_correlation = False
            rejections.append(
                RejectionRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    reason=f"prior_art_simplify:{simplify_info.get('matches', [])}",
                    baseline_results=baseline_results,
                    novelty_level=novelty,
                )
            )
            continue

        if correlation_fail:
            baseline_results.rejected_for_correlation = True
            rejections.append(
                RejectionRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    reason=(
                        f"high_correlation_with_baseline:"
                        f"{baseline_results.correlated_baseline}:r={max_r:.4f}"
                    ),
                    baseline_results=baseline_results,
                    novelty_level=novelty,
                )
            )
            continue

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
                novelty_level=novelty,
                representation_metrics=rep_metrics,
                attack_checklist=attack,
                baseline_results=baseline_results,
            )
        )

    return SearchResult(candidates=candidates, rejections=rejections)


def _baseline_results_from_independence(
    indep_result,
    atlas_graphs: list[nx.Graph],
    expression: str,
) -> BaselineResults:
    """Map independence check to BaselineResults schema."""
    comparisons: list[BaselineComparison] = []
    for bid, r in indep_result.correlations.items():
        comparisons.append(
            BaselineComparison(
                baseline_id=bid,
                expression=f"baseline:{bid}",
                equivalent=False,
                pearson_r=r,
            )
        )
    return BaselineResults(
        comparisons=comparisons,
        max_correlation=indep_result.max_correlation,
        correlated_baseline=indep_result.correlated_baseline,
        rejected_for_correlation=not indep_result.independent,
    )


def program_search(
    config: ExperimentConfig,
    graphs: list | None = None,
) -> SearchResult:
    """AST search with independence, generative holdout, and representation gates."""
    from namm.domains.program.equivalence import ast_equivalent_to_baseline_sympy
    from namm.domains.program.evolution import evolutionary_program_population

    rng = random.Random(config.seed)
    train_graphs = train_graph_set(config.train_max_order)
    test_graphs = graphs if graphs is not None else enumerate_small_graphs(config.max_order)
    atlas_graphs = _atlas_connected_graphs(config.correlation_atlas_order)
    wiener_ast = leaf("wiener_index")
    held_out = generate_held_out_families(
        config.held_out_families, max_order=config.max_order
    )
    threshold = config.effective_correlation_threshold
    ratio_threshold = config.effective_representation_ratio_threshold

    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []
    best_generative: dict | None = None

    def _fitness(node):
        try:
            vals = [evaluate_ast(node, g) for g in test_graphs[:10]]
            return float(max(vals) - min(vals)) if vals else 0.0
        except (ValueError, ZeroDivisionError, FloatingPointError):
            return 0.0

    if config.search_strategy == "evolutionary":
        ast_batch = evolutionary_program_population(
            config.seed,
            population_size=config.evolution_population,
            generations=config.evolution_generations,
            max_depth=config.ast_max_depth,
            max_leaves=config.ast_max_leaves,
            fitness_fn=_fitness,
            return_count=config.num_candidates,
        )
    else:
        ast_batch = [
            random_program_ast(
                seed=rng.randint(0, 2**31 - 1),
                max_depth=config.ast_max_depth,
                max_leaves=config.ast_max_leaves,
            )
            for _ in range(config.num_candidates)
        ]

    for ast, candidate_id in ast_batch:
        canonical = canonicalize(ast)

        try:
            agrees = ast_agrees_on_graphs(canonical, wiener_ast, test_graphs)
        except (ValueError, ZeroDivisionError, FloatingPointError) as exc:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_ast(candidate_id, canonical),
                    reason=f"evaluation_error: {exc}",
                )
            )
            continue

        if agrees or ast_equivalent_to_baseline_sympy(canonical, "wiener_index"):
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_ast(candidate_id, canonical),
                    reason="equivalent_to_wiener_baseline",
                )
            )
            continue

        cand_vals = [evaluate_ast(canonical, g) for g in atlas_graphs]
        indep = reject_if_correlated(cand_vals, atlas_graphs, threshold=threshold)
        baseline_results = _baseline_results_from_independence(
            indep, atlas_graphs, ast_to_expression(canonical)
        )
        expression = ast_to_expression(canonical)
        simplify_info = check_simplification(expression)
        simplifies = simplifies_to_known_baseline(expression)

        gen_result = generative_holdout_score(
            lambda g: evaluate_ast(canonical, g),
            train_graphs,
            held_out,
        )
        if best_generative is None or gen_result.aggregate_score > best_generative.get(
            "aggregate_score", -1
        ):
            best_generative = {
                "aggregate_score": gen_result.aggregate_score,
                "per_family_variance": gen_result.per_family_variance,
                "passed": gen_result.passed,
            }

        attack = _build_attack_checklist(
            non_equiv_pass=True,
            correlation_pass=indep.independent,
            simplify_pass=not simplifies,
            max_r=indep.max_correlation,
            correlated_baseline=indep.correlated_baseline,
            simplify_info=simplify_info,
        )
        novelty = assess_novelty_level(
            baseline_results,
            simplifies_to_known=simplifies,
            correlation_threshold=threshold,
        )
        ast_metrics = compute_ast_representation_metrics(canonical, test_graphs[:5])
        rep_metrics = RepresentationMetrics(
            json_bytes=ast_metrics["json_bytes"],
            gzip_bytes=ast_metrics["gzip_bytes"],
            eval_time_ms=ast_metrics["eval_time_ms"],
            token_count_estimate=ast_metrics["token_count_estimate"],
            projection_token_estimate=ast_metrics["projection_token_estimate"],
        )

        if ratio_threshold is not None:
            rep_gate = reject_if_low_compression_asymmetry(
                rep_metrics, threshold=ratio_threshold
            )
            if not rep_gate.passed:
                rejections.append(
                    RejectionRecord(
                        candidate_id=candidate_id,
                        formula=_formula_from_ast(candidate_id, canonical),
                        reason=(
                            f"representation_ratio_fail:"
                            f"ratio={rep_gate.ratio:.4f}<{ratio_threshold}"
                        ),
                        baseline_results=baseline_results,
                        novelty_level=novelty,
                    )
                )
                continue

        if simplifies:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_ast(candidate_id, canonical),
                    reason=f"prior_art_simplify:{simplify_info.get('matches', [])}",
                    baseline_results=baseline_results,
                    novelty_level=novelty,
                )
            )
            continue

        if not indep.independent:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_ast(candidate_id, canonical),
                    reason=(
                        f"high_correlation_with_baseline:"
                        f"{indep.correlated_baseline}:r={abs(indep.max_correlation):.4f}"
                    ),
                    baseline_results=baseline_results,
                    novelty_level=novelty,
                )
            )
            continue

        if not gen_result.passed:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_ast(candidate_id, canonical),
                    reason=(
                        f"generative_holdout_fail:score={gen_result.aggregate_score:.4f}"
                    ),
                    baseline_results=baseline_results,
                    novelty_level=novelty,
                )
            )
            continue

        values = [evaluate_ast(canonical, g) for g in test_graphs]
        score = float(max(values) - min(values)) if values else 0.0

        candidates.append(
            CandidateRecord(
                candidate_id=candidate_id,
                formula=_formula_from_ast(candidate_id, canonical),
                score=score,
                agrees_with_baseline=False,
                graphs_tested=len(test_graphs),
                status="candidate",
                novelty_level=novelty,
                representation_metrics=rep_metrics,
                attack_checklist=attack,
                baseline_results=baseline_results,
            )
        )

    return SearchResult(
        candidates=candidates,
        rejections=rejections,
        best_generative=best_generative,
    )


def _formula_from_ast(candidate_id: str, node) -> InvariantFormula:
    canonical = canonicalize(node)
    return InvariantFormula(
        id=candidate_id,
        expression=ast_to_expression(canonical),
        primitives=sorted(set(collect_leaf_names(canonical))),
        meta_origin="random_ast_composition",
        canonical_ast=ast_to_dict(canonical),
        ast_hash=ast_hash(canonical),
    )


def _formula_from_rewriting(candidate_id: str, system) -> InvariantFormula:
    from namm.domains.rewriting.rules import rules_to_dict, system_hash

    payload = rules_to_dict(system)
    rules_str = "; ".join(f"{r['left']}->{r['right']}" for r in payload["rules"])
    return InvariantFormula(
        id=candidate_id,
        expression=f"TRS[{rules_str}]",
        primitives=[f"rule:{r['left']}->{r['right']}" for r in payload["rules"]],
        meta_origin="rewriting_system_search",
        canonical_ast=payload,
        ast_hash=system_hash(system),
    )


def rewriting_search(config: ExperimentConfig) -> SearchResult:
    """Search for confluent string rewriting systems vs random baseline."""
    from namm.domains.rewriting.baseline import (
        baseline_confluence_scores,
        exceeds_random_baseline,
        known_confluent_systems,
    )
    from namm.domains.rewriting.evaluator import (
        _all_strings,
        check_normalization,
        confluence_score,
    )
    from namm.domains.rewriting.generator import (
        mutate_rewriting_system,
        random_rewriting_system,
    )
    from namm.domains.rewriting.serializer import compute_rewriting_representation_metrics

    rng = random.Random(config.seed)
    max_len = config.rewriting_max_length
    test_strings = _all_strings(("a", "b"), max_len)[:30]
    ratio_threshold = config.effective_representation_ratio_threshold

    random_baseline_scores: list[float] = []
    for j in range(min(20, config.num_candidates)):
        sys, _ = random_rewriting_system(
            seed=config.seed + j,
            num_rules=config.rewriting_num_rules,
            max_length=max_len,
        )
        random_baseline_scores.append(confluence_score(sys, max_len).score)

    known_scores = baseline_confluence_scores(max_len)
    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []

    known_systems = known_confluent_systems(max_len)

    for i in range(config.num_candidates):
        gen_seed = rng.randint(0, 2**31 - 1)
        if i % 3 == 0 and known_systems:
            base = rng.choice(known_systems)
            system, candidate_id = mutate_rewriting_system(base, gen_seed)
        else:
            system, candidate_id = random_rewriting_system(
                seed=gen_seed,
                num_rules=config.rewriting_num_rules,
                max_length=max_len,
            )
        conf = confluence_score(system, max_len)
        normalizes = check_normalization(system, max_len)

        rep_raw = compute_rewriting_representation_metrics(system)
        rep_metrics = RepresentationMetrics(
            json_bytes=rep_raw["json_bytes"],
            gzip_bytes=rep_raw["gzip_bytes"],
            eval_time_ms=rep_raw["eval_time_ms"],
            token_count_estimate=rep_raw["token_count_estimate"],
            projection_token_estimate=rep_raw["projection_token_estimate"],
        )

        if ratio_threshold is not None:
            rep_gate = reject_if_low_compression_asymmetry(
                rep_metrics, threshold=ratio_threshold
            )
            if not rep_gate.passed:
                rejections.append(
                    RejectionRecord(
                        candidate_id=candidate_id,
                        formula=_formula_from_rewriting(candidate_id, system),
                        reason=(
                            f"representation_ratio_fail:"
                            f"ratio={rep_gate.ratio:.4f}<{ratio_threshold}"
                        ),
                    )
                )
                continue

        if conf.score < config.confluence_threshold:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_rewriting(candidate_id, system),
                    reason=f"confluence_fail:score={conf.score:.4f}",
                    counterexample=conf.counterexample,
                )
            )
            continue

        if not normalizes:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_rewriting(candidate_id, system),
                    reason="normalization_fail",
                )
            )
            continue

        if not exceeds_random_baseline(conf.score, random_baseline_scores):
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_rewriting(candidate_id, system),
                    reason="does_not_exceed_random_baseline",
                )
            )
            continue

        from namm.domains.rewriting.rules import system_hash as sh

        known_hashes = {sh(s) for s in known_systems}
        if conf.confluent and sh(system) in known_hashes:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_rewriting(candidate_id, system),
                    reason="matches_known_confluent_baseline",
                )
            )
            continue

        candidates.append(
            CandidateRecord(
                candidate_id=candidate_id,
                formula=_formula_from_rewriting(candidate_id, system),
                score=conf.score,
                agrees_with_baseline=False,
                graphs_tested=conf.strings_tested,
                status="candidate",
                novelty_level=None,
                representation_metrics=rep_metrics,
                attack_checklist=AttackChecklist(
                    items=[
                        AttackChecklistItem(
                            step="R1",
                            passed=conf.confluent,
                            notes=f"confluence score={conf.score:.4f}",
                        ),
                        AttackChecklistItem(
                            step="R2",
                            passed=normalizes,
                            notes="normalization on bounded strings",
                        ),
                        AttackChecklistItem(
                            step="R3",
                            passed=exceeds_random_baseline(
                                conf.score, random_baseline_scores
                            ),
                            notes="beats random rule baseline",
                        ),
                    ],
                    signed_off=conf.confluent and normalizes,
                ),
            )
        )

    return SearchResult(
        candidates=candidates,
        rejections=rejections,
        best_generative={"known_baselines": known_scores},
    )
