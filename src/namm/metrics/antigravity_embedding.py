"""Cognitive Antigravity & Embedding Metrics for NAMM (H-CA-001 / NAMM-2026-013).

Calculates:
- D_med: Distance from median response M_0(q_H) using cosine distance over TF-IDF / n-gram embeddings.
- Pipeline compliance: Sequence verification (invariant -> model -> math/code -> countermodel -> conclusion).
- Epistemic status tag density (PHILOSOPHICAL_INFERENCE, CONJECTURE, OPERATIONAL, DEFINITION, COMPUTATIONAL_EVIDENCE).
- z* Antigravity composite score.
"""

from __future__ import annotations

import math

from dataclasses import asdict, dataclass
import re

REQUIRED_PIPELINE_SECTIONS = [
    "invariant",
    "model",
    "math/code/algorithm",
    "countermodel",
    "operational conclusion",
]

EPISTEMIC_TAGS = [
    "PHILOSOPHICAL_INFERENCE",
    "CONJECTURE",
    "OPERATIONAL",
    "DEFINITION",
    "COMPUTATIONAL_EVIDENCE",
]


@dataclass
class AntigravityMetrics:
    distance_from_median: float  # D_med in [0, 1]
    pipeline_compliance: float  # Fraction of required sections matched
    epistemic_tag_count: int  # Total valid epistemic status tags
    falsifiability_score: float  # S_fals: countermodel quality (0.0 to 1.0)
    formalizability_score: float  # F_form: presence of executable math/code
    decorative_symbolism_penalty: float  # D_sym: math notation without code/model
    z_star_score: float  # Composite z* score

    def to_dict(self) -> dict:
        return asdict(self)


def _text_to_vector(text: str, ngram_size: int = 3) -> dict[str, float]:
    """Convert text into normalized character n-gram frequency vector."""
    clean = re.sub(r"\s+", " ", text.lower().strip())
    if not clean:
        return {}

    counts: dict[str, int] = {}
    for i in range(max(1, len(clean) - ngram_size + 1)):
        gram = clean[i : i + ngram_size]
        counts[gram] = counts.get(gram, 0) + 1

    total = sum(v * v for v in counts.values())
    norm = math.sqrt(total) if total > 0 else 1.0

    return {k: v / norm for k, v in counts.items()}


def compute_embedding_distance(text_a: str, text_b: str) -> float:
    """Compute cosine distance (1 - cosine similarity) between text_a and text_b in n-gram space."""
    vec_a = _text_to_vector(text_a)
    vec_b = _text_to_vector(text_b)

    if not vec_a or not vec_b:
        return 1.0

    dot_product = sum(vec_a[k] * vec_b[k] for k in vec_a if k in vec_b)
    cosine_sim = max(0.0, min(1.0, dot_product))
    return round(1.0 - cosine_sim, 4)


def evaluate_pipeline_compliance(text: str) -> float:
    """Check section compliance for the required pipeline order."""
    text_lower = text.lower()
    matched = 0
    last_pos = -1

    for section in REQUIRED_PIPELINE_SECTIONS:
        pos = text_lower.find(section)
        if pos > last_pos and pos != -1:
            matched += 1
            last_pos = pos
        elif pos != -1:
            matched += 0.5

    return round(matched / len(REQUIRED_PIPELINE_SECTIONS), 4)


def count_epistemic_tags(text: str) -> int:
    """Count occurrences of valid epistemic status tags in text."""
    count = 0
    for tag in EPISTEMIC_TAGS:
        count += len(re.findall(rf"\[{tag}\]|`{tag}`", text))
    return count


def compute_antigravity_scores(
    response_text: str,
    median_text: str,
) -> AntigravityMetrics:
    """Compute full Cognitive Antigravity metrics (D_med, compliance, z* score)."""
    d_med = compute_embedding_distance(response_text, median_text)
    compliance = evaluate_pipeline_compliance(response_text)
    tag_count = count_epistemic_tags(response_text)

    # Formalizability score: presence of code blocks or mathematical formulas
    has_code = "```" in response_text or "def " in response_text or "class " in response_text
    has_math = "\\" in response_text or "sum(" in response_text or "forall" in response_text.lower()
    f_form = 1.0 if (has_code and has_math) else (0.6 if (has_code or has_math) else 0.2)

    # Falsifiability score: presence of countermodel section with specific refutations
    has_countermodel = "countermodel" in response_text.lower() or "falsifi" in response_text.lower()
    s_fals = 1.0 if (has_countermodel and ("fail" in response_text.lower() or "not" in response_text.lower())) else (0.5 if has_countermodel else 0.1)

    # Decorative symbolism penalty: math without code/verifiable algorithm
    d_sym = 0.4 if (has_math and not has_code) else 0.0

    # Composite z* score
    z_star = (d_med * compliance * f_form * s_fals) - d_sym
    z_star = round(max(0.0, z_star), 4)

    return AntigravityMetrics(
        distance_from_median=d_med,
        pipeline_compliance=compliance,
        epistemic_tag_count=tag_count,
        falsifiability_score=s_fals,
        formalizability_score=f_form,
        decorative_symbolism_penalty=d_sym,
        z_star_score=z_star,
    )
