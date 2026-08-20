"""Unit tests for Cognitive Class Taxonomy (CCT) metrics."""



import numpy as np



from namm.metrics.cognitive_class import (

    CLASS_PROFILES,

    compute_class_embedding_metrics,

    compute_resource_conversion,

    run_class_mas_batch,

    run_class_separation_batch,

    run_gt2_cne_sweep,

    run_resource_conversion_sweep,

    translation_cost_delta_e,

    myth_cheap_talk_decode,

)

from namm.metrics.consensus_non_optimality import CNSSimulationConfig





def test_class_embedding_separation_k1_vs_k5():

    """H-CCT-001: K1 and K5 occupy distinct regions."""

    k1 = compute_class_embedding_metrics("K1", n_samples=30, seed=42)

    k5 = compute_class_embedding_metrics("K5", n_samples=30, seed=42)

    assert k5.d_median > k1.d_median * 5
    assert k5.rho_pre > k1.rho_pre





def test_class_separation_batch():

    result = run_class_separation_batch(classes=["K1", "K3", "K5"], seeds=[42, 99])

    assert result.non_1d_score > 0.5

    assert "K1_vs_K5" in result.pairwise_separation

    assert "H-CCT-001" in result.hypothesis_support





def test_translation_cost_asymmetric():

    """High-σ → K1 costs more than K1 → high-σ (H-MCG-003 proxy)."""

    up = translation_cost_delta_e("K6", "K1")

    down = translation_cost_delta_e("K1", "K6")

    assert up > down





def test_myth_cheap_talk_fiber_loss():

    signal = np.array([1.0, 0.8, 0.5])

    decoded = myth_cheap_talk_decode(signal, "K5", "K1")

    assert np.linalg.norm(decoded) < np.linalg.norm(signal)





def test_class_heterogeneous_mas_batch():

    config = CNSSimulationConfig(num_agents=24, opinion_dim=3, seed=7)

    compositions = [

        {"K1": 1.0},

        {"K1": 0.7, "K5": 0.2, "K6": 0.1},

    ]

    batch = run_class_mas_batch(config, compositions, num_seeds=3)

    assert batch["num_runs"] == 6

    assert batch["mean_delta_w_k1_homogeneous"] >= 0

    assert "H-CCT-005" in batch["hypothesis_support"]





def test_gt2_cne_sweep_smoke():

    result = run_gt2_cne_sweep(num_players=12, seeds=[42])

    assert "by_game" in result

    assert "H-MCG-009" in result["hypothesis_support"]





def test_resource_conversion_asymmetry():

    """H-CCT-016: same τ, different U_out by class."""

    k6 = compute_resource_conversion("K6", tau=100.0, channel="research", phi=1.5)

    k1 = compute_resource_conversion("K1", tau=100.0, channel="research", phi=1.0)

    assert k6["u_out"] > k1["u_out"]





def test_resource_conversion_sweep():

    result = run_resource_conversion_sweep(

        classes=["K1", "K6"],

        channels=["research", "entertainment"],

        tau_values=[100.0],

        phi_values=[1.0],

    )

    assert result["sweep_size"] > 0

    assert result["asymmetry_high_impact_ratio"] > 1.0





def test_class_profiles_cover_key_classes():

    for cls in ("K1", "K3", "K5", "K6", "K_AI_mu", "K_AI_nd"):

        assert cls in CLASS_PROFILES


