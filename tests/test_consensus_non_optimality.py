"""Unit tests for Consensus Non-Optimality (CNS) metrics — H-CNS-001..013."""

import numpy as np

from namm.metrics.consensus_non_optimality import (
    CNSSimulationConfig,
    FuzzyContour,
    apply_consensus_operator,
    build_membership_matrix,
    delta_h_fiber,
    evaluate_cns_instance,
    generate_opinion_graph,
    initialize_agent_state,
    kuramoto_order_parameter,
    normalized_welfare_gap,
    opinion_entropy,
    projection_error,
    run_cns_batch,
    run_kuramoto_vote_sweep,
    welfare,
    welfare_optimal,
)


def test_welfare_optimal_beats_mean_consensus():
    """H-CNS-001: heterogeneous ideals → consensus mean is suboptimal."""
    ideals = np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0]])
    opinions = ideals + np.array([[0.05, 0.0], [-0.05, 0.0], [0.0, 0.05]])
    consensus = apply_consensus_operator(opinions, "mean")
    cf = welfare_optimal(ideals)
    w_c = welfare(consensus, ideals)
    w_cf = welfare(cf, ideals)
    assert w_cf > w_c
    gap = normalized_welfare_gap(w_c, w_cf)
    assert gap > 0.0


def test_consensus_operators_non_injective():
    """Consensus map collapses distinct profiles."""
    a = np.array([[1.0, 0.0], [1.0, 0.01]])
    b = np.array([[1.0, 0.0], [1.0, -0.01]])
    c_a = apply_consensus_operator(a, "mean")
    c_b = apply_consensus_operator(b, "mean")
    assert np.allclose(c_a, c_b, atol=0.02)
    assert not np.allclose(a, b)


def test_delta_h_fiber_positive():
    """H-CNS-004: entropy decreases under consensus projection."""
    rng = np.random.default_rng(42)
    opinions = rng.normal(0, 1, size=(20, 2))
    consensus = apply_consensus_operator(opinions, "mean")
    assert opinion_entropy(opinions) > 0
    assert delta_h_fiber(opinions, consensus) > 0.5


def test_projection_error():
    opinions = np.array([[1.0, 0.0], [-1.0, 0.0]])
    consensus = apply_consensus_operator(opinions, "vote")
    err = projection_error(opinions, consensus)
    assert err >= 0.0


def test_fuzzy_contour_membership():
    graph = generate_opinion_graph(16, seed=7)
    opinions, _, _, tags = initialize_agent_state(16, 3, seed=7)
    contours = [
        FuzzyContour(id="bloc", membership="gaussian_centroid", centroid=[0.0, 0.0, 0.0], sigma=0.5),
        FuzzyContour(
            id="climate",
            membership="issue_tag",
            issue_tags=["climate", "energy"],
            agent_expertise_weight=0.8,
        ),
        FuzzyContour(id="region", membership="spatial_soft", center_node=0, decay_length=2.0),
    ]
    mat = build_membership_matrix(contours, opinions, graph, tags)
    assert mat.shape == (16, 3)
    assert np.all(mat >= 0) and np.all(mat <= 1)


def test_evaluate_cns_instance_equilibrium_gap():
    config = CNSSimulationConfig(
        num_agents=24,
        opinion_dim=3,
        consensus_operator="defuzzify_mean",
        fuzzy_contours=[
            FuzzyContour(id="a", membership="gaussian_centroid", centroid=[-0.5, 0.2, 0.0], sigma=0.3),
            FuzzyContour(id="b", membership="gaussian_centroid", centroid=[0.5, -0.2, 0.0], sigma=0.3),
        ],
        seed=123,
    )
    metrics = evaluate_cns_instance(config)
    assert metrics.at_equilibrium
    assert metrics.delta_w_global >= 0.0
    assert metrics.delta_h_fiber > 0.0
    assert len(metrics.delta_w_per_contour) >= 1


def test_run_cns_batch_hypothesis_flags():
    config = CNSSimulationConfig(num_agents=20, opinion_dim=2, seed=99)
    batch = run_cns_batch(config, num_instances=12)
    assert batch["positive_gap_fraction"] > 0.5
    assert batch["mean_delta_w_global"] > 0
    assert "H-CNS-001" in batch["hypothesis_support"]


def test_kuramoto_order_parameter():
    phases = np.linspace(0, 0.1, 10)
    R_sync = kuramoto_order_parameter(phases)
    phases_inc = np.linspace(0, 2 * np.pi, 10)
    R_inc = kuramoto_order_parameter(phases_inc)
    assert R_sync > R_inc


def test_run_kuramoto_vote_sweep_smoke():
    config = CNSSimulationConfig(num_agents=12, opinion_dim=2, seed=5)
    result = run_kuramoto_vote_sweep(
        config,
        K_values=[1.0, 2.0],
        threshold_values=[0.0, 0.5],
        max_non_optimality_values=[0.2, 0.4],
        sigma_values=[0.2, 0.3],
    )
    assert result["sweep_size"] > 0
    assert "hypothesis_support" in result
    assert "H-CNS-002" in result["hypothesis_support"]


def test_cns_config_from_dict():
    data = {
        "max_non_optimality": 0.3,
        "consensus_operator": "vote",
        "num_agents": 10,
        "fuzzy_contours": [{"id": "x", "membership": "triangular", "a": 0, "b": 0.5, "c": 1}],
    }
    cfg = CNSSimulationConfig.from_dict(data, seed=1)
    assert cfg.consensus_operator == "vote"
    assert cfg.num_agents == 10
    assert len(cfg.fuzzy_contours) == 1
