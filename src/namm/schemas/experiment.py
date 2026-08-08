"""Experiment and candidate schemas matching EXPERIMENT_TEMPLATE sections."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ClaimStatus(str, Enum):
    DEFINITION = "DEFINITION"
    CONJECTURE = "CONJECTURE"
    LEMMA = "LEMMA"
    THEOREM = "THEOREM"
    COMPUTATIONAL_EVIDENCE = "COMPUTATIONAL_EVIDENCE"


class NoveltyLevel(str, Enum):
    N0 = "N0"
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"
    N4 = "N4"
    N5 = "N5"


class InvariantFormula(BaseModel):
    """Machine-native invariant formula over graph statistics."""

    id: str
    expression: str
    primitives: list[str] = Field(default_factory=list)
    meta_origin: str = "random_composition_of_graph_statistics"
    canonical_ast: dict[str, Any] | None = None
    ast_hash: str | None = None


class RepresentationMetrics(BaseModel):
    """Operational K_A proxies per REPRESENTATION_METRICS.md."""

    json_bytes: int
    gzip_bytes: int
    eval_time_ms: float
    token_count_estimate: int
    projection_token_estimate: int | None = None


class AttackChecklistItem(BaseModel):
    step: str
    passed: bool
    notes: str = ""


class AttackChecklist(BaseModel):
    items: list[AttackChecklistItem] = Field(default_factory=list)
    signed_off: bool = False


class BaselineComparison(BaseModel):
    baseline_id: str
    expression: str
    equivalent: bool
    pearson_r: float | None = None


class BaselineResults(BaseModel):
    comparisons: list[BaselineComparison] = Field(default_factory=list)
    max_correlation: float | None = None
    correlated_baseline: str | None = None
    rejected_for_correlation: bool = False


class ExperimentConfig(BaseModel):
    """Runtime configuration for an experiment run."""

    experiment_id: str
    domain: str = "finite_graphs"
    max_order: int = 8
    num_candidates: int = 50
    seed: int = 42
    research_question: str = (
        "Can random search discover a nontrivial graph invariant candidate "
        "that agrees with known baselines on small graphs but differs on at least one?"
    )
    baselines: list[str] = Field(default_factory=lambda: ["wiener_index", "algebraic_connectivity"])
    correlation_threshold: float = 0.95
    correlation_rejection_threshold: float | None = None
    correlation_atlas_order: int = 6
    train_max_order: int = 6
    held_out_families: list[str] = Field(
        default_factory=lambda: ["trees", "bipartite", "cubic"]
    )
    ast_max_depth: int = 3
    ast_max_leaves: int = 5
    representation_ratio_threshold: float | None = 2.0
    search_strategy: str = "random"
    evolution_population: int = 20
    evolution_generations: int = 5
    rewriting_max_length: int = 6
    rewriting_num_rules: int = 3
    confluence_threshold: float = 1.0

    @property
    def effective_correlation_threshold(self) -> float:
        return (
            self.correlation_rejection_threshold
            if self.correlation_rejection_threshold is not None
            else self.correlation_threshold
        )

    @property
    def is_program_domain(self) -> bool:
        return self.domain in ("program_ast", "program")

    @property
    def is_rewriting_domain(self) -> bool:
        return self.domain in ("rewriting", "string_rewriting")

    @property
    def is_graph_string_domain(self) -> bool:
        return self.domain in ("finite_graphs", "graph_string", "graph")

    @property
    def effective_representation_ratio_threshold(self) -> float | None:
        return self.representation_ratio_threshold


class CandidateRecord(BaseModel):
    """Accepted or promising candidate logged to JSONL."""

    candidate_id: str
    formula: InvariantFormula
    score: float
    agrees_with_baseline: bool
    graphs_tested: int
    status: str = "candidate"
    novelty_level: NoveltyLevel | None = None
    representation_metrics: RepresentationMetrics | None = None
    attack_checklist: AttackChecklist | None = None
    baseline_results: BaselineResults | None = None


class RejectionRecord(BaseModel):
    """Rejected candidate with failure reason."""

    candidate_id: str
    formula: InvariantFormula
    reason: str
    counterexample: dict[str, Any] | None = None
    baseline_results: BaselineResults | None = None
    novelty_level: NoveltyLevel | None = None


class ExperimentResult(BaseModel):
    """Summary artifact for machine-native + human projection output."""

    experiment_id: str
    domain: str
    research_question: str
    candidates_found: int
    rejections: int
    best_candidate: CandidateRecord | None = None
    machine_representation: dict[str, Any]
    human_projection: str
    protocol_version: str = "v2"
    certificate: dict[str, Any] | None = None
    generative_holdout: dict[str, Any] | None = None
