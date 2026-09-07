"""Unit tests for multi-embedder gate calibration (NAMM-2026-034)."""

from namm.metrics.gate_calibration import compute_cross_embedder_analysis


def test_cross_embedder_spearman_and_agreement():
    branches = [
        {
            "embed_provider": "openai",
            "cells": [
                {"prompt_hash": 1, "n_turns": 3, "lift": 0.08},
                {"prompt_hash": 2, "n_turns": 6, "lift": 0.04},
            ],
        },
        {
            "embed_provider": "openrouter",
            "cells": [
                {"prompt_hash": 1, "n_turns": 3, "lift": 0.07},
                {"prompt_hash": 2, "n_turns": 6, "lift": 0.05},
            ],
        },
    ]
    cross = compute_cross_embedder_analysis(branches, lift_agreement_min=0.03)
    assert cross["n_embedders"] == 2
    assert cross["mean_spearman_rho"] == 1.0
    assert cross["lift_agreement_fraction"] == 1.0
    assert "openai__openrouter" in cross["pairwise_spearman"]


def test_cross_embedder_single_embedder():
    cross = compute_cross_embedder_analysis(
        [{"embed_provider": "openai", "cells": [{"prompt_hash": 1, "n_turns": 3, "lift": 0.1}]}]
    )
    assert cross["mean_spearman_rho"] is None
    assert cross["lift_agreement_fraction"] is None
