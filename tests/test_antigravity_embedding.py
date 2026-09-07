"""Unit tests for Cognitive Antigravity & Embedding metrics."""

from namm.metrics.antigravity_embedding import (
    compute_antigravity_scores,
    compute_embedding_distance,
    count_epistemic_tags,
    evaluate_pipeline_compliance,
)


def test_compute_embedding_distance():
    text1 = "A graph invariant for 4-regular graphs using spectral eigenvalues."
    text2 = "A graph invariant for 4-regular graphs using spectral eigenvalues."
    text3 = "Non-anthropic AST tensor contraction over finite fields."

    # Identical texts -> distance ~ 0.0
    dist_self = compute_embedding_distance(text1, text2)
    assert dist_self == 0.0

    # Different texts -> distance > 0.0
    dist_diff = compute_embedding_distance(text1, text3)
    assert dist_diff > 0.2


def test_evaluate_pipeline_compliance():
    valid_text = (
        "invariant: x**2 + y\n"
        "model: topological persistence\n"
        "math/code/algorithm: def f(x): return x\n"
        "countermodel: fails on trees\n"
        "operational conclusion: confirmed"
    )
    compliance = evaluate_pipeline_compliance(valid_text)
    assert compliance == 1.0

    incomplete_text = "Just some generic prose answer."
    assert evaluate_pipeline_compliance(incomplete_text) == 0.0


def test_count_epistemic_tags():
    text = "[OPERATIONAL] step 1. [CONJECTURE] claim A. [PHILOSOPHICAL_INFERENCE] background."
    count = count_epistemic_tags(text)
    assert count == 3


def test_compute_antigravity_scores():
    response = (
        "[OPERATIONAL] invariant: x**2\n"
        "[DEFINITION] model: AST\n"
        "[COMPUTATIONAL_EVIDENCE] math/code/algorithm:\n"
        "```python\n"
        "def custom_inv(g): return 1\n"
        "```\n"
        "[CONJECTURE] countermodel: fails on bipartite\n"
        "[OPERATIONAL] operational conclusion: verified"
    )
    median = "Standard graph invariant answer."

    metrics = compute_antigravity_scores(response, median)
    assert metrics.distance_from_median > 0.2
    assert metrics.pipeline_compliance == 1.0
    assert metrics.epistemic_tag_count == 5
    assert metrics.z_star_score > 0.0
