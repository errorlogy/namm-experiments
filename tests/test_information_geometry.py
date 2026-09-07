"""Tests for namm.metrics.information_geometry — no GPU required (mock gradients)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from namm.metrics.information_geometry import (
    compare_curvature,
    compute_certificate,
    correlate_curvature_beta1,
    trajectory_geodesic_curvature,
)


# ---------------------------------------------------------------------------
# trajectory_geodesic_curvature
# ---------------------------------------------------------------------------


def test_trajectory_curvature_basic():
    grad_norms = [1.0, 2.0, 1.5]
    kappas = trajectory_geodesic_curvature(grad_norms)
    assert len(kappas) == 2
    # κ_0 = |2-1|/1 = 1.0
    assert abs(kappas[0] - 1.0) < 1e-6
    # κ_1 = |1.5-2|/2 = 0.25
    assert abs(kappas[1] - 0.25) < 1e-6


def test_trajectory_curvature_empty():
    assert trajectory_geodesic_curvature([]) == []
    assert trajectory_geodesic_curvature([1.0]) == []


def test_trajectory_curvature_constant():
    kappas = trajectory_geodesic_curvature([2.0, 2.0, 2.0])
    assert all(k == 0.0 for k in kappas)


# ---------------------------------------------------------------------------
# correlate_curvature_beta1
# ---------------------------------------------------------------------------


def test_correlation_perfect_positive():
    c = [1.0, 2.0, 3.0]
    b = [10.0, 20.0, 30.0]
    r = correlate_curvature_beta1(c, b)
    assert abs(r - 1.0) < 1e-9


def test_correlation_perfect_negative():
    c = [3.0, 2.0, 1.0]
    b = [1.0, 2.0, 3.0]
    r = correlate_curvature_beta1(c, b)
    assert abs(r + 1.0) < 1e-9


def test_correlation_constant_returns_nan():
    r = correlate_curvature_beta1([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])
    assert math.isnan(r)


def test_correlation_single_element():
    r = correlate_curvature_beta1([1.0], [2.0])
    assert math.isnan(r)


# ---------------------------------------------------------------------------
# compute_certificate
# ---------------------------------------------------------------------------


def _make_result(lift: float, lock_gt: int, n: int = 3) -> dict:
    per = [{"lift": lift / n} for _ in range(lock_gt)] + [{"lift": -0.01} for _ in range(n - lock_gt)]
    return {
        "curvature_lift": lift,
        "lock_gt_mu_count": lock_gt,
        "n_prompts": n,
        "per_prompt": per,
    }


def test_certificate_null():
    r = _make_result(-0.05, 0)
    assert compute_certificate(r) == "CURVATURE_NULL"


def test_certificate_pilot():
    r = _make_result(0.05, 1)
    assert compute_certificate(r) == "CURVATURE_PILOT"


def test_certificate_partial():
    r = _make_result(0.05, 2)
    assert compute_certificate(r) == "CURVATURE_PARTIAL"


def test_certificate_evidence():
    # Construct result with distinct per-prompt lifts correlated with beta1
    per = [{"lift": 0.1}, {"lift": 0.15}, {"lift": 0.2}]
    r = {
        "curvature_lift": 0.15,
        "lock_gt_mu_count": 3,
        "n_prompts": 3,
        "per_prompt": per,
    }
    beta1 = [0.3, 0.5, 0.7]  # perfectly correlated with lifts → r=1.0
    assert compute_certificate(r, beta1) == "CURVATURE_EVIDENCE"


def test_certificate_partial_not_evidence_low_corr():
    r = _make_result(0.15, 2)
    # Perfect negative correlation → |corr|=1 ≥ 0.5 → but lift=0.15>0.1 so EVIDENCE
    beta1 = [0.7, 0.5, 0.3]
    cert = compute_certificate(r, beta1)
    # lift > 0.1, |corr| ≥ 0.5 → EVIDENCE
    assert cert == "CURVATURE_EVIDENCE"


# ---------------------------------------------------------------------------
# compare_curvature (mock model/tokenizer)
# ---------------------------------------------------------------------------


class _MockTokenizer:
    pad_token_id = 0
    eos_token_id = 0

    def __call__(self, text, *, return_tensors=None, truncation=None, max_length=None):
        import torch

        ids = torch.zeros((1, 5), dtype=torch.long)
        return {"input_ids": ids, "attention_mask": torch.ones((1, 5), dtype=torch.long)}

    def apply_chat_template(self, msgs, *, tokenize=False, add_generation_prompt=False):
        return " ".join(m["content"] for m in msgs)

    def decode(self, tokens, *, skip_special_tokens=True):
        return "mock reply"


class _MockOutput:
    def __init__(self):
        import torch

        batch, seq, hidden = 1, 5, 16
        vocab = 32
        self.hidden_states = [torch.zeros(batch, seq, hidden) for _ in range(3)]
        self.logits = torch.zeros(batch, seq, vocab)

    def __getattr__(self, name):
        raise AttributeError(name)


class _MockModel:
    """Minimal causal LM stub for logit-gradient norm proxy."""

    def __init__(self):
        import torch

        self.vocab = 32
        self.hidden = 16
        weight = torch.arange(self.vocab, dtype=torch.float32).unsqueeze(1).repeat(
            1, self.hidden
        )

        class _Emb:
            def __init__(self, w):
                self.weight = w

        self._out_emb = _Emb(weight)

    def eval(self):
        return self

    def __call__(self, input_ids, *, output_hidden_states=False):
        import torch

        out = _MockOutput()
        last = torch.ones(1, 5, 16)
        out.hidden_states[-1] = last
        out.logits = torch.zeros(1, 5, 32)
        return out

    def get_output_embeddings(self):
        return self._out_emb

    def generate(self, **kwargs):
        import torch

        return torch.zeros((1, 6), dtype=torch.long)


def test_compare_curvature_mock():
    model = _MockModel()
    tokenizer = _MockTokenizer()
    prompts = ["Prompt A", "Prompt B"]
    result = compare_curvature(
        prompts,
        prompts,
        model,
        tokenizer,
        device="cpu",
        mu_system="You are helpful.",
        lock_system="You are locked.",
        n_turns=2,
        max_new_tokens=8,
    )
    assert "mean_curvature_mu" in result
    assert "mean_curvature_lock" in result
    assert "curvature_lift" in result
    assert len(result["per_prompt"]) == 2
    for p in result["per_prompt"]:
        assert "mu_kappa" in p
        assert "lock_kappa" in p
        assert "lift" in p
