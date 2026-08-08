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
        if config.is_program_domain and best.formula.canonical_ast:
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

    if best:
        if config.is_program_domain and best.formula.canonical_ast:
            ast_node = parse_ast_dict(best.formula.canonical_ast)
            proj = human_projection_from_ast(
                ast_node, candidate_id=best.candidate_id, trust_certificate=True
            )
            human_lines.extend(["", proj])
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

    (output_dir / "result.json").write_bytes(
        orjson.dumps(experiment_result.model_dump(), option=orjson.OPT_INDENT_2)
    )
    (output_dir / "human_projection.md").write_text(human_projection, encoding="utf-8")
    (output_dir / "HUMAN_PROJECTION.md").write_text(human_projection, encoding="utf-8")

    if certificate:
        (output_dir / "certificate.json").write_bytes(
            orjson.dumps(certificate, option=orjson.OPT_INDENT_2)
        )

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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
