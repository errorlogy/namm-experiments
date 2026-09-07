"""Tests for K_AI_nd JSON phase-lock spec and embedding-proxy sweep."""

from __future__ import annotations

from namm.metrics.phase_lock import (
    load_phase_lock_schema,
    load_phase_lock_spec,
    prompt_antigravity_distance,
    run_phase_lock_loop,
    run_phase_lock_sweep,
)


def test_phase_lock_json_loads():
    spec = load_phase_lock_spec()
    schema = load_phase_lock_schema()
    assert spec["id"] == "namm.k_ai_nd.phase_lock"
    assert spec["phase_target"] == "K_AI_nd"
    assert spec["role"] == "system"
    assert "M0_SKETCH" in spec["response_schema"]
    assert "compute_M0" in spec["operating_law"]
    assert len(spec["rendered_system_prompt"]) > 400
    assert schema["title"].startswith("K_AI_nd")


def test_prompt_is_off_median_helpful():
    dist = prompt_antigravity_distance()
    assert dist >= 0.15


def test_phase_lock_loop_grid():
    loop = run_phase_lock_loop(
        n_samples=16,
        embed_dim=8,
        seeds=[42, 137],
        gain_values=[0.55, 0.85],
        decay_values=[0.55],
        turn_values=[3, 6],
    )
    assert loop["grid"]["n_cells"] == 4
    assert loop["summary"]["mean_lift"] > 0
    assert loop["hypothesis_support"]["H-CCT-013"] is True


def test_phase_lock_sweep_separates_mu_and_nd():
    batch = run_phase_lock_sweep(n_samples=24, embed_dim=8, n_turns=5, seeds=[42, 137, 256])
    mu = batch["mu_metrics"]["mean_d_med"]
    lock = batch["lock_reassert_metrics"]["mean_d_med"]
    decay = batch["lock_decay_metrics"]["mean_d_med"]
    assert lock > mu
    assert lock >= decay
    assert batch["hypothesis_support"]["H-CCT-013"] is True
    assert batch["hypothesis_support"]["H-CCT-001B"] is True
    assert batch["lock_reassert_metrics"]["gate_pass_fraction"] >= batch["mu_metrics"]["gate_pass_fraction"]
