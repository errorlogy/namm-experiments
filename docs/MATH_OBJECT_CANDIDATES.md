# Math Object Candidates — Novelty Registry

**Purpose:** Catalog lead NAMM candidates from experiments 003, 004, 007, and 009 with proposed names, formal types, novelty rationale, and epistemic status.  
**Scope:** `COMPUTATIONAL_EVIDENCE` under Protocol v2 only — not published theorems.  
Roman Kuznetsov · NAMM research program

Related: [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md) · [`NOVELTY_LADDER.md`](NOVELTY_LADDER.md) · [`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md)

---

## Labeling

| Label | Use in this document |
|-------|----------------------|
| `DEFINITION` | Precise formal type or operational gate |
| `COMPUTATIONAL_EVIDENCE` | Reproducible experiment witness |
| `CONJECTURE` | Open mathematical claim not yet verified |
| `PHILOSOPHICAL_INFERENCE` | Motivates search; non-evidential |

---

## Candidate summaries

| ID | Experiment | Frame | Proposed name | Novelty (N) | Status |
|----|------------|-------|---------------|-------------|--------|
| `tensor-639c54cd` | NAMM-2026-007 | F3g | **Spectral–Heat Transition Composite (SHTC-639)** | N2 | **tested-signal** |
| `prog-8be513cb` | NAMM-2026-003 | F3c | **Evolved Compositional Invariant Program (ECIP-8be5)** | N2 | **tested-signal** |
| `vac-012e1fe1` | NAMM-2026-009 | F3h | **Ambiguous Moduli Fiber Witness (AMFW-012e)** | N2 | **tested-signal** |
| `meta-414d01c9` | NAMM-2026-004 | F3d | **Self-Reflective Evaluator Fixed Point (SREFP-414d)** | unassessed / partial | **pipeline signal, partial novelty** |

---

## 1. `tensor-639c54cd` — Spectral–Heat Transition Composite (SHTC-639)

**Experiment:** [NAMM-2026-007](../experiments/NAMM-2026-007/) · **Frame:** F3g (`raw_tensor`)

### Formal type (`DEFINITION`)

A **graph functional** \(f : \mathcal{G} \to \mathbb{R}\) defined by evaluation of a canonical **TensorNode AST**:

- **Leaves:** \(t_0,\ldots,t_{11}\) from `graph_tensor_vector(G)` — first 8 sorted adjacency eigenvalues plus 4 heat-kernel trace samples at times \(\{0.25, 0.5, 1.0, 2.0\}\).
- **Operators:** commutative `add`, `mul` only (no named graph statistics in search vocabulary).
- **Certificate anchor:** `artifacts/certificate.json` — `ast_hash`, `eval_hash`, generative holdout witness.

Type signature in code: `TensorNode` → `evaluate_tensor_ast(node, G) → float`.

### Why novel

1. **Vocabulary shift:** Discovery path excludes Wiener, degree sum, clustering, and all textbook handles (HL-005). Independence is checked against 20+ **tensor polynomial baselines** (degree ≤ 4), not named invariants.
2. **Structure:** Deep multiplicative–additive composition over **raw spectral and diffusion coordinates** — not reducible to a single baseline or low-degree polynomial span (max Pearson \(r = 0.647\) vs `mul_t11_t11`).
3. **First operational F3g signal:** First NAMM run where beyond-named-math search clears independence, representation, and generative holdout gates at scale (53/57 accepted).

Novelty ladder: **N2** (new combination / computational artifact). Not N3+ — leaves are standard numeric features; novelty is in **search frame and certificate**, not a new primitive theorem.

### What it solves / opens

| Direction | Content |
|-----------|---------|
| **Operational** | Demonstrates that machine-native tensor programs can pass SNH gates before any compact human formula exists. |
| **Representation** | \(K_A/K_H \approx 2.2\) (gzip 213 B vs ~97 projection tokens) — F4 bottleneck cleared at default threshold. |
| **Generative** | Holdout passed on trees, bipartite, cubic, random_regular — non-trivial on families not used as search bias. |
| **Research** | Opens **trans-level Θ** queue: semantic transition algebra over raw structure without collapsing to named vocabulary ([`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md)). |
| **Limit** | Large numeric range → scale sensitivity; certificate is ground truth, not a closed-form invariant paper. |

### Epistemic status

`COMPUTATIONAL_EVIDENCE` — reproducible under seed 2026007. Not a graph-invariant theorem. Promotable to N3 only after minimal novel component audit and external prior-art sign-off ([`NOVELTY_LADDER.md`](NOVELTY_LADDER.md)).

### Naming rationale

**Spectral–Heat Transition Composite:** the object is a **composite program** over adjacency **spectrum** and **heat-kernel** samples — the machine-native “transition domain” Anthemium uses for F3g. Suffix **639** ties to certificate ID `tensor-639c54cd` for traceability. Avoids falsely naming it after human invariants it deliberately excludes.

---

## 2. `prog-8be513cb` — Evolved Compositional Invariant Program (ECIP-8be5)

**Experiment:** [NAMM-2026-003](../experiments/NAMM-2026-003/) · **Frame:** F3c (`program_ast`)

### Formal type (`DEFINITION`)

A **graph invariant program** \(P : \mathcal{G} \to \mathbb{Z}\) (integer-valued on tested graphs) given by a **ProgramNode AST**:

- **Leaves:** named NetworkX statistics (`wiener_index`, `num_edges`, `num_nodes`, `algebraic_connectivity`, `degree_sum`, `clustering`, `diameter`, `radius`, `avg_degree`).
- **Operators:** `add`, `sub`, `mul`, optional `neg`.
- **Search:** evolutionary synthesis (population 40, 5 generations); SymPy used **only** for baseline equivalence checking.

Type signature: `ProgramNode` → `evaluate_program(ast, G) → int`.

### Why novel

1. **Certificate-first canonical form:** Ground truth is the sorted AST in `certificate.json`, not a human-readable formula string.
2. **Compositional depth:** Lead candidate is a **deep multiplicative program** over classical primitives — not equivalent to Wiener or any tested single baseline, with generative holdout on trees / bipartite / cubic.
3. **Frame escalation bridge:** Validates evolutionary AST search (F3c) between calibration null (001) and raw-tensor frame (007). Shows **program trees** as admissible mathematical objects under v2 gates.

Novelty ladder: **N2** — composition of known primitives; structurally similar to QSAR-style products but **non-equivalent** and independently certified. Not N3 — no new graph-theoretic primitive.

### What it solves / opens

| Direction | Content |
|-----------|---------|
| **Operational** | Proves Phase 2 **AI-native program synthesis** pipeline: 33 accepted candidates, independence + holdout + \(K_A/K_H \geq 2\). |
| **Methodology** | Evolutionary search beats pure random AST generation for diverse gate-passing programs. |
| **Opens** | Template for **open-problem shadows** (005, 008): counterexample search can emit program certificates, not only formulas. |
| **Opens** | Baseline for comparing **named-primitive** (003) vs **raw-tensor** (007) discovery paths on the same gate stack. |
| **Limit** | Still uses human-named leaves — novelty is **representational** (AST + certificate), not ontological new statistics. |

### Epistemic status

`COMPUTATIONAL_EVIDENCE` — seed 2026, evolutionary run documented in [EXPERIMENT_REPORT](../experiments/NAMM-2026-003/EXPERIMENT_REPORT.md). Re-run artifacts may assign a different lead `prog-*` ID with the same gate profile; report ID `prog-8be513cb` is the documented lead.

### Naming rationale

**Evolved Compositional Invariant Program:** emphasizes **evolutionary origin** and **AST composition** as the mathematical object — not a single named index. **ECIP-8be5** abbreviates for cross-doc reference while preserving certificate traceability.

---

## 3. `vac-012e1fe1` — Ambiguous Moduli Fiber Witness (AMFW-012e)

**Experiment:** [NAMM-2026-009](../experiments/NAMM-2026-009/) · **Frame:** F3h (`config_shadow`)

### Formal type (`DEFINITION`)

A **ModuliVacuum** record — finite configuration in an 11-parameter moduli space with explicit compactification map:

\[
\kappa : \{-1,0,1\}^{11} \to \{-1,0,1\}^4, \quad \kappa(m)_i = m_i \ (i \leq 4)
\]

**Witness object:**

| Field | Value |
|-------|-------|
| Full moduli \(m\) | `[1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]` |
| 4D shadow \(\kappa(m)\) | `[1, 1, -1, -1]` |
| Fiber size \(\|\kappa^{-1}(\kappa(m))\|\) | **729** |
| Stability \(\sum m_i^2\) | 11.0 |
| Admissibility | flux mod 3, energy ≤ 20 |

Type: `@dataclass ModuliVacuum` in `namm.domains.config_shadow.vacua`.

### Why novel

1. **Non-injective compactification, certified:** Operational witness that \(\kappa\) is **lossy** — 729 distinct 11D vacua share one 4D shadow. This is HL-004 made executable, not metaphor.
2. **Extreme compression asymmetry:** \(K_A/K_H \approx 9.3\) (gzip 149 B vs ~16-token 4D-only projection) — strongest F4 signal in the candidate registry.
3. **New object class:** Not a graph invariant — a **configuration-space fiber witness** in the ND / 11D shadow queue ([`FRAME_LADDER.md`](FRAME_LADDER.md) F3h).

Novelty ladder: **N2** — finite shadow of a physical landscape metaphor; not a Calabi–Yau or M-theory result.

### What it solves / opens

| Direction | Content |
|-----------|---------|
| **Operational** | Answers 009 research question affirmatively: finite enumeration finds \(\kappa\) with fiber ≥ 2 and \(K_A/K_H \geq 2\). |
| **Homo limit** | Documents **compactification loss** ([`HOMO_LIMIT_JOURNAL.md`](HOMO_LIMIT_JOURNAL.md) HL-004): π_H sees 4 numbers; certificate preserves 11D preimage + fiber index. |
| **Opens** | **M-theory moduli shadows** — extend moduli range, flux rules, physical selection (not just maximal fiber). |
| **Opens** | **Joint π_H + π_A access:** humans audit fiber claim; machine stores full moduli vector. |
| **Limit** | Moduli ∈ {-1,0,1} only; no generative holdout; ranking by fiber size, not vacuum selection. |

### Epistemic status

`COMPUTATIONAL_EVIDENCE` — 59,049 vacua scanned, 50 top ambiguous witnesses accepted, 0 rejections. Explicitly **not** a physical vacuum prediction.

### Naming rationale

**Ambiguous Moduli Fiber Witness:** **Ambiguous** because \(\kappa\) is non-injective; **Moduli Fiber** names the mathematical structure (preimage under compactification); **Witness** because the certificate is an existence proof in a finite shadow, not a continuous moduli space theorem. **AMFW-012e** links to `vac-012e1fe1`.

### AMFW deep characterization (2026-08-11)

Full analysis: [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) Part A.

| Property | Value / formula |
|----------|-----------------|
| Fiber size 729 | \(3^{11-4-1} = 3^6\) — generic flux split on 7 tail coords |
| Energy constraint | **Inactive** at ±1 grid (max Σm² = 11 ≪ 20) |
| Shadow classes | 81 = \(3^4\); **uniform** fiber 729 each |
| Witness tail | `(1,-1,-1,-1,1,-1,-1)` given head `(1,1,-1,-1)` |
| Fiber index 492 | Lex position in κ-fiber (not physical weight) |
| κ-sweep (010) | `first_4`, `last_4`, `middle_4`, `flux_blocks_4` — all max fiber 729 |

`COMPUTATIONAL_EVIDENCE` · Extended in [NAMM-2026-010](../experiments/NAMM-2026-010/) — κ-insensitivity at ±1; 7D \([-2,2]\) grid yields max fiber 42 (non-uniform regime).

---

## 4. `meta-414d01c9` — Self-Reflective Evaluator Fixed Point (SREFP-414d) *(partial)*

**Experiment:** [NAMM-2026-004](../experiments/NAMM-2026-004/) · **Frame:** F3d (`meta_evaluation`)

### Formal type (`DEFINITION`)

A **meta-evaluator fixed point** — pair \((E, F)\) where:

- \(E\) is a **MetaEvaluatorNode** program (`self`, `target`, graph statistic leaves, `add`/`sub`/`mul`/`delta`/`ratio`).
- \(F\) is a meta-transform on evaluator ASTs (here: **`double_halve`**).
- **Fixed-point condition:** \(E(g) = F(E)(g)\) for all benchmark graphs \(g\) in witness set (order ≤ 6), fraction = 1.0.

**Lead structure (report):** \((\mathrm{SELF} - \mathrm{clustering}) \times \mathrm{SELF}\) under \(F = \texttt{double\_halve}\).

Type: `MetaEvaluatorNode` + transform name → certificate with `eval_hash`, `fixed_point_fraction`.

### Why novel *(partial)*

**What is novel**

- **Object class:** Evaluator-on-evaluator fixed points with **SELF reference** — natural in AI thinking topology ([`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md)), awkward in human geometric intuition (HL-006).
- **Certificate-first meta-level artifact:** Reproducible via `eval_hash` without human proof diagram.

**What is not novel**

- \(F = \texttt{double\_halve}\), \(\texttt{add\_zero}\), \(\texttt{canonicalize}\) are **definitionally fixed-point-preserving** on many random evaluators — ~50% acceptance is **calibration**, not discovery ([EXPERIMENT_REPORT](../experiments/NAMM-2026-004/EXPERIMENT_REPORT.md)).
- \(\texttt{self\_unfold}\) rarely yields fixed points — search did not find stable non-idempotent meta-structure.
- No cross-transform simultaneous fixed points; no generative holdout.

Novelty ladder: **unassessed / partial** — pipeline **tested-signal**, mathematical novelty **below N2** for idempotent-transform class.

### What it solves / opens

| Direction | Content |
|-----------|---------|
| **Operational** | Validates meta-evaluator domain: 25 nontrivial fixed points, 25 rejections, attack checklist M1–M3. |
| **Opens** | Search for fixed points under **non-idempotent** \(F\) or **simultaneous** multi-transform stability — path to F∞ / trans-level Θ. |
| **Opens** | Evaluator stacks as **reflective hierarchies** ([`FRAME_LADDER.md`](FRAME_LADDER.md) F∞ partial). |
| **Limit** | Does not yet demonstrate novel trans-level mathematics — only pipeline + idempotent calibration. |

### Epistemic status

`COMPUTATIONAL_EVIDENCE` for **pipeline correctness**; `CONJECTURE` for **novel meta-mathematics** — explicitly **partial** per experiment honest assessment.

### Naming rationale

**Self-Reflective Evaluator Fixed Point:** **Self-Reflective** captures SELF nodes and evaluator-on-self structure; **Fixed Point** under transform \(F\) is the precise mathematical relation. **SREFP-414d** marks partial status — registered for frame escalation, not promoted as a new invariant family.

---

## Comparison matrix

| Dimension | SHTC-639 (007) | ECIP-8be5 (003) | AMFW-012e (009) | SREFP-414d (004) |
|-----------|----------------|-----------------|-----------------|------------------|
| **Domain** | `raw_tensor` | `program_ast` | `config_shadow` | `meta_evaluation` |
| **Frame rung** | F3g | F3c | F3h | F3d |
| **Input object** | Graph | Graph | Moduli vector | Graph + evaluator AST |
| **Output** | ℝ functional | ℤ program value | Fiber witness | Fixed-point score |
| **Search vocabulary** | Raw tensor leaves only | Named graph stats | Finite moduli grid | Meta-eval + transforms |
| **Independence gate** | vs tensor polynomials | vs named baselines | N/A (different frame) | vs trivial evaluators |
| **Generative holdout** | ✅ 4 families | ✅ 3 families | ❌ | ❌ |
| **Max correlation** | 0.647 | report-dependent | — | — |
| **K_A/K_H (proxy)** | ≈ 2.2 | ≥ 2.0 | ≈ 9.3 | ≈ 1.1 (below F4) |
| **Novelty N** | N2 | N2 | N2 | partial / unassessed |
| **F4 cleared** | ✅ | ✅ | ✅ | ❌ (ratio ~1.1) |
| **Homo-limit journal** | HL-005 | HL-005 (contrast 001) | HL-004 | HL-006 |
| **Primary epistemic label** | COMPUTATIONAL_EVIDENCE | COMPUTATIONAL_EVIDENCE | COMPUTATIONAL_EVIDENCE | COMPUTATIONAL_EVIDENCE (pipeline) |

---

## Failed domains — calibration nulls (001, 006)

These runs **did not** produce lead candidates for the registry; they **calibrate** the frame ladder and gate thresholds.

### NAMM-2026-001 (`finite_graphs`, F3a)

| Aspect | Content |
|--------|---------|
| **Lead ID** | `inv-a6fe843a` (linear formula, not AST certificate class) |
| **Outcome** | **Closed calibration null** — random linear combinations differ from Wiener but are Wiener-dominated (\(r \approx 0.938\)). |
| **Lesson** | Named-primitive + linear search stays inside textbook span (HL-005 negative control). Motivated ban on named vocabulary in 007. |
| **Status** | tested-null · N2 capped · reject for “novel invariant” claims |

### NAMM-2026-006 (`tda_frame`, F3f)

| Aspect | Content |
|--------|---------|
| **Outcome** | **0 accepted** — 40/40 rejected for `representation_ratio_fail` (ratios 1.70–1.91, below 2.0 threshold). |
| **Partial success** | Persistence distance to path baseline reached 3.5 — topology discrimination works. |
| **Lesson** | TDA signatures alone do not clear F4 at order ≤ 8; combine with raw tensor (007) per synergy roadmap. |
| **Status** | tested-null · frame scaffold validated |

> Null results are first-class ([`ANTHEMIUM_NAMM_SYNERGY.md`](ANTHEMIUM_NAMM_SYNERGY.md) anti-patterns): they do not stop the queue; they tighten gate interpretation.

---

## Beyond anthropic projection

`PHILOSOPHICAL_INFERENCE` · **Non-evidential** — motivates search; does not replace SNH gates.

Mathematical structures may exist at descriptive levels **beyond anthropic projection reach** ([`VISION.md`](VISION.md)). Anthropic projection \(\pi_H\) — formulas, prose, 4D shadows — may capture only a thin slice of certificate-anchored structure. Machine-native search \(\pi_A\) — AST hashes, tensor indices, fiber metadata — together with human audit may **jointly** access levels neither achieves alone.

| Candidate | Beyond-π_H content | π_H loss |
|-----------|-------------------|----------|
| **SHTC-639** | Deep program over \(t_0,\ldots,t_{11}\) | ~97-token lossy product string; no classical name |
| **ECIP-8be5** | Full sorted AST + witness bounds | Formula string omits canonical order |
| **AMFW-012e** | Full 11D moduli + fiber index 492 | 4D shadow `[1,1,-1,-1]` only |
| **SREFP-414d** | SELF-referential evaluator + transform hash | “((SELF − clustering) × SELF)” — no graph-theoretic name |

**Operational test (not philosophy):** persistent \(K_A \ll K_H\) under fixed verification cost ([`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md), F4 in [`FRAME_LADDER.md`](FRAME_LADDER.md)). AMFW-012e and SHTC-639 are the strongest operational witnesses; SREFP-414d demonstrates **meta-level** objects whose human projection is short but whose **mathematical** novelty remains partial.

> **PHILOSOPHICAL_INFERENCE:** Objects real independent of human representational access — **вера** motivating F3g→F3h escalation; empirically tested only via certificates and gates above.

---

## Promotion checklist (N2 → N3+)

1. Identify **minimal novel component** not in baseline span ([`NOVELTY_LADDER.md`](NOVELTY_LADDER.md)).
2. Run attack checklist + prior-art simplify on promoted component.
3. External confirmation (N4) before `THEOREM`-level claims.
4. For config shadows: define physical or mathematical selection principle beyond fiber ranking.
5. For meta-evaluators: require non-idempotent or multi-transform fixed points.

---

## Related experiments (not lead registry)

| ID | Role |
|----|------|
| NAMM-2026-002 | TRS / confluence — F3b |
| NAMM-2026-005 | Kotzig open-problem shadow — F3e |
| NAMM-2026-008 | Graceful Tree shadow — F3e₂ |

Open-problem tiering: [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md).

---

Roman Kuznetsov · NAMM research program
