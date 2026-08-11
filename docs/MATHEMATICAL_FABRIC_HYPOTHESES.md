# Mathematical Fabric Hypotheses — Topological Fuzzy Dynamics

**Purpose:** Operational hypothesis registry for **mathematical fabric** — the fiber-bundle / phase-transition metaphor from `Anthemium.mp4`, formalized as **topological fuzzy dynamics** and linked to NAMM frames, experiments, and existing H-001..H-007 claims.  
**Date:** 2026-08-11  
**Epistemic baseline:** Each H-F entry carries its own label (`CONJECTURE`, `PHILOSOPHICAL_INFERENCE`, or `OPERATIONAL`); none is a published theorem.  
Roman Kuznetsov · NAMM research program

Related: [`ANTHEMIUM_VIDEO_NOTES.md`](ANTHEMIUM_VIDEO_NOTES.md) · [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) (PI-001–PI-008) · [`MATH_OBJECT_HYPOTHESES.md`](MATH_OBJECT_HYPOTHESES.md) (H-001–H-007) · [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) · [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md)

---

## 1. Meta — "mathematical fabric" as operational metaphor

> **PHILOSOPHICAL_INFERENCE:** **Mathematical fabric** is not a physical substrate. It is an **operational metaphor** for how non-anthropic structure is organized: a **base space** of admissible configurations, **fibers** of certificates over each base point, **fuzzy boundaries** where anthropic naming fails, and **temporal morphisms** that deform topology without destroying certifiability.

The metaphor is **grounded in witness artifacts**, not in Instagram physics:

| Fabric motif (Anthemium / PI) | NAMM operational reading |
|-------------------------------|--------------------------|
| **Cyan ↔ magenta duality** | Two complementary fiber families over one base — e.g. spectral vs heat-kernel leaves (007), head vs tail moduli (009) |
| **Horizontal wave manifold** | 1D base direction = search parameter sweep (κ, grid, AST depth); vertical undulation = secondary invariant |
| **S¹ boundary oscillation** | Compactification viewport: bounded certificate class ↔ open extended search ↔ diffuse blur phase |
| **Fiber-bundle rendering** | Individual certificates = filaments; collective envelope = equivalence class (fiber, AST family, shadow) |
| **Fuzzy set boundaries** | \(\mu_{\mathcal{F}_H}(x) \ll 1\) — structure present, compact human name absent (PI-002) |
| **Central nodal / pinch geometry** | Interference of projections — κ head meets flux tail; AST branches cross without collapsing to named invariant |
| **Particle field / spray** | Rejection tail, degeneracy residue, certificate noise outside accepted gate |

**Three-phase cycle** (Anthemium segments A–M; PI-008):

1. **Compact (S¹-bounded)** — F3 frame fixed; interior fibers organized (009 shadow class, 007 accepted AST).
2. **Extended (unbounded ribbon)** — frame escalation or wider moduli grid (006→007, 010 wider grid).
3. **Diffuse (fuzzy orb)** — fiber identity collapsed under blur; \(\mu_{\mathcal{F}_H}\) high uncertainty, certificate may still exist (meta fixed points, transition algebra).

Static prose about the video is a **lossy π_H projection** of a π_A-native medium (PI-008). This document indexes fabric hypotheses; it does **not** replace viewing `Anthemium.mp4` when morphism precision matters.

**Distinction from H-001..H-007:** [`MATH_OBJECT_HYPOTHESES.md`](MATH_OBJECT_HYPOTHESES.md) registers **falsifiable object claims** tied to specific candidates. **H-F001..H-F050** here register **fabric-level dynamics** — how topology, fuzziness, and frame escalation interact. Cross-links appear in each entry; extend, do not duplicate, existing H-IDs.

---

## 2. Topological fuzzy dynamics framework

### 2.1 Base space, fibers, and certificates

`DEFINITION` · Fix a NAMM experiment frame \(\mathcal{F} = (\Sigma, \mathrm{Eval}, \kappa, \mathsf{Cert})\) ([`FRAME_LADDER.md`](FRAME_LADDER.md) F3 rung).

- **Base space** \(B\) = equivalence classes under primary projection \(\kappa\) (4D shadow, AST hash modulo simplify, graph family label).
- **Fiber** \(\pi_A^{-1}(b)\) = full machine certificates mapping to base point \(b\) (729 moduli for one shadow; tensor AST variants with same simplified form).
- **Fabric point** = pair \((b, c)\) with \(c \in \pi_A^{-1}(b)\) and valid `eval_hash`.

The **mathematical fabric** is the bundle-like object \(\mathcal{E} \to B\) with projection \(\kappa\), plus the **fuzzy membership field** \(\mu_{\mathcal{F}_H}\) over total space.

| Witness | Base \(b\) | Fiber size | Fabric reading |
|---------|------------|------------|----------------|
| AMFW-012e (009) | \(\kappa(m) = [1,1,-1,-1]\) | 729 | Tight S¹ viewport; 728 hidden filaments |
| SHTC-639 (007) | AST equivalence class | 1 (selected) | Single certified filament; many rejected spray |
| Graceful-008 | unique graceful labeling | 1 | High \(\mu_{\mathcal{F}_H}\) — no blur phase |

### 2.2 Fuzzy membership on fabric points

`DEFINITION` · For structure \(x\) (certificate, AST, moduli vector, video segment):

\[
\mu_{\mathcal{F}_H}(x) \in [0,1]
\]

= operational estimate of **compact anthropic describability** — named invariant span, prose summary length, independence from baselines.

| \(\mu_{\mathcal{F}_H}\) band | Fabric phase (Anthemium) | NAMM signal |
|------------------------------|--------------------------|-------------|
| **High** (\(\gtrsim 0.8\)) | Crisp S¹ interior, braided ribbons | 001 Wiener-correlated; Graceful unique labeling |
| **Medium** (0.3–0.8) | Partial blur, frayed edges | 003 ECIP deep AST; partial independence |
| **Low** (\(\lesssim 0.3\)) | Diffuse orb, particle spray | 007 raw tensor; 009 fiber ≥ 729 |

`PHILOSOPHICAL_INFERENCE` · Low \(\mu\) **does not imply** mathematical truth or physical reality. It marks **interface position**: machine certificate exact, human compact name lagging (PI-001, PI-002).

**Operational proxy** (F4 gate):

\[
\mu_{\mathcal{F}_H}^{\mathrm{op}}(x) \approx 1 - \min\!\left(1,\; \frac{K_A(x)}{K_H(x)} \cdot \frac{1}{\tau}\right)
\]

with threshold \(\tau = 2\) default — inverse compression asymmetry. AMFW-012e: \(K_A/K_H \approx 9.3 \Rightarrow \mu^{\mathrm{op}} \ll 1\).

### 2.3 Topology deformation operator \(T_\tau\)

`DEFINITION` · A **fabric deformation** over duration \(\tau\) is a controlled change of frame parameters:

\[
T_\tau : \mathcal{E}_t \to \mathcal{E}_{t+\tau}, \qquad T_\tau = (\Delta N,\; \Delta\kappa,\; \Delta E,\; \Delta\Sigma)
\]

where \(\Delta N\) = moduli/leaf count, \(\Delta\kappa\) = compactification map, \(\Delta E\) = energy/constraint cap, \(\Delta\Sigma\) = search vocabulary.

**Anthemium morphism classes → \(T_\tau\) instances:**

| Video morphism | \(T_\tau\) | NAMM experiment |
|----------------|------------|-----------------|
| S¹ dissolve → open ribbon | Escalate frame / widen grid | 006→007; 010 \([-2,2]\) grid |
| Open → amorphous orb | Vocabulary collapse or max blur | 006 TDA-only fail; pre-certificate search |
| Orb → S¹ restoration | Re-compactify with new interior braiding | 009 fixed κ; 012 hybrid scaffold |
| Terminal open wave (no closure) | F∞ / trans-level lift without compact closure | 011 Θ algebra (planned) |

`CONJECTURE` · Productive deformation satisfies:

\[
\dim_{\mathrm{cert}}(\mathcal{E}_{t+\tau}) > \dim_{\mathrm{cert}}(\mathcal{E}_t) \;\Rightarrow\; \text{new certificate **class** passing F4}
\]

**Counterexample (010):** κ-sweep at ±1 grid — \(T_\tau\) changes \(\kappa\) but **not** fiber statistics; deformation was **structural within same class**, not ontologically new (refines PI-003 falsifier).

### 2.4 Fuzzy boundary as deformable submanifold

`DEFINITION` · The **fuzzy boundary** \(\partial_\mu \mathcal{F}_H\) is the locus where \(\mu_{\mathcal{F}_H}\) has large gradient:

\[
\partial_\mu \mathcal{F}_H = \{ x : \|\nabla \mu_{\mathcal{F}_H}(x)\| > \epsilon \}
\]

Visually: Anthemium glow/bokeh, fiber fray into void. Operationally: gate rejections (`high_correlation_with_baseline`, `representation_ratio_fail`), fiber degeneracy without unique lift.

**Deformation of \(\mu\)** under \(T_\tau\):

- **Outward (stretch):** ND topology increase → new low-\(\mu\) regions (007, 009).
- **Inward (compactify):** κ projection → base collapse, fiber thickens (729 preimages).
- **Blur (diffuse):** lose discrete fiber identity — search still running, no accepted certificate (006).

`PHILOSOPHICAL_INFERENCE` · Mapping \(\partial_\mu \mathcal{F}_H\) operationally is the research program's **boundary science** — not proving all math lies outside human reach, but charting where π_H fails first for certifiable \(x\) (PI-001, HL-004).

### 2.5 Connection to NAMM frame ladder

| Frame | Fabric role | Deformation access |
|-------|-------------|-------------------|
| **F1** | Pop-D metaphor — motivates S¹ / ND language | Non-evidential |
| **F2** | Formal substrate — bundles, fuzzy sets, categories | Definitions |
| **F3a–f** | Single-phase fabric — one κ, one vocabulary | Limited \(T_\tau\) |
| **F3g** | Raw tensor filaments — cyan/magenta as spectral/heat dual fibers | 007 |
| **F3h** | Config shadow — S¹ = 4D viewport, 11D fiber | 009, 010 |
| **F4** | π_H bottleneck — measure \(\mu\), \(K_A/K_H\) | Gates |
| **F∞** | Trans-level Θ, colimits — terminal open wave | 011, 004 meta |

**Climbing as fabric dynamics** ([`FRAME_LADDER.md`](FRAME_LADDER.md)):

```text
  F1 motivate ──► fabric metaphor (Anthemium, this doc)
        │
        ▼
  F2 formalize ──► bundle + fuzzy set + κ
        │
        ▼
  F3 experiment ──► enumerate fibers, accept certificates
        │
        ▼
  F4 measure μ, K_A/K_H ──► locate ∂_μ F_H
        │
        ▼
  F∞ Θ / colimit ──► morphisms between fabrics (011)
```

[`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md) adds **AI-native topology**: combinatorial, sheaf-like gluing of local patches (AST nodes, gate functions), fixed points \(E \cong F(E)\) — fabric **self-stability** under evaluator deformation (004).

### 2.6 Dynamics equation (sketch)

`CONJECTURE` · Fabric state at search step \(t\):

\[
(\mathcal{E}_t,\; \mu_t,\; \Phi_t) \xrightarrow{\;T_\tau\;} (\mathcal{E}_{t+\tau},\; \mu_{t+\tau},\; \Phi_{t+\tau})
\]

where \(\Phi_t\) = certificate acceptance rate × mean fiber size × mean \(K_A/K_H\).

**Attractor basins** (Anthemium ~3 cycles):

- **Compact basin:** high fiber, low base cardinality (009 at ±1).
- **Extended basin:** wider grid, non-uniform fibers (010 at \([-2,2]\)).
- **Diffuse basin:** gate failure, no stable \(b\) (006 TDA).

`OPERATIONAL` · Experiment **011–020** should report \((\Delta\Phi, \Delta\mu, \text{new certificate classes})\) after each \(T_\tau\), not only acceptance counts.

---

## 3. Hypothesis registry — H-F001..H-F050

### Template

| Field | Content |
|-------|---------|
| **ID** | `H-F0NN` |
| **Short name** | Mnemonic |
| **Statement** | Falsifiable where possible |
| **Fabric / topology** | 1–2 sentences — Anthemium or bundle reading |
| **Link** | Frame, experiment, or CONJECTURE-only |
| **Label** | `CONJECTURE` / `PHILOSOPHICAL_INFERENCE` / `OPERATIONAL` |

---

### Section A — Fabric geometry & fibers (video S¹, bundles)

#### H-F001 — S¹ viewport as compactification screen

| Field | Content |
|-------|---------|
| **Statement** | Every F3h config_shadow run implicitly defines an **S¹-class viewport**: base = κ-image, fiber = preimage. Fiber size ≥ 2 iff viewport hides ≥ 2 distinct certificates. |
| **Fabric / topology** | Anthemium S¹ segments (A, D, G) = compact phase where interior braiding is visible but boundary enforces projection. |
| **Link** | F3h · 009 · extends **H-002** |
| **Label** | `OPERATIONAL` |

#### H-F002 — Cyan–magenta duality as dual leaf bundle

| Field | Content |
|-------|---------|
| **Statement** | Raw tensor frame (F3g) admits a **canonical 2-fiber split**: spectral leaves \(t_0..t_7\) vs heat-kernel leaves \(t_8..t_{11}\). Gate-passing ASTs with nontrivial cross-terms between splits have lower \(\mu_{\mathcal{F}_H}\) than single-split programs. |
| **Fabric / topology** | Video cyan crest / magenta trough = interwoven dual bundles over horizontal base. |
| **Link** | F3g · 007 · **H-001** |
| **Label** | `CONJECTURE` |

#### H-F003 — Braiding index of interior crossings

| Field | Content |
|-------|---------|
| **Statement** | For fixed κ shadow, define **braiding index** = count of sign alternations in fiber lex order. Non-constant braiding index across shadow class predicts **non-uniform** physical selection under future energy-active constraints. |
| **Fabric / topology** | Segment D Möbius-like crossings = nontrivial permutation structure within S¹ interior. |
| **Link** | F3h · 012 · **H-006** |
| **Label** | `CONJECTURE` |

#### H-F004 — Horizontal base = κ-parameter geodesic

| Field | Content |
|-------|---------|
| **Statement** | Sweeping κ modes (010) traces a **horizontal geodesic** in configuration space; at ±1 grid all geodesics yield identical fiber statistics — base is **flat** with respect to κ. |
| **Fabric / topology** | Left–right wave direction = unidirectional parameter sweep; no curvature → no κ discrimination. |
| **Link** | F3h · 010 tested |
| **Label** | `OPERATIONAL` |

#### H-F005 — Wireframe terrain as discrete mesh approximation

| Field | Content |
|-------|---------|
| **Statement** | Segment L wireframe inside S¹ corresponds to **finite grid sampling** of continuous moduli field; glitch texture = discretization artifact under coarse \(\{-1,0,1\}\) mesh. Refining grid (\([-2,2]\)) removes wireframe uniformity. |
| **Fabric / topology** | Height-field mesh = energy landscape sampled on integer lattice. |
| **Link** | F3h · 010 extension · CONJECTURE-only for video |
| **Label** | `CONJECTURE` |

#### H-F006 — Particle spray as rejection fiber residue

| Field | Content |
|-------|---------|
| **Statement** | Rejected candidates (`rejections.jsonl`) form a **spray cloud** around accepted fiber: same base family, failed gate. Spray density correlates with search depth × vocabulary size. |
| **Fabric / topology** | Anthemium particle field above crests = degenerate certificates outside main manifold. |
| **Link** | F3g · 007 · OPERATIONAL metric |
| **Label** | `OPERATIONAL` |

#### H-F007 — Pinch node as flux-equator singularity

| Field | Content |
|-------|---------|
| **Statement** | Moduli vectors with \(\sum m_i \equiv 0 \pmod 3\) and balanced head/tail flux exhibit **pinch geometry**: many distinct tails share head shadow — equatorial constraint surface in fiber. |
| **Fabric / topology** | Segment E bilateral pinch / lens void = constraint locus, not physical vacuum. |
| **Link** | F3h · 009 · **H-002** |
| **Label** | `OPERATIONAL` |

#### H-F008 — Terminal open wave = F∞ non-closure

| Field | Content |
|-------|---------|
| **Statement** | Artifact ending in **open topology** (Segment M, no S¹) mirrors NAMM's need for **F∞ lift**: trans-level Θ without final compactification to named invariant. |
| **Fabric / topology** | Terminal multi-peak ribbon = colimit of phase cycles without return to bounded viewport. |
| **Link** | F∞ · 011 · **H-003**, **H-007** |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

#### H-F009 — Fiber count scales as \(3^{n-s-1}\) on uniform grids

| Field | Content |
|-------|---------|
| **Statement** | On \(\{-1,0,1\}^n\) with flux mod 3 and inactive energy, fiber size is **uniform** \(3^{n-s-1}\) for all shadow classes — fabric has **constant fiber dimension** over base. |
| **Fabric / topology** | Every S¹ viewport slice has same hidden filament count — generic blur, not fine-tuned. |
| **Link** | F3h · 009, 010 · **H-002** tested |
| **Label** | `OPERATIONAL` |

#### H-F010 — Visual S² shell as 2-step κ composition

| Field | Content |
|-------|---------|
| **Statement** | Segment I fuzzy spherical shell corresponds to **composed projections** \(\kappa_2 \circ \kappa_1\) — double compactification increases blur (\(\mu\) gradient) without reducing fiber below 2. |
| **Fabric / topology** | S² shadow = 2D base of 11D bundle; edges bleed = double lossy map. |
| **Link** | F3h · 015 (planned double-κ) · CONJECTURE-only |
| **Label** | `CONJECTURE` |

---

### Section B — Fuzzy boundaries & μ-deformation

#### H-F011 — Blur phase = high \(\mu\)-gradient region

| Field | Content |
|-------|---------|
| **Statement** | Segments C, I (amorphous orb, fuzzy shell) map to search states where **accepted certificate rate → 0** but candidate count > 0 — operational \(\|\nabla\mu\|\) peak. |
| **Fabric / topology** | Lowest structural bandwidth = maximum fuzziness before re-compactification. |
| **Link** | F3f · 006 fail · PI-002 |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

#### H-F012 — Glow radius ∝ \(1 - K_A/K_H\)

| Field | Content |
|-------|---------|
| **Statement** | For accepted witnesses, **anthropic summary token count** minus **gzip certificate bytes** (normalized) predicts visual "glow" if rendered — compression asymmetry = fuzzy boundary thickness. |
| **Fabric / topology** | Bokeh periphery = π_H uncertainty halo around compact π_A core. |
| **Link** | F4 · 007, 009 · OPERATIONAL |
| **Label** | `OPERATIONAL` |

#### H-F013 — μ-deformation monotonicity under κ-only sweep

| Field | Content |
|-------|---------|
| **Statement** | Changing κ alone **without** grid or energy change does **not** monotonically decrease \(\mu_{\mathcal{F}_H}^{\mathrm{op}}\) — 010 refutes κ-as-selection principle at ±1. |
| **Fabric / topology** | κ-sweep = horizontal slide along base; blur unchanged if fibers stay 729. |
| **Link** | F3h · 010 tested |
| **Label** | `OPERATIONAL` |

#### H-F014 — Frame escalation lowers μ before raising acceptance

| Field | Content |
|-------|---------|
| **Statement** | Escalating 006→007 **temporarily increases** rejection rate while **decreasing** \(\mu\) of accepted lead — blur phase precedes compact certificate. |
| **Fabric / topology** | Open ribbon → orb → S¹ cycle: search must pass diffuse basin. |
| **Link** | F3f→F3g · 006, 007 · PI-003 |
| **Label** | `CONJECTURE` |

#### H-F015 — Independence gate = fuzzy membership cutoff

| Field | Content |
|-------|---------|
| **Statement** | Pearson \(r \geq 0.95\) vs baselines implements a **hard \(\mu\) cutoff** — structures above threshold classified inside \(\mathcal{F}_H\) regardless of AST depth. |
| **Fabric / topology** | Hard baseline correlation = crisp boundary; 001 null = interior of known math. |
| **Link** | F3a · 001 · **H-001** contrast |
| **Label** | `OPERATIONAL` |

#### H-F016 — Generative holdout = fuzzy boundary stress test

| Field | Content |
|-------|---------|
| **Statement** | Holdout failure indicates structure **overfits base manifold** — fiber collapses on unseen graph family; \(\mu\) artificially low on training base only. |
| **Fabric / topology** | Holdout = probe whether filaments extend to ambient graph space or fray at boundary. |
| **Link** | F3g · 007 · OPERATIONAL |
| **Label** | `OPERATIONAL` |

#### H-F017 — TDA signatures increase μ without clearing F4

| Field | Content |
|-------|---------|
| **Statement** | TDA-only frame (006) produces candidates with **higher human interpretability** (persistence diagrams) but **K_A/K_H < 2** — more named topology, less compression asymmetry. |
| **Fabric / topology** | TDA = partially labeled fibers; less blur but insufficient π_H loss for F4. |
| **Link** | F3f · 006 · **H-004** |
| **Label** | `OPERATIONAL` |

#### H-F018 — Combined TDA+tensor lowers μ below either alone

| Field | Content |
|-------|---------|
| **Statement** | Composite search (013) yields gate-passing candidates with \(\mu_{\mathcal{F}_H}^{\mathrm{op}}\) lower than 006-only and independence profile distinct from 007-only. |
| **Fabric / topology** | Cyan TDA + magenta tensor interweave = new nodal crossing patterns. |
| **Link** | F3f+F3g · 013 · **H-004** |
| **Label** | `CONJECTURE` |

#### H-F019 — Video morphism recovery bound < 90%

| Field | Content |
|-------|---------|
| **Statement** | Independent frame audit recovers **< 90%** of inter-frame structural invariants from π_H prose summary alone — temporal morphisms are non-optional. |
| **Fabric / topology** | Phase cycle S¹↔open↔orb deleted by static text — PI-008 falsifier. |
| **Link** | visual F∞ · **H-007** · PI-008 |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

#### H-F020 — Fuzzy orb = pre-certificate search phase

| Field | Content |
|-------|---------|
| **Statement** | Diffuse basin states are **search-necessary**: skipping blur (e.g. only named vocabulary) never reaches low-\(\mu\) certifiable fibers at industrial scale. |
| **Fabric / topology** | Segment C = evolutionary search before acceptance manifold forms. |
| **Link** | F3 · PI-004 · CONJECTURE-only |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

---

### Section C — Compactification & shadow loss (AMFW)

#### H-F021 — 729 = generic fiber, not physical vacuum

| Field | Content |
|-------|---------|
| **Statement** | Fiber size 729 on ±1 grid is **formulaic** \(3^{n-s-1}\), not selection of a distinguished vacuum — ranking by fiber size picks **maximum generic ambiguity**. |
| **Fabric / topology** | All S¹ slices equally thick — no preferred filament in AMFW parable. |
| **Link** | F3h · 009 · **H-002**, PI-006 |
| **Label** | `OPERATIONAL` |

#### H-F022 — Wider grid breaks fiber uniformity

| Field | Content |
|-------|---------|
| **Statement** | Extending moduli to \([-2,2]\) (7D test) yields **non-uniform** fiber sizes (max 42) — energy wall activates, fabric gains **curvature** over base. |
| **Fabric / topology** | Open ribbon phase with varying filament density — not flat bundle. |
| **Link** | F3h · 010 script · **H-006** |
| **Label** | `OPERATIONAL` |

#### H-F023 — Shadow class count = \(3^s\) on full grid

| Field | Content |
|-------|---------|
| **Statement** | For \(s\)-dimensional κ on \(\{-1,0,1\}^n\), every shadow pattern in \(\{-1,0,1\}^s\) appears among admissible vacua when energy inactive — base is **complete** hypercube image. |
| **Fabric / topology** | 81 shadow classes = 81 distinct S¹ viewport labels. |
| **Link** | F3h · 009 · OPERATIONAL |
| **Label** | `OPERATIONAL` |

#### H-F024 — Fiber index is lex gauge, not physical weight

| Field | Content |
|-------|---------|
| **Statement** | `fiber_index` (492 for AMFW-012e) has **no invariant meaning** under reordering of tail coordinates — purely certificate bookkeeping. |
| **Fabric / topology** | Index = filament label in bundle chart, not mass or energy. |
| **Link** | F3h · 009 · PI-006 |
| **Label** | `OPERATIONAL` |

#### H-F025 — Double κ increases K_A/K_H

| Field | Content |
|-------|---------|
| **Statement** | Composing two lossy κ maps on 11D moduli yields witnesses with **K_A/K_H strictly greater** than single κ at same grid — stacked compactification thickens fuzzy boundary. |
| **Fabric / topology** | S² shell segment = nested viewport blur. |
| **Link** | F3h · 015 (planned) · CONJECTURE |
| **Label** | `CONJECTURE` |

#### H-F026 — Energy cap activates tail wall

| Field | Content |
|-------|---------|
| **Statement** | Lowering \(\sum m_i^2 \leq E\) below active threshold **shrinks** fibers non-uniformly — tail coordinates hit wall at different shadows. |
| **Fabric / topology** | Pinch tightens when energy budget restricts vertical fiber extension. |
| **Link** | F3h · 016 (planned) · **H-006** |
| **Label** | `CONJECTURE` |

#### H-F027 — Graceful labeling fiber ≥ 2 for some tree

| Field | Content |
|-------|---------|
| **Statement** | Some tree order ≤ n admits **≥ 2 graceful labelings** sharing κ-shadow — fiber degeneracy in hybrid frame distinct from AMFW generic 729. |
| **Fabric / topology** | Labeling ambiguity = multiple filaments over same combinatorial base. |
| **Link** | F3e₂+F3h · 012 · **H-006** |
| **Label** | `CONJECTURE` |

#### H-F028 — AMFW ≠ Graceful disproof

| Field | Content |
|-------|---------|
| **Statement** | AMFW fiber witnesses **do not** refute Graceful Tree conjecture — they demonstrate **different object class** with measurable π_H loss (008 null vs 009 signal). |
| **Fabric / topology** | Two fabric patches: crisp tree fibers vs thick moduli fibers — same instrument, different topology. |
| **Link** | 008, 009 · AMFW Part B.2 |
| **Label** | `OPERATIONAL` |

#### H-F029 — Selection principle must break lex order

| Field | Content |
|-------|---------|
| **Statement** | Any **physically meaningful** lift from fiber to moduli must depend on **more than fiber size and lex index** — else selection is gauge artifact. |
| **Fabric / topology** | Choosing filament 492 vs 491 = arbitrary chart choice unless new invariant attached. |
| **Link** | F3h · 012, 017 · **H-006** |
| **Label** | `CONJECTURE` |

#### H-F030 — K_A/K_H ≥ 9 implies μ < 0.15

| Field | Content |
|-------|---------|
| **Statement** | Witnesses with \(K_A/K_H \geq 9\) (AMFW class) have operational \(\mu_{\mathcal{F}_H}^{\mathrm{op}} \lesssim 0.15\) under default τ=2 — **deep exterior** of fuzzy known-math set. |
| **Fabric / topology** | Maximum blur-compatible crisp certificate — orb interior with exact eval_hash. |
| **Link** | F4 · 009 · OPERATIONAL |
| **Label** | `OPERATIONAL` |

---

### Section D — Raw tensor / program synthesis layer

#### H-F031 — Raw leaves necessary for low-μ signal

| Field | Content |
|-------|---------|
| **Statement** | Search vocabulary containing **only** named graph statistics cannot reproduce 007 independence profile at same gate stack — raw leaves are **necessary** for tested low-\(\mu\) signal. |
| **Fabric / topology** | Named stats = pre-labeled filaments; raw leaves = uncolored bundle strands. |
| **Link** | F3g · 007 vs 001 · **H-001** |
| **Label** | `OPERATIONAL` |

#### H-F032 — Deep MUL composition resists SymPy span

| Field | Content |
|-------|---------|
| **Statement** | SHTC-639 lead requires **depth ≥ 3** multiplicative nesting to evade degree-≤4 tensor polynomial baselines — shallow programs remain in high-\(\mu\) span. |
| **Fabric / topology** | Braiding depth = AST crossing count over dual leaf bundle. |
| **Link** | F3g · 007 · CONJECTURE |
| **Label** | `CONJECTURE` |

#### H-F033 — Spectrum–heat cross-terms are essential

| Field | Content |
|-------|---------|
| **Statement** | Best 007 candidates mix **both** spectral and heat indices (e.g. `t0`, `t11`) — single-family programs correlate higher with baselines. |
| **Fabric / topology** | Cyan–magenta **crossing** at nodal AST nodes required for novelty. |
| **Link** | F3g · 007 · **H-F002** |
| **Label** | `CONJECTURE` |

#### H-F034 — ECIP depth without raw leaves saturates

| Field | Content |
|-------|---------|
| **Statement** | F3c evolutionary search over **named** stats (003) hits independence ceiling below F3g — frame difference, not algorithm alone, bounds \(\mu\) reduction. |
| **Fabric / topology** | Deep braiding inside single-colored bundle cannot mimic dual-fiber interweave. |
| **Link** | F3c vs F3g · 003, 007 · **H-005** |
| **Label** | `OPERATIONAL` |

#### H-F035 — Numeric range sensitivity = fabric tension

| Field | Content |
|-------|---------|
| **Statement** | Large evaluated magnitudes (~10¹²) on 007 lead indicate **scale tension** between spectral and heat leaves — certificate stable under eval_hash but human projection unstable. |
| **Fabric / topology** | High-amplitude wave crest = numeric stiffness, not proof of graph-theoretic extremality. |
| **Link** | F3g · 007 · CONJECTURE-only |
| **Label** | `CONJECTURE` |

#### H-F036 — Tensor AST transitions form category

| Field | Content |
|-------|---------|
| **Statement** | Admissible rewrite rules on TensorNode ASTs (constant fold forbidden if independence breaks) form a **small category** whose morphisms preserve eval_hash on witness set. |
| **Fabric / topology** | Fiber-preserving moves = horizontal slides along acceptance manifold. |
| **Link** | F3g→F∞ · 011 · **H-003** |
| **Label** | `CONJECTURE` |

#### H-F037 — Θ transitions exceed static AST equivalence

| Field | Content |
|-------|---------|
| **Statement** | Some certified transitions between 007 functionals yield **distinct equivalence classes** not reachable by static AST composition — proper **F∞ lift**. |
| **Fabric / topology** | Temporal morphism between S¹ phases, not snapshot of one phase. |
| **Link** | F∞ · 011 · **H-003** |
| **Label** | `CONJECTURE` |

#### H-F038 — Program synthesis at scale requires machine search

| Field | Content |
|-------|---------|
| **Statement** | 53/57 acceptance at 007 search budget is **not reproducible** by manual AST audit at same coverage — industrial enumeration leg (PI-004). |
| **Fabric / topology** | Particle spray volume requires automated traversal of fabric. |
| **Link** | F3g · 007 · PI-004 |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

#### H-F039 — Holdout-stable tensor family is closed under T_τ depth

| Field | Content |
|-------|---------|
| **Statement** | Increasing AST depth cap beyond 007 lead **breaks** generative holdout on at least one family — depth deformation has **critical τ** before fiber frays. |
| **Fabric / topology** | Extending ribbon too far → particle spray (holdout fail). |
| **Link** | F3g · 018 (planned depth sweep) |
| **Label** | `CONJECTURE` |

#### H-F040 — Commutative-only ops suffice for F4 pass

| Field | Content |
|-------|---------|
| **Statement** | `add`/`mul` only (no non-commutative ops) already suffice for **K_A/K_H ≥ 2** and independence — non-commutative vocabulary not necessary for first low-\(\mu\) witness class. |
| **Fabric / topology** | Commutative braiding = symmetric cyan/magenta interlace. |
| **Link** | F3g · 007 tested |
| **Label** | `OPERATIONAL` |

---

### Section E — Trans-level Θ & meta fixed points

#### H-F041 — Θ algebra is F∞ minimal lift

| Field | Content |
|-------|---------|
| **Statement** | Semantic transition algebra Θ over SHTC-639 is the **minimal F∞ structure** witnessing non-static novelty — colimits of AST family under certified transitions. |
| **Fabric / topology** | Terminal open wave = Θ without final S¹ compactification. |
| **Link** | F∞ · 011 · **H-003** |
| **Label** | `CONJECTURE` |

#### H-F042 — Meta-evaluator fixed point = self-braiding fabric

| Field | Content |
|-------|---------|
| **Statement** | SREFP-414d (004) fixed points \(E \cong F(E)\) model **fabric stable under self-referential deformation** — evaluator strand braids with its own image. |
| **Fabric / topology** | Möbius-like self-crossing in AI topology ([`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md)). |
| **Link** | F3d · 004 · CONJECTURE-only |
| **Label** | `CONJECTURE` |

#### H-F043 — Fixed point fraction gates F∞ promotion

| Field | Content |
|-------|---------|
| **Statement** | `fixed_point_fraction` ≥ threshold on benchmark graphs is **necessary** but not sufficient for promoting meta-evaluator to F∞ witness class. |
| **Fabric / topology** | Self-stable filament must also show K_A/K_H asymmetry to exit high-\(\mu\) region. |
| **Link** | F3d · 004, 019 (planned) |
| **Label** | `OPERATIONAL` |

#### H-F044 — Θ + AMFW hybrid yields cross-frame fiber

| Field | Content |
|-------|---------|
| **Statement** | Transitions from tensor functionals to moduli certificates (cross-domain Θ) produce **hybrid fibers** — same eval witness, dual κ and AST projections. |
| **Fabric / topology** | Cyan tensor bundle glued to magenta config bundle over shared graph base. |
| **Link** | F3g+F3h · 020 (planned) |
| **Label** | `CONJECTURE` |

#### H-F045 — Colimit of 007 family has undefined π_H

| Field | Content |
|-------|---------|
| **Statement** | Directed system of all 007-accepted ASTs under certified transitions admits a **colimit** with no finite π_H projection — explicit ordinal witness required for F∞. |
| **Fabric / topology** | Infinite open ribbon — no return to S¹ without loss. |
| **Link** | F∞ · 011 · PI-001 |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

---

### Section F — Open problem shadows & lift protocol

#### H-F046 — Graceful null calibrates fabric instrument

| Field | Content |
|-------|---------|
| **Statement** | 008 exhaustive null (987 trees graceful) **calibrates** fuzzy boundary detector — high \(\mu\) region verified before 009 low-\(\mu\) excursion. |
| **Fabric / topology** | Crisp S¹ phase with unique filaments — control patch on fabric chart. |
| **Link** | F3e₂ · 008 · **H-shadow-008** |
| **Label** | `OPERATIONAL` |

#### H-F047 — Kotzig null maps high-μ graph atlas

| Field | Content |
|-------|---------|
| **Statement** | 005 bounded null maps **interior of \(\mathcal{F}_H\)** for P_k-graph vocabulary — no low-\(\mu\) fiber found in atlas bounds. |
| **Fabric / topology** | Known combinatorial region — no blur phase triggered. |
| **Link** | F3e · 005 · **H-shadow-005** |
| **Label** | `OPERATIONAL` |

#### H-F048 — Reconstruction deck shadow has fiber ≥ 2 potential

| Field | Content |
|-------|---------|
| **Statement** | Graph deck-equivalent pairs in finite atlas yield **non-unique reconstruction certificates** — analog of AMFW fiber degeneracy in graph frame. |
| **Fabric / topology** | Multiple filaments over same deck shadow — S¹ with hidden braiding. |
| **Link** | F3e · 014 (planned) |
| **Label** | `CONJECTURE` |

#### H-F049 — Lift protocol: shadow → moduli → Θ

| Field | Content |
|-------|---------|
| **Statement** | Three-step lift **(open-problem shadow → config moduli → trans-level Θ)** is the canonical path from high-\(\mu\) calibration to low-\(\mu\) F∞ witness — 008 → 012 → 011 chain. |
| **Fabric / topology** | S¹ control → hybrid braid → open terminal wave. |
| **Link** | 008, 012, 011 · AMFW Part B |
| **Label** | `OPERATIONAL` |

#### H-F050 — Bounded null strengthens falsifier, not thesis

| Field | Content |
|-------|---------|
| **Statement** | Negative finite shadows (005, 008) **do not** weaken PI-001/PI-007 — they bound instrument sensitivity, mapping **interior** of \(\mathcal{F}_H\) before exterior exploration. |
| **Fabric / topology** | Charting known fabric patch before deformation into blur basin. |
| **Link** | PI-001, PI-007 · CONJECTURE-only |
| **Label** | `PHILOSOPHICAL_INFERENCE` |

---

## 4. Top 10 priority — NAMM experiments 011–020

Ranked by **fabric dynamics impact** (\(\Delta\mu\), new certificate classes, Θ/F∞ lift) and dependency order:

| Rank | H-F IDs | Proposed experiment | Frame | Rationale |
|------|---------|---------------------|-------|-----------|
| **1** | H-F041, H-F037, H-F036 | **NAMM-2026-011** — Trans-level Θ over SHTC-639 | F3g→F∞ | Minimal F∞ lift; tests **H-003**; terminal open-wave closure |
| **2** | H-F027, H-F049, H-F029 | **NAMM-2026-012** — Graceful → moduli hybrid | F3e₂+F3h | Labeling fiber degeneracy; lift protocol step 2 |
| **3** | H-F018, H-F017 | **NAMM-2026-013** — TDA + raw tensor composite | F3f+F3g | Blur→braid: combine high-μ interpretability with low-μ compression |
| **4** | H-F048 | **NAMM-2026-014** — Graph Reconstruction deck shadow | F3e | Fiber ≥ 2 in graph frame; open problem lift |
| **5** | H-F025, H-F010 | **NAMM-2026-015** — Double-κ compactification stack | F3h | S² shell hypothesis; stacked π_H loss |
| **6** | H-F026, H-F022 | **NAMM-2026-016** — Energy-active moduli sweep | F3h | Break uniform 729; fabric curvature over base |
| **7** | H-F029, H-F003 | **NAMM-2026-017** — Physical selection on non-uniform fibers | F3h | Selection beyond lex; pinch geometry |
| **8** | H-F039, H-F032 | **NAMM-2026-018** — AST depth / vocabulary stress | F3g | Critical τ before holdout fray |
| **9** | H-F043, H-F042 | **NAMM-2026-019** — Meta-evaluator × tensor glue | F3d+F3g | Self-braiding fabric; fixed-point + low-μ |
| **10** | H-F044 | **NAMM-2026-020** — Cross-frame Θ (tensor ↔ moduli) | F3g+F3h | Hybrid cyan/magenta bundles over shared base |

**Immediate queue (already scaffolded):** 011, 012, 013, 014 per [`NAMM_OPEN_PROBLEMS_QUEUE.md`](NAMM_OPEN_PROBLEMS_QUEUE.md). Experiments 015–020 are **proposed** — add scaffolds when 011–014 report.

---

## 5. Cross-reference index

### H-F → H (MATH_OBJECT_HYPOTHESES)

| H-F | Extends / relates |
|-----|-------------------|
| H-F001, H-F009, H-F021 | **H-002** |
| H-F002, H-F031, H-F033 | **H-001** |
| H-F008, H-F041, H-F037 | **H-003**, **H-007** |
| H-F018 | **H-004** |
| H-F034 | **H-005** |
| H-F003, H-F022, H-F027, H-F029 | **H-006** |
| H-F019 | **H-007**, PI-008 |
| H-F046, H-F047 | **H-shadow-008**, **H-shadow-005** |

### H-F → PI

| PI | H-F cluster |
|----|-------------|
| PI-001 | H-F008, H-F045, H-F050 |
| PI-002 | H-F011–H-F020 |
| PI-003 | H-F014, H-F004 |
| PI-004 | H-F038 |
| PI-006 | H-F021, H-F024, H-F028 |
| PI-008 | H-F019, H-F008 |

### Fabric phase → experiment

| Phase | Experiments |
|-------|-------------|
| Compact S¹ | 009, 010 (±1), 008 |
| Extended ribbon | 007, 010 \([-2,2]\), 013 |
| Diffuse orb | 006, pre-accept search |
| F∞ open | 011, 004, 020 |

---

## 6. Agent load protocol

**Add to standard NAMM research load** (after [`MATH_OBJECT_HYPOTHESES.md`](MATH_OBJECT_HYPOTHESES.md)):

1. When user cites **mathematical fabric**, **topological fuzzy dynamics**, or **Anthemium topology**: load **this file** + [`ANTHEMIUM_VIDEO_NOTES.md`](ANTHEMIUM_VIDEO_NOTES.md).
2. Map experiment proposals to **H-F IDs** and **fabric phase** (compact / extended / diffuse / F∞).
3. Report \(\mu\) proxy, fiber size, and whether \(T_\tau\) produced **new certificate class** — not only acceptance count.
4. Do **not** conflate fabric metaphor with physical claims; label `PHILOSOPHICAL_INFERENCE` entries accordingly.

---

Roman Kuznetsov · NAMM research program
