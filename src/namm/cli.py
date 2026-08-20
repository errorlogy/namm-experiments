"""Typer CLI for NAMM experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import structlog
import typer
import yaml

from namm.baselines import run_search
from namm.domains.program.ast import parse_ast_dict
from namm.domains.program.canonical import canonicalize
from namm.domains.program.serializer import build_certificate, human_projection_from_ast
from namm.schemas.experiment import ExperimentConfig, ExperimentResult
from namm.verifiers import verify_candidate

app = typer.Typer(help="NAMM experiments CLI")
logger = structlog.get_logger()

WORKSPACE = Path(__file__).resolve().parents[2]


def _load_config(experiment_id: str) -> ExperimentConfig:
    config_path = WORKSPACE / "experiments" / experiment_id / "config.yaml"
    if not config_path.exists():
        raise typer.BadParameter(f"Config not found: {config_path}")
    with config_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["experiment_id"] = experiment_id
    return ExperimentConfig(**data)


def _write_jsonl(path: Path, records: list) -> None:
    import orjson

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        for record in records:
            f.write(orjson.dumps(record.model_dump(), option=orjson.OPT_APPEND_NEWLINE))
        if not records:
            f.write(b"")


def _k_h_estimate(human_projection: str) -> int:
    return max(1, len(human_projection.split()))


def run_experiment_impl(config: ExperimentConfig, output_dir: Path) -> ExperimentResult:
    """Core experiment runner."""
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )
    log = structlog.get_logger(experiment_id=config.experiment_id)
    log.info("experiment_start", domain=config.domain, seed=config.seed)

    from namm.domains.graph.generator import enumerate_small_graphs

    output_dir.mkdir(parents=True, exist_ok=True)

    result = run_search(config)
    candidates = result.candidates
    rejections = result.rejections

    _write_jsonl(output_dir / "candidates.jsonl", candidates)
    _write_jsonl(output_dir / "rejections.jsonl", rejections)

    best = max(candidates, key=lambda c: c.score) if candidates else None
    verification = None
    certificate: dict | None = None
    generative_holdout = result.best_generative

    if best:
        if config.is_rewriting_domain and best.formula.canonical_ast:
            from namm.domains.rewriting.evaluator import _all_strings, confluence_score
            from namm.domains.rewriting.rules import parse_rules_dict
            from namm.domains.rewriting.serializer import build_rewriting_certificate

            system = parse_rules_dict(best.formula.canonical_ast)
            test_strings = _all_strings(tuple(system.alphabet), system.max_length)[:30]
            conf = confluence_score(system, system.max_length)
            certificate = build_rewriting_certificate(
                candidate_id=best.candidate_id,
                system=system,
                seed=config.seed,
                test_strings=test_strings,
                confluence={
                    "confluent": conf.confluent,
                    "score": conf.score,
                    "strings_tested": conf.strings_tested,
                },
                extra={
                    "domain": config.domain,
                    "protocol_version": "v2-ai-native",
                },
            )
            verification = {
                "domain": "rewriting",
                "system_hash": best.formula.ast_hash,
                "eval_hash": certificate["eval_hash"],
            }
        elif config.is_meta_domain and best.formula.canonical_ast:
            from namm.domains.meta.ast import parse_meta_dict
            from namm.domains.meta.canonical import canonicalize_meta
            from namm.domains.meta.evaluator import fixed_point_score
            from namm.domains.meta.serializer import build_meta_certificate
            from namm.domains.meta.transform import apply_transform

            eval_payload = best.formula.canonical_ast
            transform_name = eval_payload.get("transform", "canonicalize")
            ast_node = canonicalize_meta(
                parse_meta_dict(eval_payload["evaluator"])
            )
            transformed = apply_transform(transform_name, ast_node)
            ref_graphs = enumerate_small_graphs(config.max_order)[:20]
            fp_frac = fixed_point_score(ast_node, transformed, ref_graphs)
            certificate = build_meta_certificate(
                candidate_id=best.candidate_id,
                evaluator=ast_node,
                transformed=transformed,
                transform_name=transform_name,
                seed=config.seed,
                reference_graphs=ref_graphs,
                witness_bounds={
                    "max_order": config.max_order,
                    "graph_count": len(ref_graphs),
                    "fixed_point_threshold": config.meta_fixed_point_threshold,
                    "transforms": config.meta_transforms,
                },
                fixed_point_fraction=fp_frac,
                extra={
                    "domain": config.domain,
                    "protocol_version": "v2-ai-native-topology",
                },
            )
            verification = {
                "domain": "meta_evaluation",
                "meta_hash": best.formula.ast_hash,
                "eval_hash": certificate["eval_hash"],
                "fixed_point_fraction": fp_frac,
            }
        elif config.is_program_domain and best.formula.canonical_ast:
            from namm.domains.program.evaluator import evaluate_ast

            ast_node = canonicalize(parse_ast_dict(best.formula.canonical_ast))
            ref_graphs = enumerate_small_graphs(config.max_order)[:20]
            certificate = build_certificate(
                candidate_id=best.candidate_id,
                node=ast_node,
                seed=config.seed,
                reference_graphs=ref_graphs,
                witness_bounds={
                    "train_max_order": config.train_max_order,
                    "test_max_order": config.max_order,
                    "atlas_order": config.correlation_atlas_order,
                    "held_out_families": config.held_out_families,
                    "graph_count": len(ref_graphs),
                },
                extra={
                    "domain": config.domain,
                    "protocol_version": "v2-ai-native",
                    "generative_holdout": generative_holdout,
                },
            )
            verification = {
                "domain": "program_ast",
                "ast_hash": best.formula.ast_hash,
                "eval_hash": certificate["eval_hash"],
            }
        elif config.is_open_problem_domain and best.formula.canonical_ast:
            import hashlib

            payload = best.formula.canonical_ast
            witness = {
                "problem": config.open_problem_id,
                "k_min": config.pk_k_min,
                "k_max": config.pk_k_max,
                "max_order": config.max_order,
                "graphs_scanned": generative_holdout.get("graphs_scanned")
                if generative_holdout
                else None,
                "counterexample_count": generative_holdout.get("counterexample_count")
                if generative_holdout
                else 0,
                "candidate": payload,
            }
            eval_hash = hashlib.sha256(
                repr(sorted(witness.items())).encode()
            ).hexdigest()[:16]
            certificate = {
                "candidate_id": best.candidate_id,
                "domain": config.domain,
                "protocol_version": "v2-open-problem-shadow",
                "eval_hash": eval_hash,
                "witness": witness,
                "status": best.status,
                "score": best.score,
            }
            verification = {
                "domain": "open_problem_shadow",
                "problem": config.open_problem_id,
                "eval_hash": eval_hash,
                "counterexample": payload.get("is_counterexample", False),
            }
        elif config.is_tensor_domain and best.formula.canonical_ast:
            from namm.domains.tensor.ast import parse_ast_dict
            from namm.domains.tensor.canonical import canonicalize as canon_tensor
            from namm.domains.tensor.serializer import build_tensor_certificate

            heat_times = tuple(config.tensor_heat_times)
            ast_node = canon_tensor(parse_ast_dict(best.formula.canonical_ast))
            ref_graphs = enumerate_small_graphs(config.max_order)[:20]
            certificate = build_tensor_certificate(
                candidate_id=best.candidate_id,
                node=ast_node,
                seed=config.seed,
                reference_graphs=ref_graphs,
                witness_bounds={
                    "train_max_order": config.train_max_order,
                    "test_max_order": config.max_order,
                    "spectrum_size": config.tensor_spectrum_size,
                    "heat_times": list(config.tensor_heat_times),
                    "held_out_families": config.held_out_families,
                    "graph_count": len(ref_graphs),
                    "baseline_count": "20+ tensor polynomials deg≤4",
                },
                extra={
                    "domain": config.domain,
                    "protocol_version": "v2-beyond-homo-tensor",
                    "generative_holdout": generative_holdout,
                },
                spectrum_size=config.tensor_spectrum_size,
                heat_times=heat_times,
            )
            verification = {
                "domain": "raw_tensor",
                "ast_hash": best.formula.ast_hash,
                "eval_hash": certificate["eval_hash"],
            }
        elif config.is_tda_domain and best.formula.canonical_ast:
            import networkx as nx

            from namm.domains.tda.homology import (
                graph_persistence_signature,
                persistence_distance,
            )
            from namm.domains.tda.serializer import build_tda_certificate

            payload = best.formula.canonical_ast
            g = nx.Graph()
            g.add_nodes_from(range(payload["order"]))
            g.add_edges_from((u, v) for u, v in payload["edges"])
            baseline_g = nx.path_graph(max(3, config.max_order // 2))
            if config.tda_baseline_graph == "cycle":
                baseline_g = nx.cycle_graph(max(3, config.max_order // 2))
            baseline_sig = graph_persistence_signature(
                baseline_g,
                max_edge_length=config.tda_max_edge_length,
            )
            sig = graph_persistence_signature(
                g, max_edge_length=config.tda_max_edge_length
            )
            dist = persistence_distance(sig, baseline_sig)
            certificate = build_tda_certificate(
                candidate_id=best.candidate_id,
                graph=g,
                seed=config.seed,
                baseline_signature=baseline_sig,
                witness_bounds={
                    "max_order": config.max_order,
                    "tda_max_edge_length": config.tda_max_edge_length,
                    "tda_min_baseline_distance": config.tda_min_baseline_distance,
                    "baseline_graph": config.tda_baseline_graph,
                    "distance_to_baseline": dist,
                },
                extra={
                    "domain": config.domain,
                    "protocol_version": "v2-tda-frame",
                    "score": best.score,
                },
            )
            verification = {
                "domain": "tda_frame",
                "signature_hash": sig.signature_hash,
                "eval_hash": certificate["eval_hash"],
                "distance_to_baseline": dist,
            }
        elif config.is_config_shadow_domain and best.formula.canonical_ast:
            from namm.domains.config_shadow.serializer import build_config_shadow_certificate
            from namm.domains.config_shadow.vacua import ModuliVacuum

            payload = best.formula.canonical_ast
            vacuum = ModuliVacuum(
                moduli=tuple(payload["moduli"]),
                shadow_4d=tuple(payload["shadow_4d"]),
                fiber_size=payload["fiber_size"],
                fiber_index=payload["fiber_index"],
                stability_score=payload["stability_score"],
                vacuum_id=payload.get("vacuum_id", best.candidate_id),
            )
            kappa_mode = payload.get("kappa_mode", config.kappa_mode)
            certificate = build_config_shadow_certificate(
                candidate_id=best.candidate_id,
                vacuum=vacuum,
                seed=config.seed,
                witness_bounds={
                    "config_dim": config.config_dim,
                    "shadow_dim": config.shadow_dim,
                    "moduli_range": [config.moduli_min, config.moduli_max],
                    "max_energy": config.config_max_energy,
                    "flux_modulus": config.flux_modulus,
                    "vacua_scanned": generative_holdout.get("vacua_scanned")
                    if generative_holdout
                    else None,
                    "ambiguous_fibers": generative_holdout.get("ambiguous_fibers")
                    if generative_holdout
                    else None,
                },
                extra={
                    "domain": config.domain,
                    "kappa_mode": kappa_mode,
                    "kappa_sweep": generative_holdout.get("kappa_sweep")
                    if generative_holdout
                    else None,
                },
            )
            verification = {
                "domain": "config_shadow",
                "vacuum_id": vacuum.vacuum_id,
                "eval_hash": certificate["eval_hash"],
                "fiber_size": vacuum.fiber_size,
            }
        else:
            verification = verify_candidate(
                best.formula.expression,
                "1*wiener_index",
                max_order=min(5, config.max_order),
            )

    machine_repr = {
        "experiment_id": config.experiment_id,
        "domain": config.domain,
        "max_order": config.max_order,
        "seed": config.seed,
        "protocol_version": "v2",
        "correlation_threshold": config.effective_correlation_threshold,
        "candidates_count": len(candidates),
        "rejections_count": len(rejections),
        "best_candidate": best.model_dump() if best else None,
        "verification": verification,
        "generative_holdout": generative_holdout,
    }

    human_lines = [
        f"# {config.experiment_id} — Human Projection",
        "",
        f"**Protocol:** v2 AI-native (see docs/AI_NATIVE_NAMM.md)",
        f"**Domain:** {config.domain}",
        f"**Research question:** {config.research_question}",
        "",
        f"- Graphs tested: order ≤ {config.max_order}",
        f"- Correlation threshold: {config.effective_correlation_threshold}",
        f"- Candidates found: {len(candidates)}",
        f"- Rejected: {len(rejections)}",
    ]
    if config.is_program_domain:
        human_lines.append(f"- Train order: ≤ {config.train_max_order}")
        human_lines.append(f"- Held-out families: {', '.join(config.held_out_families)}")
        human_lines.append(
            "\n> Trust certificate; full object in certificate.json."
        )
    if config.is_rewriting_domain:
        human_lines.append(f"- Max string length: {config.rewriting_max_length}")
        human_lines.append(f"- Confluence threshold: {config.confluence_threshold}")
        human_lines.append(
            "\n> Trust certificate; full object in certificate.json."
        )
    if config.is_meta_domain:
        human_lines.append(f"- Meta max depth: {config.meta_max_depth}")
        human_lines.append(f"- Fixed-point threshold: {config.meta_fixed_point_threshold}")
        human_lines.append(f"- Transforms: {', '.join(config.meta_transforms)}")
        human_lines.append(
            "\n> Trust certificate; meta-evaluator fixed points are AI-topology artifacts."
        )
    if config.is_open_problem_domain:
        human_lines.append(f"- Open problem: {config.open_problem_id}")
        human_lines.append(f"- P_k range: {config.pk_k_min}..{config.pk_k_max}")
        human_lines.append(
            "\n> Finite shadow search; counterexample would refute Kotzig for listed k."
        )
    if config.is_tensor_domain:
        human_lines.append(f"- Tensor spectrum size: {config.tensor_spectrum_size}")
        human_lines.append(f"- Heat times: {config.tensor_heat_times}")
        human_lines.append(f"- Train order: ≤ {config.train_max_order}")
        human_lines.append(f"- Held-out families: {', '.join(config.held_out_families)}")
        human_lines.append(
            "\n> Beyond homo-known: numeric tensor leaves only (no wiener/degree_sum)."
        )
    if config.is_tda_domain:
        human_lines.append(f"- TDA baseline: {config.tda_baseline_graph}")
        human_lines.append(f"- Min persistence distance: {config.tda_min_baseline_distance}")
        human_lines.append(f"- Max edge length (Rips): {config.tda_max_edge_length}")
        human_lines.append(
            "\n> Trust certificate; persistence signature in certificate.json."
        )
    if config.is_config_shadow_domain:
        human_lines.append(f"- Config dim: {config.config_dim}D")
        human_lines.append(f"- Shadow dim: {config.shadow_dim}D")
        human_lines.append(f"- κ mode: {config.kappa_mode}")
        human_lines.append(
            f"- Moduli range: [{config.moduli_min}, {config.moduli_max}]"
        )
        human_lines.append(f"- Max energy Σm²: {config.config_max_energy}")
        human_lines.append(f"- Flux modulus: {config.flux_modulus}")
        if generative_holdout and generative_holdout.get("kappa_sweep"):
            human_lines.append(
                f"- κ sweep: {generative_holdout['kappa_sweep']}"
            )
        human_lines.append(
            "\n> HL-004: π_H sees shadow only; certificate preserves fiber."
        )

    if best:
        if config.is_rewriting_domain and best.formula.canonical_ast:
            from namm.domains.rewriting.rules import parse_rules_dict
            from namm.domains.rewriting.serializer import human_projection_from_system

            system = parse_rules_dict(best.formula.canonical_ast)
            proj = human_projection_from_system(system, candidate_id=best.candidate_id)
            human_lines.extend(["", proj])
        elif config.is_meta_domain and best.formula.canonical_ast:
            from namm.domains.meta.ast import parse_meta_dict
            from namm.domains.meta.canonical import canonicalize_meta
            from namm.domains.meta.evaluator import fixed_point_score
            from namm.domains.meta.serializer import human_projection_from_meta
            from namm.domains.meta.transform import apply_transform

            eval_payload = best.formula.canonical_ast
            transform_name = eval_payload.get("transform", "canonicalize")
            ast_node = canonicalize_meta(
                parse_meta_dict(eval_payload["evaluator"])
            )
            transformed = apply_transform(transform_name, ast_node)
            ref_graphs = enumerate_small_graphs(config.max_order)[:20]
            fp_frac = fixed_point_score(ast_node, transformed, ref_graphs)
            proj = human_projection_from_meta(
                ast_node,
                candidate_id=best.candidate_id,
                transform_name=transform_name,
                fixed_point_fraction=fp_frac,
            )
            human_lines.extend(["", proj])
        elif config.is_program_domain and best.formula.canonical_ast:
            ast_node = parse_ast_dict(best.formula.canonical_ast)
            proj = human_projection_from_ast(
                ast_node, candidate_id=best.candidate_id, trust_certificate=True
            )
            human_lines.extend(["", proj])
        elif config.is_open_problem_domain and best.formula.canonical_ast:
            payload = best.formula.canonical_ast
            human_lines.extend(
                [
                    "",
                    f"**Open-problem shadow:** `{config.open_problem_id}`",
                    f"- k={payload.get('k')} order={payload.get('order')}",
                    f"- Counterexample: {payload.get('is_counterexample')}",
                    f"- Score (pair fraction): {best.score:.4f}",
                    f"- Edges: {payload.get('edges')}",
                ]
            )
        elif config.is_tensor_domain and best.formula.canonical_ast:
            from namm.domains.tensor.ast import parse_ast_dict
            from namm.domains.tensor.canonical import canonicalize as canon_tensor
            from namm.domains.tensor.serializer import human_projection_from_tensor

            ast_node = parse_ast_dict(best.formula.canonical_ast)
            proj = human_projection_from_tensor(
                canon_tensor(ast_node),
                candidate_id=best.candidate_id,
                trust_certificate=True,
            )
            human_lines.extend(["", proj])
        elif config.is_tda_domain and best.formula.canonical_ast:
            from namm.domains.tda.homology import PersistenceSignature
            from namm.domains.tda.serializer import human_projection_from_tda

            payload = best.formula.canonical_ast
            sig = PersistenceSignature(**payload["signature"])
            dist = generative_holdout.get("best_distance", 0.0) if generative_holdout else 0.0
            proj = human_projection_from_tda(
                sig,
                candidate_id=best.candidate_id,
                graph_order=payload["order"],
                distance_to_baseline=dist,
            )
            human_lines.extend(["", proj])
        elif config.is_config_shadow_domain and best.formula.canonical_ast:
            from namm.domains.config_shadow.serializer import human_projection_from_config
            from namm.domains.config_shadow.vacua import ModuliVacuum

            payload = best.formula.canonical_ast
            vacuum = ModuliVacuum(
                moduli=tuple(payload["moduli"]),
                shadow_4d=tuple(payload["shadow_4d"]),
                fiber_size=payload["fiber_size"],
                fiber_index=payload["fiber_index"],
                stability_score=payload["stability_score"],
                vacuum_id=payload.get("vacuum_id", best.candidate_id),
            )
            proj = human_projection_from_config(
                vacuum, candidate_id=best.candidate_id
            )
            human_lines.extend(["", proj])
            human_lines.extend(
                [
                    f"- Fiber size (certificate only): {vacuum.fiber_size}",
                    f"- Fiber index: {vacuum.fiber_index}",
                    f"- 11D moduli (certificate): {list(vacuum.moduli)}",
                ]
            )
        else:
            human_lines.extend(
                [
                    "",
                    f"**Best candidate:** `{best.formula.expression}`",
                ]
            )
        human_lines.extend(
            [
                f"- Score (value range): {best.score:.4f}",
                f"- Novelty level: {best.novelty_level.value if best.novelty_level else 'unassessed'}",
                f"- Agrees with Wiener baseline: {best.agrees_with_baseline}",
            ]
        )
        if best.baseline_results and best.baseline_results.max_correlation is not None:
            human_lines.append(
                f"- Max Pearson r vs baselines: {best.baseline_results.max_correlation:.4f} "
                f"({best.baseline_results.correlated_baseline})"
            )
        if best.representation_metrics:
            rm = best.representation_metrics
            k_a = rm.json_bytes
            k_h = _k_h_estimate("\n".join(human_lines))
            human_lines.append(
                f"- K_A proxies: json={rm.json_bytes}B gzip={rm.gzip_bytes}B "
                f"eval={rm.eval_time_ms:.3f}ms projection_tokens≈{rm.projection_token_estimate or rm.token_count_estimate}"
            )
            if k_a > 0:
                human_lines.append(f"- K_A/K_H (bytes/tokens proxy): {k_a}/{k_h}")
    else:
        human_lines.append("\nNo nontrivial candidates found in this run.")

    human_projection = "\n".join(human_lines)

    experiment_result = ExperimentResult(
        experiment_id=config.experiment_id,
        domain=config.domain,
        research_question=config.research_question,
        candidates_found=len(candidates),
        rejections=len(rejections),
        best_candidate=best,
        machine_representation=machine_repr,
        human_projection=human_projection,
        certificate=certificate,
        generative_holdout=generative_holdout,
    )

    import orjson

    if certificate:
        (output_dir / "certificate.json").write_bytes(
            orjson.dumps(certificate, option=orjson.OPT_INDENT_2)
        )

    (output_dir / "result.json").write_bytes(
        orjson.dumps(experiment_result.model_dump(), option=orjson.OPT_INDENT_2)
    )
    (output_dir / "human_projection.md").write_text(human_projection, encoding="utf-8")
    (output_dir / "HUMAN_PROJECTION.md").write_text(human_projection, encoding="utf-8")

    log.info(
        "experiment_complete",
        candidates=len(candidates),
        rejections=len(rejections),
    )
    return experiment_result


@app.command("run-experiment")
def run_experiment(
    experiment_id: str = typer.Option(..., "--id", help="Experiment ID, e.g. NAMM-2026-001"),
) -> None:
    """Run a NAMM experiment and write artifacts."""
    sci_flow_ids = {
        f"NAMM-2026-0{i}" for i in range(21, 31)
    }
    if experiment_id in sci_flow_ids:
        from namm.sci_flow import run_sci_flow

        result = run_sci_flow(experiment_id)
        output_dir = WORKSPACE / "experiments" / experiment_id / "artifacts"
        typer.echo(f"Experiment {experiment_id} complete (sci-flow).")
        typer.echo(f"  Modules: {', '.join(result.modules_used)}")
        typer.echo(f"  Certificate status: {result.certificate.get('status')}")
        typer.echo(f"  Hypothesis confirmed: {result.experiment_result.get('hypothesis_confirmed')}")
        typer.echo(f"  Artifacts: {output_dir}")
        return

    if experiment_id == "NAMM-2026-013":
        import sys
        exp_dir = str(WORKSPACE / "experiments" / "NAMM-2026-013")
        if exp_dir not in sys.path:
            sys.path.insert(0, exp_dir)
        from run_experiment import run_namm_2026_013_benchmark
        res = run_namm_2026_013_benchmark()
        output_dir = WORKSPACE / "experiments" / experiment_id / "artifacts"
        typer.echo(f"Experiment {experiment_id} (Cognitive Antigravity) complete.")
        typer.echo(f"  Hypothesis Confirmed: {res['hypothesis_confirmed']}")
        typer.echo(f"  D_med Lift: +{res['metrics_summary']['d_med_lift_percent']}%")
        typer.echo(f"  Artifacts: {output_dir}")
        return

    config = _load_config(experiment_id)
    output_dir = WORKSPACE / "experiments" / experiment_id / "artifacts"
    result = run_experiment_impl(config, output_dir)
    typer.echo(f"Experiment {experiment_id} complete.")
    typer.echo(f"  Candidates: {result.candidates_found}")
    typer.echo(f"  Rejections: {result.rejections}")
    typer.echo(f"  Artifacts: {output_dir}")



@app.command("verify")
def verify(
    expr: str = typer.Option(..., help="Candidate invariant expression"),
    baseline: str = typer.Option("1*wiener_index", help="Baseline expression"),
    max_order: int = typer.Option(5, help="Max graph order for exhaustive check"),
) -> None:
    """Verify a candidate invariant against a baseline."""
    result = verify_candidate(expr, baseline, max_order=max_order)
    import orjson

    typer.echo(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())
sci_flow_app = typer.Typer(help="Sci Flow — route experiments to scientific modules")
app.add_typer(sci_flow_app, name="sci-flow")

llm_app = typer.Typer(help="LLM + embedding providers (API and local)")
app.add_typer(llm_app, name="llm")


@sci_flow_app.command("run")
def sci_flow_run(
    experiment_id: str = typer.Option(..., "--experiment", "-e", help="Experiment ID"),
    variant: Optional[str] = typer.Option(None, "--variant", help="Config variant (e.g. kuramoto)"),
) -> None:
    """Run an experiment through the sci-flow pipeline."""
    from namm.sci_flow import run_sci_flow

    result = run_sci_flow(experiment_id, variant=variant)
    output_dir = WORKSPACE / "experiments" / experiment_id / "artifacts"
    typer.echo(f"Sci-flow {experiment_id} complete.")
    typer.echo(f"  Modules: {', '.join(result.modules_used)}")
    typer.echo(f"  Branch: {result.branch}")
    typer.echo(f"  Certificate: {result.certificate.get('status')}")
    typer.echo(f"  Artifacts: {output_dir}")


@sci_flow_app.command("describe")
def sci_flow_describe(
    experiment_id: str = typer.Option(..., "--experiment", "-e", help="Experiment ID"),
) -> None:
    """Show resolved modules for an experiment without running."""
    import orjson
    from namm.sci_flow import SciFlowRunner

    runner = SciFlowRunner()
    desc = runner.describe_modules(experiment_id)
    typer.echo(orjson.dumps(desc, option=orjson.OPT_INDENT_2).decode())


@sci_flow_app.command("catalog")
def sci_flow_catalog() -> None:
    """List all sci-flow registered modules."""
    import orjson
    from namm.sci_flow.adapters import module_catalog

    typer.echo(orjson.dumps(module_catalog(), option=orjson.OPT_INDENT_2).decode())


@app.command("search-arxiv")
def search_arxiv_cmd(
    query: str = typer.Option(..., "--query", "-q", help="Search query string"),
    max_results: int = typer.Option(5, "--max-results", "-n", help="Max results to fetch"),
    cat: Optional[str] = typer.Option(None, "--cat", "-c", help="Comma-separated arXiv categories e.g. cs.AI,math.CO"),
) -> None:
    """Search arXiv literature for Prior Art and open problem references."""
    from namm.prior_art.arxiv import search_arxiv

    categories = cat.split(",") if cat else ["cs.AI", "cs.LO", "math.CO", "stat.ML"]
    papers = search_arxiv(query=query, max_results=max_results, categories=categories)

    typer.echo(f"Found {len(papers)} papers on arXiv for query: '{query}'")
    for idx, paper in enumerate(papers, 1):
        typer.echo(f"\n[{idx}] {paper.title}")
        typer.echo(f"    Authors: {', '.join(paper.authors[:3])}")
        typer.echo(f"    arXiv ID: {paper.arxiv_id} | Published: {paper.published[:10]}")
        typer.echo(f"    Categories: {', '.join(paper.categories)}")
        typer.echo(f"    URL: {paper.abs_url}")
        typer.echo(f"    Summary: {paper.summary[:200]}...")


@llm_app.command("status")
def llm_status_cmd() -> None:
    """Show configured LLM/embedding providers and auto-selection."""
    import orjson
    from namm.llm.client import provider_status

    typer.echo(orjson.dumps(provider_status(), option=orjson.OPT_INDENT_2).decode())


@llm_app.command("embed")
def llm_embed_cmd(
    text: str = typer.Argument(..., help="Text to embed"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p"),
    model: Optional[str] = typer.Option(None, "--model", "-m"),
) -> None:
    """Embed text and print vector shape + first values."""
    import orjson
    from namm.llm.client import embed

    vec = embed(text, provider=provider, model=model)
    typer.echo(
        orjson.dumps(
            {"shape": list(vec.shape), "head": vec[:8].tolist(), "provider": provider or "auto"},
            option=orjson.OPT_INDENT_2,
        ).decode()
    )


@llm_app.command("chat")
def llm_chat_cmd(
    prompt: str = typer.Argument(..., help="User prompt"),
    system: Optional[str] = typer.Option(None, "--system", "-s"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p"),
    model: Optional[str] = typer.Option(None, "--model", "-m"),
) -> None:
    """Send a chat completion via configured provider."""
    from namm.llm.client import chat

    typer.echo(chat(prompt, system=system, provider=provider, model=model))


@llm_app.command("loop")
def llm_loop_cmd(
    chat_provider: Optional[str] = typer.Option(None, "--chat-provider"),
    embed_provider: Optional[str] = typer.Option(None, "--embed-provider"),
    skip_chat: bool = typer.Option(False, "--skip-chat"),
    pause_s: float = typer.Option(2.0, "--pause-s"),
) -> None:
    """Run NAMM-2026-031 live AMAT loop (prompts × turns × policies)."""
    import orjson
    from namm.metrics.live_embeddings import run_phase_lock_live_loop

    result = run_phase_lock_live_loop(
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        skip_chat=skip_chat,
        pause_s=pause_s,
    )
    typer.echo(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())


@llm_app.command("probe")
def llm_probe_cmd(
    prompt: Optional[str] = typer.Option(
        None,
        "--prompt",
        help="User turn for AMAT live probe (default: CNS question)",
    ),
    embed_provider: Optional[str] = typer.Option(None, "--embed-provider"),
    chat_provider: Optional[str] = typer.Option(None, "--chat-provider"),
    skip_chat: bool = typer.Option(False, "--skip-chat", help="Embed prompts only, no LLM completion"),
) -> None:
    """Run AMAT phase-lock live embedding probe (030 pilot)."""
    import orjson
    from namm.metrics.live_embeddings import run_phase_lock_live_probe

    kwargs: dict = {
        "chat_provider": chat_provider,
        "embed_provider": embed_provider,
        "skip_chat": skip_chat,
    }
    if prompt:
        kwargs["user_prompt"] = prompt
    result = run_phase_lock_live_probe(**kwargs)
    typer.echo(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())


def main() -> None:
    app()


if __name__ == "__main__":
    main()

