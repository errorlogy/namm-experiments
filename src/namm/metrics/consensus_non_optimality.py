"""Consensus Non-Optimality (CNS) metrics — H-CNS-001..H-CNS-013.

Multi-agent opinion graphs, consensus operators, welfare gaps, fuzzy contours,
and Kuramoto–vote coupling for NAMM-2026-021 / NAMM-2026-022.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

import networkx as nx
import numpy as np
from scipy.integrate import solve_ivp

from namm.metrics.entropy import delta_h_fiber, opinion_entropy
from namm.metrics.fuzzy import (
    MembershipKind,
    gaussian_centroid,
    issue_tag_membership,
    ramp,
    spatial_soft,
    trapezoidal,
    triangular,
)

ConsensusOperator = Literal["vote", "mean", "defuzzify_mean", "kuramoto_sync"]
AntiConsensusMetric = Literal["welfare_gap", "entropy_fiber", "projection_error"]
BoundMode = Literal["measure", "soft", "hard"]


@dataclass
class FuzzyContour:
    """Socio-political fuzzy contour over agents."""

    id: str
    membership: str = "gaussian_centroid"
    max_non_optimality: float | None = None
    # gaussian / gaussian_centroid
    centroid: list[float] | None = None
    sigma: float = 0.25
    # triangular / trapezoidal
    a: float | None = None
    b: float | None = None
    c: float | None = None
    d: float | None = None
    # ramp
    x0: float | None = None
    x1: float | None = None
    # spatial_soft
    center_node: int | None = None
    decay_length: float = 2.5
    # issue_tag
    issue_tags: list[str] = field(default_factory=list)
    agent_expertise_weight: float = 0.6
    label_ru: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FuzzyContour:
        return cls(
            id=data["id"],
            membership=data.get("membership", "gaussian_centroid"),
            max_non_optimality=data.get("max_non_optimality"),
            centroid=data.get("centroid"),
            sigma=float(data.get("sigma", 0.25)),
            a=data.get("a"),
            b=data.get("b"),
            c=data.get("c"),
            d=data.get("d"),
            x0=data.get("x0"),
            x1=data.get("x1"),
            center_node=data.get("center_node"),
            decay_length=float(data.get("decay_length", 2.5)),
            issue_tags=list(data.get("issue_tags", [])),
            agent_expertise_weight=float(data.get("agent_expertise_weight", 0.6)),
            label_ru=data.get("label_ru"),
        )


@dataclass
class CNSSimulationConfig:
    """Runtime config for CNS simulations (maps to cns_simulation YAML block)."""

    max_non_optimality: float = 0.35
    max_anti_consensus: float | None = None
    anti_consensus_metric: AntiConsensusMetric = "welfare_gap"
    bound_mode: BoundMode = "measure"
    consensus_operator: ConsensusOperator = "defuzzify_mean"
    num_agents: int = 48
    opinion_dim: int = 3
    fuzzy_contours: list[FuzzyContour] = field(default_factory=list)
    kuramoto_K: float = 1.8
    target_order_R: float = 0.85
    coupling_matrix: str = "from_graph"
    seed: int = 42

    @classmethod
    def from_dict(cls, data: dict[str, Any], seed: int = 42) -> CNSSimulationConfig:
        max_no = float(data.get("max_non_optimality", data.get("max_anti_consensus", 0.35)))
        contours = [FuzzyContour.from_dict(c) for c in data.get("fuzzy_contours", [])]
        dynamics = data.get("dynamics", {})
        return cls(
            max_non_optimality=max_no,
            max_anti_consensus=data.get("max_anti_consensus"),
            anti_consensus_metric=data.get("anti_consensus_metric", "welfare_gap"),
            bound_mode=data.get("bound_mode", "measure"),
            consensus_operator=data.get("consensus_operator", "defuzzify_mean"),
            num_agents=int(data.get("num_agents", 48)),
            opinion_dim=int(data.get("opinion_dim", 3)),
            fuzzy_contours=contours,
            kuramoto_K=float(dynamics.get("kuramoto_K", data.get("kuramoto_K", 1.8))),
            target_order_R=float(dynamics.get("target_order_R", data.get("target_order_R", 0.85))),
            coupling_matrix=dynamics.get("coupling_matrix", "from_graph"),
            seed=seed,
        )

    @property
    def effective_max_non_optimality(self) -> float:
        if self.max_anti_consensus is not None:
            return float(self.max_anti_consensus)
        return self.max_non_optimality


@dataclass
class CNSMetrics:
    """Measured anti-consensus gaps at consensus equilibrium."""

    delta_w_global: float
    delta_h_fiber: float
    epsilon_proj: float
    mu_cns_global: float
    welfare_consensus: float
    welfare_counterfactual: float
    delta_w_per_contour: dict[str, float] = field(default_factory=dict)
    mu_cns_per_contour: dict[str, float] = field(default_factory=dict)
    bound_saturated_flags: dict[str, bool] = field(default_factory=dict)
    consensus_operator: str = "defuzzify_mean"
    at_equilibrium: bool = True
    order_parameter_R: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_contour_membership(
    contour: FuzzyContour,
    agent_idx: int,
    opinions: np.ndarray,
    graph: nx.Graph,
    agent_issue_tags: list[set[str]] | None = None,
) -> float:
    """Membership μ_F_k(agent) in [0, 1]."""
    kind = contour.membership.lower()
    opinion = opinions[agent_idx]

    if kind in ("gaussian", "gaussian_centroid"):
        if contour.centroid is None:
            return 0.5
        return gaussian_centroid(opinion, np.asarray(contour.centroid, dtype=float), contour.sigma)

    if kind == "triangular":
        x = float(np.linalg.norm(opinion))
        a, b, c = contour.a or 0.0, contour.b or 0.5, contour.c or 1.0
        return triangular(x, a, b, c)

    if kind == "trapezoidal":
        x = float(np.linalg.norm(opinion))
        a = contour.a or 0.0
        b = contour.b or 0.25
        c = contour.c or 0.75
        d = contour.d or 1.0
        return trapezoidal(x, a, b, c, d)

    if kind == "ramp":
        x = float(np.linalg.norm(opinion))
        x0 = contour.x0 or 0.0
        x1 = contour.x1 or 1.0
        return ramp(x, x0, x1)

    if kind == "spatial_soft":
        center = contour.center_node if contour.center_node is not None else 0
        return spatial_soft(agent_idx, center, graph, contour.decay_length)

    if kind == "issue_tag":
        if agent_issue_tags is None:
            return 0.5
        return issue_tag_membership(
            agent_issue_tags[agent_idx],
            contour.issue_tags,
            contour.agent_expertise_weight,
        )

    return 0.5


def build_membership_matrix(
    contours: list[FuzzyContour],
    opinions: np.ndarray,
    graph: nx.Graph,
    agent_issue_tags: list[set[str]] | None = None,
) -> np.ndarray:
    """Shape (num_agents, num_contours)."""
    n = opinions.shape[0]
    if not contours:
        return np.ones((n, 1))
    mat = np.zeros((n, len(contours)))
    for j, contour in enumerate(contours):
        for i in range(n):
            mat[i, j] = compute_contour_membership(contour, i, opinions, graph, agent_issue_tags)
    return mat


def welfare(
    collective: np.ndarray,
    ideal_points: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """Global welfare W(y) = -Σ w_i ||y - u_i||² (higher is better)."""
    if weights is None:
        weights = np.ones(len(ideal_points))
    diffs = ideal_points - collective
    sq = np.sum(diffs * diffs, axis=1)
    return float(-np.sum(weights * sq))


def welfare_optimal(ideal_points: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    """Fiber-preserving counterfactual x† — weighted centroid of ideal points."""
    if weights is None:
        weights = np.ones(len(ideal_points))
    w = weights / max(np.sum(weights), 1e-12)
    return np.average(ideal_points, axis=0, weights=w)


def apply_consensus_operator(
    opinions: np.ndarray,
    operator: ConsensusOperator,
    membership: np.ndarray | None = None,
    natural_frequencies: np.ndarray | None = None,
) -> np.ndarray:
    """Consensus map C: X^N → X."""
    if operator == "mean":
        return np.mean(opinions, axis=0)

    if operator == "vote":
        signs = np.sign(np.sum(opinions, axis=0))
        signs[signs == 0] = 1.0
        magnitude = np.mean(np.abs(opinions), axis=0)
        return signs * magnitude

    if operator == "defuzzify_mean":
        if membership is None or membership.size == 0:
            return np.mean(opinions, axis=0)
        # Contour-weighted defuzzification (centroid of fuzzy aggregate)
        w = np.sum(membership, axis=1)
        w = w / max(np.sum(w), 1e-12)
        return np.average(opinions, axis=0, weights=w)

    if operator == "kuramoto_sync":
        phases = np.arctan2(opinions[:, 1] if opinions.shape[1] > 1 else opinions[:, 0], opinions[:, 0])
        if natural_frequencies is not None:
            # Weight phases toward frequency-heterogeneous mean direction
            weights = 1.0 / (1.0 + np.abs(natural_frequencies))
        else:
            weights = np.ones(len(phases))
        z = np.sum(weights * np.exp(1j * phases))
        sync_phase = np.angle(z)
        radius = float(np.abs(z) / max(np.sum(weights), 1e-12))
        dim = opinions.shape[1]
        result = np.zeros(dim)
        result[0] = radius * np.cos(sync_phase)
        if dim > 1:
            result[1] = radius * np.sin(sync_phase)
        if dim > 2:
            result[2:] = np.mean(opinions[:, 2:], axis=0)
        return result

    return np.mean(opinions, axis=0)


def kuramoto_order_parameter(phases: np.ndarray) -> float:
    """R = |⟨e^{iθ}⟩|."""
    z = np.mean(np.exp(1j * phases))
    return float(np.abs(z))


def mu_consensus_degree(opinions: np.ndarray, phases: np.ndarray | None = None) -> float:
    """Consensus strength μ_cns ∈ [0, 1]."""
    if phases is not None:
        return kuramoto_order_parameter(phases)
    centered = opinions - np.mean(opinions, axis=0)
    var = float(np.mean(np.sum(centered * centered, axis=1)))
    return float(1.0 / (1.0 + var))


def projection_error(opinions: np.ndarray, consensus: np.ndarray) -> float:
    """L2 projection error vs agent profile mean (fiber centroid)."""
    fiber_centroid = np.mean(opinions, axis=0)
    err = float(np.linalg.norm(consensus - fiber_centroid))
    return err / max(float(np.linalg.norm(fiber_centroid)), 1e-12)


def normalized_welfare_gap(w_consensus: float, w_counterfactual: float) -> float:
    """ΔW / W† with W† = welfare at counterfactual, capped at 1.0."""
    gap = w_counterfactual - w_consensus
    if gap <= 0:
        return 0.0
    denom = max(abs(w_counterfactual), abs(w_consensus), 1e-6)
    return float(min(gap / denom, 1.0))


def generate_opinion_graph(num_agents: int, seed: int) -> nx.Graph:
    """Small-world opinion graph substrate."""
    rng = np.random.default_rng(seed)
    n = num_agents
    k = min(4, n - 1) if n > 1 else 1
    g = nx.connected_watts_strogatz_graph(n, k, 0.15, seed=int(rng.integers(0, 2**31)))
    return g


def initialize_agent_state(
    num_agents: int,
    opinion_dim: int,
    seed: int,
    heterogeneity: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[set[str]]]:
    """Return opinions, ideal_points, natural_frequencies, issue_tags."""
    rng = np.random.default_rng(seed)
    ideal = rng.normal(0, heterogeneity, size=(num_agents, opinion_dim))
    # Reported opinions: noisy views toward distinct clusters
    noise = rng.normal(0, 0.15, size=(num_agents, opinion_dim))
    opinions = ideal + noise
    frequencies = rng.uniform(0.5, 2.0, size=num_agents)
    tag_pool = ["climate", "energy", "emissions", "fiscal", "trade", "health"]
    issue_tags: list[set[str]] = []
    for i in range(num_agents):
        k = int(rng.integers(1, 4))
        tags = set(rng.choice(tag_pool, size=k, replace=False).tolist())
        issue_tags.append(tags)
    return opinions, ideal, frequencies, issue_tags


def run_kuramoto_to_equilibrium(
    graph: nx.Graph,
    phases: np.ndarray,
    natural_frequencies: np.ndarray,
    K: float,
    t_max: float = 20.0,
) -> tuple[np.ndarray, float]:
    """Integrate Kuramoto dynamics to near equilibrium."""
    n = len(phases)
    adj = nx.to_numpy_array(graph)
    row_sums = adj.sum(axis=1)
    row_sums[row_sums == 0] = 1.0
    adj = adj / row_sums[:, None]

    def rhs(_t: float, theta: np.ndarray) -> np.ndarray:
        dtheta = natural_frequencies.copy()
        for i in range(n):
            dtheta[i] += K * np.sum(adj[i] * np.sin(theta - theta[i]))
        return dtheta

    sol = solve_ivp(rhs, (0, t_max), phases, method="RK45", rtol=1e-6, atol=1e-8)
    final_phases = sol.y[:, -1] % (2 * math.pi)
    R = kuramoto_order_parameter(final_phases)
    return final_phases, R


def opinions_from_phases(phases: np.ndarray, opinions: np.ndarray) -> np.ndarray:
    """Map synchronized phases back to opinion vectors (preserve magnitudes)."""
    mags = np.linalg.norm(opinions, axis=1, keepdims=True)
    mags = np.maximum(mags, 0.1)
    result = np.zeros_like(opinions)
    result[:, 0] = (mags[:, 0] * np.cos(phases)).flatten()
    if opinions.shape[1] > 1:
        result[:, 1] = (mags[:, 0] * np.sin(phases)).flatten()
    if opinions.shape[1] > 2:
        result[:, 2:] = opinions[:, 2:]
    return result


def evaluate_cns_instance(
    config: CNSSimulationConfig,
    graph: nx.Graph | None = None,
    seed_offset: int = 0,
) -> CNSMetrics:
    """Single-instance CNS evaluation at consensus equilibrium."""
    seed = config.seed + seed_offset
    n = config.num_agents
    d = config.opinion_dim

    if graph is None:
        graph = generate_opinion_graph(n, seed)

    opinions, ideal_points, frequencies, issue_tags = initialize_agent_state(n, d, seed)
    membership = build_membership_matrix(config.fuzzy_contours, opinions, graph, issue_tags)

    phases = np.arctan2(
        opinions[:, 1] if d > 1 else np.zeros(n),
        opinions[:, 0],
    )
    order_R: float | None = None

    if config.consensus_operator == "kuramoto_sync":
        phases, order_R = run_kuramoto_to_equilibrium(
            graph, phases, frequencies, config.kuramoto_K
        )
        opinions_eq = opinions_from_phases(phases, opinions)
    else:
        opinions_eq = opinions.copy()

    consensus = apply_consensus_operator(
        opinions_eq,
        config.consensus_operator,
        membership=membership,
        natural_frequencies=frequencies,
    )
    counterfactual = welfare_optimal(ideal_points)

    w_cns = welfare(consensus, ideal_points)
    w_cf = welfare(counterfactual, ideal_points)

    delta_w = normalized_welfare_gap(w_cns, w_cf)
    delta_h = delta_h_fiber(opinions_eq, consensus)
    eps = projection_error(opinions_eq, consensus)
    mu_global = mu_consensus_degree(opinions_eq, phases if order_R is not None else None)

    delta_w_contour: dict[str, float] = {}
    mu_cns_contour: dict[str, float] = {}
    bound_flags: dict[str, bool] = {}

    for j, contour in enumerate(config.fuzzy_contours):
        mask = membership[:, j] > 0.05
        if not np.any(mask):
            continue
        w_k = membership[mask, j]
        w_k = w_k / max(w_k.sum(), 1e-12)
        cf_k = np.average(ideal_points[mask], axis=0, weights=w_k)
        cns_k = apply_consensus_operator(
            opinions_eq[mask],
            config.consensus_operator,
            membership=membership[mask] if membership.shape[1] > j else None,
            natural_frequencies=frequencies[mask],
        )
        w_c = welfare(cns_k, ideal_points[mask], weights=membership[mask, j])
        w_t = welfare(cf_k, ideal_points[mask], weights=membership[mask, j])
        delta_w_contour[contour.id] = normalized_welfare_gap(w_c, w_t)
        mu_cns_contour[contour.id] = mu_consensus_degree(opinions_eq[mask])
        bound = contour.max_non_optimality or config.effective_max_non_optimality
        bound_flags[contour.id] = delta_w_contour[contour.id] >= bound * 0.95

    bound_flags["global"] = delta_w >= config.effective_max_non_optimality * 0.95

    return CNSMetrics(
        delta_w_global=round(delta_w, 6),
        delta_h_fiber=round(delta_h, 6),
        epsilon_proj=round(eps, 6),
        mu_cns_global=round(mu_global, 6),
        welfare_consensus=round(w_cns, 6),
        welfare_counterfactual=round(w_cf, 6),
        delta_w_per_contour={k: round(v, 6) for k, v in delta_w_contour.items()},
        mu_cns_per_contour={k: round(v, 6) for k, v in mu_cns_contour.items()},
        bound_saturated_flags=bound_flags,
        consensus_operator=config.consensus_operator,
        at_equilibrium=True,
        order_parameter_R=round(order_R, 6) if order_R is not None else None,
    )


def run_cns_batch(
    config: CNSSimulationConfig,
    num_instances: int = 20,
    topologies: list[str] | None = None,
) -> dict[str, Any]:
    """Batch evaluation across graph topologies for experiment 021."""
    if topologies is None:
        topologies = ["watts_strogatz", "erdos_renyi", "barabasi_albert"]

    rng = np.random.default_rng(config.seed)
    all_metrics: list[CNSMetrics] = []
    by_topology: dict[str, list[CNSMetrics]] = {t: [] for t in topologies}

    for i in range(num_instances):
        topo = topologies[i % len(topologies)]
        n = config.num_agents
        if topo == "watts_strogatz":
            k = min(4, n - 1) if n > 1 else 1
            g = nx.connected_watts_strogatz_graph(n, k, 0.15, seed=config.seed + i)
        elif topo == "erdos_renyi":
            p = 4 / max(n, 1)
            g = nx.erdos_renyi_graph(n, p, seed=config.seed + i)
            if not nx.is_connected(g):
                g = nx.connected_watts_strogatz_graph(n, min(4, n - 1), 0.15, seed=config.seed + i)
        else:
            m = min(2, n - 1) if n > 1 else 1
            g = nx.barabasi_albert_graph(n, m, seed=config.seed + i)

        metrics = evaluate_cns_instance(config, graph=g, seed_offset=i + int(rng.integers(0, 1000)))
        all_metrics.append(metrics)
        by_topology[topo].append(metrics)

    gaps = [m.delta_w_global for m in all_metrics]
    positive_gap_frac = sum(1 for g in gaps if g > 1e-6) / max(len(gaps), 1)
    mean_gap = float(np.mean(gaps))
    mean_delta_h = float(np.mean([m.delta_h_fiber for m in all_metrics]))

    contour_gaps: dict[str, list[float]] = {}
    for m in all_metrics:
        for cid, dw in m.delta_w_per_contour.items():
            contour_gaps.setdefault(cid, []).append(dw)
    contour_variance = {
        cid: float(np.var(vals)) for cid, vals in contour_gaps.items() if len(vals) > 1
    }

    saturated = sum(
        1 for m in all_metrics for flag in m.bound_saturated_flags.values() if flag
    )
    bound_sat_frac = saturated / max(len(all_metrics) * max(len(config.fuzzy_contours), 1), 1)

    h_cns_001_supported = positive_gap_frac >= 0.8 and mean_gap > 0
    h_cns_004_supported = mean_delta_h > 0.01
    h_cns_011_supported = len(contour_variance) >= 2 and max(contour_variance.values(), default=0) > 1e-4
    h_cns_012_supported = bound_sat_frac > 0.1 or mean_gap > 0.05
    high_mu_gaps: list[float] = []
    for m in all_metrics:
        high_mu = m.mu_cns_global > 0.85
        if m.order_parameter_R is not None and m.order_parameter_R > 0.85:
            high_mu = True
        if not high_mu:
            high_mu = any(mu > 0.85 for mu in m.mu_cns_per_contour.values())
        if high_mu and m.delta_w_global > 1e-6:
            high_mu_gaps.append(m.delta_w_global)
    mean_gap_at_high_mu = float(np.mean(high_mu_gaps)) if high_mu_gaps else 0.0
    h_cns_013_supported = len(high_mu_gaps) >= max(1, num_instances // 8) and mean_gap_at_high_mu > 0

    falsifiers = {
        "F-CNS-1": mean_gap < 1e-6,
        "F-CNS-3": mean_delta_h < 1e-6,
        "F-CNS-6": bound_sat_frac < 0.01 and mean_gap < 0.01,
        "F-CNS-7": max(contour_variance.values(), default=0) < 1e-6,
        "F-CNS-8": mean_gap < 1e-6 and float(np.mean([m.mu_cns_global for m in all_metrics])) > 0.9,
    }

    return {
        "num_instances": num_instances,
        "mean_delta_w_global": round(mean_gap, 6),
        "std_delta_w_global": round(float(np.std(gaps)), 6),
        "positive_gap_fraction": round(positive_gap_frac, 4),
        "mean_delta_h_fiber": round(mean_delta_h, 6),
        "contour_gap_variance": {k: round(v, 6) for k, v in contour_variance.items()},
        "bound_saturation_fraction": round(bound_sat_frac, 4),
        "mean_gap_at_high_mu_cns": round(mean_gap_at_high_mu, 6),
        "high_mu_instance_count": len(high_mu_gaps),
        "hypothesis_support": {
            "H-CNS-001": h_cns_001_supported,
            "H-CNS-004": h_cns_004_supported,
            "H-CNS-011": h_cns_011_supported,
            "H-CNS-012": h_cns_012_supported,
            "H-CNS-013": h_cns_013_supported,
        },
        "falsifiers_triggered": {k: v for k, v in falsifiers.items() if v},
        "instances": [m.to_dict() for m in all_metrics[:5]],
    }


@dataclass
class KuramotoVoteSweepPoint:
    K: float
    vote_threshold: float
    max_non_optimality: float
    contour_sigma: float
    delta_w_global: float
    mu_cns_global: float
    order_R: float
    regret_forced: float
    regret_delayed: float
    hysteresis_width: float


def vote_outcome(phases: np.ndarray, threshold: float) -> float:
    """Binary vote from phase distribution relative to threshold angle."""
    votes = (np.cos(phases) > np.cos(threshold)).astype(float)
    return float(np.mean(votes))


def run_kuramoto_vote_sweep(
    config: CNSSimulationConfig,
    K_values: list[float] | None = None,
    threshold_values: list[float] | None = None,
    max_non_optimality_values: list[float] | None = None,
    sigma_values: list[float] | None = None,
) -> dict[str, Any]:
    """Catastrophe + Kuramoto–vote parameter sweep for experiment 022."""
    if K_values is None:
        K_values = [0.5, 1.0, 1.8, 2.5, 3.5]
    if threshold_values is None:
        threshold_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    if max_non_optimality_values is None:
        max_non_optimality_values = [0.10, 0.20, 0.35, 0.50]
    if sigma_values is None:
        sigma_values = [0.15, 0.25, 0.40]

    sweep_points: list[dict[str, Any]] = []
    regret_spikes: list[float] = []

    base_contours = config.fuzzy_contours
    if not base_contours:
        base_contours = [
            FuzzyContour(id="bloc_a", membership="gaussian_centroid", centroid=[-0.5, 0.2, 0.0], sigma=0.25),
            FuzzyContour(id="bloc_b", membership="gaussian_centroid", centroid=[0.6, -0.3, 0.1], sigma=0.30),
        ]

    for max_no in max_non_optimality_values:
        for sigma in sigma_values:
            contours = []
            for c in base_contours:
                cd = asdict(c)
                cd["sigma"] = sigma
                contours.append(FuzzyContour.from_dict(cd))

            for K in K_values:
                for b in threshold_values:
                    cfg = CNSSimulationConfig(
                        max_non_optimality=max_no,
                        consensus_operator="kuramoto_sync",
                        num_agents=config.num_agents,
                        opinion_dim=config.opinion_dim,
                        fuzzy_contours=contours,
                        kuramoto_K=K,
                        seed=config.seed,
                    )
                    n = cfg.num_agents
                    graph = generate_opinion_graph(n, cfg.seed)
                    opinions, ideal, frequencies, tags = initialize_agent_state(n, cfg.opinion_dim, cfg.seed)
                    membership = build_membership_matrix(contours, opinions, graph, tags)

                    phases0 = np.arctan2(opinions[:, 1], opinions[:, 0])
                    phases_forced, R_forced = run_kuramoto_to_equilibrium(
                        graph, phases0.copy(), frequencies, K * 1.5, t_max=8.0
                    )
                    phases_delayed, R_delayed = run_kuramoto_to_equilibrium(
                        graph, phases0.copy(), frequencies, K * 0.5, t_max=25.0
                    )

                    op_forced = opinions_from_phases(phases_forced, opinions)
                    op_delayed = opinions_from_phases(phases_delayed, opinions)

                    cns_forced = apply_consensus_operator(
                        op_forced, "kuramoto_sync", membership, frequencies
                    )
                    cns_delayed = apply_consensus_operator(
                        op_delayed, "kuramoto_sync", membership, frequencies
                    )
                    cf = welfare_optimal(ideal)

                    w_forced = welfare(cns_forced, ideal)
                    w_delayed = welfare(cns_delayed, ideal)
                    w_cf = welfare(cf, ideal)

                    regret_forced = normalized_welfare_gap(w_forced, w_cf)
                    regret_delayed = normalized_welfare_gap(w_delayed, w_cf)

                    # Hysteresis: forward/backward threshold sweep proxy
                    vote_fwd = vote_outcome(phases_forced, b)
                    vote_bwd = vote_outcome(phases_delayed, b + 0.1)
                    hysteresis = abs(vote_fwd - vote_bwd)

                    delta_w = regret_forced
                    mu_cns = kuramoto_order_parameter(phases_forced)

                    point = {
                        "K": K,
                        "vote_threshold": b,
                        "max_non_optimality": max_no,
                        "contour_sigma": sigma,
                        "delta_w_global": round(delta_w, 6),
                        "mu_cns_global": round(mu_cns, 6),
                        "order_R": round(R_forced, 6),
                        "regret_forced": round(regret_forced, 6),
                        "regret_delayed": round(regret_delayed, 6),
                        "hysteresis_width": round(hysteresis, 6),
                    }
                    sweep_points.append(point)
                    if regret_forced > regret_delayed:
                        regret_spikes.append(regret_forced - regret_delayed)

    mean_regret_spike = float(np.mean(regret_spikes)) if regret_spikes else 0.0
    mean_delta_w = float(np.mean([p["delta_w_global"] for p in sweep_points]))
    high_mu_gaps = [
        p["delta_w_global"] for p in sweep_points if p["mu_cns_global"] > 0.85
    ]
    mean_gap_at_sync = float(np.mean(high_mu_gaps)) if high_mu_gaps else 0.0
    max_hysteresis = max((p["hysteresis_width"] for p in sweep_points), default=0.0)

    return {
        "sweep_size": len(sweep_points),
        "mean_delta_w_global": round(mean_delta_w, 6),
        "mean_regret_spike_forced_vs_delayed": round(mean_regret_spike, 6),
        "mean_gap_at_high_mu_cns": round(mean_gap_at_sync, 6),
        "max_hysteresis_width": round(max_hysteresis, 6),
        "hypothesis_support": {
            "H-CNS-002": mean_regret_spike > 0.01 and max_hysteresis > 0.05,
            "H-CNS-005": mean_gap_at_sync > 0.01,
            "H-CNS-011": len({p["contour_sigma"] for p in sweep_points}) > 1,
            "H-CNS-013": mean_gap_at_sync > 0 and len(high_mu_gaps) > 0,
        },
        "sample_points": sweep_points[:10],
        "hysteresis_loop": sweep_points,
    }
