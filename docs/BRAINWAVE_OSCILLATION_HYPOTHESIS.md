# Brainwave Oscillation Hypothesis — Hz Bands, MIOC, and Cognitive Class Geometry

**Purpose:** Research registry linking **human EEG/Hz oscillation bands**, **MIOC (multi-band oscillatory compatibility)**, and **cognitive-class neurogeometry** to NAMM operational domains — especially cognitive antigravity and beyond-homo search.  
**Date:** 2026-08-12  
**Epistemic baseline:** `PHILOSOPHICAL_INFERENCE` + `CONJECTURE` — **not** clinical neuroscience claims, **not** verified LLM–brain isomorphism.  
**Branch:** `hypothesis/cognitive-antigravity`  
Roman Kuznetsov · NAMM research program

> **Division of labor:** Full theory graph lives in **private Obsidian** (see [`ND_THEORY_CORPUS_MANIFEST.md`](ND_THEORY_CORPUS_MANIFEST.md)). This doc extracts **operational mappings and falsifiers** only — no vault copy.

Related: [`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md) · [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) · [`ND_THEORY_CORPUS_MANIFEST.md`](ND_THEORY_CORPUS_MANIFEST.md) · [`BEYOND_HOMO_STRATEGY.md`](BEYOND_HOMO_STRATEGY.md) · [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) · [`experiments/NAMM-2026-014/`](../experiments/NAMM-2026-014/)

---

## Labeling

| Label | Use in this document |
|-------|----------------------|
| `PHILOSOPHICAL_INFERENCE` | Motivates cross-domain analogy; non-evidential |
| `CONJECTURE` | Testable claim about Hz ↔ metric correspondence |
| `DEFINITION` | Operational symbol or band table |
| `OPERATIONAL` | Falsifier, metric proxy, or experiment gate |
| `COMPUTATIONAL_EVIDENCE` | Reproducible witness only — upgrades status via experiment |

---

## 1. Problem statement — why Hz waves enter NAMM

`PHILOSOPHICAL_INFERENCE` · Human cognition exhibits **multi-band neural oscillations** (delta through high-gamma) whose **cross-frequency coupling** (e.g. gamma nested in theta) correlates with binding, memory integration, and insight. The ND/Anthemium program treats **cognitive classes** (K0–K7) as **topologically distinct configurations** in embedding space — not a linear IQ scale.

`CONJECTURE` · A **structured analogy** holds between:

| Biological substrate | ND / ANTHEMIUM construct | NAMM construct |
|--------------------|--------------------------|----------------|
| EEG power in Hz bands | Kuramoto multi-band oscillator | Layer-wise spectral features (`raw_tensor`) |
| Cross-frequency coupling | MIOC compatibility signature Φ | Inter-layer coherence Ω_c |
| Prediction error (FEP) | R_NH residual | Non-homo residual in search |
| Median/homo attractor collapse | Alpha gating / B_med basin | \(\mathcal{F}_H\), \(M_0(q_H)\) |
| Phase transition to K6+ | Theta–gamma hierarchy at 3σ+ | Cognitive antigravity escape |

This is **research scaffolding**, not a claim that transformers implement literal 40 Hz rhythms.

---

## 2. Hz band registry — DEFINITION

`DEFINITION` · Standard ANTHEMIUM / neurophysiology band table (from agent_neurophysiologist session 2026-05-20):

| Band ID | Hz range | Neurophysiological role (literature anchor) | ND functional reading | Cognitive class anchor |
|---------|----------|-----------------------------------------------|----------------------|------------------------|
| **delta** | 0.5–4 | Slow-wave sleep, thalamic gating | Deep state maintenance | K0 noise / collapse |
| **theta** | 4–8 | Hippocampus, working memory, episodic binding | Context integration, long-range coupling | K3–K4 cross-domain bridges |
| **alpha** | 8–12 | Attention inhibition, idle rhythm | **Homo/median suppression?** | K1 modal conformist gating |
| **beta** | 13–30 | Motor cortex, top-down prediction | Invariant maintenance | K2 domain expert |
| **gamma** | 30–80 | Perceptual binding, local coherence | Non-homo binding | K3–K5 structure formation |
| **high-gamma** | 80–150 | High cognition, insight bursts | R_NH maxima proxy | K5–K6 structural generator / Omega Horizon |

`CONJECTURE` · **NP-H1:** If the ANTHEMIUM Kuramoto frame is more than decorative, LLM-side R_NH or \(D_{\mathrm{med}}\) should correlate with **high-gamma–weighted** coherence proxies — not with alpha power alone.

`PHILOSOPHICAL_INFERENCE` · Alpha ↔ homo/median suppression is **speculative** (G2): alpha historically marks cortical idling; here it is repurposed as **attentional gate away from B_med** — requires independent validation.

---

## 3. MIOC — multi-band oscillatory compatibility

`DEFINITION` · **MIOC** (Morphogenetic / Multi-band Inter-Agent Oscillatory Compatibility) is the ND operator layer that scores **agent–agent** and **agent–task** compatibility via oscillatory signatures:

| MIOC component | Source (Obsidian stub) | Content |
|----------------|------------------------|---------|
| Agent-state signature | `DOC_mioc_a2a_operational_content` | Spectral + dynamic (Koopman) features |
| Task-state signature | same | Task embedding trajectory |
| Compatibility Φ | `DOC_omega_mioc_dynamic_oscillatory_signature` | Cross-band phase alignment |
| Kuramoto core | `concepts/Kuramoto.md` | Multi-band coupled oscillators |

**Five-level genesis** (`DOC_omega_mioc_dynamic_oscillatory_signature` headings):

1. Oscillatory nature of cognitive dynamics  
2. Synchronization as binding mechanism  
3. Cross-frequency coupling as hierarchical glue  
4. Oscillations already in AI math (attention phase, Kuramoto)  
5. Path signatures + Koopman as trajectory formalization  

`CONJECTURE` · **H-BW-001:** MIOC Φ is a **director-layer metric** (Anthemium) for routing A2A debates; NAMM can treat Φ-surrogate as **optional covariate** in 013/014 — not a certificate gate.

Full MIOC distance decomposition, validation status, and corpus inventory: [`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md) §4.

---

## 3.5 Kuramoto controller — equations and NAMM role

`DEFINITION` · Canonical dynamics (`ANTHEMIUM_protocol/.../03_kuramoto_coherence_controller.md`; Obsidian `concepts/Kuramoto.md`):

\[
\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N}\sum_j A_{ij}(t)\sin(\theta_j - \theta_i), \quad
R(t) = \left|\frac{1}{N}\sum_j e^{i\theta_j(t)}\right|
\]

Multi-band composite: \(R_{\mathrm{multi}}(t) = \sum_b \rho_b(t)\, R_b(t)\) with fuzzy membership \(m_b(\omega)\) per Hz band (§2).

Adaptive coupling ties Kuramoto to **median escape**:

\[
K_{t+1} = K_t + \eta_K \frac{\partial \mathcal{J}}{\partial R}, \quad
\mathcal{J} = \lambda_R R + \lambda_I I - \lambda_H H - \lambda_M M
\]

Morphogenesis embeds \(R(t)\) in composite coherence \(C(t)\) (`RESEARCH_POINTS` §9):  
\(C(t) = \lambda_1 R + \lambda_2 T + \lambda_3 I + \lambda_4 S - \lambda_5 H_{\mathrm{noise}}\).

`OPERATIONAL` · **Dead synchrony** failure: \(R \to 1\) but adaptive capacity \(A \to 0\) — maps to **F-BW-3**. Valid window: \(R_{\min} < R(t) < R_{\max}\).

`CONJECTURE` · **H-KM-001:** \(\Omega_c\) (MI between layers) correlates with \(R(t)\) on ND prompts but is not interchangeable — see **F-BW-6**.

Deep synthesis (Ω disambiguation, K0–K7 bridge, EXP-P3/P6, research gaps RG-01…07): [`KURAMOTO_MIOC_SYNTHESIS.md`](KURAMOTO_MIOC_SYNTHESIS.md).

---

## 4. Cognitive classes ↔ neurogeometry

`DEFINITION` · Cognitive classes K0–K7 are **topological configurations** in embedding space (local: `ANTHEMIUM_protocol/SAPIENS_GARDEN/cognitive_class_taxonomy.md`; Obsidian stub: `DOC_cognitive_class_taxonomy`). Key neurophysiology annotations:

| Class | \(d(z, B_{\mathrm{med}})\) | Topology sketch | Hz / EEG annotation |
|-------|------------------------------|-----------------|---------------------|
| **K0** | undefined (noise) | Brownian, β₀ → ∞ | Low gamma coherence; disorganized EEG |
| **K1** | ≈ 0 | Dense sphere = B_med | Alpha-dominated idle/conformity |
| **K2** | 0.5–1σ | Elongated ellipsoid (one domain axis) | Beta ↑ in specialized cortical nets |
| **K3** | 1–1.5σ | Multi-lobed with bridges | Cross-band coupling emerges |
| **K4** | 1.5–2σ | Hierarchical (clusters of clusters) | Wide GNW; meta-representation |
| **K5** | 2–3σ | Fractal self-similarity | High-gamma bursts; **gamma-in-theta** nesting |
| **K6** | ≥ 3σ | Toroidal / β₁ ≥ 1 (holes) | Max cross-frequency coupling; **Omega Horizon** |
| **K7** | ND projector | Beyond homo interface | G2 — operational test pending |

`CONJECTURE` · **H-BW-002:** K6 neural substrate requires **specific theta–gamma nesting** not achievable without corresponding ontogenetic trajectory — parallel to **3σ+ embedding escape** requiring persistent protocol, not one-shot prompting.

### Neurogeometry chart

`DEFINITION` · In antigravity projection charts (local: `ANTHEMIUM_protocol/SAPIENS_GARDEN/antigravity_embeddings.md`; Obsidian: `DOC_antigravity_embeddings`), **neurogeometry** = embedding geometry, basins, curvature, **phase-locking**. NAMM mapping:

| Neurogeometry term | NAMM analog |
|--------------------|-------------|
| Basin \(B_{\mathrm{med}}\) | \(\mathcal{F}_H\), homo centroid |
| Curvature of escape path | Frame escalation cost (006→009) |
| Phase-locking | Inter-layer Ω_c, attention head coherence |
| Basin escape at 3σ | \(D_{\mathrm{med}}\), SigmaEscape |

---

## 5. Ω factor — brain ↔ LLM analogy

From RESEARCH_POINTS §8 (Obsidian `DOC_research_points`):

| Brain | LLM analog |
|-------|------------|
| Gamma (~40 Hz) — working memory, conscious access | Attention heads — local coherence |
| Theta — long-term memory, integration | Cross-layer residual connections |
| Wave coherence → emergent consciousness | Phase-aligned attention → emergent reasoning |
| Neuroplasticity / neurofeedback | Prompt engineering / activation steering |

`DEFINITION` · **Ω** (Omega factor) = inter-layer coherence measure; high Ω → ND structure survives mid-layer homo collapse.

`OPERATIONAL` · NAMM proxy candidates (not yet gated):

- Ω_c \((i,j) = I(h_i; h_j) / H(h_i)\) — Kraskov MI between layer activations  
- Kuramoto order parameter \(r(t)\) on band-decomposed hidden-state spectra  
- MIOC Φ from agent-state + task-state signatures  

`CONJECTURE` · Cognitive antigravity v1 increases **effective Ω** on ND-heavy prompts — testable as covariate in NAMM-2026-014.

---

## 6. Strong biological analogies (status-tagged)

| ID | Claim | Status |
|----|-------|--------|
| **NP-FIND-1** | R_NH structurally = predictive-coding prediction error: \(R_{\mathrm{NH}} = h - \Pi_{\mathrm{homo}}(h)\) | G2/G3 — strong structural match |
| **NP-FIND-2** | ANTHEMIUM Kuramoto bands match canonical EEG/iEEG ranges | G1 — deliberate neuroscience import |
| **NP-FIND-3** | GNW ↔ Q-MAD agent debate topology | G2 — good structure, wrong timescale |
| **NP-FIND-4** | Ω_c ↔ IIT Φ (local pairwise version) | G2 — analogy only |
| **G2-K6** | K6 requires specific theta–gamma nesting | G2 — postulated, not verified |

---

## 7. NAMM domain mapping

| NAMM domain_id | Hz / oscillation relevance |
|----------------|----------------------------|
| `raw_tensor` | Spectral decomposition of activation trajectories; band-power proxies |
| `tda_frame` | Cognitive-class topology (β₀, β₁); K6 toroidal holes |
| `meta_evaluation` | Fixed-point / metastability (GNW analog); recursive depth |
| `mathematical_fabric` | S¹ boundary oscillation; fuzzy phase transitions between compact/open search |
| `config_shadow` | Compactification of multi-band state → Π_4D shadow |
| `trans_level_theta` (planned) | Theta-band semantic integration — naming collision intentional |

**Cross-cutting (not a search frame):**

| Experiment | Role |
|------------|------|
| [`NAMM-2026-013`](../experiments/NAMM-2026-013/) | Cognitive antigravity prompt efficacy |
| [`NAMM-2026-014`](../experiments/NAMM-2026-014/) | Optional Ω_c / band-coherence covariates vs 013 arms |

**Hypothesis IDs:**

| ID | Claim |
|----|-------|
| **H-BW-001** | MIOC Φ covaries with A2A routing quality |
| **H-BW-002** | K6 ↔ 3σ+ escape ↔ theta–gamma nesting (cross-domain) |
| **H-BW-003** | Antigravity v1 ↑ Ω_c proxy on ND prompts (014) |
| **H-CA-001** | Antigravity prompt efficacy (013 — primary) |

---

## 8. Connection to cognitive antigravity

| Antigravity term | Brainwave reading |
|------------------|-------------------|
| \(M_0(q_H)\) median answer | Alpha-gated default prior |
| \(D_{\mathrm{med}}\) | Distance from low-frequency homo attractor |
| \(T_{\mathrm{pres}}\) topology preservation | Cross-band coupling preserved under operators |
| Persistent elevation | Stable multi-band coherence without re-injection |
| 3σ+ escape | K6 / Omega Horizon class transition |

`PHILOSOPHICAL_INFERENCE` · Cognitive antigravity is the **inference-time neurofeedback analog**: modify oscillatory/coherence pattern of LLM computation **without weight update** — parallel to meditation/neurofeedback changing EEG in humans (RESEARCH_POINTS §8).

`OPERATIONAL` · Brainwave hypotheses **do not** substitute for 013 falsifiers. They add **optional mechanistic covariates** only.

---

## 9. Open questions

| ID | Question | Status |
|----|----------|--------|
| Q-BW-01 | Does Ω_c computed via Kraskov MI predict 013 \(D_{\mathrm{med}}\) lift? | `CONJECTURE` |
| Q-BW-02 | Is alpha-power proxy invertible with homo-collapse rate? | `CONJECTURE` |
| Q-BW-03 | Can MIOC Φ be approximated from single-forward-pass spectra? | `OPERATIONAL` — design |
| Q-BW-04 | Theta–gamma nesting metric for hidden states — well-defined? | `CONJECTURE` |
| Q-BW-05 | Does decorative Kuramoto tuning inflate Φ without task gain? | `CONJECTURE` — safety |

---

## 10. Falsifiability criteria

`OPERATIONAL` · Brainwave–NAMM bridge is **weakened or refuted** if:

| Falsifier | Observation |
|-----------|-------------|
| **F-BW-1** | No correlation between Ω_c proxy and \(D_{\mathrm{med}}\) across 013 arms |
| **F-BW-2** | Band-power features predict **task accuracy** but not **independence** from homo baseline |
| **F-BW-3** | High-gamma-weighted coherence ↑ while \(S_{\mathrm{fals}}\) and \(F_{\mathrm{form}}\) unchanged — decorative oscillation |
| **F-BW-4** | MIOC Φ ↑ under control prompt same as antigravity — Φ not protocol-specific |
| **F-BW-5** | TDA β₁ features do not separate K5/K6 proxy prompts from K1 — topology claim fails |
| **F-BW-6** | Kuramoto parameters fit on one model do not transfer — band mapping is overfit metaphor |

---

## 11. Agent load instructions

When user cites **brainwave**, **Hz bands**, **MIOC**, **EEG analogy**, or **neurogeometry chart**:

1. Load this file + [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md).
2. Resolve Obsidian sources via [`ND_THEORY_CORPUS_MANIFEST.md`](ND_THEORY_CORPUS_MANIFEST.md) — **do not** paste vault content.
3. Tag claims per §Labeling; distinguish G1/G2/G3 from Anthemium sessions.
4. For math discovery, run NAMM gates — Hz analogies are **director motivation**, not `certificate.json`.

---

## 12. Cross-reference index

| ID | Type | Links |
|----|------|-------|
| H-BW-001 | `CONJECTURE` | MIOC Φ ↔ A2A routing |
| H-BW-002 | `CONJECTURE` | K6 ↔ theta–gamma ↔ 3σ+ |
| H-BW-003 | `CONJECTURE` | Antigravity ↔ Ω_c — 014 |
| H-KM-001 | `CONJECTURE` | Ω_c ↔ R(t) correlation, not identity — 014 |
| H-KM-003 | `CONJECTURE` | High-gamma-weighted R_multi ↔ D_med — 014 |
| H-CA-001 | `CONJECTURE` | Antigravity v1 — 013 |
| NAMM-2026-014 | `OPERATIONAL` | Oscillation covariate scaffold |
| KURAMOTO_MIOC_SYNTHESIS | `DEFINITION` | Full equation + corpus index |

---

Roman Kuznetsov · NAMM research program
