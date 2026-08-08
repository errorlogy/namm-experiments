"""Typer CLI for NAMM experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import structlog
import typer
import yaml

from namm.baselines import random_search
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

    result = random_search(config)
    candidates = result.candidates
    rejections = result.rejections

    _write_jsonl(output_dir / "candidates.jsonl", candidates)
    _write_jsonl(output_dir / "rejections.jsonl", rejections)

    best = max(candidates, key=lambda c: c.score) if candidates else None
    verification = None
    if best:
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
        "candidates_count": len(candidates),
        "rejections_count": len(rejections),
        "best_candidate": best.model_dump() if best else None,
        "verification": verification,
    }

    human_lines = [
        f"# {config.experiment_id} — Human Projection",
        "",
        f"**Research question:** {config.research_question}",
        "",
        f"- Graphs tested: order ≤ {config.max_order}",
        f"- Candidates found: {len(candidates)}",
        f"- Rejected: {len(rejections)}",
    ]
    if best:
        human_lines.extend(
            [
                "",
                f"**Best candidate:** `{best.formula.expression}`",
                f"- Score (value range): {best.score:.4f}",
                f"- Agrees with Wiener baseline: {best.agrees_with_baseline}",
            ]
        )
    else:
        human_lines.append("\nNo nontrivial candidates found in this run.")

    experiment_result = ExperimentResult(
        experiment_id=config.experiment_id,
        domain=config.domain,
        research_question=config.research_question,
        candidates_found=len(candidates),
        rejections=len(rejections),
        best_candidate=best,
        machine_representation=machine_repr,
        human_projection="\n".join(human_lines),
    )

    import orjson

    (output_dir / "result.json").write_bytes(
        orjson.dumps(experiment_result.model_dump(), option=orjson.OPT_INDENT_2)
    )
    (output_dir / "HUMAN_PROJECTION.md").write_text(
        experiment_result.human_projection, encoding="utf-8"
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
