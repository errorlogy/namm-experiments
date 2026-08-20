"""Unit tests for live gate calibration (NAMM-2026-033)."""

from namm.metrics.gate_calibration import calibrate_gates, evaluate_calibrated_pass


def test_calibrate_gates_percentile_and_zscore():
    null = [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25]
    cfg = {
        "legacy_d_med_min": 1.2,
        "percentile": 0.95,
        "z_score_min": 2.0,
        "lift_ratio_min": 1.08,
    }
    thr = calibrate_gates(null, cfg)
    assert thr["percentile_threshold"] >= 1.2
    assert thr["null_mean"] == 1.025
    assert thr["legacy_d_med_min"] == 1.2


def test_evaluate_calibrated_lift_ratio_passes_when_legacy_fails():
    base_gates = {
        "beta1_min": 0.0,
        "d_eff_min": 0.0,
        "R_star_lo": 0.0,
        "R_star_hi": 1.0,
        "mu_cns_max": 1.0,
    }
    thresholds = {
        "legacy_d_med_min": 1.2,
        "percentile_threshold": 1.15,
        "z_score_threshold": 1.18,
        "lift_ratio_min": 1.08,
    }
    lock_metrics = {
        "d_med": 0.95,
        "beta_1": 1.5,
        "d_eff": 2.5,
        "order_R": 0.5,
        "mu_cns_proxy": 0.4,
    }
    mu_d = 0.85
    result = evaluate_calibrated_pass(
        lock_metrics, mu_d_med=mu_d, thresholds=thresholds, base_gates=base_gates
    )
    assert result["legacy_gate_pass"] is False
    assert result["lift_ratio_pass"] is True
    assert result["calibrated_gate_pass"] is True
