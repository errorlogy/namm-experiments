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
    if config.is_tda_domain:
        return tda_search(config)
    if config.is_open_problem_domain:
        return open_problem_search(config)
    if config.is_meta_domain:
        return meta_search(config, graphs=graphs)
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


def _formula_from_meta(
    candidate_id: str,
    node,
    *,
    transform_name: str,
) -> InvariantFormula:
    from namm.domains.meta.ast import meta_to_dict
    from namm.domains.meta.canonical import canonicalize_meta, meta_hash

    canonical = canonicalize_meta(node)
    return InvariantFormula(
        id=candidate_id,
        expression=f"MetaEval[F={transform_name}]",
        primitives=["meta_evaluator", f"transform:{transform_name}"],
        meta_origin="meta_fixed_point_search",
        canonical_ast={
            "evaluator": meta_to_dict(canonical),
            "transform": transform_name,
        },
        ast_hash=meta_hash(canonical),
    )


def _is_trivial_meta(node) -> bool:
    """Reject single-leaf evaluators when nontrivial_only is set."""
    from namm.domains.meta.ast import MetaEvaluatorNode

    if node.is_leaf():
        return True
    if node.op in ("self", "target"):
        return True
    return False


def open_problem_search(config: ExperimentConfig) -> SearchResult:
    """Finite-shadow counterexample search for catalogued open problems."""
    import uuid

    from namm.domains.open_problem.pk_graph import PkSearchHit, search_pk_counterexamples

    problem = config.open_problem_id
    if problem != "kotzig_pk":
        return SearchResult(
            candidates=[],
            rejections=[
                RejectionRecord(
                    candidate_id=f"unsupported-{problem}",
                    formula=InvariantFormula(
                        id=f"unsupported-{problem}",
                        expression=f"open_problem:{problem}",
                        meta_origin="open_problem_shadow",
                    ),
                    reason=f"unsupported_open_problem:{problem}",
                )
            ],
        )

    result = search_pk_counterexamples(
        max_order=config.max_order,
        k_min=config.pk_k_min,
        k_max=config.pk_k_max,
    )

    def _hit_to_formula(hit: PkSearchHit) -> InvariantFormula:
        edge_str = ",".join(f"{u}-{v}" for u, v in hit.edge_list)
        return InvariantFormula(
            id=f"pk-{uuid.uuid4().hex[:8]}",
            expression=f"PkGraph[k={hit.k},n={hit.graph_order},edges={edge_str}]",
            primitives=[f"pk_k:{hit.k}", f"order:{hit.graph_order}"],
            meta_origin="kotzig_pk_counterexample_search",
            canonical_ast={
                "problem": "kotzig_pk",
                "k": hit.k,
                "order": hit.graph_order,
                "edges": hit.edge_list,
                "violations": hit.violations,
                "is_counterexample": hit.is_counterexample,
            },
            ast_hash=f"pk-{hit.k}-{hit.graph_order}-{len(hit.edge_list)}",
        )

    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []

    if result.counterexamples:
        for hit in result.counterexamples:
            formula = _hit_to_formula(hit)
            candidates.append(
                CandidateRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    score=1.0,
                    agrees_with_baseline=False,
                    graphs_tested=result.graphs_scanned,
                    status="counterexample",
                    attack_checklist=AttackChecklist(
                        items=[
                            AttackChecklistItem(
                                step="O1",
                                passed=True,
                                notes=(
                                    f"Kotzig counterexample: P_{hit.k}-graph "
                                    f"order {hit.graph_order}"
                                ),
                            )
                        ],
                        signed_off=True,
                    ),
                    representation_metrics=RepresentationMetrics(
                        json_bytes=len(str(hit.edge_list)),
                        gzip_bytes=len(str(hit.edge_list)),
                        eval_time_ms=0.0,
                        token_count_estimate=len(hit.edge_list) * 4,
                        projection_token_estimate=40,
                    ),
                )
            )
    else:
        for hit in result.best_near_misses:
            formula = _hit_to_formula(hit)
            rejections.append(
                RejectionRecord(
                    candidate_id=formula.id,
                    formula=formula,
                    reason=(
                        f"not_pk_graph:score={hit.score:.4f},"
                        f"violations={len(hit.violations)}"
                    ),
                    counterexample={
                        "k": hit.k,
                        "order": hit.graph_order,
                        "score": hit.score,
                        "sample_violations": hit.violations[:3],
                    },
                )
            )
        if result.best_near_misses:
            best = result.best_near_misses[0]
            formula = _hit_to_formula(best)
            candidates.append(
                CandidateRecord(
                    candidate_id=f"near-{best.k}-{best.graph_order}",
                    formula=formula,
                    score=best.score,
                    agrees_with_baseline=False,
                    graphs_tested=result.graphs_scanned,
                    status="near_miss",
                    attack_checklist=AttackChecklist(
                        items=[
                            AttackChecklistItem(
                                step="O1",
                                passed=False,
                                notes=(
                                    f"No counterexample order≤{config.max_order}; "
                                    f"best near-miss score={best.score:.4f} k={best.k}"
                                ),
                            )
                        ],
                        signed_off=False,
                    ),
                )
            )

    return SearchResult(
        candidates=candidates,
        rejections=rejections,
        best_generative={
            "problem": "kotzig_pk",
            "graphs_scanned": result.graphs_scanned,
            "counterexample_count": len(result.counterexamples),
            "k_range": [config.pk_k_min, config.pk_k_max],
        },
    )


def meta_search(
    config: ExperimentConfig,
    graphs: list | None = None,
) -> SearchResult:
    """Search for meta-evaluator fixed points E ≈ F(E) on benchmark graphs."""
    from namm.domains.graph.generator import enumerate_small_graphs
    from namm.domains.meta.canonical import canonicalize_meta
    from namm.domains.meta.evaluator import fixed_point_score
    from namm.domains.meta.generator import random_meta_evaluator
    from namm.domains.meta.serializer import compute_meta_representation_metrics
    from namm.domains.meta.transform import apply_transform, list_transforms

    rng = random.Random(config.seed)
    benchmark_graphs = graphs if graphs is not None else enumerate_small_graphs(config.max_order)
    ratio_threshold = config.effective_representation_ratio_threshold
    fp_threshold = config.meta_fixed_point_threshold

    available = set(list_transforms())
    transforms = [t for t in config.meta_transforms if t in available]
    if not transforms:
        transforms = [t for t in list_transforms() if t != "identity"]

    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []
    best_generative: dict | None = None

    for i in range(config.num_candidates):
        gen_seed = rng.randint(0, 2**31 - 1)
        evaluator, candidate_id = random_meta_evaluator(
            gen_seed,
            max_depth=config.meta_max_depth,
            include_self=config.meta_include_self,
            include_target=(i % 4 == 0),
        )
        transform_name = rng.choice(transforms)
        transformed = apply_transform(transform_name, evaluator)
        canonical = canonicalize_meta(evaluator)

        if config.meta_nontrivial_only and _is_trivial_meta(canonical):
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_meta(
                        candidate_id, canonical, transform_name=transform_name
                    ),
                    reason="trivial_evaluator",
                )
            )
            continue

        fp_frac = fixed_point_score(canonical, transformed, benchmark_graphs)
        if best_generative is None or fp_frac > best_generative.get("best_fixed_point_fraction", -1):
            best_generative = {
                "best_fixed_point_fraction": fp_frac,
                "transform": transform_name,
                "graphs_tested": len(benchmark_graphs),
            }

        rep_raw = compute_meta_representation_metrics(canonical, benchmark_graphs[:10])
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
                        formula=_formula_from_meta(
                            candidate_id, canonical, transform_name=transform_name
                        ),
                        reason=(
                            f"representation_ratio_fail:"
                            f"ratio={rep_gate.ratio:.4f}<{ratio_threshold}"
                        ),
                    )
                )
                continue

        if fp_frac < fp_threshold:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_meta(
                        candidate_id, canonical, transform_name=transform_name
                    ),
                    reason=f"fixed_point_fail:score={fp_frac:.4f}<{fp_threshold}",
                    counterexample={
                        "transform": transform_name,
                        "fixed_point_fraction": fp_frac,
                    },
                )
            )
            continue

        values = [
            fixed_point_score(canonical, apply_transform(t, canonical), benchmark_graphs)
            for t in transforms[:3]
        ]
        cross_transform_stability = sum(values) / len(values) if values else fp_frac

        candidates.append(
            CandidateRecord(
                candidate_id=candidate_id,
                formula=_formula_from_meta(
                    candidate_id, canonical, transform_name=transform_name
                ),
                score=fp_frac * (1.0 + 0.1 * cross_transform_stability),
                agrees_with_baseline=False,
                graphs_tested=len(benchmark_graphs),
                status="candidate",
                novelty_level=None,
                representation_metrics=rep_metrics,
                attack_checklist=AttackChecklist(
                    items=[
                        AttackChecklistItem(
                            step="M1",
                            passed=fp_frac >= fp_threshold,
                            notes=f"fixed point F={transform_name} score={fp_frac:.4f}",
                        ),
                        AttackChecklistItem(
                            step="M2",
                            passed=not _is_trivial_meta(canonical),
                            notes="nontrivial evaluator structure",
                        ),
                        AttackChecklistItem(
                            step="M3",
                            passed=True,
                            notes=f"cross-transform stability={cross_transform_stability:.4f}",
                        ),
                    ],
                    signed_off=fp_frac >= fp_threshold,
                ),
            )
        )

    return SearchResult(
        candidates=candidates,
        rejections=rejections,
        best_generative=best_generative,
    )


def _baseline_graph_for_tda(name: str, order: int) -> nx.Graph:
    if name == "cycle":
        return nx.cycle_graph(max(3, order))
    if name == "complete":
        return nx.complete_graph(max(3, order))
    return nx.path_graph(max(3, order))


def _formula_from_tda(candidate_id: str, graph: nx.Graph, sig) -> InvariantFormula:
    from namm.domains.tda.homology import PersistenceSignature

    assert isinstance(sig, PersistenceSignature)
    return InvariantFormula(
        id=candidate_id,
        expression=(
            f"TDA[β1={sig.betti_1},H1={sig.total_persistence_h1:.4f},"
            f"n={graph.number_of_nodes()}]"
        ),
        primitives=[
            f"betti_1:{sig.betti_1}",
            f"entropy:{sig.persistence_entropy_h1:.4f}",
        ],
        meta_origin="tda_persistence_search",
        canonical_ast={
            "signature": sig.to_dict(),
            "edges": [[int(u), int(v)] for u, v in graph.edges()],
            "order": graph.number_of_nodes(),
        },
        ast_hash=sig.signature_hash,
    )


def tda_search(config: ExperimentConfig) -> SearchResult:
    """Search for graphs whose persistence signature differs from baseline."""
    from namm.domains.tda.generator import random_tda_graph
    from namm.domains.tda.homology import graph_persistence_signature, persistence_distance
    from namm.domains.tda.serializer import compute_tda_representation_metrics

    rng = random.Random(config.seed)
    baseline_g = _baseline_graph_for_tda(
        config.tda_baseline_graph, max(3, config.max_order // 2)
    )
    baseline_sig = graph_persistence_signature(
        baseline_g,
        max_edge_length=config.tda_max_edge_length,
        filtration_steps=config.tda_filtration_steps,
    )
    ratio_threshold = config.effective_representation_ratio_threshold
    min_dist = config.tda_min_baseline_distance

    candidates: list[CandidateRecord] = []
    rejections: list[RejectionRecord] = []
    best_generative: dict | None = None

    for _ in range(config.num_candidates):
        gen_seed = rng.randint(0, 2**31 - 1)
        graph, candidate_id = random_tda_graph(gen_seed, max_order=config.max_order)

        try:
            sig = graph_persistence_signature(
                graph,
                max_edge_length=config.tda_max_edge_length,
                filtration_steps=config.tda_filtration_steps,
            )
        except (ValueError, ImportError) as exc:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=InvariantFormula(
                        id=candidate_id,
                        expression="TDA[error]",
                        meta_origin="tda_persistence_search",
                    ),
                    reason=f"tda_evaluation_error: {exc}",
                )
            )
            continue

        dist = persistence_distance(sig, baseline_sig)
        if best_generative is None or dist > best_generative.get("best_distance", -1):
            best_generative = {
                "best_distance": dist,
                "baseline": config.tda_baseline_graph,
                "baseline_signature": baseline_sig.to_dict(),
            }

        rep_raw = compute_tda_representation_metrics(graph)
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
                        formula=_formula_from_tda(candidate_id, graph, sig),
                        reason=(
                            f"representation_ratio_fail:"
                            f"ratio={rep_gate.ratio:.4f}<{ratio_threshold}"
                        ),
                    )
                )
                continue

        if dist < min_dist:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_tda(candidate_id, graph, sig),
                    reason=f"baseline_too_close:distance={dist:.4f}<{min_dist}",
                    counterexample={
                        "distance": dist,
                        "signature": sig.to_dict(),
                    },
                )
            )
            continue

        if sig.betti_1 == 0 and baseline_sig.betti_1 == 0:
            rejections.append(
                RejectionRecord(
                    candidate_id=candidate_id,
                    formula=_formula_from_tda(candidate_id, graph, sig),
                    reason="no_h1_feature:betti_1=0",
                )
            )
            continue

        score = dist * (1.0 + sig.persistence_entropy_h1)

        candidates.append(
            CandidateRecord(
                candidate_id=candidate_id,
                formula=_formula_from_tda(candidate_id, graph, sig),
                score=score,
                agrees_with_baseline=False,
                graphs_tested=1,
                status="candidate",
                novelty_level=None,
                representation_metrics=rep_metrics,
                attack_checklist=AttackChecklist(
                    items=[
                        AttackChecklistItem(
                            step="T1",
                            passed=dist >= min_dist,
                            notes=f"persistence distance={dist:.4f}",
                        ),
                        AttackChecklistItem(
                            step="T2",
                            passed=sig.betti_1 > 0 or sig.total_persistence_h1 > 0,
                            notes=(
                                f"β₁={sig.betti_1}, "
                                f"H¹ total={sig.total_persistence_h1:.4f}"
                            ),
                        ),
                        AttackChecklistItem(
                            step="T3",
                            passed=True,
                            notes=f"baseline={config.tda_baseline_graph}",
                        ),
                    ],
                    signed_off=dist >= min_dist,
                ),
            )
        )

    return SearchResult(
        candidates=candidates,
        rejections=rejections,
        best_generative=best_generative,
    )
