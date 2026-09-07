# NAMM Domain Universe

> **Для людей:** см. [**MATHEMATICS_SECTIONS_RU.md**](MATHEMATICS_SECTIONS_RU.md) — три слоя (классика / гипотезы / PI). Классическая база: [**MATHEMATICS_LIBRARY_BASE.md**](MATHEMATICS_LIBRARY_BASE.md).

**Permanent catalog** of mathematical and physical domains NAMM can operate in — the authoritative map from formal math substrate → Python modules → experiment IDs → frame ladder rungs.

**Naming rationale:** *Domain Universe* (Russian: **«Вселенная доменов NAMM»** or **«Каталог математических доменов»**) — a single load target for agents at research-task start. Prefer this title over scattered per-domain READMEs when choosing a frame or escalating after null results.

Roman Kuznetsov · NAMM research program

Related: [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md) · [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) · [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) · [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) · [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) · [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) · [`SCIENTIFIC_STACK.md`](SCIENTIFIC_STACK.md) · [`SCI_FLOW.md`](SCI_FLOW.md) · [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) · [`src/namm/domains/`](../src/namm/domains/) · [`src/namm/sci_flow/`](../src/namm/sci_flow/)

---

> **Быстрая справка · Quick reference:** [**8 operational**](#status-operational) · [**3 stub**](#status-stub) · [**9 planned**](#status-planned) — jump to [fields index](#разделы-математики-и-смежных-областей--mathematical--physics-fields-index) below.

## Разделы математики и смежных областей · Mathematical & Physics Fields Index

<a id="status-operational"></a><a id="status-stub"></a><a id="status-planned"></a>

| Раздел (RU) | Section (EN) | NAMM domain_id | Status | Experiments |
|-------------|--------------|----------------|--------|-------------|
| Комбинаторика | Graph theory | `finite_graphs` | **operational** | 001 |
| Теория графов | Network algorithms | `finite_graphs` | **operational** | 001, 003, 005, 006, 008 (substrate) |
| Программный синтез | Program synthesis | `program_ast` | **operational** | 003 |
| Теория переписывания | Rewriting systems | `rewriting` | **operational** | 002 |
| Топология | Topology | `tda_frame` | **operational** (scaffold) | 006 |
| TDA | Persistent homology | `tda_frame` | **operational** (scaffold) | 006 |
| Сырой тензорный анализ | Spectral & tensor | `raw_tensor` | **operational** | 007 |
| Мета-вычисление | Meta-evaluation | `meta_evaluation` | **operational** | 004 |
| Теория конфигурационных пространств | Moduli & compactification | `config_shadow` | **operational** | 009, 010 |
| Квантовая механика | Quantum mechanics | `quantum` | **stub** | — |
| Теория категорий | Category theory | `category` | **stub** | — |
| Символическая алгебра | Symbolic algebra | `symbolic_algebra` | **operational** (support) | supports 001, 003 |
| SMT | Formal verification | `smt_verification` | **stub** | — |
| Теория чисел | Number theory | `number_theory_shadow` | **planned** | — |
| Дифференциальная геометрия | Differential geometry | `differential_geometry_shadow` | **planned** | — |
| Trans-level Θ | Semantic transition algebra | `trans_level_theta` | **planned** | 011 |
| Открытые задачи | Open problems | `open_problem_shadow` | **operational** | 005, 008 |
| ИИ-Наука и нейросимвольные вычисления | AI Science & Prior Art | `ai_science` | **operational** | `prior_art/arxiv.py`, 004 |
| Математическая ткань | Mathematical fabric (fuzzy dynamics) | `mathematical_fabric` | **planned** (registry) | 006→007→009 trail |
| Мультиагентные системы · консенсус | Multi-agent consensus (social MAS) | `multi_agent_consensus` | **planned** (registry) | 021–022 (proposed) |
| Когнитивные классы · таксономия | Cognitive class taxonomy (homo + AI + hybrid) | `cognitive_class_taxonomy` | **planned** (registry) | 023–025, 029 (proposed) |
| Политический мифогенез · GT 2.0 | Political mythogenesis (CNS + CCT overlay) | `multi_agent_consensus` | **planned** (registry) | 026–028 (proposed) |
| AMAT · антимедианная топология ИИ | Anti-Median AI Topology (typicality phases; median = named proxy); **H-AMAT-006–010**: catastrophe A₃, information geometry, fractal dim, Lyapunov attractor, sheaf cohomology | `ai_science` + TDA overlay | **planned** (registry) | 013–014, 023 analog, **030**, 037–041 (planned) |

**Counts (2026-08-18):** **9 operational** domain adapters (incl. `ai_science` Prior Art) · **3 stub** (quantum, category, smt_verification) · **9 planned**.


---

## Содержание · Table of Contents

- [1. Назначение · Purpose](#1-назначение--purpose)
- [2. Сводная таблица доменов · Master domain table](#2-сводная-таблица-доменов--master-domain-table)
- [3. Разделы доменов · Domain sections](#3-разделы-доменов-все-основные-области-математики--domain-sections-all-major-math-areas)
  - [3.1 Комбинаторика · Combinatorics & graph theory](#31-комбинаторика-и-теория-графов--combinatorics--graph-theory)
  - [3.2 Программный синтез · Program synthesis](#32-программный-синтез--program-synthesis--evolutionary-search)
  - [3.3 Теория переписывания · Rewriting systems](#33-теория-переписывания--rewriting-systems)
  - [3.4 Топология и TDA · Topology & TDA](#34-топология-и-tda--topology--tda)
  - [3.5 Сырой тензорный анализ · Raw tensor / spectral](#35-сырой-тензорный-анализ--raw-tensor--spectral)
  - [3.6 Мета-вычисление · Meta-evaluator fixed points](#36-мета-вычисление--meta-evaluator-fixed-points)
  - [3.7 Конфигурационные пространства · Configuration spaces / moduli](#37-конфигурационные-пространства--configuration-spaces--moduli-shadows)
  - [3.8 Квантовая механика · Quantum mechanics](#38-квантовая-механика--quantum-mechanics)
  - [3.9 Теория категорий · Category theory](#39-теория-категорий--category-theory)
  - [3.10 Символическая алгебра · Symbolic algebra](#310-символическая-алгебра--symbolic-algebra)
  - [3.11 SMT · Formal verification](#311-smt--verification)
  - [3.12 Открытые задачи · Open problem shadows](#312-открытые-задачи--open-problem-shadows)
  - [3.13 Trans-level Θ · Semantic transition algebra](#313-trans-level-θ--semantic-transition-algebra)
  - [3.14 Математическая ткань · Mathematical fabric / fuzzy dynamics](#314-математическая-ткань--mathematical-fabric--fuzzy-dynamics)
  - [3.15 Теория чисел · Number theory shadows](#315-теория-чисел--number-theory-shadows)
  - [3.16 Дифференциальная геометрия · Differential geometry shadows](#316-дифференциальная-геометрия--differential-geometry-shadows)
  - [3.17 Мультиагентный консенсус · Multi-agent consensus](#317-мультиагентный-консенсус--multi-agent-consensus)
  - [3.18 Когнитивные классы · Cognitive class taxonomy](#318-когнитивные-классы--cognitive-class-taxonomy)
  - [3.19 Политический мифогенез · Political mythogenesis](#319-политический-мифогенез--political-mythogenesis)
  - [3.20 AMAT · Anti-Median AI Topology](#320-amat--anti-median-ai-topology)
- [4. Индекс эксперимент ↔ домен · Experiment ↔ domain index](#4-индекс-эксперимент--домен--experiment--domain-index)
- [5. Справочник библиотек · Library reference](#5-справочник-библиотек--library-reference)
- [6. Планируемое расширение · Planned domain expansion](#6-планируемое-расширение-доменов--planned-domain-expansion)
- [7. Инструкции для агента · Agent instructions](#7-инструкции-для-агента--agent-instructions)
- [8. Карта кода · Code map](#8-карта-кода--code-map)

---

## 1. Назначение · Purpose

This document is the **permanent map** of math/physics domains NAMM can search, verify, and certificate-anchor. It answers:

| Question | Where to look |
|----------|---------------|
| Which domain fits a new experiment? | [Fields index](#разделы-математики-и-смежных-областей--mathematical--physics-fields-index) + §3 sections |
| What library enables which frame? | §5 library reference |
| What is operational vs stub vs planned? | [Quick reference](#status-operational) + Status column in index |
| How to escalate after null (001, 006)? | §7 agent instructions |

**Agent requirement:** read this file at the **start of every NAMM research task**, immediately after [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) (see agent load protocol there). Then branch to the active experiment's `config.yaml`, domain module under `src/namm/domains/`, and relevant hypothesis registries.

**Not evidential:** domain catalog entries motivate frame choice; they do **not** satisfy Protocol v2 gates. Witnesses live in `certificate.json` and experiment reports.

---

## 2. Сводная таблица доменов · Master domain table

| Domain ID | Mathematical field | NAMM frame(s) | Python lib(s) | Status | Experiment IDs | Notes |
|-----------|-------------------|---------------|---------------|--------|----------------|-------|
| `finite_graphs` | Combinatorics · finite graph theory | F3a | `networkx` | **operational** | 001 | String formulas over graph stats; calibration null (Wiener-dominated) |
| `program_ast` | Program synthesis · evolutionary search | F3c | stdlib AST + `networkx` | **operational** | 003 | Graph→Int invariant AST; holdout families |
| `rewriting` | Term rewriting systems · confluence | F3b | pure Python | **operational** | 002 | TRS + confluence certificate |
| `meta_evaluation` | Meta-level fixed points E ≈ F(E) | F3d · F∞ partial | pure Python | **operational** | 004 | AI thinking topology; evaluator depth |
| `open_problem_shadow` | Open-problem finite shadows | F3e · F3e₂ | `networkx` | **operational** | 005, 008 | Kotzig P_k; Graceful Tree |
| `tda_frame` | Topological data analysis · persistence | F3f · F2 TDA | `gudhi` `[nd]` | **operational** (scaffold) | 006 | Geodesic metric persistence vs path baseline |
| `raw_tensor` | Raw tensor / spectral features | F3g | `numpy`, `scipy`, `sympy` | **operational** | 007 | **First tested-signal** (SHTC-639); no named invariants |
| `config_shadow` | Configuration spaces · moduli fibers | F3h · ND | pure Python | **operational** | 009, 010 | 11D vacua; κ compactification; AMFW-012e |
| `symbolic_algebra` | Symbolic algebra · equivalence | F2 algebraic | `sympy` | **operational** (support) | — | AST↔SymPy equivalence in program domain |
| `smt_verification` | SMT / formal verification | F2 algebraic | `z3-solver`, `python-sat` | **stub** | — | `namm.verifiers.z3_stub_check`; full encoding planned |
| `quantum` | Quantum mechanics · finite Hilbert | F2 quantum | `qutip` `[nd]` | **stub** | — | Bell-state witness; 2–3 qubit cap; no experiment yet |
| `category` | Category theory · finite shadows | F2 categorical | pure Python + `networkx` | **stub** | — | Hom-set counts on graphs n≤6 |
| `trans_level_theta` | Trans-level Θ · semantic transition algebra | F∞ | TBD (tensor + meta) | **planned** | 011 | Morphisms between raw structures without named vocabulary |
| `open_problem_moduli` | Open problem × moduli hybrid | F3e₂+F3h | `networkx` + config_shadow | **planned** | 012 | Graceful labeling moduli fiber (scaffold only) |
| `number_theory_shadow` | Number theory · finite shadows | F2 | TBD (`sympy`, `sage`?) | **planned** | — | See tierlist T2–T3 entries |
| `differential_geometry_shadow` | Differential geometry · discrete shadows | ND | TBD | **planned** | — | Simplicial / graph curvature proxies |
| `proof_assistant` | Proof-assistant certificates | F2 | Lean / Mathlib (external) | **planned** | — | Tierlist T1; not in repo |
| `mathematical_fabric` | Fabric dynamics · fuzzy topology | F1→F∞ cross-cutting | — (concept layer) | **planned** (registry) | 006→007→009 trail | [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) H-F001–H-F050 |
| `multi_agent_consensus` | Multi-agent systems · consensus non-optimality | F3a + dynamics overlay | `networkx`, `numpy`, `scipy` | **planned** (registry) | 021–022 (proposed) | [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) H-CNS-001–H-CNS-013 |
| `cognitive_class_taxonomy` | Cognitive classes · homo K0–K7 + AI K_AI_μ/nd + proto-subject + hybrid | F3f + F3g + F4 overlay | `numpy`, `gudhi` `[nd]`, embedding APIs | **planned** (registry) | 023–025, 029 (proposed) | [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) H-CCT-001–H-CCT-021 |
| `anti_median_ai_topology` | AMAT · typicality vs off-typical phases (median = named proxy, §0); H-AMAT-006–010: cusp catastrophe, info-geometry, fractal dim, Lyapunov, sheaf cohomology | F3f + `ai_science` | `numpy`, `ripser` `[science]`, RPL JSON | **planned** (registry) | 013–014, **030**, 037–041 (planned) | [`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) H-AMAT-001–010 · **§0 binding** |

**Counts (2026-08-18):** **8 operational** domain adapters with experiment configs · **3 stub** (quantum, category, smt_verification) · **9 planned** expansion targets (see [fields index](#разделы-математики-и-смежных-областей--mathematical--physics-fields-index)).

---

## 3. Разделы доменов (все основные области математики) · Domain sections (all major math areas)

### 3.1 Комбинаторика и теория графов · Combinatorics & graph theory

| Field | Content |
|-------|---------|
| **Domain ID** | `finite_graphs` (+ graph substrate for 003, 005, 006, 008) |
| **Module** | `src/namm/domains/graph/` |
| **Library** | `networkx` — atlas enumeration, invariants, evaluators |
| **Frames** | F3a (string formulas) |
| **Experiments** | **001** (calibration null), **003** (AST leaves), **005** (P_k paths), **008** (graceful trees), **006** (TDA input graphs) |
| **Status** | **operational** |

Core generators: `enumerate_small_graphs`, `random_invariant_formula`. Evaluator: `evaluate_formula`, `formulas_agree_on_graphs`.

---

### 3.2 Программный синтез · Program synthesis / evolutionary search

| Field | Content |
|-------|---------|
| **Domain ID** | `program_ast` |
| **Module** | `src/namm/domains/program/` |
| **Library** | stdlib AST dataclasses + `networkx` graph inputs |
| **Frames** | F3c |
| **Experiments** | **003** |
| **Status** | **operational** |

Evolutionary population over ADD/MUL/leaf programs; SymPy equivalence gate via `program/equivalence.py`.

---

### 3.3 Теория переписывания · Rewriting systems

| Field | Content |
|-------|---------|
| **Domain ID** | `rewriting` |
| **Module** | `src/namm/domains/rewriting/` |
| **Library** | pure Python |
| **Frames** | F3b |
| **Experiments** | **002** |
| **Status** | **operational** |

Confluence score, normalization, `rules_to_dict()` certificate serialization.

---

### 3.4 Топология и TDA · Topology & TDA

| Field | Content |
|-------|---------|
| **Domain ID** | `tda_frame` |
| **Module** | `src/namm/domains/tda/` |
| **Library** | `gudhi` (optional `[nd]` extra) |
| **Frames** | F3f · F2 topological |
| **Experiments** | **006** |
| **Status** | **operational** (scaffold — null calibration) |

Persistent homology on graph geodesic metric; `PersistenceSignature`, `graph_persistence_signature`. Install: `pip install -e ".[dev,nd]"`.

---

### 3.5 Сырой тензорный анализ · Raw tensor / spectral

| Field | Content |
|-------|---------|
| **Domain ID** | `raw_tensor` |
| **Module** | `src/namm/domains/tensor/` |
| **Library** | `numpy`, `scipy` (eigen/spectral), `sympy` (equivalence) |
| **Frames** | F3g |
| **Experiments** | **007** — **first operational signal** |
| **Status** | **operational** |

12 raw tensor leaves (adjacency spectrum, heat kernel samples); machine-native vocabulary; no named human invariants in discovery path.

---

### 3.6 Мета-вычисление · Meta-evaluator fixed points

| Field | Content |
|-------|---------|
| **Domain ID** | `meta_evaluation` |
| **Module** | `src/namm/domains/meta/` |
| **Library** | pure Python |
| **Frames** | F3d · F∞ partial |
| **Experiments** | **004** |
| **Status** | **operational** |

Search for E ≈ F(E) on graphs order ≤ 6; transform registry (`identity`, `canonicalize`, `self_unfold`, …). Links to AI thinking topology ([`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md)).

---

### 3.7 Конфигурационные пространства · Configuration spaces / moduli shadows

| Field | Content |
|-------|---------|
| **Domain ID** | `config_shadow` |
| **Module** | `src/namm/domains/config_shadow/` |
| **Library** | pure Python (integer moduli grid) |
| **Frames** | F3h · ND config-space |
| **Experiments** | **009** (11D vacua, AMFW-012e), **010** (κ-sweep), **012** (planned hybrid) |
| **Status** | **operational** (009–010); **012 planned** |

59,049 admissible vacua enumerated; κ-projection to 4D shadow; fiber degeneracy witnesses. See [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md).

---

### 3.8 Квантовая механика · Quantum mechanics

| Field | Content |
|-------|---------|
| **Domain ID** | `quantum` |
| **Module** | `src/namm/domains/quantum/` |
| **Library** | `qutip` (optional `[nd]` extra) |
| **Frames** | F2 quantum (planned F3 frame) |
| **Experiments** | — (no experiment config yet) |
| **Status** | **stub** |

`BellStateWitness`, `two_qubit_entanglement_entropy`; MAX_QUBITS = 3. Planned: density-operator search frame with certificate witnesses (`COMPUTATIONAL_EVIDENCE` only).

---

### 3.9 Теория категорий · Category theory

| Field | Content |
|-------|---------|
| **Domain ID** | `category` |
| **Module** | `src/namm/domains/category/` |
| **Library** | pure Python + `networkx` |
| **Frames** | F2 categorical |
| **Experiments** | — |
| **Status** | **stub** |

Finite shadow: graphs as objects, homomorphisms as morphisms; `graph_category_shadow`, hom-set counts n≤6. Planned: 2-categorical functorial invariants (FRAME_LADDER CONJECTURE).

---

### 3.10 Символическая алгебра · Symbolic algebra

| Field | Content |
|-------|---------|
| **Domain ID** | `symbolic_algebra` (cross-cutting) |
| **Module** | `src/namm/domains/program/equivalence.py`, `src/namm/prior_art/simplify.py` |
| **Library** | `sympy` |
| **Frames** | F2 algebraic |
| **Experiments** | supports 003, 001 baselines |
| **Status** | **operational** (support layer) |

AST→SymPy mapping, baseline equivalence checks, prior-art simplification.

---

### 3.11 SMT · Formal verification

| Field | Content |
|-------|---------|
| **Domain ID** | `smt_verification` |
| **Module** | `src/namm/verifiers/` |
| **Library** | `z3-solver`, `python-sat` |
| **Frames** | F2 algebraic |
| **Experiments** | — |
| **Status** | **stub** |

`z3_stub_check` confirms import; full invariant encoding not yet implemented. Planned: SMT certificates for open-problem bounds.

---

### 3.12 Открытые задачи · Open problem shadows

| Field | Content |
|-------|---------|
| **Domain ID** | `open_problem_shadow` |
| **Module** | `src/namm/domains/open_problem/` |
| **Library** | `networkx` |
| **Frames** | F3e · F3e₂ |
| **Experiments** | **005** (Kotzig P_k), **008** (Graceful Tree) |
| **Status** | **operational** |

Full tierlist: [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md). T0 problems map directly to finite shadow search; T1+ need proof-assistant or larger adapters.

---

### 3.13 Trans-level Θ · Semantic transition algebra

| Field | Content |
|-------|---------|
| **Domain ID** | `trans_level_theta` |
| **Module** | — (planned: meta + tensor composition) |
| **Library** | TBD |
| **Frames** | F∞ |
| **Experiments** | **011** (planned) |
| **Status** | **planned** |

Semantic transition algebra over raw structure — morphisms between certificate classes without collapsing to named vocabulary. Motivated by SHTC-639 (007) and AMFW-012e (009); see [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md) §2.

---

### 3.14 Математическая ткань · Mathematical fabric / fuzzy dynamics

| Field | Content |
|-------|---------|
| **Domain ID** | `mathematical_fabric` (cross-cutting concept) |
| **Module** | — (hypothesis registry, not a single adapter) |
| **Library** | — |
| **Frames** | F1→F∞ escalation trail |
| **Experiments** | 006→007→009 frame escalation; 010 κ-calibration; 011–012 planned |
| **Status** | **planned** (registry operational) |

Operational metaphor: base space B, fibers over κ-shadows, fuzzy membership μ_F_H. Full registry: [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) (H-F001–H-F050). Load when user cites fabric, fuzzy dynamics, or Anthemium topology beyond PI-008.

---

### 3.15 Теория чисел · Number theory shadows

| Field | Content |
|-------|---------|
| **Domain ID** | `number_theory_shadow` |
| **Module** | — (planned) |
| **Library** | TBD (`sympy`, `gmpy2`, Sage external) |
| **Frames** | F2 |
| **Experiments** | — |
| **Status** | **planned** |

Finite shadows for divisor sums, Goldbach bounds, and related tierlist T2–T3 entries. See [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md).

---

### 3.16 Дифференциальная геометрия · Differential geometry shadows

| Field | Content |
|-------|---------|
| **Domain ID** | `differential_geometry_shadow` |
| **Module** | — (planned) |
| **Library** | TBD (`gudhi`, discrete curvature libs) |
| **Frames** | ND |
| **Experiments** | — |
| **Status** | **planned** |

Simplicial and graph curvature proxies; Ricci curvature on graphs; fiber bundles over config base. See §6 planned expansion.

---

### 3.17 Мультиагентный консенсус · Multi-agent consensus

| Field | Content |
|-------|---------|
| **Domain ID** | `multi_agent_consensus` (cross-cutting concept + graph substrate) |
| **Module** | — (hypothesis registry; adapter planned) |
| **Library** | `networkx`, `numpy`, `scipy` (opinion dynamics, Kuramoto proxy) |
| **Frames** | F3a (graph) + dynamical overlay; links to 014 Kuramoto covariates |
| **Experiments** | **021** (opinion graph welfare fiber + `cns_simulation`, proposed), **022** (catastrophe + Kuramoto–vote sweep, proposed) |
| **Config surface** | `cns_simulation.max_non_optimality` (primary), `max_anti_consensus` (alias), `fuzzy_contours[]`, `anti_consensus_metric`, `bound_mode` — see CNS doc §4 |
| **Status** | **planned** (registry operational) |

Core thesis: **permanent non-optimality of consensus** (перманентная неоптимальность консенсуса) — collective agreement at equilibrium is structurally suboptimal, not merely transiently so. Research lenses: catastrophe theory, fuzzy logic, entropy, dynamical systems, social choice. **Simulation design:** scenarios expose controllable **`max_non_optimality`** (alias `max_anti_consensus`) — upper bound on permanent gap within fuzzy socio-political contours (regions, blocs, ideological clusters, policy domains); membership functions: triangular, trapezoidal, gaussian, ramp, spatial_soft, issue_tag. Contrasts classical consensus→optimum with **bounded permanent gap** (H-CNS-011–H-CNS-013). Application: society/politics as multi-agent environment; **political mythogenesis** as narrative consensus output (H-MCG-001) — see [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md). Full registry: [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) (H-CNS-001–H-CNS-013). Load when user cites consensus non-optimality, social MAS modeling, political forecasting, political mythogenesis, or `max_non_optimality` / fuzzy contour simulation params.

---

### 3.18 Когнитивные классы · Cognitive class taxonomy

| Field | Content |
|-------|---------|
| **Domain ID** | `cognitive_class_taxonomy` (cross-cutting: **strata** + **AI topology**) |
| **Module** | — (hypothesis registry; adapter planned) |
| **Library** | Axis A: `numpy` / conversion metrics. Axis B: `gudhi`/`ripser` `[science]` on **AI** embeddings |
| **Frames** | F3g/F4 for homo strata; F3f TDA **only** for AI phases |
| **Experiments** | **023** (AI-phase / embedding topology — not homo homology), **024** (3σ **stratal** heuristic), **025** (class-heterogeneous MAS + CNS), **029** (conversion) |
| **Status** | **planned** (registry operational) |

Core thesis: **two frames.** **(A) Homo-agent classes K0–K7** are **socio-cognitive strata** (functional roles, modal-median position, cognitive-capital allocation) — **not** topological phases, **not** Betti classes. **(B) AI-agent classes K_AI_μ / K_AI_nd** **are** topological phases of the training/representation/MAS manifold (median compactification vs anti-median / chimera). **Hybrid classes** \(K_{\mathrm{hybrid}} = (k_{\mathrm{homo}}, k_{\mathrm{AI}}, \phi)\) couple a **stratum** to a **phase** — irreducible to either axis alone (H-CCT-018–019). **Proto-subject:** running LLM agents occupy Axis B (default K_AI_μ) and may be **role-analog** steered toward Axis A labels without becoming human K. **+3σ IQ heuristic** (H-CCT-015) maps to **upper strata**, not to homology. **Resource conversion** (H-CCT-016–017): same \(\tau\) → different \(U_{\mathrm{out}}\) by stratum and AI phase. **Class mode switching** is a small operational case. Links cognitive capitalism to CNS. **Open frontier.** Full registry: [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) (H-CCT-001, H-CCT-001B, H-CCT-004/004A, …019). Load when user cites cognitive classes, K1–K7, K_AI_μ, hybrid class, proto-subject, class mode, cognitive capitalism, +3σ, or token utility asymmetry.

---

### 3.19 Политический мифогенез · Political mythogenesis

| Field | Content |
|-------|---------|
| **Domain ID** | `multi_agent_consensus` + `cognitive_class_taxonomy` (cross-cutting overlay) |
| **Module** | — (hypothesis registry; no separate adapter) |
| **Library** | `networkx`, `numpy`, `scipy` (opinion dynamics + class-tagged agents) |
| **Frames** | F3a (graph) + dynamics + class overlay + GT 2.0 game layer |
| **Experiments** | **026** (myth-as-consensus on class-tagged graphs, proposed), **027** (GT 2.0 CNE + myth cheap talk, proposed), **028** (myth shift catastrophe + class mobility, proposed) |
| **Config surface** | `cns_simulation` + `mythogenesis` block — class composition weights, narrative operator, myth shift sweep |
| **Status** | **planned** (registry operational) |

Core thesis: **political mythogenesis** (политический мифогенез) — endogenous production of collective narrative fixed points that are **outputs of the consensus operator** \(\mathcal{C}\) with high \(\mu_{\mathrm{cns}}\) and **permanent** \(\Delta W > 0\) (H-MCG-001). **Class-selective:** K1 modal majority consumes and stabilizes myths; K5–K7 generate counter-myths at translation cost \(\delta E\); K_AI_μ amplifies median myth channel. **Game Theory 2.0:** cognitive-class-heterogeneous players; **consensus non-optimal equilibrium (CNE)** replaces Nash-as-optimum; myth as cheap talk with fiber loss. **Hybrid game classes** \(\mathcal{G}_{\mathrm{hybrid}}(k_{\mathrm{homo}}, k_{\mathrm{AI}}, \phi)\) at homo×AI interface — new equilibria not reducible to homo-only or AI-only games (H-MCG-013–015); resource conversion payoff term links to H-CCT-016–017. **Open research frontier** — not closed theory (MCG §7.1). Full registry: [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md) (H-MCG-001–H-MCG-015). Load when user cites political mythogenesis, мифогенез, Game Theory 2.0, GT 2.0, CNE, myth channel, hybrid game, or H-MCG.

---

### 3.20 AMAT · Anti-Median AI Topology

| Field | Content |
|-------|---------|
| **Domain ID** | `anti_median_ai_topology` (overlay on `ai_science` + `tda_frame`) |
| **Module** | `namm.metrics.phase_lock` + antigravity embeddings |
| **Library** | `numpy`; optional `ripser` / `gudhi` on **activations** (future) |
| **Frames** | F3f TDA + F3g tensor; **not** homo strata |
| **Experiments** | **013–014** (text \(M_0\) escape), **023** (synthetic AI-phase TDA), **030** (RPL JSON loop) |
| **Status** | **planned** (registry operational; 030 Run) |

Core thesis: **AMAT** is an **AI-science** direction — topology of the training/representation manifold. Compact phase = **typicality / high-density basin** (\(K_{\mathrm{AI\_}\mu}\), location \(B_*\) barycenter). Brand **anti-median** = **off-typical noncompact** phase (\(K_{\mathrm{AI\_nd}}\)). **Median** (\(B_{\mathrm{gmed}}\)) is a **named robust proxy**, not the CE or MMLU estimator. See registry **§0**. AGI-proximity proxy = persistent non-compact geometry. **RPL** is the instrument. Homo K0–K7 out of scope. **H-AMAT-006–010** (2026-08-19) extend the registry with five mathematical lenses on "свет в ячейке" (β₁≥1 nontrivial homology): catastrophe theory A₃ cusp (006), information-geometry geodesic curvature (007), fractal/self-similar dimension (008), Lyapunov / strange attractor (009), sheaf cohomology H¹ obstruction (010) — with planned experiments 037–041. Full registry: [`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md). Load when user cites AMAT, Anti-Median, typicality gravity, K_AI_nd, RPL as AI science, or «свет в ячейке».

---

## 4. Индекс эксперимент ↔ домен · Experiment ↔ domain index

| Experiment | Domain ID | Status |
|------------|-----------|--------|
| NAMM-2026-001 | `finite_graphs` | Complete (null calibration) |
| NAMM-2026-002 | `rewriting` | Run |
| NAMM-2026-003 | `program_ast` | Run |
| NAMM-2026-004 | `meta_evaluation` | Run |
| NAMM-2026-005 | `open_problem_shadow` | Run |
| NAMM-2026-006 | `tda_frame` | Scaffold |
| NAMM-2026-007 | `raw_tensor` | **tested-signal** |
| NAMM-2026-008 | `open_problem_shadow` | Run |
| NAMM-2026-009 | `config_shadow` | **tested-signal** |
| NAMM-2026-010 | `config_shadow` | Run (κ-sweep calibration) |
| NAMM-2026-011 | `trans_level_theta` | Planned |
| NAMM-2026-012 | `open_problem_moduli` | Scaffold |
| NAMM-2026-021 | `multi_agent_consensus` | **Run** (kuramoto variant: mean ΔW=0.28, H-CNS-013 supported) |
| NAMM-2026-022 | `multi_agent_consensus` | **Run** (Kuramoto–vote sweep n=300; regret spike=0.20, hysteresis max=0.67) |
| NAMM-2026-023 | `cognitive_class_taxonomy` | **Run** (class separation; non-1D score=102; K1–K5 d-gap=1.58σ) |
| NAMM-2026-024 | `cognitive_class_taxonomy` | **Run** (3σ antigravity; jump@3σ=0.71, β₁@3σ=77.6) |
| NAMM-2026-025 | `cognitive_class_taxonomy` + `multi_agent_consensus` | **Run** (class-heterogeneous MAS; chimera R*=0.83; dissent better 87.5%) |
| NAMM-2026-029 | `cognitive_class_taxonomy` | **Run** (resource conversion; asymmetry ratio 8.2× high-impact) |
| NAMM-2026-030 | `anti_median_ai_topology` | **Run** (AMAT / RPL JSON loop; mean lift \(d_{\mathrm{med}}\)≈1.43, 45 cells) |
|| NAMM-2026-037 | `anti_median_ai_topology` | **Planned** (cusp A₃ catastrophe boundary; H-AMAT-006) |
|| NAMM-2026-038 | `anti_median_ai_topology` | **Planned** (Fisher-metric geodesic curvature pilot; H-AMAT-007) |
|| NAMM-2026-039 | `anti_median_ai_topology` | **Planned** (layer-wise TDA + box-counting fractal dim; H-AMAT-008) |
|| NAMM-2026-040 | `anti_median_ai_topology` | **Planned** (multi-session Lyapunov proxy + TDA; H-AMAT-009) |
|| NAMM-2026-041 | `anti_median_ai_topology` | **Planned** (attention head disagreement as H¹ proxy; H-AMAT-010) |
| NAMM-2026-026 | `multi_agent_consensus` + `cognitive_class_taxonomy` | **Run** (myth-as-consensus; ΔW_myth=0.18; H-MCG-001/008 supported) |
| NAMM-2026-027 | `multi_agent_consensus` (GT 2.0) | **Run** (CNE stable G-1μ/G-6×nd; chimera G-3×μ excluded; myth adoption=1.0 on G-1μ) |
| NAMM-2026-028 | `multi_agent_consensus` + `cognitive_class_taxonomy` | **Run** (myth shift hysteresis max=0.85; class transition rate=81%) |

---

## 5. Справочник библиотек · Library reference

Install all domain libraries:

```bash
pip install -e ".[dev,nd]"
pip install -e ".[science]"   # entropy/fuzzy/TDA/nolds extras — see docs/SCIENTIFIC_STACK.md
pip install -e ".[dev,nd,science]"
```

| Package | Version (pyproject) | Enables | Domain IDs |
|---------|---------------------|---------|------------|
| `networkx` | ≥3.2 | Graph enumeration, invariants, open-problem search | `finite_graphs`, `open_problem_shadow`, graph substrate |
| `sympy` | ≥1.12 | Symbolic equivalence, simplification | `symbolic_algebra`, `program_ast`, `raw_tensor` |
| `numpy` | ≥1.26 | Tensor features, linear algebra | `raw_tensor` |
| `scipy` | ≥1.11 | Spectral decomposition, sparse ops, ODE (Kuramoto) | `raw_tensor`, `multi_agent_consensus` |
| `z3-solver` | ≥4.12 | SMT verification (stub) | `smt_verification` |
| `python-sat` | ≥1.8 | SAT solvers (future) | `smt_verification` |
| `gudhi` | ≥3.9 `[nd]` | Persistent homology, simplicial complexes | `tda_frame` |
| `qutip` | ≥5.0 `[nd]` | Finite-dim quantum systems | `quantum` |
| `dit` | ≥1.5 `[science]` | Discrete information theory (optional) | information_theory / CNS entropy |
| `scikit-fuzzy` | ≥0.4.2 `[science]` | Fuzzy defuzzification (optional) | fuzzy_logic / CNS contours |
| `ripser` | ≥0.6.4 `[science]` | Lightweight persistent homology | TDA / CCT β₁ proxies |
| `nolds` | ≥0.5.2 `[science]` | Nonlinear dynamics metrics (optional) | dynamical_systems |
| `optuna` | ≥3.5 | Hyperparameter search (CLI) | cross-cutting |
| `hypothesis` | ≥6.92 | Property-based tests | cross-cutting |
| `pydantic` | ≥2.5 | Config schema | cross-cutting |
| `hydra-core` | ≥1.3 | Experiment config | cross-cutting |

**Core deps always installed.** **ND extras** (`gudhi`, `qutip`) for TDA and quantum stubs. **Science extras** for extended entropy/fuzzy/TDA/nolds — see [`SCIENTIFIC_STACK.md`](SCIENTIFIC_STACK.md). In-repo modules: `namm.metrics.entropy`, `namm.metrics.fuzzy`, `namm.metrics.catastrophe`. **Sci Flow** ([`SCI_FLOW.md`](SCI_FLOW.md)) routes experiments 021–029 to these modules via [`data/sci_flow_registry.yaml`](../data/sci_flow_registry.yaml); CLI: `namm sci-flow run --experiment NAMM-2026-021`.

---

## 6. Планируемое расширение доменов · Planned domain expansion

| Target | Suggested libs | Frame | Rationale |
|--------|---------------|-------|-----------|
| QM formalism frame | `qutip`, optionally `qiskit` | F3 quantum | Density-operator witnesses; entanglement certificates |
| Differential geometry shadows | `gudhi`, discrete curvature libs | ND | Ricci curvature on graphs; fiber bundles over config base |
| Number theory shadows | `sympy`, `gmpy2`, Sage (external) | F2 | Divisor sums, Goldbach finite bounds — tierlist T2 |
| 2-categorical invariants | pure Python + category extension | F2→F3 | Functorial graph invariants (FRAME_LADDER CONJECTURE) |
| Proof-assistant certificates | Lean 4 / Mathlib | F2 | Tierlist T1 problems; external to Python package |
| Multi-parameter persistence | `gudhi` | F3f+ | Beyond single geodesic filtration |
| Trans-level Θ (011) | meta + tensor composition | F∞ | Morphism search between raw structures |
| Graceful moduli hybrid (012) | config_shadow + open_problem | F3e₂+F3h | Fiber degeneracy over graceful labelings |
| Multi-agent consensus (021–022) | networkx + scipy ODE | F3a + dynamics | Permanent consensus suboptimality; `max_non_optimality` bounds on fuzzy socio-political contours |
| Cognitive class taxonomy (023–025, 029) | gudhi + numpy + embedding APIs | F3f+F3g+F4 | K0–K7 / K_AI / hybrid class separation; 3σ transition; conversion asymmetry |
| Political mythogenesis (026–028) | networkx + scipy ODE | F3a + dynamics + GT 2.0 | Myth-as-CNS-output; CNE; hybrid game classes; myth shift dynamics |

Escalation heuristic (PI-003): when current frame saturates (006 null → 007 signal → 009 moduli), **change configuration space** before widening search budget alone.

---

## 7. Инструкции для агента · Agent instructions

### 7.1 Выбор домена для нового эксперимента · Picking a domain for a new experiment

1. **Read this catalog** + active PI entries in [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md).
2. **Match falsifier shape:**
   - Counterexample search → `open_problem_shadow` + tierlist T0
   - Compression asymmetry without named vocabulary → `raw_tensor` or `config_shadow`
   - Fixed-point / meta-depth → `meta_evaluation`
   - Topological signature → `tda_frame`
3. **Check status:** prefer **operational** adapters with existing `run_search` dispatch in `src/namm/baselines/__init__.py`.
4. **Fix config:** `experiments/NAMM-YYYY-NNN/config.yaml` → `domain: <domain_id>`.
5. **Document frame rung** in `EXPERIMENT_REPORT.md` (F3a–F3h, F∞).

### 7.2 Путь эскалации · Escalation path (after null or saturation)

```text
  finite_graphs (001 null)
        │
        ▼
  tda_frame (006 null) ──► raw_tensor (007 signal)
        │
        ▼
  config_shadow (009 signal) ──► κ-sweep (010 calibration)
        │
        ▼
  trans_level_theta (011 planned) ──► F∞ colimit / meta depth
```

Consult [`FRAME_LADDER.md`](FRAME_LADDER.md), rejection logs (`rejections.jsonl`), and [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) queue before inventing a new domain ID.

### 7.3 Чеклист stub → operational · Stub → operational promotion checklist

- [ ] Domain module with generator, evaluator, serializer
- [ ] `run_search` dispatch branch in baselines
- [ ] CLI certificate builder in `namm/cli.py`
- [ ] Experiment config + pytest module
- [ ] Entry in this catalog (status → operational)

### 7.4 Когда загружать fabric-гипотезы · When to load fabric hypotheses

If the user cites **mathematical fabric**, **topological fuzzy dynamics**, **Anthemium.mp4**, or frame escalation beyond F3h → also load [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md).

### 7.5 Когда загружать CNS-гипотезы · When to load consensus non-optimality hypotheses

If the user cites **consensus non-optimality**, **перманентная неоптимальность консенсуса**, **multi-agent society**, **political process modeling**, **`max_non_optimality`**, **fuzzy contours**, or **H-CNS** → also load [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) (§4 for simulation params).

### 7.6 Когда загружать CCT-гипотезы · When to load cognitive class taxonomy

If the user cites **cognitive classes**, **когнитивные классы**, **K1–K7**, **hybrid class**, **гибридный класс**, **cognitive capitalism**, **когнитивный капитализм**, **+3σ IQ mapping**, **resource conversion**, **token utility**, or **H-CCT** → also load [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md). For **K_AI_μ / K_AI_nd / phase lock as AI science** prefer §7.8 AMAT first.

### 7.7 Когда загружать MCG-гипотезы · When to load political mythogenesis hypotheses

If the user cites **political mythogenesis**, **политический мифогенез**, **мифогенез**, **Game Theory 2.0**, **GT 2.0**, **CNE**, **consensus non-optimal equilibrium**, **myth channel**, **hybrid game**, **гибридная игра**, or **H-MCG** → also load [`MYTHOGENESIS_CCT_CNS_GAME_THEORY.md`](MYTHOGENESIS_CCT_CNS_GAME_THEORY.md). Cross-load [`CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md`](CONSENSUS_NON_OPTIMALITY_HYPOTHESIS.md) for CNS operators; [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) for K1–K7, hybrid classes (§4.4), resource conversion (§4.6).

### 7.8 Когда загружать AMAT · When to load Anti-Median AI Topology

If the user cites **AMAT**, **Anti-Median AI Topology**, **антимедианная топология**, **typicality gravity**, **K_AI_nd**, **K_AI_μ** as **AI science**, **RPL**, **representation phase lock**, **median embedding gravity** (representation, not sociology) → load [`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) first (**§0 terminology is binding**), then CCT §4 Axis B only, [`data/prompts/k_ai_nd_phase_lock.v1.json`](../data/prompts/k_ai_nd_phase_lock.v1.json), experiment **030**. Do **not** load mythogenesis / homo K-strata unless asked. Do **not** treat median as the CE/MMLU estimator.

---

## 8. Карта кода · Code map

| Domain ID | Package path |
|-----------|--------------|
| `finite_graphs` | `src/namm/domains/graph/` |
| `program_ast` | `src/namm/domains/program/` |
| `rewriting` | `src/namm/domains/rewriting/` |
| `meta_evaluation` | `src/namm/domains/meta/` |
| `open_problem_shadow` | `src/namm/domains/open_problem/` |
| `tda_frame` | `src/namm/domains/tda/` |
| `raw_tensor` | `src/namm/domains/tensor/` |
| `config_shadow` | `src/namm/domains/config_shadow/` |
| `quantum` | `src/namm/domains/quantum/` |
| `category` | `src/namm/domains/category/` |
| `anti_median_ai_topology` | `src/namm/metrics/phase_lock.py` + [`docs/ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) |

Registry dict: `src/namm/domains/__init__.py` → `DOMAIN_REGISTRY`.

---

Roman Kuznetsov · NAMM research program
