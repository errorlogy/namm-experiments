# Consensus Non-Optimality Hypothesis — Перманентная неоптимальность консенсуса в мультиагентных системах

**Purpose:** Research hypothesis registry for **permanent non-optimality of consensus** in multi-agent systems — the claim that collective agreement states are **structurally suboptimal** at equilibrium, not merely transiently so during convergence.  
**Date:** 2026-08-18  
**Epistemic baseline:** `PHILOSOPHICAL_INFERENCE` + `CONJECTURE` — **not** a social-science theorem, **not** a policy prescription.  
**Branch:** `hypothesis/consensus-non-optimality`  
Roman Kuznetsov · NAMM research program

Related: [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) (μ_F_H, fiber degeneracy) · [`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md) · [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md) · [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) · [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) (K1 consensus trap, class-heterogeneous MAS) · [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) (political myth as CNS output; GT 2.0 / CNE) · [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`proactive-ai/docs/NAMM_INTEGRATION.md`](../proactive-ai/docs/NAMM_INTEGRATION.md)

---

## Labeling

| Label | Use in this document |
|-------|----------------------|
| `PHILOSOPHICAL_INFERENCE` | Motivates the hypothesis; non-evidential |
| `CONJECTURE` | Testable claim about consensus suboptimality |
| `DEFINITION` | Precise operational content |
| `OPERATIONAL` | Falsifier, metric proxy, or experiment gate |
| `COMPUTATIONAL_EVIDENCE` | Reproducible witness — upgrades status only via experiment |

---

## 1. Core hypothesis — permanent non-optimality

`PHILOSOPHICAL_INFERENCE` · In many multi-agent environments — computational, social, or political — **consensus** is treated as the gold standard: synchronization, majority vote, Nash equilibrium, Kuramoto order parameter \(R \to 1\), fuzzy aggregation to a single label. This document registers the opposing thesis:

> **Consensus non-optimality (CNS thesis):** For a broad class of multi-agent systems with lossy projection, heterogeneous preferences, and bounded communication, **every reachable consensus state is strictly suboptimal** relative to a counterfactual that preserves dissenting information — and this suboptimality is **permanent** (structural at equilibrium), not a transient convergence artifact.

`DEFINITION` · Distinguish:

| Term | Meaning |
|------|---------|
| **Transient non-optimality** | System still converging; consensus not yet reached; apparent loss from premature agreement |
| **Permanent non-optimality** | At consensus fixed point \(x^*\), global welfare / information / reachability metric \(W(x^*) < W(x^\dagger)\) for some feasible non-consensus \(x^\dagger\) — **by construction of the consensus map**, not by noise |

`CONJECTURE` · **H-CNS-001 (permanent gap):** There exists a family of consensus operators \(\mathcal{C}: \mathcal{X}^N \to \mathcal{X}\) (vote, mean, κ-projection, fuzzy defuzzification) such that for all admissible agent states, \(\mathcal{C}\) is **non-injective** and **Welfare-decreasing** on the consensus fiber — analogous to AMFW κ losing 728 of 729 moduli ([`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md)).

`PHILOSOPHICAL_INFERENCE` · Society-as-MAS: electoral majorities, media narrative convergence, and institutional lock-in are **operational instances** of \(\mathcal{C}\) — modeling targets, not moral judgments in this registry.

---

## 2. Research lenses — multiple formal angles

Each lens supplies **definitions**, **predictions**, and **NAMM-attachable falsifiers**. They compose; none alone proves H-CNS-001.

### 2.1 Catastrophe theory · теория катастроф

`DEFINITION` · Collective decision manifolds admit **cusp/fold** structures (Thom): small parameter shifts (turnout, media coupling, threshold) produce **discontinuous** jumps in consensus outcome while local agent utilities vary smoothly.

| Construct | MAS reading | NAMM analog |
|-----------|-------------|-------------|
| Control parameters \((a,b)\) | Polarization, issue salience | κ grid, energy cap in config_shadow |
| State variable \(x\) | Public opinion / policy | Base point \(b \in B\) |
| Fold catastrophe | Sudden consensus flip | Fabric deformation \(T_\tau\) across blur phase (H-F011–H-F014) |
| Hysteresis | Path-dependent consensus | Rejection log; certificate branch history |

`CONJECTURE` · **H-CNS-002:** Near catastrophe locus, **forced consensus** (early termination of debate) increases expected regret vs allowing extended non-equilibrium phase — measurable as welfare gap at fixed \(N\).

### 2.2 Fuzzy logic · нечёткая логика

`DEFINITION` · Consensus degree \(\mu_{\mathrm{cns}}(x) \in [0,1]\) — strength of collective agreement. Distinct from fabric membership \(\mu_{\mathcal{F}_H}\) ([`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md)): high \(\mu_{\mathrm{cns}}\) can coincide with **low** \(\mu_{\mathcal{F}_H}\) (compact agreement on lossy shadow).

| Fuzzy construct | Role |
|-----------------|------|
| Fuzzy relation "agrees-with" | Agent–agent compatibility matrix |
| T-norm aggregation | Majority as fuzzy AND — loses tail beliefs |
| Defuzzification | **Consensus map** \(\mathcal{C}\) — primary information destroyer |
| \(\partial_\mu\) boundary | Agents near 0.5 membership — first casualties of consensus |

`CONJECTURE` · **H-CNS-003:** Defuzzified consensus **minimizes variance** of reported opinions but **maximizes projection error** vs full fuzzy preimage — dual to fiber thickening under κ (729 preimages, one shadow).

### 2.3 Entropy · энтропия и информация

`DEFINITION` · Let \(H(X)\) = Shannon entropy of collective state; \(I(X;Y)\) mutual information between agent views and outcome.

`CONJECTURE` · **H-CNS-004 (consensus entropy law):** Under consensus operator \(\mathcal{C}\),

\[
H(\mathcal{C}(X_1,\ldots,X_N)) \;\leq\; H(X_1,\ldots,X_N) - \Delta H_{\mathrm{fiber}}
\]

with **permanent** \(\Delta H_{\mathrm{fiber}} > 0\) when \(\mathcal{C}\) is many-to-one. Consensus **compresses**; compression is not free — operational link to NAMM \(K_A/K_H \geq 2\) gate (F4).

| Metric | Consensus phase | Dissent-preserving phase |
|--------|-----------------|--------------------------|
| Entropy \(H\) | Low | Higher |
| Reachable policy set | Collapsed | Larger |
| Certificate detail | Single shadow | Full fiber |

### 2.4 Dynamical systems · динамические системы

`DEFINITION` · Agent opinions \(\theta_i(t)\); coupling matrix \(A_{ij}\). Kuramoto order \(R(t) = \left|\frac{1}{N}\sum_j e^{i\theta_j}\right|\) ([`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md)).

| Regime | Dynamics | Optimality |
|--------|----------|------------|
| \(R \ll 1\) | Incoherent exploration | High diversity cost, high information |
| \(R \to 1\) | Synchronized consensus | Low variance, **structural suboptimality** (H-CNS-001) |
| Metastable chimera | Partial sync | Trade-off surface — candidate **less suboptimal** than full sync |
| Fixed point of meta-evaluator | \(E \cong F(E)\) (004) | Self-referential consensus — permanent trap |

`CONJECTURE` · **H-CNS-005:** Maximum \(R(t)\) **does not** maximize global utility \(W\) for heterogeneous \(\omega_i\); optimal \(R^* \in (0,1)\) — **permanent partial coherence** beats full consensus.

`PHILOSOPHICAL_INFERENCE` · "Dead synchrony" in Kuramoto literature (identical phase, zero innovation) is the oscillatory face of CNS thesis.

### 2.5 Social choice & game theory · социальный выбор

`DEFINITION` · Agents with preferences \(\prec_i\); social welfare function \(W\); consensus via voting rule \(f\).

| Classical obstruction | CNS reading |
|----------------------|-------------|
| Arrow impossibility | No perfect consensus rule — **permanent** compromise loss |
| Condorcet cycles | Consensus on one alternative **excludes** consistent global order |
| Nash equilibrium | Stable ≠ optimal — permanent gap |
| Median voter theorem | Convergence to median **destroys** tail preferences |

`CONJECTURE` · **H-CNS-006:** For finite agent graphs (NAMM: `finite_graphs`), **local consensus** on clusters yields **global suboptimality** — network modularization amplifies permanent gap vs centralized optimum.

### 2.6 Graph / network substrate · теория графов

`OPERATIONAL` · Primary NAMM attach point: **`finite_graphs`** + **`meta_evaluation`**.

| Object | Experiment role |
|--------|-----------------|
| Opinion graph \(G=(V,E)\) | Coupling topology for dynamics |
| Community structure | Local consensus basins |
| Spectral gap | Convergence speed vs optimality gap trade-off |
| Fiber over opinion projection | κ analog: many micro-states → one macro-consensus |

---

## 3. Application domains — society as multi-agent environment

`PHILOSOPHICAL_INFERENCE` · **Operational modeling targets** (not evidential claims about specific events):

| Domain | MAS formalization | CNS prediction |
|--------|-------------------|----------------|
| Electoral politics | Agents = voters/blocs; \(\mathcal{C}\) = aggregation rule | Permanent welfare loss on minority fibers; catastrophe flips at thresholds |
| Media / narrative | Agents = outlets; coupling via attention graph | High \(\mu_{\mathrm{cns}}\) on simplified narrative ↔ low \(\mu_{\mathcal{F}_H}\) for full event |
| Political mythogenesis | Agents = class-tagged voters/elites; \(\mathcal{C}\) = narrative canon | Stable myth = CNS fixed point: high \(\mu_{\mathrm{cns}}\), permanent \(\Delta W_{\mathrm{myth}}\) — H-MCG-001 |
| Institutional policy | Agents = ministries; consensus = committee vote | Locked-in suboptimal equilibrium (path dependence) |
| Protest / mobilization | Agents = heterogeneous θᵢ; Kuramoto sync | Full sync (mass single slogan) minimizes information for adaptive response |
| Forecasting | Ensemble of models/agents | **Ensemble diversity** > forced consensus mean for out-of-distribution events |

`CONJECTURE` · **H-CNS-007:** Political **forecasting gain** from preserving structured dissent (fiber-aware ensemble) exceeds gain from narrative consensus on historical calibration — testable on bounded synthetic environments before real data.

---

## 4. Simulation parameterization — bounded anti-consensus in fuzzy contours

`DEFINITION` · **Anti-consensus gap** (also **anti-consensus** in scenario configs): the permanent suboptimality at a consensus fixed point, operationalized as one of:

| Symbol | Metric | Normalization |
|--------|--------|---------------|
| \(\Delta W\) | Welfare loss vs fiber-preserving counterfactual | \(\Delta W / W^\dagger\) → \([0,1]\) |
| \(\Delta H_{\mathrm{fiber}}\) | Entropy destroyed by consensus map \(\mathcal{C}\) | \(\Delta H / H_{\mathrm{pre}}\) |
| \(\epsilon_{\mathrm{proj}}\) | Projection error vs full fuzzy preimage (§2.2) | L2 or KL vs agent profile |

`DEFINITION` · **Socio-political contour** \(F_k\): a fuzzy set over agent–issue pairs with membership \(\mu_{F_k}(a, x) \in [0,1]\). Examples: electoral bloc, ideological cluster, policy domain (climate, fiscal), geographic region, institutional committee. Agents and issues may belong to **multiple contours** with graded membership — not hard partitions.

| Contour type | Fuzzy membership source | Simulation role |
|--------------|-------------------------|-----------------|
| Electoral bloc | Agent ideology vector · centroid distance | Local consensus basin; per-bloc \(\Delta W\) |
| Policy domain | Issue tags · agent expertise weights | Domain-specific consensus operator |
| Geographic region | Spatial adjacency · soft boundary | Coupling topology + contour overlap |
| Institutional layer | Committee / ministry assignment | Hierarchical \(\mathcal{C}\) composition |

`DEFINITION` · **`max_non_optimality`** / **`max_anti_consensus`** (scenario parameters — **synonyms** in config): an upper bound on the normalized permanent suboptimality gap **within** a contour (or globally). Prefer **`max_non_optimality`** in NAMM experiment YAML; use **`max_anti_consensus`** in proactive-ai scenario overlays and crosswalk. Both keys must stay in sync when both appear. In NAMM experiments this is a **design knob**, not an assumption that consensus is optimal:

| Mode | Behavior |
|------|----------|
| **`measure`** | Record observed \(\Delta W\), \(\Delta H_{\mathrm{fiber}}\); no bound enforced — falsification mode |
| **`soft`** | Penalize scenarios where gap exceeds bound; still sample over operators |
| **`hard`** | Reject or resample instances with gap \(> \texttt{max\_non\_optimality}\) — controlled synthetic worlds |

`PHILOSOPHICAL_INFERENCE` · Parameterizing `max_non_optimality` **does not** assert consensus can be made optimal by tuning. It specifies **how much structural loss a scenario admits** when testing whether consensus operators converge to welfare maxima — the opposite of classical MAS defaults that treat \(R \to 1\) or defuzzified mean as the attractor of interest.

### 4.1 Contrast with consensus-as-optimum assumption

| Assumption | CNS simulation design |
|------------|----------------------|
| Consensus fixed point **is** (or approximates) global optimum | Consensus fixed point is **lossy projection**; optimum may lie on non-consensus fiber |
| Single global welfare metric | Contour-indexed metrics \(\Delta W_k\) under fuzzy membership weights |
| Convergence = success | Convergence at \(x^*\) with **mandatory** gap measurement; optional bound |
| Homogeneous agent pool | Graded contour membership; cross-contour coupling modulates gap |
| "More agreement = better" | `max_non_optimality` caps **acceptable** loss per contour for scenario calibration |
| Consensus at \(\mu_{\mathrm{cns}} \to 1\) → optimum | **Bounded permanent gap** in \((0, \texttt{max\_non\_optimality}]\) even at full agreement (H-CNS-013) |

**Membership functions** (config-selectable on each contour):

| Function | Parameters | Typical contour |
|----------|------------|-----------------|
| `triangular` | `a, b, c` | Ideological cluster (single peak) |
| `trapezoidal` | `a, b, c, d` | Electoral bloc with soft edges |
| `gaussian` / `gaussian_centroid` | `center` or `centroid`, `sigma` | Bloc around prototype vector |
| `ramp` | `x0, x1` | Policy-domain salience gradient |
| `spatial_soft` | `center_node`, `decay_length` | Geographic region on opinion graph |
| `issue_tag` | `issue_tags`, `agent_expertise_weight` | Policy domain (climate, fiscal, …) |

`CONJECTURE` · **H-CNS-011 (contour-modulated gap):** For fixed consensus operator \(\mathcal{C}\), anti-consensus gap \(\Delta W_k\) **varies systematically** across fuzzy socio-political contours \(F_k\) — high \(\mu_{\mathrm{cns}}\) within a contour does not imply low \(\Delta W_k\) when contour fiber is thick (link H-CNS-003, H-F021).

`CONJECTURE` · **H-CNS-012 (bounded falsification):** Scenarios with per-contour `max_non_optimality` bounds enable **controlled falsification** of consensus-as-optimum: if observed gaps persist below bound while welfare counterfactuals dominate, the bound is vacuous; if gaps **saturate** the bound across operators, permanent non-optimality is **structurally necessary** in that contour class.

`CONJECTURE` · **H-CNS-013 (consensus–optimum decoupling):** Under non-trivial fuzzy contour overlap, no consensus operator in the configured enum achieves \(\Delta W_{\mathrm{cns}} = 0\) while \(\mu_{\mathrm{cns}} \to 1\); classical “high agreement → optimum” fails **within** \((0, \texttt{max\_non\_optimality}]\) — tested in **021–022**.

`OPERATIONAL` · Fuzzy contour membership feeds the same formalism as fabric \(\mu_{\mathcal{F}_H}\) ([`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md)) but on **agent–issue** space, not certificate space: defuzzification of contour-weighted opinions is a **consensus map** with contour-specific fiber loss.

### 4.2 Example scenario parameters (YAML)

`OPERATIONAL` · NAMM experiment configs and proactive-ai scenarios may expose a `cns_simulation` block. Illustrative scaffold for **NAMM-2026-021**:

```yaml
experiment_id: NAMM-2026-021
domain: multi_agent_consensus
hypothesis_id: H-CNS-011
hypothesis_doc: docs/CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md
branch: hypothesis/consensus-non-optimality
status: proposed
seed: 2026021
research_question: >
  On bounded opinion graphs with fuzzy socio-political contours, does equilibrium
  consensus stay strictly suboptimal with Delta W bounded by max_non_optimality?
protocol_version: cns-simulation-v1

cns_simulation:
  # Global default; overridable per contour — keys are synonyms (keep in sync)
  max_non_optimality: 0.35
  max_anti_consensus: 0.35
  anti_consensus_metric: welfare_gap   # welfare_gap | entropy_fiber | projection_error
  bound_mode: measure                  # measure | soft | hard

  consensus_operator: defuzzify_mean   # vote | kuramoto_sync | kappa_projection | defuzzify_mean
  num_agents: 48
  opinion_dim: 3

  fuzzy_contours:
    - id: bloc_progressive
      label_ru: "прогрессивный блок"
      membership: gaussian_centroid
      centroid: [-0.7, 0.3, 0.1]
      sigma: 0.25
      max_non_optimality: 0.28         # per-contour bound (tighter than global)

    - id: bloc_conservative
      membership: gaussian_centroid
      centroid: [0.8, -0.2, 0.0]
      sigma: 0.30
      max_non_optimality: 0.32

    - id: policy_domain_climate
      membership: issue_tag
      issue_tags: [climate, energy, emissions]
      agent_expertise_weight: 0.6
      max_non_optimality: 0.40         # thick fiber — higher admissible gap

    - id: region_nordic_cluster
      membership: spatial_soft
      center_node: 12
      decay_length: 2.5
      max_non_optimality: 0.22

  dynamics:
    coupling_matrix: from_graph        # finite_graphs substrate
    kuramoto_K: 1.8
    target_order_R: 0.85               # forced sync setpoint (contrast with H-CNS-005)

  outputs:
    - delta_w_global
    - delta_w_per_contour
    - delta_h_fiber
    - mu_cns_per_contour
    - bound_saturated_flags

hypotheses:
  - H-CNS-001
  - H-CNS-004
  - H-CNS-006
  - H-CNS-011
  - H-CNS-012
  - H-CNS-013
falsifiers:
  - F-CNS-1
  - F-CNS-4
  - F-CNS-6
  - F-CNS-7
```

Multi-scenario sweep (022-style catastrophe boundary):

```yaml
cns_simulation:
  max_non_optimality: 0.40           # fixed cap during K/threshold sweep
  sweep:
    - param: max_non_optimality
      values: [0.10, 0.20, 0.35, 0.50]
    - param: consensus_operator
      values: [vote, defuzzify_mean, kuramoto_sync]
    - param: fuzzy_contours[0].sigma
      values: [0.15, 0.25, 0.40]       # contour sharpness → membership gradient
  record: hysteresis_loop              # catastrophe lens (H-CNS-002)
```

`OPERATIONAL` · Proactive-ai twin-world scenarios may attach contour metadata to beliefs and events:

```yaml
metadata:
  cns_contours:
    - policy_domain_climate
    - bloc_progressive
  max_non_optimality: 0.30
  max_anti_consensus: 0.30           # alias — sync with max_non_optimality
  preserve_dissent: true               # fiber-aware ensemble vs forced consensus
```

### 4.3 Metrics exposed to NAMM experiments

| Config key | Type | Maps to |
|------------|------|---------|
| `max_non_optimality` | float ∈ (0,1] | Primary key — upper bound on normalized \(\Delta W\) or \(\Delta H_{\mathrm{fiber}}\) |
| `max_anti_consensus` | float ∈ (0,1] | Alias of `max_non_optimality` (proactive-ai crosswalk) |
| `anti_consensus_metric` | enum | Which gap functional to measure / bound |
| `bound_mode` | enum | measure / soft / hard enforcement |
| `fuzzy_contours[].membership` | enum | gaussian_centroid · issue_tag · spatial_soft · committee |
| `fuzzy_contours[].max_non_optimality` | float | Per-contour override (alias: `max_anti_consensus`) |
| `consensus_operator` | enum | Instance of \(\mathcal{C}\) (§1) |
| `preserve_dissent` | bool | Fiber ensemble vs single defuzzified outcome |
| `target_order_R` | float | Kuramoto sync setpoint for dynamics overlay |

| Output key | Hypothesis link |
|------------|-----------------|
| `delta_w_per_contour` | H-CNS-011 |
| `bound_saturated_flags` | H-CNS-012 |
| `mu_cns_per_contour` | H-CNS-003, H-CNS-013 |
| `delta_h_fiber` | H-CNS-004 |
| `delta_w_global` at \(\mu_{\mathrm{cns}} \to 1\) | H-CNS-013 |

---

## 5. Connection to NAMM framework

CNS is a **cross-cutting hypothesis layer** — not yet a standalone domain adapter. It composes existing NAMM constructs:

| NAMM construct | CNS role |
|----------------|----------|
| κ projection / fiber (009, 010) | **Paradigm:** consensus = shadow; 728 hidden states = permanent information loss |
| \(\mu_{\mathcal{F}_H}\) (fabric) | Agreement compactness ≠ descriptive completeness |
| Meta-evaluator fixed points (004) | Self-reinforcing consensus traps |
| Kuramoto / MIOC (014) | Sync order \(R\) vs utility — quantifiable trade-off |
| Cognitive antigravity (013) | Escape from **median consensus** in LLM outputs |
| Cognitive class taxonomy (023–025) | K1 majority trap; class-heterogeneous MAS; \(\delta E\) ↔ fiber loss (H-CCT-005, H-CCT-007) |
| Political mythogenesis (026–028) | Myth as \(\mathcal{C}\) output; GT 2.0 CNE; class-selective myth trap — H-MCG-001–012 |
| Proactive AI (EIA) | Endogenous initiative vs **passive consensus** to user prior |
| Protocol v2 gates | Certificate over prose — dissent preserved in `certificate.json` |
| Frame escalation (006→007→009) | When consensus frame saturates, change **configuration space** not budget |

**Proposed domain_id:** `multi_agent_consensus` — **planned** (registry only). See [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) §3.17.

**Hypothesis ID cluster:** `H-CNS-001` … `H-CNS-013` (this doc).

**Simulation surface:** `cns_simulation` block in experiment config — `max_non_optimality` / `max_anti_consensus`, fuzzy contour membership, per-contour bounds (§4).

---

## 6. Open research questions

| ID | Question (RU / EN) | Status |
|----|-------------------|--------|
| Q-CNS-01 | Является ли перманентный разрыв **универсальным** для всех правил консенсуса или существует класс \(\mathcal{C}^*\) с нулевым fiber-loss? / Is permanent gap universal or does a lossless consensus class exist? | `CONJECTURE` |
| Q-CNS-02 | Какова **оптимальная** \(R^*\) (частичная когерентность) vs полный консенсус \(R=1\)? / Optimal partial coherence? | `CONJECTURE` — link 014 |
| Q-CNS-03 | Можно ли **измерить** \(\Delta H_{\mathrm{fiber}}\) на конечных графах так же, как fiber_size в 009? | `OPERATIONAL` |
| Q-CNS-04 | Катастрофические скачки консенсуса **предсказуемы** из cusp параметров на opinion graph? | `CONJECTURE` |
| Q-CNS-05 | Связан ли CNS с **Arrow** только при малых \(N\) или масштабируется на LLM multi-agent debate? | `CONJECTURE` |
| Q-CNS-06 | Proactive initiative (EIA) **снижает** или **увеличивает** permanent gap vs reactive consensus? | `CONJECTURE` |
| Q-CNS-07 | Существует ли **forecasting** benchmark где fiber-preserving ensemble бьёт consensus aggregator? | `OPERATIONAL` — 021 |
| Q-CNS-08 | Совместима ли CNS с democratic legitimacy norms — **descriptive** vs **normative** split? | `PHILOSOPHICAL_INFERENCE` |
| Q-CNS-09 | Как **max_non_optimality** per contour влияет на обнаружимость H-CNS-001 — bound saturation vs vacuous bound? / Does per-contour max non-optimality bound affect detectability of permanent gap? | `OPERATIONAL` — 021 |
| Q-CNS-10 | Какие функции принадлежности контуров (gaussian vs spatial vs issue_tag) максимизируют разброс \(\Delta W_k\)? / Which contour membership shapes maximize cross-contour gap variance? | `CONJECTURE` |
| Q-CNS-11 | Как политический миф как выход \(\mathcal{C}\) связан с \(\Delta W\) при \(\mu_{\mathrm{cns}} \to 1\)? / How does political myth as C output relate to permanent gap? | `CONJECTURE` — link H-MCG-001, [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) |

---

## 7. Falsifiability criteria

`OPERATIONAL` · CNS thesis is **weakened or refuted** if:

| Falsifier | Observation |
|-----------|-------------|
| **F-CNS-1** | Construct consensus rule \(\mathcal{C}^*\) on bounded NAMM graph frame with **zero** welfare gap at equilibrium — \(\Delta W = 0\) for all admissible profiles |
| **F-CNS-2** | Full sync \(R=1\) **maximizes** \(W\) for heterogeneous agents — optimal consensus exists |
| **F-CNS-3** | Fiber entropy loss \(\Delta H_{\mathrm{fiber}} \to 0\) under refined consensus — gap is transient only |
| **F-CNS-4** | Forecasting: consensus aggregator **dominates** fiber ensemble on all synthetic political MAS instances (021) |
| **F-CNS-5** | Catastrophe model **fails** to predict discontinuity onset better than linear regression on same features |
| **F-CNS-6** | For all contour classes and operators, observed \(\Delta W_k < \texttt{max\_non\_optimality}\) with **no** bound saturation — gap is scenario artifact, not structural |
| **F-CNS-7** | Per-contour gap variance ≈ 0 — contours are cosmetic labels, not distinct fuzzy fibers |
| **F-CNS-8** | Full agreement \(\mu_{\mathrm{cns}} \to 1\) achieves \(\Delta W = 0\) within configured bounds — consensus–optimum decoupling fails (refutes H-CNS-013) |

**Partial confirmation:** Reproducible \(\Delta W > 0\) or \(\Delta H_{\mathrm{fiber}} > 0\) at consensus fixed points across ≥ 3 topologies — `COMPUTATIONAL_EVIDENCE` under Protocol v2. **Strong confirmation (021):** `bound_saturated_flags` true for ≥ 2 contour classes under `bound_mode: measure`.

---

## 8. Proposed experiments (placeholders)

`OPERATIONAL` · Scaffolds created — IDs **021–022** (`experiments/NAMM-2026-021/`, `NAMM-2026-022/`).

### NAMM-2026-021 — Opinion graph consensus vs welfare fiber

| Field | Content |
|-------|---------|
| **Domain** | `finite_graphs` (+ planned `multi_agent_consensus`) |
| **Frame** | F3a + dynamical overlay |
| **Tests** | H-CNS-001, H-CNS-004, H-CNS-006 |
| **Design** | Enumerate small opinion graphs; agent utilities on nodes; compare consensus map vs Pareto / fiber-preserving aggregator; measure \(\Delta W\), \(\Delta H\); **`cns_simulation`** block with fuzzy contours + `max_non_optimality` (§4) |
| **Config keys** | `max_non_optimality`, `max_anti_consensus`, `fuzzy_contours[]`, `anti_consensus_metric`, `bound_mode`, `delta_w_per_contour` |
| **Tests (add)** | H-CNS-011, H-CNS-012, H-CNS-013 |
| **Success** | Stable \(\Delta W > 0\) at consensus for ≥ 80% of admissible instances; contour-dependent gap variance |
| **Falsifier** | Universal \(\Delta W = 0\) — CNS false on this class; F-CNS-6, F-CNS-7 |

### NAMM-2026-022 — Catastrophe boundary in coupled Kuramoto–vote model

| Field | Content |
|-------|---------|
| **Domain** | `multi_agent_consensus` + Kuramoto proxy |
| **Frame** | F3g spectral / 014 covariate |
| **Tests** | H-CNS-002, H-CNS-005 |
| **Design** | Sweep coupling \(K\), threshold \(b\); locate fold/cusp; compare regret at forced vs delayed consensus; sweep `max_non_optimality` × contour `sigma` (§4.2) |
| **Config keys** | `cns_simulation.sweep`, `max_non_optimality`, `record: hysteresis_loop` |
| **Tests (add)** | H-CNS-011, H-CNS-013 |
| **Success** | Hysteresis + measurable regret spike near catastrophe locus; gap persists at \(\mu_{\mathrm{cns}} \to 1\) within bound |
| **Link** | [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md), 014 |

---

## 9. Hypothesis registry — H-CNS-001..H-CNS-013

| ID | Statement | Lens | Label |
|----|-----------|------|-------|
| **H-CNS-001** | Reachable consensus states are strictly suboptimal at equilibrium (permanent gap) | Core | `CONJECTURE` |
| **H-CNS-002** | Forced consensus near catastrophe locus increases regret | Catastrophe | `CONJECTURE` |
| **H-CNS-003** | Defuzzification minimizes variance, maximizes projection error | Fuzzy | `CONJECTURE` |
| **H-CNS-004** | Consensus reduces entropy by permanent fiber term \(\Delta H_{\mathrm{fiber}} > 0\) | Entropy | `CONJECTURE` |
| **H-CNS-005** | Optimal order \(R^* \in (0,1)\) — full sync suboptimal | Dynamics | `CONJECTURE` |
| **H-CNS-006** | Local cluster consensus → global suboptimality on graphs | Social choice + graphs | `CONJECTURE` |
| **H-CNS-007** | Fiber-preserving forecast ensemble beats consensus aggregator (bounded MAS) | Applications | `CONJECTURE` |
| **H-CNS-008** | κ-style consensus in config_shadow is canonical lossy MAS operator | NAMM bridge | `OPERATIONAL` |
| **H-CNS-009** | Meta-evaluator fixed points are consensus traps with \(\Delta W > 0\) | Meta (004) | `CONJECTURE` |
| **H-CNS-010** | Proactive initiative increases reachable non-consensus states vs reactive agent | EIA bridge | `CONJECTURE` |
| **H-CNS-011** | Anti-consensus gap \(\Delta W_k\) varies systematically across fuzzy socio-political contours | Simulation / fuzzy | `CONJECTURE` |
| **H-CNS-012** | Parameterized `max_non_optimality` enables controlled falsification of consensus-as-optimum | Simulation design | `OPERATIONAL` |
| **H-CNS-013** | Full agreement (\(\mu_{\mathrm{cns}} \to 1\)) does not imply \(\Delta W_{\mathrm{cns}} = 0\) within bound | Simulation / classical contrast | `CONJECTURE` |

---

## 10. Agent load instructions

When the user cites **consensus non-optimality**, **перманентная неоптимальность консенсуса**, **multi-agent society modeling**, or **CNS / H-CNS**:

1. Load this file + [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) §3.17.
2. Cross-load fabric doc if fuzzy / fiber language appears ([`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md)).
3. For oscillatory/social coupling: [`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md).
4. Map proposals to **H-CNS IDs** and experiment placeholders **021–022**.
5. For simulation design: load **§4** — `max_non_optimality` / `max_anti_consensus`, fuzzy contour membership, `cns_simulation` YAML block.
6. Label claims; do **not** treat CNS as normative political doctrine — it is a **structural modeling hypothesis**.
7. For **political mythogenesis**, **мифогенез**, **Game Theory 2.0**, or **H-MCG**: load [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md).

---

## 11. Cross-reference index

| ID | Type | Links |
|----|------|-------|
| H-CNS-001 … H-CNS-013 | `CONJECTURE` / `OPERATIONAL` | This doc §9 |
| `cns_simulation` | Config schema (proposed) | This doc §4 |
| Q-CNS-09, Q-CNS-10 | Open questions | This doc §6 |
| H-F021, H-F024 | Fiber degeneracy | [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) |
| H-BW-001 | MIOC Φ | [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md) |
| H-CA-001 | Median escape | [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) |
| H-CCT-005, H-CCT-007, H-CCT-010 | Class ↔ consensus | [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) |
| H-MCG-001 … H-MCG-012 | Myth ↔ CNS ↔ GT 2.0 | [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) |
| NAMM-2026-021 | `OPERATIONAL` | Opinion graph welfare fiber (proposed) |
| NAMM-2026-022 | `OPERATIONAL` | Catastrophe + Kuramoto–vote (proposed) |
| `multi_agent_consensus` | Domain (planned) | [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) |

---

Roman Kuznetsov · NAMM research program
