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


class InvariantFormula(BaseModel):
    """Machine-native invariant formula over graph statistics."""

    id: str
    expression: str
    primitives: list[str] = Field(default_factory=list)
    meta_origin: str = "random_composition_of_graph_statistics"


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


class CandidateRecord(BaseModel):
    """Accepted or promising candidate logged to JSONL."""

    candidate_id: str
    formula: InvariantFormula
    score: float
    agrees_with_baseline: bool
    graphs_tested: int
    status: str = "candidate"


class RejectionRecord(BaseModel):
    """Rejected candidate with failure reason."""

    candidate_id: str
    formula: InvariantFormula
    reason: str
    counterexample: dict[str, Any] | None = None


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
