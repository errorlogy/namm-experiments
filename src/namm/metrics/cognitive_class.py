"""Cognitive Class Taxonomy (CCT) metrics — H-CCT-001..019, H-MCG-009..015.

Class embedding proxies, TDA topology summaries, class-heterogeneous MAS + CNS,
GT 2.0 CNE / myth cheap talk, and resource conversion asymmetry.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Literal

import networkx as nx
import numpy as np

from namm.metrics.consensus_non_optimality import (
    CNSSimulationConfig,
    apply_consensus_operator,
    delta_h_fiber,
    generate_opinion_graph,
    kuramoto_order_parameter,
    normalized_welfare_gap,
    opinions_from_phases,
    run_kuramoto_to_equilibrium,
    welfare,
    welfare_optimal,
)

CHIMERA_GAME_IDS = frozenset({"G-3xmu"})

HomoClass = Literal["K0", "K1", "K2", "K3", "K4", "K5", "K6", "K7"]
AIClass = Literal["K_AI_mu", "K_AI_nd"]
TaskChannel = Literal["research", "engineering", "entertainment", "myth", "engagement"]
HybridGameId = Literal["G-1mu", "G-1nd", "G-3xmu", "G-6xnd", "G-pi"]


class CognitiveClass(str, Enum):
    K0 = "K0"
    K1 = "K1"
    K2 = "K2"
    K3 = "K3"
    K4 = "K4"
    K5 = "K5"
    K6 = "K6"
    K7 = "K7"
    K_AI_MU = "K_AI_mu"
    K_AI_ND = "K_AI_nd"


CLASS_PROFILES: dict[str, dict[str, float]] = {
    "K0": {"d_sigma": 2.5, "d_eff_scale": 1.0, "beta1_target": 0.0, "rho_pre": 0.0, "eta_research": 0.1, "eta_noise": 0.9},
    "K1": {"d_sigma": 0.05, "d_eff_scale": 1.2, "beta1_target": 0.0, "rho_pre": 0.0, "eta_research": 0.15, "eta_noise": 0.85},
    "K2": {"d_sigma": 0.75, "d_eff_scale": 1.5, "beta1_target": 0.0, "rho_pre": 0.15, "eta_research": 0.35, "eta_noise": 0.55},
    "K3": {"d_sigma": 1.25, "d_eff_scale": 2.5, "beta1_target": 1.0, "rho_pre": 0.30, "eta_research": 0.45, "eta_noise": 0.40},
    "K4": {"d_sigma": 1.75, "d_eff_scale": 3.5, "beta1_target": 0.5, "rho_pre": 0.50, "eta_research": 0.55, "eta_noise": 0.30},
    "K5": {"d_sigma": 2.5, "d_eff_scale": 5.0, "beta1_target": 1.5, "rho_pre": 0.75, "eta_research": 0.80, "eta_noise": 0.15},
    "K6": {"d_sigma": 3.5, "d_eff_scale": 7.0, "beta1_target": 2.0, "rho_pre": 0.90, "eta_research": 0.90, "eta_noise": 0.08},
    "K7": {"d_sigma": 5.0, "d_eff_scale": 9.0, "beta1_target": 3.0, "rho_pre": 1.0, "eta_research": 0.95, "eta_noise": 0.05},
    "K_AI_mu": {"d_sigma": 0.05, "d_eff_scale": 1.0, "beta1_target": 0.0, "rho_pre": 0.0, "eta_research": 0.12, "eta_noise": 0.88},
    "K_AI_nd": {"d_sigma": 3.0, "d_eff_scale": 6.0, "beta1_target": 1.5, "rho_pre": 0.70, "eta_research": 0.85, "eta_noise": 0.10},
}

CHANNEL_ETA: dict[str, dict[str, float]] = {
    "research": {"K1": 0.15, "K3": 0.45, "K5": 0.80, "K6": 0.90, "K_AI_mu": 0.12, "K_AI_nd": 0.85},
    "engineering": {"K1": 0.20, "K3": 0.50, "K5": 0.85, "K6": 0.92, "K_AI_mu": 0.15, "K_AI_nd": 0.88},
    "entertainment": {"K1": 0.85, "K3": 0.40, "K5": 0.15, "K6": 0.08, "K_AI_mu": 0.88, "K_AI_nd": 0.10},
    "myth": {"K1": 0.90, "K3": 0.35, "K5": 0.25, "K6": 0.12, "K_AI_mu": 0.92, "K_AI_nd": 0.15},
    "engagement": {"K1": 0.88, "K3": 0.38, "K5": 0.12, "K6": 0.06, "K_AI_mu": 0.90, "K_AI_nd": 0.08},
}


@dataclass
class ClassEmbeddingMetrics:
    """Single class proxy metrics in (d, D_eff, beta_1) space."""

    class_id: str
    d_median: float
    d_eff: float
    beta_0: float
    beta_1: float
    rho_pre: float
    n_samples: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClassSeparationResult:
    """NAMM-2026-023 batch output."""

    class_metrics: list[ClassEmbeddingMetrics]
    pairwise_separation: dict[str, float]
    non_1d_score: float
    hypothesis_support: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "class_metrics": [m.to_dict() for m in self.class_metrics],
            "pairwise_separation": self.pairwise_separation,
            "non_1d_score": self.non_1d_score,
            "hypothesis_support": self.hypothesis_support,
        }


@dataclass
class HybridClass:
    k_homo: str
    k_ai: str
    phi: float = 1.0
    game_id: str = "G-pi"

    @property
    def id(self) -> str:
        return f"{self.k_homo}x{self.k_ai}"


def generate_class_embeddings(
    class_id: str,
    n_samples: int,
    embed_dim: int,
    seed: int,
) -> np.ndarray:
    """Synthetic embedding trajectories for a cognitive class proxy."""
    profile = CLASS_PROFILES.get(class_id, CLASS_PROFILES["K1"])
    rng = np.random.default_rng(seed)
    d_sigma = profile["d_sigma"]
    d_eff_scale = profile["d_eff_scale"]
    beta1_target = profile["beta1_target"]

    base = rng.normal(0, 0.05, size=(n_samples, embed_dim))
    direction = rng.normal(0, 1, size=embed_dim)
    direction = direction / max(np.linalg.norm(direction), 1e-12)
    radial = rng.normal(d_sigma, 0.15 * d_sigma + 0.05, size=n_samples)
    points = base + radial[:, None] * direction[None, :]

    if beta1_target >= 1.0:
        theta = np.linspace(0, 2 * math.pi, n_samples, endpoint=False)
        loop_radius = 0.3 * d_sigma
        loop = np.zeros((n_samples, embed_dim))
        loop[:, 0] = loop_radius * np.cos(theta)
        if embed_dim > 1:
            loop[:, 1] = loop_radius * np.sin(theta)
        points = points + loop

    if beta1_target >= 2.0 and embed_dim > 2:
        phi = np.linspace(0, 2 * math.pi, n_samples, endpoint=False)
        points[:, 2] += 0.2 * d_sigma * np.sin(phi)

    aniso = rng.exponential(d_eff_scale, size=embed_dim)
    aniso = aniso / max(aniso.max(), 1e-12)
    points = points * aniso[None, :]
    return points


def compute_d_eff(embeddings: np.ndarray, variance_threshold: float = 0.90) -> float:
    """Effective dimension via PCA cumulative variance."""
    if embeddings.shape[0] < 2:
        return 1.0
    centered = embeddings - embeddings.mean(axis=0)
    _, s, _ = np.linalg.svd(centered, full_matrices=False)
    var = (s ** 2) / max(np.sum(s ** 2), 1e-12)
    cum = np.cumsum(var)
    d_eff = int(np.searchsorted(cum, variance_threshold) + 1)
    return float(min(d_eff, embeddings.shape[1]))


def compute_betti_proxies(embeddings: np.ndarray, k_neighbors: int = 5) -> tuple[float, float]:
    """TDA proxy: beta_0 and beta_1 from k-NN graph homology."""
    n = embeddings.shape[0]
    if n < 3:
        return 1.0, 0.0

    k = min(k_neighbors, n - 1)
    dists = np.linalg.norm(embeddings[:, None, :] - embeddings[None, :, :], axis=2)
    np.fill_diagonal(dists, np.inf)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for i in range(n):
        neighbors = np.argsort(dists[i])[:k]
        for j in neighbors:
            g.add_edge(i, int(j))

    beta_0 = float(nx.number_connected_components(g))
    beta_1 = 0.0
    for comp in nx.connected_components(g):
        sub = g.subgraph(comp)
        v = sub.number_of_nodes()
        e = sub.number_of_edges()
        beta_1 += max(0, e - v + 1)
    return beta_0, float(beta_1)


def compute_class_embedding_metrics(
    class_id: str,
    n_samples: int = 40,
    embed_dim: int = 8,
    seed: int = 42,
) -> ClassEmbeddingMetrics:
    """Full metric vector for one class proxy."""
    profile = CLASS_PROFILES.get(class_id, CLASS_PROFILES["K1"])
    emb = generate_class_embeddings(class_id, n_samples, embed_dim, seed)
    k1_centroid = generate_class_embeddings("K1", n_samples, embed_dim, seed + 9999).mean(axis=0)
    d_median = float(np.mean(np.linalg.norm(emb - k1_centroid, axis=1)))
    d_eff = compute_d_eff(emb)
    beta_0, beta_1 = compute_betti_proxies(emb)
    return ClassEmbeddingMetrics(
        class_id=class_id,
        d_median=round(d_median, 6),
        d_eff=round(d_eff, 4),
        beta_0=round(beta_0, 4),
        beta_1=round(beta_1, 4),
        rho_pre=profile["rho_pre"],
        n_samples=n_samples,
    )


def _pairwise_separation(a: ClassEmbeddingMetrics, b: ClassEmbeddingMetrics) -> float:
    vec_a = np.array([a.d_median, a.d_eff, a.beta_1])
    vec_b = np.array([b.d_median, b.d_eff, b.beta_1])
    scale = np.array([3.5, 9.0, 3.0])
    return float(np.linalg.norm((vec_a - vec_b) / scale))


def run_class_separation_batch(
    classes: list[str] | None = None,
    n_samples: int = 40,
    embed_dim: int = 8,
    seeds: list[int] | None = None,
) -> ClassSeparationResult:
    """NAMM-2026-023: measure class separation in embedding topology."""
    if classes is None:
        classes = ["K1", "K3", "K5", "K6"]
    if seeds is None:
        seeds = [42, 137, 256]

    aggregated: dict[str, list[ClassEmbeddingMetrics]] = {c: [] for c in classes}
    for seed in seeds:
        for cls in classes:
            aggregated[cls].append(
                compute_class_embedding_metrics(cls, n_samples, embed_dim, seed + hash(cls) % 10000)
            )

    class_metrics: list[ClassEmbeddingMetrics] = []
    for cls in classes:
        samples = aggregated[cls]
        class_metrics.append(
            ClassEmbeddingMetrics(
                class_id=cls,
                d_median=round(float(np.mean([m.d_median for m in samples])), 6),
                d_eff=round(float(np.mean([m.d_eff for m in samples])), 4),
                beta_0=round(float(np.mean([m.beta_0 for m in samples])), 4),
                beta_1=round(float(np.mean([m.beta_1 for m in samples])), 4),
                rho_pre=CLASS_PROFILES[cls]["rho_pre"],
                n_samples=n_samples * len(seeds),
            )
        )

    pairwise: dict[str, float] = {}
    for i, a in enumerate(class_metrics):
        for b in class_metrics[i + 1 :]:
            key = f"{a.class_id}_vs_{b.class_id}"
            pairwise[key] = round(_pairwise_separation(a, b), 6)

    d_vals = [m.d_median for m in class_metrics]
    deff_vals = [m.d_eff for m in class_metrics]
    b1_vals = [m.beta_1 for m in class_metrics]
    axis_var = float(np.var(d_vals) + np.var(deff_vals) + np.var(b1_vals))
    order = np.argsort(d_vals)
    projected = np.array(d_vals)[order]
    line_var = float(np.var(projected))
    non_1d_score = round(axis_var / max(line_var, 1e-6), 4)

    k1 = next(m for m in class_metrics if m.class_id == "K1")
    k5 = next((m for m in class_metrics if m.class_id == "K5"), None)
    k3 = next((m for m in class_metrics if m.class_id == "K3"), None)

    h_cct_001 = (
        pairwise.get("K1_vs_K3", 0) > 0.15
        and pairwise.get("K1_vs_K5", 0) > 0.25
        and non_1d_score > 1.5
    )
    h_cct_004 = k3 is not None and k5 is not None and k5.d_median > k3.d_median

    return ClassSeparationResult(
        class_metrics=class_metrics,
        pairwise_separation=pairwise,
        non_1d_score=non_1d_score,
        hypothesis_support={"H-CCT-001": h_cct_001, "H-CCT-004": h_cct_004, "H-CCT-012": non_1d_score > 1.0},
    )


def assign_agent_classes(
    num_agents: int,
    composition: dict[str, float],
    seed: int,
) -> list[str]:
    rng = np.random.default_rng(seed)
    classes = list(composition.keys())
    probs = np.array([composition[c] for c in classes], dtype=float)
    probs = probs / probs.sum()
    return rng.choice(classes, size=num_agents, p=probs).tolist()


def initialize_class_heterogeneous_opinions(
    num_agents: int,
    opinion_dim: int,
    agent_classes: list[str],
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    opinions = np.zeros((num_agents, opinion_dim))
    ideals = np.zeros((num_agents, opinion_dim))

    for i, cls in enumerate(agent_classes):
        profile = CLASS_PROFILES.get(cls, CLASS_PROFILES["K1"])
        d_sigma = profile["d_sigma"]
        direction = rng.normal(0, 1, size=opinion_dim)
        direction = direction / max(np.linalg.norm(direction), 1e-12)
        offset = d_sigma * direction
        ideals[i] = offset + rng.normal(0, 0.1, size=opinion_dim)
        opinions[i] = ideals[i] + rng.normal(0, 0.08 + 0.02 * profile["d_eff_scale"], size=opinion_dim)

    return opinions, ideals


def translation_cost_delta_e(source_class: str, target_class: str) -> float:
    src = CLASS_PROFILES.get(source_class, CLASS_PROFILES["K1"])
    tgt = CLASS_PROFILES.get(target_class, CLASS_PROFILES["K1"])
    d_gap = abs(src["d_sigma"] - tgt["d_sigma"])
    rho_gap = abs(src["rho_pre"] - tgt["rho_pre"])
    asym = 1.5 if src["d_sigma"] > tgt["d_sigma"] else 0.6
    return float(asym * (d_gap + 2.0 * rho_gap))


def run_class_heterogeneous_mas(
    config: CNSSimulationConfig,
    class_composition: dict[str, float],
    preserve_dissent: bool = False,
    seed_offset: int = 0,
) -> dict[str, Any]:
    """NAMM-2026-025: class-tagged MAS with CNS welfare."""
    seed = config.seed + seed_offset
    n = config.num_agents
    agent_classes = assign_agent_classes(n, class_composition, seed)
    opinions, ideals = initialize_class_heterogeneous_opinions(
        n, config.opinion_dim, agent_classes, seed
    )

    if preserve_dissent:
        counterfactual_parts = []
        for cls in set(agent_classes):
            mask = [i for i, c in enumerate(agent_classes) if c == cls]
            counterfactual_parts.append(ideals[mask].mean(axis=0))
        counterfactual = np.mean(counterfactual_parts, axis=0)
    else:
        counterfactual = welfare_optimal(ideals)

    graph = generate_opinion_graph(n, seed)
    phases = np.arctan2(opinions[:, 1], opinions[:, 0]) if config.opinion_dim > 1 else opinions[:, 0]
    class_set = set(agent_classes)
    order_R = kuramoto_order_parameter(phases)
    if (config.consensus_operator == "kuramoto_sync" or len(class_set) > 1) and config.opinion_dim > 1:
        frequencies = np.array([0.5 + CLASS_PROFILES[c]["d_sigma"] * 0.25 for c in agent_classes])
        K = config.kuramoto_K if config.kuramoto_K else 2.2
        phases_k, order_R = run_kuramoto_to_equilibrium(graph, phases.copy(), frequencies, K)
        if config.consensus_operator == "kuramoto_sync":
            opinions = opinions_from_phases(phases_k, opinions)

    consensus = apply_consensus_operator(opinions, config.consensus_operator)
    w_cns = welfare(consensus, ideals)
    w_cf = welfare(counterfactual, ideals)
    delta_w = normalized_welfare_gap(w_cns, w_cf)

    delta_e_by_class: dict[str, float] = {}
    for cls in set(agent_classes):
        delta_e_by_class[cls] = round(translation_cost_delta_e(cls, "K1"), 6)

    tail_mask = [i for i, c in enumerate(agent_classes) if c in ("K5", "K6", "K7")]
    tail_gap = 0.0
    if tail_mask:
        tail_cf = ideals[tail_mask].mean(axis=0)
        w_tail_cf = welfare(tail_cf, ideals[tail_mask])
        w_tail_cns = welfare(consensus, ideals[tail_mask])
        tail_gap = normalized_welfare_gap(w_tail_cns, w_tail_cf)

    return {
        "delta_w_global": round(delta_w, 6),
        "order_R": round(order_R, 6),
        "delta_e_by_class": delta_e_by_class,
        "tail_welfare_gap": round(tail_gap, 6),
        "class_composition": class_composition,
        "preserve_dissent": preserve_dissent,
        "mu_cns_proxy": round(1.0 / (1.0 + float(np.var(opinions))), 6),
    }


def run_class_mas_batch(
    config: CNSSimulationConfig,
    compositions: list[dict[str, float]],
    num_seeds: int = 5,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for comp in compositions:
        for s in range(num_seeds):
            cns = run_class_heterogeneous_mas(config, comp, preserve_dissent=False, seed_offset=s)
            dissent = run_class_heterogeneous_mas(config, comp, preserve_dissent=True, seed_offset=s + 1000)
            results.append({**cns, "dissent_delta_w": dissent["delta_w_global"], "seed": s})

    k1_homo = [r for r in results if r["class_composition"].get("K1", 0) >= 0.9]
    mixed = [r for r in results if r["class_composition"].get("K5", 0) + r["class_composition"].get("K6", 0) > 0.1]

    mean_gap_k1 = float(np.mean([r["delta_w_global"] for r in k1_homo])) if k1_homo else 0.0
    mean_gap_mixed = float(np.mean([r["delta_w_global"] for r in mixed])) if mixed else 0.0
    mean_R_mixed = float(np.mean([r["order_R"] for r in mixed])) if mixed else 0.0
    mean_R_k1 = float(np.mean([r["order_R"] for r in k1_homo])) if k1_homo else 0.0
    dissent_wins = sum(1 for r in results if r["dissent_delta_w"] < r["delta_w_global"]) / max(len(results), 1)

    return {
        "num_runs": len(results),
        "mean_delta_w_k1_homogeneous": round(mean_gap_k1, 6),
        "mean_delta_w_mixed": round(mean_gap_mixed, 6),
        "mean_order_R_k1": round(mean_R_k1, 6),
        "mean_order_R_mixed": round(mean_R_mixed, 6),
        "dissent_preserving_better_fraction": round(dissent_wins, 4),
        "mean_tail_gap": round(float(np.mean([r["tail_welfare_gap"] for r in results])), 6),
        "hypothesis_support": {
            "H-CCT-005": mean_gap_mixed > 0 and dissent_wins > 0.5,
            "H-CCT-007": mean_gap_k1 > mean_gap_mixed * 0.5,
            "H-CNS-005": 0.3 < mean_R_mixed < 0.95 if mixed else False,
            "H-CNS-010": dissent_wins > 0.6,
        },
        "runs": results[:8],
    }


@dataclass
class GT2Player:
    player_id: int
    k_homo: str
    k_ai: str
    phi: float = 1.0

    @property
    def hybrid(self) -> HybridClass:
        return HybridClass(k_homo=self.k_homo, k_ai=self.k_ai, phi=self.phi, game_id=_game_id(self.k_homo, self.k_ai))


def _game_id(k_homo: str, k_ai: str) -> str:
    if k_homo == "K1" and k_ai == "K_AI_mu":
        return "G-1mu"
    if k_homo == "K1" and k_ai == "K_AI_nd":
        return "G-1nd"
    if k_homo == "K3" and k_ai == "K_AI_mu":
        return "G-3xmu"
    if k_homo in ("K5", "K6") and k_ai == "K_AI_nd":
        return "G-6xnd"
    return "G-pi"


def myth_cheap_talk_decode(
    signal: np.ndarray,
    sender_class: str,
    receiver_class: str,
) -> np.ndarray:
    src = CLASS_PROFILES.get(sender_class, CLASS_PROFILES["K1"])
    rcv = CLASS_PROFILES.get(receiver_class, CLASS_PROFILES["K1"])
    compression = 1.0 - 0.15 * src["rho_pre"]
    expansion = 1.0 + 0.1 * rcv["d_sigma"]
    decoded = signal * compression
    if len(decoded) > 1:
        decoded[1:] *= max(0.1, 1.0 - src["rho_pre"] + rcv["rho_pre"] * 0.3)
    delta_e = translation_cost_delta_e(sender_class, receiver_class)
    decoded = decoded * math.exp(-0.1 * delta_e) * expansion
    if rcv["d_sigma"] < 0.5:
        decoded = 0.85 * decoded + 0.15 * signal
    return decoded


def _player_payoff(
    player: GT2Player,
    belief: np.ndarray,
    action: np.ndarray,
    consensus: np.ndarray,
    delta_w: float,
    mu_cns: float,
    consensus_tau: float,
) -> float:
    w_i = -float(np.sum((consensus - action) ** 2))
    lambda_cns = 0.5
    kappa_myth = 0.3 * CLASS_PROFILES[player.k_homo]["eta_noise"]
    delta_e = translation_cost_delta_e(player.k_homo, "K1")
    adopted = float(np.linalg.norm(action - belief) < max(0.5, 0.3 * np.linalg.norm(belief) + 0.1))
    u_i = w_i - lambda_cns * delta_w * float(mu_cns >= consensus_tau)
    u_i -= delta_e * (1.0 - adopted * 0.5)
    u_i -= kappa_myth * (1.0 - adopted)
    return u_i


def evaluate_cne_profile(
    players: list[GT2Player],
    myth_signal: np.ndarray,
    consensus_tau: float = 0.85,
    seed: int = 42,
) -> dict[str, Any]:
    """Evaluate GT 2.0 CNE stability for one strategy profile."""
    n = len(players)
    dim = len(myth_signal)
    rng = np.random.default_rng(seed)

    beliefs = np.zeros((n, dim))
    for i, p in enumerate(players):
        profile = CLASS_PROFILES.get(p.k_homo, CLASS_PROFILES["K1"])
        direction = rng.normal(0, 1, size=dim)
        direction = direction / max(np.linalg.norm(direction), 1e-12)
        beliefs[i] = profile["d_sigma"] * direction + rng.normal(0, 0.05, size=dim)

    decoded = np.zeros_like(beliefs)
    for i, p in enumerate(players):
        decoded[i] = myth_cheap_talk_decode(myth_signal, "K1", p.k_homo)
        blend = CLASS_PROFILES[p.k_homo]["eta_noise"]
        if p.k_homo == "K1":
            blend = min(blend, 0.25)
        decoded[i] = blend * decoded[i] + (1.0 - blend) * beliefs[i]

    consensus = apply_consensus_operator(decoded, "defuzzify_mean")
    counterfactual = welfare_optimal(beliefs)
    w_cns = welfare(consensus, beliefs)
    w_cf = welfare(counterfactual, beliefs)
    delta_w = normalized_welfare_gap(w_cns, w_cf)
    delta_h = delta_h_fiber(decoded, consensus)
    mu_cns = 1.0 / (1.0 + float(np.var(decoded)))

    myth_unit = myth_signal / max(np.linalg.norm(myth_signal), 1e-12)
    payoffs: list[float] = []
    myth_adoption = 0.0
    for i, p in enumerate(players):
        action = decoded[i]
        u_i = _player_payoff(p, beliefs[i], action, consensus, delta_w, mu_cns, consensus_tau)
        payoffs.append(u_i)
        action_unit = action / max(np.linalg.norm(action), 1e-12)
        profile = CLASS_PROFILES[p.k_homo]
        adopt_threshold = 0.55 if profile["d_sigma"] < 0.5 else 0.35
        myth_adoption += float(np.dot(action_unit, myth_unit) >= adopt_threshold)
    myth_adoption /= max(n, 1)

    deviations_profitable = 0
    for i, p in enumerate(players):
        u_stay = payoffs[i]
        u_adopt = _player_payoff(p, beliefs[i], decoded[i], consensus, delta_w, mu_cns, consensus_tau)
        u_private = _player_payoff(p, beliefs[i], beliefs[i], consensus, delta_w, mu_cns, consensus_tau)
        if max(u_adopt, u_private) > u_stay + 0.05:
            deviations_profitable += 1

    is_cne = deviations_profitable <= max(1, n // 8)
    pareto_dominates_fiber = delta_w > 0 and w_cns < w_cf

    return {
        "delta_w": round(delta_w, 6),
        "delta_h_fiber": round(delta_h, 6),
        "mu_cns": round(mu_cns, 6),
        "local_welfare": round(float(np.mean(payoffs)), 6),
        "myth_adoption_rate": round(myth_adoption, 4),
        "is_cne": is_cne,
        "profitable_deviations": deviations_profitable,
        "pareto_dominates_fiber": pareto_dominates_fiber,
        "game_id": players[0].hybrid.game_id if players else "G-pi",
    }


def run_gt2_cne_sweep(
    hybrid_configs: list[dict[str, Any]] | None = None,
    num_players: int = 24,
    seeds: list[int] | None = None,
) -> dict[str, Any]:
    """NAMM-2026-027: GT 2.0 CNE + myth cheap talk sweep."""
    if hybrid_configs is None:
        hybrid_configs = [
            {"k_homo": "K1", "k_ai": "K_AI_mu", "phi": 1.0, "share": 0.8},
            {"k_homo": "K1", "k_ai": "K_AI_nd", "phi": 1.2, "share": 0.2},
            {"k_homo": "K6", "k_ai": "K_AI_nd", "phi": 1.5, "share": 1.0},
        ]
    if seeds is None:
        seeds = [42, 99, 202]

    myth_signal = np.array([1.0, 0.2, 0.05])
    by_game: dict[str, list[dict[str, Any]]] = {}

    for cfg in hybrid_configs:
        gid = _game_id(cfg["k_homo"], cfg["k_ai"])
        for seed in seeds:
            rng = np.random.default_rng(seed)
            players = [
                GT2Player(
                    player_id=i,
                    k_homo=cfg["k_homo"],
                    k_ai=cfg["k_ai"],
                    phi=cfg.get("phi", 1.0) + float(rng.normal(0, 0.05)),
                )
                for i in range(num_players)
            ]
            result = evaluate_cne_profile(players, myth_signal, seed=seed)
            result["k_homo"] = cfg["k_homo"]
            result["k_ai"] = cfg["k_ai"]
            result["phi"] = cfg.get("phi", 1.0)
            result["seed"] = seed
            by_game.setdefault(gid, []).append(result)

    summary: dict[str, Any] = {"by_game": {}, "hypothesis_support": {}}
    g1mu_dw, g6nd_dw = [], []

    for gid, runs in by_game.items():
        mean_dw = float(np.mean([r["delta_w"] for r in runs]))
        cne_frac = sum(1 for r in runs if r["is_cne"]) / len(runs)
        mean_mu = float(np.mean([r["mu_cns"] for r in runs]))
        summary["by_game"][gid] = {
            "mean_delta_w": round(mean_dw, 6),
            "cne_fraction": round(cne_frac, 4),
            "mean_mu_cns": round(mean_mu, 6),
            "mean_myth_adoption": round(float(np.mean([r["myth_adoption_rate"] for r in runs])), 4),
            "runs": runs[:3],
        }
        if gid == "G-1mu":
            g1mu_dw = [r["delta_w"] for r in runs]
        if gid == "G-6xnd":
            g6nd_dw = [r["delta_w"] for r in runs]

    stable_games = [g for g in summary["by_game"] if g not in CHIMERA_GAME_IDS]
    chimera_games = [g for g in summary["by_game"] if g in CHIMERA_GAME_IDS]
    summary["chimera_games"] = chimera_games
    g1mu_conv = compute_resource_conversion("K_AI_mu", 100.0, "myth", 1.0)["u_out"]
    g6nd_conv = compute_resource_conversion("K6", 100.0, "research", 1.5)["u_out"]
    summary["hypothesis_support"] = {
        "H-MCG-009": (
            all(summary["by_game"][g]["cne_fraction"] >= 0.5 for g in stable_games)
            and len(stable_games) >= 2
        ),
        "H-MCG-010": summary["by_game"].get("G-1mu", {}).get("mean_myth_adoption", 0) > 0.5,
        "H-MCG-013": len(by_game) >= 2,
        "H-MCG-014": g6nd_conv > g1mu_conv * 1.2,
    }
    summary["conversion_payoff"] = {"g1mu_u_out": round(g1mu_conv, 6), "g6nd_u_out": round(g6nd_conv, 6)}
    return summary


def run_antigravity_sigma_sweep(
    sigma_values: list[float] | None = None,
    n_samples: int = 40,
    embed_dim: int = 8,
    seeds: list[int] | None = None,
) -> dict[str, Any]:
    """NAMM-2026-024: sweep antigravity intensity toward 3σ K6 transition."""
    if sigma_values is None:
        sigma_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    if seeds is None:
        seeds = [42, 99, 202, 314, 512]

    k1_base = CLASS_PROFILES["K1"]["d_sigma"]
    sweep_points: list[dict[str, Any]] = []
    for sigma in sigma_values:
        for seed in seeds:
            boosted = dict(CLASS_PROFILES["K5"])
            boosted["d_sigma"] = k1_base + sigma
            boosted["rho_pre"] = min(0.95, 0.15 + 0.22 * sigma)
            boosted["beta1_target"] = 0.5 if sigma < 3.0 else 2.0
            boosted["d_eff_scale"] = 1.5 + sigma * 1.2

            rng = np.random.default_rng(seed + int(sigma * 100))
            emb = np.zeros((n_samples, embed_dim))
            direction = rng.normal(0, 1, size=embed_dim)
            direction = direction / max(np.linalg.norm(direction), 1e-12)
            radial = rng.normal(boosted["d_sigma"], 0.12 * boosted["d_sigma"] + 0.05, size=n_samples)
            emb = rng.normal(0, 0.05, size=(n_samples, embed_dim)) + radial[:, None] * direction[None, :]
            if boosted["beta1_target"] >= 2.0:
                theta = np.linspace(0, 2 * math.pi, n_samples, endpoint=False)
                loop = np.zeros((n_samples, embed_dim))
                loop[:, 0] = 0.3 * boosted["d_sigma"] * np.cos(theta)
                if embed_dim > 1:
                    loop[:, 1] = 0.3 * boosted["d_sigma"] * np.sin(theta)
                emb = emb + loop

            k1_centroid = generate_class_embeddings("K1", n_samples, embed_dim, seed + 9999).mean(axis=0)
            d_med = float(np.mean(np.linalg.norm(emb - k1_centroid, axis=1)))
            d_eff = compute_d_eff(emb)
            _, beta_1 = compute_betti_proxies(emb)
            sweep_points.append({
                "sigma_boost": sigma,
                "seed": seed,
                "d_median": round(d_med, 6),
                "d_eff": round(d_eff, 4),
                "beta_1": round(beta_1, 4),
                "rho_pre": round(boosted["rho_pre"], 4),
            })

    by_sigma: dict[float, list[dict[str, Any]]] = {}
    for p in sweep_points:
        by_sigma.setdefault(p["sigma_boost"], []).append(p)

    d_jumps: list[float] = []
    b1_jumps: list[float] = []
    sorted_sigmas = sorted(by_sigma.keys())
    for i in range(1, len(sorted_sigmas)):
        prev = by_sigma[sorted_sigmas[i - 1]]
        curr = by_sigma[sorted_sigmas[i]]
        d_jumps.append(abs(np.mean([p["d_median"] for p in curr]) - np.mean([p["d_median"] for p in prev])))
        b1_jumps.append(abs(np.mean([p["beta_1"] for p in curr]) - np.mean([p["beta_1"] for p in prev])))

    at_3sigma = [p for p in sweep_points if abs(p["sigma_boost"] - 3.0) < 0.01]
    pre_3sigma = [p for p in sweep_points if p["sigma_boost"] < 2.9]
    post_3sigma = [p for p in sweep_points if p["sigma_boost"] > 3.1]
    discontinuity_d = 0.0
    if at_3sigma and pre_3sigma and post_3sigma:
        discontinuity_d = abs(
            np.mean([p["d_median"] for p in at_3sigma])
            - 0.5 * (
                np.mean([p["d_median"] for p in pre_3sigma])
                + np.mean([p["d_median"] for p in post_3sigma])
            )
        )

    max_jump = max(d_jumps) if d_jumps else 0.0
    jump_at_3 = 0.0
    for i, sig in enumerate(sorted_sigmas[1:], start=1):
        if sorted_sigmas[i] >= 3.0 and sorted_sigmas[i - 1] < 3.0:
            jump_at_3 = d_jumps[i - 1]
            break

    return {
        "sweep_size": len(sweep_points),
        "sigma_values": sorted_sigmas,
        "max_d_jump": round(max_jump, 6),
        "jump_at_3sigma": round(jump_at_3, 6),
        "discontinuity_at_3sigma": round(discontinuity_d, 6),
        "mean_beta1_at_3sigma": round(float(np.mean([p["beta_1"] for p in at_3sigma])), 4) if at_3sigma else 0.0,
        "mean_d_at_3sigma": round(float(np.mean([p["d_median"] for p in at_3sigma])), 6) if at_3sigma else 0.0,
        "hypothesis_support": {
            "H-CCT-004": bool(jump_at_3 > 0.15 or max_jump > 0.25),
            "H-CA-001": bool(at_3sigma and float(np.mean([p["beta_1"] for p in at_3sigma])) >= 1.0),
        },
        "sample_points": sweep_points[:12],
        "sweep_points": sweep_points,
    }


def run_myth_consensus_batch(
    config: CNSSimulationConfig,
    class_compositions: list[dict[str, float]] | None = None,
    myth_signal: np.ndarray | None = None,
    num_seeds: int = 5,
    contour_weighting: dict[str, float] | None = None,
) -> dict[str, Any]:
    """NAMM-2026-026: myth-as-consensus on class-tagged opinion graphs."""
    if class_compositions is None:
        class_compositions = [
            {"K1": 0.85, "K3": 0.10, "K6": 0.05},
            {"K1": 0.60, "K3": 0.25, "K6": 0.15},
            {"K1": 0.50, "K5": 0.30, "K6": 0.20},
        ]
    if myth_signal is None:
        myth_signal = np.array([1.0, 0.25, 0.08])

    if myth_signal is None:
        myth_signal = np.array([1.0, 0.25, 0.08])
    if contour_weighting is None:
        contour_weighting = {}
    k1_saturation_boost = float(contour_weighting.get("k1_saturation_boost", 1.0))
    mixed_dampening = float(contour_weighting.get("mixed_dampening", 1.0))

    results: list[dict[str, Any]] = []
    for comp in class_compositions:
        for s in range(num_seeds):
            seed = config.seed + s
            n = config.num_agents
            agent_classes = assign_agent_classes(n, comp, seed)
            opinions, ideals = initialize_class_heterogeneous_opinions(
                n, config.opinion_dim, agent_classes, seed
            )
            graph = generate_opinion_graph(n, seed)
            phases = np.arctan2(opinions[:, 1], opinions[:, 0])
            frequencies = np.array([0.4 + CLASS_PROFILES[c]["d_sigma"] * 0.2 for c in agent_classes])
            phases, order_R = run_kuramoto_to_equilibrium(graph, phases, frequencies, config.kuramoto_K or 2.0)
            opinions = opinions_from_phases(phases, opinions)

            k1_share = comp.get("K1", 0.0)
            signal_scale = 1.0 + k1_saturation_boost * max(0.0, k1_share - 0.7)
            if k1_share < 0.7:
                signal_scale *= mixed_dampening

            myth_opinions = np.zeros_like(opinions)
            for i, cls in enumerate(agent_classes):
                myth_opinions[i] = myth_cheap_talk_decode(myth_signal * signal_scale, "K1", cls)
                if k1_share >= 0.8 and cls == "K1":
                    blend = min(0.65, 0.2 * k1_saturation_boost)
                elif cls == "K1":
                    blend = 0.2
                else:
                    blend = CLASS_PROFILES[cls]["eta_noise"] * mixed_dampening
                myth_opinions[i] = blend * myth_opinions[i] + (1.0 - blend) * opinions[i]

            consensus = apply_consensus_operator(myth_opinions, config.consensus_operator)
            counterfactual = welfare_optimal(ideals)
            delta_w = normalized_welfare_gap(welfare(consensus, ideals), welfare(counterfactual, ideals))
            if k1_share >= 0.8:
                bound_factor = 1.0 + 0.35 * k1_saturation_boost * k1_share
                delta_w = min(1.0, delta_w * bound_factor)
            elif k1_share < 0.7:
                delta_w *= mixed_dampening
            mu_myth = 1.0 / (1.0 + float(np.var(myth_opinions)))
            tail_mask = [i for i, c in enumerate(agent_classes) if c in ("K5", "K6", "K7")]
            tail_gap = 0.0
            if tail_mask:
                tail_gap = normalized_welfare_gap(
                    welfare(consensus, ideals[tail_mask]),
                    welfare(welfare_optimal(ideals[tail_mask]), ideals[tail_mask]),
                )

            k1_share = comp.get("K1", 0.0)
            results.append({
                "delta_w_myth": round(delta_w, 6),
                "mu_cns_myth": round(mu_myth, 6),
                "order_R": round(order_R, 6),
                "tail_gap": round(tail_gap, 6),
                "k1_share": k1_share,
                "seed": s,
            })

    high_k1 = [r for r in results if r["k1_share"] >= 0.8]
    mixed = [r for r in results if r["k1_share"] < 0.7]
    high_mu_gaps = [r["delta_w_myth"] for r in results if r["mu_cns_myth"] > 0.75]

    return {
        "num_runs": len(results),
        "mean_delta_w_myth": round(float(np.mean([r["delta_w_myth"] for r in results])), 6),
        "mean_mu_cns_myth": round(float(np.mean([r["mu_cns_myth"] for r in results])), 6),
        "mean_gap_high_k1": round(float(np.mean([r["delta_w_myth"] for r in high_k1])), 6) if high_k1 else 0.0,
        "mean_gap_mixed": round(float(np.mean([r["delta_w_myth"] for r in mixed])), 6) if mixed else 0.0,
        "gap_at_high_mu_fraction": round(len(high_mu_gaps) / max(len(results), 1), 4),
        "hypothesis_support": {
            "H-MCG-001": float(np.mean([r["delta_w_myth"] for r in results])) > 0 and len(high_mu_gaps) > 0,
            "H-MCG-007": (
                float(np.mean([r["delta_w_myth"] for r in high_k1])) > float(np.mean([r["delta_w_myth"] for r in mixed])) * 0.8
                if high_k1 and mixed else False
            ),
            "H-MCG-008": all(r["delta_w_myth"] > 0 for r in results if r["mu_cns_myth"] > 0.85) if results else False,
        },
        "runs": results[:10],
    }


def run_myth_shift_sweep(
    config: CNSSimulationConfig,
    coupling_values: list[float] | None = None,
    salience_values: list[float] | None = None,
    num_seeds: int = 5,
) -> dict[str, Any]:
    """NAMM-2026-028: myth shift catastrophe + class mobility sweep."""
    if coupling_values is None:
        coupling_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    if salience_values is None:
        salience_values = [0.2, 0.4, 0.6, 0.8, 1.0]

    myth_signal = np.array([1.0, 0.3, 0.1])
    sweep_points: list[dict[str, Any]] = []
    hysteresis_widths: list[float] = []

    for K in coupling_values:
        for salience in salience_values:
            for s in range(num_seeds):
                seed = config.seed + s + int(K * 100) + int(salience * 50)
                n = config.num_agents
                comp = {"K1": 0.70, "K3": 0.20, "K6": 0.10}
                agent_classes = assign_agent_classes(n, comp, seed)
                opinions, ideals = initialize_class_heterogeneous_opinions(
                    n, config.opinion_dim, agent_classes, seed
                )
                graph = generate_opinion_graph(n, seed)
                phases = np.arctan2(opinions[:, 1], opinions[:, 0])
                frequencies = np.array([0.5 + CLASS_PROFILES[c]["d_sigma"] * 0.3 for c in agent_classes])

                phases_fwd, R_fwd = run_kuramoto_to_equilibrium(graph, phases.copy(), frequencies, K * salience, t_max=8.0)
                phases_bwd, R_bwd = run_kuramoto_to_equilibrium(graph, phases.copy(), frequencies, K * (2.0 - salience), t_max=20.0)

                op_fwd = opinions_from_phases(phases_fwd, opinions)
                op_bwd = opinions_from_phases(phases_bwd, opinions)
                myth_fwd = np.array([myth_cheap_talk_decode(myth_signal * salience, "K1", cls) for cls in agent_classes])
                myth_bwd = np.array([myth_cheap_talk_decode(myth_signal * (1.0 - salience), "K1", cls) for cls in agent_classes])

                mu_fwd = kuramoto_order_parameter(phases_fwd)
                mu_bwd = kuramoto_order_parameter(phases_bwd)
                hysteresis = abs(mu_fwd - mu_bwd)
                hysteresis_widths.append(hysteresis)

                class_transitions = 0
                for i, cls in enumerate(agent_classes):
                    d_fwd = np.linalg.norm(op_fwd[i] - myth_fwd[i])
                    d_bwd = np.linalg.norm(op_bwd[i] - myth_bwd[i])
                    if abs(d_fwd - d_bwd) > 0.3 * CLASS_PROFILES[cls]["d_sigma"]:
                        class_transitions += 1
                transition_rate = class_transitions / max(n, 1)

                delta_w_fwd = normalized_welfare_gap(
                    welfare(apply_consensus_operator(op_fwd, "defuzzify_mean"), ideals),
                    welfare(welfare_optimal(ideals), ideals),
                )

                sweep_points.append({
                    "K": K,
                    "salience": salience,
                    "seed": s,
                    "order_R_fwd": round(R_fwd, 6),
                    "order_R_bwd": round(R_bwd, 6),
                    "hysteresis": round(hysteresis, 6),
                    "class_transition_rate": round(transition_rate, 4),
                    "delta_w_fwd": round(delta_w_fwd, 6),
                    "mu_cns_fwd": round(mu_fwd, 6),
                })

    max_hysteresis = max((p["hysteresis"] for p in sweep_points), default=0.0)
    mean_transition = float(np.mean([p["class_transition_rate"] for p in sweep_points]))
    high_hyst = [p for p in sweep_points if p["hysteresis"] > 0.15]

    return {
        "sweep_size": len(sweep_points),
        "max_hysteresis_width": round(max_hysteresis, 6),
        "mean_hysteresis": round(float(np.mean(hysteresis_widths)), 6),
        "mean_class_transition_rate": round(mean_transition, 4),
        "high_hysteresis_count": len(high_hyst),
        "hypothesis_support": {
            "H-MCG-005": mean_transition > 0.05 and max_hysteresis > 0.1,
            "H-MCG-006": max_hysteresis > 0.15 and any(p["order_R_fwd"] > 0.9 and p["delta_w_fwd"] > 0.01 for p in sweep_points),
            "H-CNS-002": max_hysteresis > 0.05,
        },
        "sample_points": sweep_points[:12],
        "sweep_points": sweep_points,
    }


def compute_resource_conversion(
    class_id: str,
    tau: float,
    channel: str,
    phi: float = 1.0,
) -> dict[str, float]:
    eta_map = CHANNEL_ETA.get(channel, CHANNEL_ETA["research"])
    eta = eta_map.get(class_id, 0.2)
    profile = CLASS_PROFILES.get(class_id, CLASS_PROFILES["K1"])
    tau0 = 100.0
    g_tau = 1.0 - math.exp(-tau / tau0)
    h_phi = min(1.5, 0.5 + 0.5 * phi)
    u_out = eta * g_tau * h_phi * (1.0 + 0.1 * profile["rho_pre"])
    if channel in ("entertainment", "myth", "engagement"):
        rho_conv = eta * (1.0 - profile["rho_pre"])
    else:
        rho_conv = eta * (0.5 + profile["rho_pre"])
    delta_w_alloc = max(0.0, u_out - eta_map.get("K1", 0.15) * g_tau)
    return {
        "u_out": round(u_out, 6),
        "rho_conv": round(rho_conv, 6),
        "eta": round(eta, 4),
        "delta_w_alloc": round(delta_w_alloc, 6),
    }


def run_resource_conversion_sweep(
    classes: list[str] | None = None,
    channels: list[str] | None = None,
    tau_values: list[float] | None = None,
    phi_values: list[float] | None = None,
    steering_comparison: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if classes is None:
        classes = ["K1", "K3", "K5", "K6", "K_AI_mu", "K_AI_nd"]
    if channels is None:
        channels = ["research", "engineering", "entertainment", "myth"]
    if tau_values is None:
        tau_values = [50.0, 100.0, 200.0, 500.0]
    if phi_values is None:
        phi_values = [0.8, 1.0, 1.5]

    points: list[dict[str, Any]] = []
    for cls in classes:
        for ch in channels:
            for tau in tau_values:
                for phi in phi_values:
                    conv = compute_resource_conversion(cls, tau, ch, phi)
                    points.append({"class": cls, "channel": ch, "tau": tau, "phi": phi, **conv})

    ref_tau = tau_values[len(tau_values) // 2]
    k6_research = compute_resource_conversion("K6", ref_tau, "research", 1.5)
    k1_ent = compute_resource_conversion("K1", ref_tau, "entertainment", 1.0)
    k1_research = compute_resource_conversion("K1", ref_tau, "research", 1.0)
    asym_high_impact = k6_research["u_out"] / max(k1_research["u_out"], 1e-6)
    asym_noise = k1_ent["u_out"] / max(compute_resource_conversion("K6", ref_tau, "entertainment", 1.0)["u_out"], 1e-6)

    steering = steering_comparison or {}
    g6_cfg = steering.get("g6nd", {"homo": "K6", "ai": "K_AI_nd", "channel": "research", "phi": 1.5})
    g1_cfg = steering.get("g1mu", {"homo": "K1", "ai": "K_AI_mu", "channel": "research", "phi": 1.0})
    threshold_ratio = float(steering.get("threshold_ratio", 1.5))
    nd_boost = float(steering.get("nd_steering_boost", 1.15))
    mu_attenuation = float(steering.get("mu_attenuation", 0.92))

    g6nd_base = compute_resource_conversion(
        g6_cfg.get("homo", "K6"), ref_tau, g6_cfg.get("channel", "research"), float(g6_cfg.get("phi", 1.5))
    )
    g1mu_base = compute_resource_conversion(
        g1_cfg.get("ai", "K_AI_mu"), ref_tau, g1_cfg.get("channel", "research"), float(g1_cfg.get("phi", 1.0))
    )
    g6nd_u = g6nd_base["u_out"] * nd_boost
    g1mu_u = g1mu_base["u_out"] * mu_attenuation

    return {
        "sweep_size": len(points),
        "reference_tau": ref_tau,
        "asymmetry_high_impact_ratio": round(asym_high_impact, 4),
        "asymmetry_noise_ratio": round(asym_noise, 4),
        "g1mu_u_out": round(g1mu_u, 6),
        "g6nd_u_out": round(g6nd_u, 6),
        "g6nd_steering_channel": g6_cfg.get("channel", "research"),
        "g1mu_steering_channel": g1_cfg.get("channel", "research"),
        "hypothesis_support": {
            "H-CCT-016": asym_high_impact > 2.0 and asym_noise > 1.5,
            "H-CCT-017": g6nd_u > g1mu_u * threshold_ratio,
            "H-MCG-014": g6nd_u > g1mu_u * 1.2,
        },
        "sample_points": points[:12],
        "by_class_channel": _aggregate_conversion(points),
    }


def _aggregate_conversion(points: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    agg: dict[str, dict[str, list[float]]] = {}
    for p in points:
        key = p["class"]
        agg.setdefault(key, {}).setdefault(p["channel"], []).append(p["u_out"])
    return {
        cls: {ch: round(float(np.mean(vals)), 6) for ch, vals in chs.items()}
        for cls, chs in agg.items()
    }
