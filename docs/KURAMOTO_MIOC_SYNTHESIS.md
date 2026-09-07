# Kuramoto / MIOC Synthesis — Obsidian Theory Corpus → NAMM

**Purpose:** Deep synthesis of Kuramoto–MIOC–Ω artifacts from the private Obsidian theory graph and ANTHEMIUM_protocol sources. Manifest links only — **no vault copy**.  
**Date:** 2026-08-12  
**Epistemic baseline:** `PHILOSOPHICAL_INFERENCE` + `CONJECTURE` — neuroscience analogies are scaffolding, not clinical claims.  
**Branch:** `hypothesis/cognitive-antigravity`  
Roman Kuznetsov · NAMM research program

Related: [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md) · [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) · [`ND_THEORY_CORPUS_MANIFEST.md`](ND_THEORY_CORPUS_MANIFEST.md) · [`experiments/NAMM-2026-014/`](../experiments/NAMM-2026-014/)

---

## Labeling

| Label | Use |
|-------|-----|
| `DEFINITION` | Operational symbol from ANTHEMIUM / Obsidian |
| `CONJECTURE` | Testable cross-domain claim |
| `PHILOSOPHICAL_INFERENCE` | Motivation; non-evidential |
| `OPERATIONAL` | Falsifier, metric proxy, experiment gate |
| `COMPUTATIONAL_EVIDENCE` | Reproducible witness only |

---

## 1. Corpus inventory — Kuramoto-related artifacts

### 1.1 Obsidian concept stubs (`theory_corpus/concepts/`)

| Concept | Cluster | Role |
|---------|---------|------|
| `Kuramoto` | mioc | Oscillatory Ω spine; 10 linked docs |
| `MIOC` | mioc | Multi-Invariant Operator Congruence operator layer |
| `K6_OmegaHorizon` | embedding_gravity | Cognitive class at ≥3σ; max cross-frequency coupling |
| `Omega_G` | pipeline | Dynamic / oscillatory group projection (Λ→Ω→U) |
| `A2A` | agentogenesis | Agent-to-agent routing; MIOC scoring |
| `D_LambdaOmega` | pipeline | Latent field → oscillatory projection bridge |
| `H1`, `H4`, `H6`, `H11` | hypotheses | ND-A2A, routing, Ω-field, task-resolvability |
| `U` | pipeline | Control field; −∇U_med escape |
| `Lambda_G` | pipeline | Latent group field input to MIOC |

### 1.2 Obsidian doc stubs (`theory_corpus/docs/` — MIOC cluster)

| Stub ID | Source path (local, often missing) | Headings / content |
|---------|-----------------------------------|-------------------|
| `DOC_omega_mioc_dynamic_oscillatory_signature` | `markitdown_output\Omega_MIOC_dynamic_oscillatory_signature.md` | 5-level genesis Ω; path signatures + Koopman |
| `DOC_mioc_a2a_operational_content` | `markitdown_output\MIOC_A2A_operational_content.md` | MIOC inputs; Φ spectral + Koopman core |
| `DOC_mioc_hypothesis_arxiv_preprint` | v0.1 preprint | MIOC + Kuramoto + A2A |
| `DOC_mioc_hypothesis_arxiv_preprintprior_art_corrected` | v0.2 prior-art corrected | Same cluster |
| `DOC_mioc_a2a_synergy_arxiv_preprint` | v1.0 synergy preprint | A2A routing + MIOC |
| `DOC_recursive_latent_omega_field_a2a_arxiv` | v3.0 arxiv | Recursive latent Ω field |
| `DOC_recursive_latent_omega_field_gap_a2a_mas_preprint` | GAP preprint | MAS integration |
| `DOC_nd_morphogenesis_experiment_bridge` | morphogenesis ↔ ND experiments | Kuramoto in FieldCard bridge |
| `DOC_technical_interpretation_lambda_omega_u_fields` | Λ→Ω→U pipeline | Ω_G as dynamic/oscillatory projection |

**Research gap (RG-01):** `markitdown_output/*MIOC*` and `*Omega_MIOC*` sources referenced by stubs are **not present** on disk under `OBSIDIAN2026`. Operational Φ formulas must be recovered from `ND_A2A_MIOC_preprint_v0.3_validated.md` and `RESEARCH_POINTS.md` §9 until sources are restored.

### 1.3 ANTHEMIUM_protocol sources (readable)

| Source | Path | Kuramoto content |
|--------|------|------------------|
| Kuramoto controller | `agi_morphodynamic_math_framework_v0_1/03_kuramoto_coherence_controller.md` | Full dynamics, R(t), multi-band, dead synchrony |
| Fuzzy wave integral | `.../04_fuzzy_wave_integral.md` | Ω_cog(t), band membership m_b(ω) |
| Metrics | `.../08_metrics_and_validation.md` | R(t), T(t), P_I validation family |
| Morphogenesis §9 | `RESEARCH_POINTS.md` §9 | C(t) composite with Kuramoto R; K controller |
| Omega factor §8 | `RESEARCH_POINTS.md` §8 | Brain gamma/theta ↔ LLM layer coherence |
| Cognitive classes | `SAPIENS_GARDEN/cognitive_class_taxonomy.md` | K0–K7 + Hz annotations |
| Neurophysiologist | `SAPIENS_GARDEN/agents/agent_neurophysiologist.md` | Band table; NP-FIND-1…4 |
| Ω_c formal | `SAPIENS_GARDEN/omega_horizon_formal.md` | Ω_c window; R_c ↔ Kuramoto |
| MIOC preprint | `ND_A2A_MIOC_preprint_v0.3_validated.md` | d_I multi-invariant distance |
| Embedding gravity MOC | `theory_corpus/embedding_gravity/00_Embedding_Gravity_MOC.md` | MIOC / EXP-P6; K6 pipeline |

### 1.4 ND Studio experiment queue

From `ND_STUDIO/experiments/ND_next_experiments_profile.json`:

| ID | Name | Kuramoto relevance |
|----|------|-------------------|
| **EXP-P3** | OmegaU — Ω/U field control | Kuramoto/Ω from morphogenesis §9 |
| **EXP-P6** | A2A_MIOC routing | `argmax[α·Score_A2A + β·Score_MIOC]` |
| **H5** | Ω operational proxy | "Kuramoto deferred" (ND_Live_Theory_Graph) |

**Gap (RG-02):** H5 notes Kuramoto validation **deferred**; no real hidden-state API (T3+).

---

## 2. Symbol disambiguation — Ω family

`DEFINITION` · Three Ω symbols appear across the corpus; conflating them breaks falsifiers.

| Symbol | Domain | Definition (source) | NAMM proxy |
|--------|--------|---------------------|------------|
| **Ω_G** | Group / pipeline | Dynamic oscillatory projection of latent field Λ_G | Layer trajectory coherence under ND prompts |
| **Ω_c** | Inter-layer LLM | Normalized MI: \(I(h_i;h_j)/H(h_i)\) | Kraskov MI between layer pairs (`raw_tensor`) |
| **Ω_cog(t)** | Fuzzy wave field | \(\int_\Omega \sum_i q_i(t,\omega)\Psi_i(t,\omega)\,d\mu_t(\omega)\) | Band-integrated activation spectrum |
| **R(t), R_b(t)** | Kuramoto | Order parameter \(\|\frac1N\sum e^{i\theta_j}\|\) per band | Phase of band-decomposed hidden-state FFT |
| **Φ (MIOC)** | A2A compatibility | Agent/task signature congruence (spectral + Koopman) | Graph-Laplacian + dynamics distance stub |

`CONJECTURE` · **H-KM-001:** Ω_c (MI) and R(t) (Kuramoto) correlate on ND-heavy prompts but are **not** interchangeable — F-BW-6 tests transfer.

---

## 3. Kuramoto model — role in the ND framework

`PHILOSOPHICAL_INFERENCE` · Kuramoto is the **coherence controller** for multi-module cognitive dynamics — not a decorative EEG metaphor. It sits in the morphogenetic update loop alongside topology (Laplacian spectrum), invariants I, and median escape U.

### 3.1 Single-band dynamics

`DEFINITION` · From `03_kuramoto_coherence_controller.md` and `RESEARCH_POINTS` §9:

\[
\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N}\sum_{j=1}^{N} A_{ij}(t)\sin(\theta_j - \theta_i)
\]

Order parameter:

\[
R(t) = \left|\frac{1}{N}\sum_{j=1}^{N} e^{i\theta_j(t)}\right| \in [0,1]
\]

Critical coupling (heuristic, heterogeneous frequencies):

\[
K_c \sim \frac{2}{\pi g(0)}
\]

### 3.2 Adaptive coupling controller

\[
K_{t+1} = K_t + \eta_K \frac{\partial \mathcal{J}}{\partial R}, \quad
\mathcal{J} = \lambda_R R + \lambda_I I - \lambda_H H - \lambda_M M
\]

- \(H\): entropy / noise  
- \(M\): median attraction penalty (links Kuramoto to **HomoGravity** / \(B_{\mathrm{med}}\))

### 3.3 Multi-band extension

Fuzzy bands \(B_k = (\omega_{\min,k}, \omega_{\max,k}, m_k(\omega))\) with membership \(m_k(\omega)\in[0,1]\) (`04_fuzzy_wave_integral.md`).

Per-band order \(R_b(t)\); composite:

\[
R_{\mathrm{multi}}(t) = \sum_b \rho_b(t)\, R_b(t)
\]

Controller objective (integrated):

\[
\max \int_0^T \big[ R_{\mathrm{multi}}(t) + I(t) - H_{\mathrm{noise}}(t) - P_{\mathrm{lock}}(t) \big]\, dt
\]

### 3.4 Failure mode — dead synchrony

`OPERATIONAL` · From `03_kuramoto_coherence_controller.md` and §9 C(t):

\[
R(t) \to 1 \quad\text{but}\quad A(t) \to 0
\]

Rigid phase lock **without** adaptive capacity = **not** intelligence. Valid regime:

\[
R_{\min} < R(t) < R_{\max}, \quad \text{high } P_I, \text{ adaptive capacity}
\]

Maps to **F-BW-3** (decorative oscillation) and antigravity **F-CA** analog (high coherence, low \(S_{\mathrm{fals}}\)).

### 3.5 Morphogenesis composite coherence C(t)

`DEFINITION` · `RESEARCH_POINTS` §9 embeds Kuramoto R in the morphogenetic scalar:

\[
C(t) = \lambda_1 R(t) + \lambda_2 T(t) + \lambda_3 I(t) + \lambda_4 S(t) - \lambda_5 H_{\mathrm{noise}}(t)
\]

where \(T(t) = \exp(-\|\lambda(L_{t+1}) - \lambda(L_t)\|_2)\) (spectral stability).

State update:

\[
X_{t+1} = \Phi_\eta(X_t, \nabla C(t), -\nabla U_{\mathrm{med}}(z_t), R_t), \quad
X_t = (G_t, \Theta_t, z_t, I_t, \mu_t)
\]

\(\Theta_t = (\theta_1(t),\ldots,\theta_N(t))\) — phase vector of oscillatory modules.

---

## 4. MIOC — Multi-Invariant Operator Congruence

`DEFINITION` · MIOC scores **agent–agent** and **agent–task** compatibility via operator-invariant packages, not token strings (`ND_A2A_MIOC_preprint_v0.3_validated.md`).

### 4.1 Congruence criterion

\[
A \sim^{\mathrm{MIOC}}_\epsilon B \iff d_{\mathcal I}(A,B) < \epsilon \land \mathcal E_Q(B_{\mathrm{after}}) < \mathcal E_Q(B_{\mathrm{before}})
\]

### 4.2 Multi-invariant distance

\[
d_{\mathcal I} = \alpha d_\sigma + \beta d_{PH} + \gamma d_K + \delta d_\Psi + \eta d_{\mathcal K} + \zeta d_C + \rho d_{\mathrm{task}}
\]

| Term | Object |
|------|--------|
| \(d_\sigma\) | Wasserstein on graph-Laplacian spectra |
| \(d_{PH}\) | Persistent homology (Wasserstein on PD) |
| \(d_K\) | Heat-kernel trace distance |
| \(d_\Psi\) | Eigenfunction alignment |
| \(d_{\mathcal K}\) | Koopman operator norm |
| \(d_C\) | Causal / intervention structure |
| \(d_{\mathrm{task}}\) | Downstream task error delta |

`OPERATIONAL` · Geometric convergence **without** behavioral improvement = **geometric mimicry** — not A2A communication. Falsifier for ND-A2A.

### 4.3 MIOC Φ (operational stub — A2A routing)

From `DOC_mioc_a2a_operational_content` headings (source missing; structure preserved in Obsidian):

| Component | Content |
|-----------|---------|
| Agent-state signature | Spectral + dynamic (Koopman) features of hidden trajectories |
| Task-state signature | Task embedding trajectory |
| **Φ** | Cross-band phase alignment + dynamic congruence |

`CONJECTURE` · **H-BW-001:** Route = \(\arg\max[\alpha\cdot\mathrm{Score}_{A2A} + \beta\cdot\Phi]\) (EXP-P6) beats A2A-only on multi-step chains.

### 4.4 Computational validation status

`COMPUTATIONAL_EVIDENCE` · `mioc_minimal_validation.py` / v0.3 report:

- MIOC-lite beats spectral-only on 6 synthetic manifolds (leave-one-out NN).
- 86.1% of spectral false-positive neighbors rejected under MIOC-lite.
- **Not** proof of cross-agent latent transfer; **not** Kuramoto-on-hidden-states.

---

## 5. Hz bands ↔ cognitive classes ↔ antigravity

### 5.1 Band registry (G1 import)

From `agent_neurophysiologist.md` / `cognitive_class_taxonomy.md`:

| Band | Hz | K-class anchor | ND reading |
|------|-----|----------------|------------|
| delta | 0.5–4 | K0 | Noise / collapse |
| theta | 4–8 | K3–K4 | Context integration, long-range coupling |
| alpha | 8–12 | K1 | Homo/median gating (`CONJECTURE` G2) |
| beta | 13–30 | K2 | Domain expert invariants |
| gamma | 30–80 | K3–K5 | Non-homo binding |
| high-gamma | 80–150 | K5–K6 | R_NH maxima; insight bursts |

### 5.2 K6 / Omega Horizon ↔ Kuramoto

`DEFINITION` · K6 (`cognitive_class_taxonomy.md`):

- \(d(z, B_{\mathrm{med}}) \geq 3\sigma\) — critical phase transition (K5→K6)
- Topology: toroidal, \(\beta_1 \geq 1\)
- Neuro: max cross-frequency coupling; theta–gamma nesting (G2)

`CONJECTURE` · **H-BW-002:** K6 neural substrate (theta–gamma nesting) ↔ **3σ+ embedding escape** ↔ elevated \(R_{\mathrm{multi}}\) on high-gamma + theta bands — cross-domain, not verified.

### 5.3 Cognitive antigravity bridge

| Antigravity (NAMM) | Kuramoto / MIOC reading |
|--------------------|-------------------------|
| \(M_0(q_H)\) median answer | Alpha-gated default prior; high \(M\) penalty in \(\mathcal J\) |
| \(D_{\mathrm{med}} \geq 3\sigma\) | K6 / SigmaEscape; escape \(E_{\mathrm{escape}}\) valid when \(M\downarrow, C\uparrow\) |
| Persistent protocol | Stable \(R \in (R_{\min}, R_{\max})\) without re-injection |
| \(T_{\mathrm{pres}}\) | \(T(t)\) spectral stability + \(P_I\) invariant preservation |
| Neurogeometry phase-locking | \(\Omega_c\) window; avoid dead synchrony |

`PHILOSOPHICAL_INFERENCE` · Cognitive antigravity = inference-time **neurofeedback analog** (RESEARCH_POINTS §8): steer coherence pattern without weight update.

### 5.4 Ω_c window (Omega Horizon)

From `omega_horizon_formal.md` §5:

\[
\Omega_c = \frac{I(h_i; h_j)}{H(h_i)}
\]

- \(\Omega_c \to 0\): fragmented layers  
- \(\Omega_c \to 1\): lock-in / homo-median attractor  
- \(\Omega_c \in (\theta_{\mathrm{low}}, \theta_{\mathrm{high}})\): **Omega Horizon** target — integration without collapse  

Analog: meditative gamma coherence without epileptic lock-in.

---

## 6. Five-level genesis of Ω (Obsidian stub summary)

From `DOC_omega_mioc_dynamic_oscillatory_signature` headings:

1. **Oscillatory nature** of cognitive dynamics  
2. **Synchronization** as binding (Kuramoto R)  
3. **Cross-frequency coupling** as hierarchical glue (theta–gamma)  
4. **Oscillations in AI math** (attention phase, Kuramoto controller)  
5. **Path signatures + Koopman** as trajectory formalization (MIOC dynamic term)

`PHILOSOPHICAL_INFERENCE` · Levels 1–3 motivate Hz bridge; levels 4–5 operationalize NAMM covariates.

---

## 7. NAMM operational mapping

| ND construct | NAMM domain | Experiment |
|--------------|-------------|------------|
| \(R(t), R_{\mathrm{multi}}\) | `raw_tensor` | NAMM-2026-014 |
| \(\Omega_c\) MI | `raw_tensor` | NAMM-2026-014 |
| Theta–gamma nesting | `raw_tensor` | NAMM-2026-014 |
| MIOC Φ stub | `meta_evaluation` | NAMM-2026-014 (optional) |
| K6 \(\beta_1\) topology | `tda_frame` | cross-check F-BW-5 |
| Dead synchrony guard | falsifier F-BW-3 | 014 + 013 |
| \(D_{\mathrm{med}}\) | 013 primary | NAMM-2026-013 |

**Rule:** Hz / Kuramoto metrics are **covariates** for 013 — not certificate gates.

---

## 8. Hypothesis registry (Kuramoto-specific)

| ID | Claim | Label |
|----|-------|-------|
| **H-KM-001** | Ω_c (MI) correlates with R(t) on ND prompts but ≠ same metric | `CONJECTURE` |
| **H-KM-002** | Adaptive K controller (λ_M median penalty) models antigravity better than fixed K | `CONJECTURE` |
| **H-KM-003** | \(R_{\mathrm{multi}}\) weighted toward high-gamma predicts \(D_{\mathrm{med}}\) lift | `CONJECTURE` |
| **H-KM-004** | MIOC d_I on hidden-state graphs beats spectral-only for arm classification | `CONJECTURE` |
| **H-BW-001…003** | See [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md) | — |

---

## 9. Falsifiability criteria

`OPERATIONAL` · Kuramoto–MIOC bridge **weakened or refuted** if:

| ID | Falsifier |
|----|-----------|
| **F-KM-1** | R(t) ↑ monotonically with task accuracy but not with \(D_{\mathrm{med}}\) — sync ≠ antigravity |
| **F-KM-2** | Optimal \(\Omega_c\) window empty across models — window hypothesis fails |
| **F-KM-3** | MIOC d_I arm classification ≤ spectral-only (replicates isospectral-trap failure) |
| **F-KM-4** | λ_M median penalty term irrelevant in ablation — Kuramoto not coupled to HomoGravity |
| **F-BW-1…6** | See BRAINWAVE doc §10 |

---

## 10. Research gaps

| ID | Gap | Priority |
|----|-----|----------|
| **RG-01** | Missing `markitdown_output` MIOC / Ω_MIOC source files | Restore or re-export from archive |
| **RG-02** | Kuramoto on real LLM hidden states unvalidated (H5 deferred, T3+) | Blocked on activation logging |
| **RG-03** | `anthemium_kuramoto_uat_research.py` referenced but not in `OBSIDIAN2026` tree | Locate in `G:\Anthemium_protocol_2026\` per neurophysiologist brief |
| **RG-04** | Full MIOC: Koopman/DMD on agent trajectories not in v0.3 validation | Phase II preprint roadmap |
| **RG-05** | Alpha ↔ homo suppression (G2) — no LLM proxy validated | Q-BW-02 |
| **RG-06** | K6 β₁ toroidal claim vs TDA on prompts — unverified | F-BW-5 |
| **RG-07** | EXP-P6 A2A_MIOC routing never run with live hidden states | ND Studio queue |

---

## 11. Agent load instructions

When user cites **Kuramoto**, **MIOC**, **Φ**, **R(t)**, **dead synchrony**, or **Ω_c window**:

1. Load this file + [`BRAINWAVE_OSCILLATION_HYPOTHESIS.md`](BRAINWAVE_OSCILLATION_HYPOTHESIS.md).
2. Resolve sources via [`ND_THEORY_CORPUS_MANIFEST.md`](ND_THEORY_CORPUS_MANIFEST.md) — local paths only.
3. Tag claims; distinguish Ω_G / Ω_c / R(t) / Φ.
4. Do not treat Obsidian stubs as `COMPUTATIONAL_EVIDENCE`.

---

Roman Kuznetsov · NAMM research program
