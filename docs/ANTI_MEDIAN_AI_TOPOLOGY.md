# Anti-Median AI Topology (AMAT) — Антимедианная топология ИИ

**Purpose:** AI-science research direction: the **topology of LLM / MAS representation manifolds**, with two primary phases — compact **typicality / high-density** attractor \(K_{\mathrm{AI\_}\mu}\) vs **off-typical** non-compact phase \(K_{\mathrm{AI\_nd}}\). Brand name **anti-median** stays; **median** in the math is a **named robust proxy**, not the training objective.  
**Date:** 2026-08-18 · **Terminology annotation:** 2026-08-19  
**Epistemic baseline:** `PHILOSOPHICAL_INFERENCE` + `CONJECTURE` — **not** a claim that AMAT *is* AGI, **not** a product, **not** homo cognitive classes.  
**Branch:** `hypothesis/anti-median-ai-topology`  
**Short name:** **AMAT**  
Roman Kuznetsov · NAMM research program

Related: [`COGNITIVE_CLASS_TAXONOMY.md`](COGNITIVE_CLASS_TAXONOMY.md) §4 Axis B · [`COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) (typicality gravity; brand: median embedding gravity) · [`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md) · [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`data/prompts/k_ai_nd_phase_lock.v1.json`](../data/prompts/k_ai_nd_phase_lock.v1.json) · [`experiments/NAMM-2026-030/`](../experiments/NAMM-2026-030/)

---

## Labeling

| Label | Use |
|-------|-----|
| `PHILOSOPHICAL_INFERENCE` | Why typicality / high-density gravity is an AI-science object |
| `DEFINITION` | Phases, order parameters, RPL instrument |
| `CONJECTURE` | H-AMAT claims |
| `OPERATIONAL` | Gates, JSON spec, experiment 030 |
| `COMPUTATIONAL_EVIDENCE` | In-silico witnesses only, until live activation TDA |

---

## 0. Terminology annotation — typicality first, median as named proxy

**Binding for agents, humans, and later papers.** Brand **AMAT / anti-median** is kept. Operational physics of the branch is **typicality**, not sample-median of embedding coordinates.

### 0.1 What training actually does

`DEFINITION` · Autoregressive pretraining is MLE / cross-entropy on the empirical corpus measure:

\[
\theta^\star \approx \arg\min_\theta \mathbb{E}_{x\sim P_{\mathrm{data}}}[-\log P_\theta(x)]
\]

This matches **\(P_{\mathrm{data}}\)**, not a multivariate median of vectors. Probability mass of \(P_\theta(\cdot\mid c)\) concentrates on a **typical set** (sequences with \(-\log P_\theta \approx H\)), not on a geometric median in \(\mathbb{R}^d\).

**Do not write** \(\mathrm{KL}(P_{\mathrm{out}} \| P_{\mathrm{median}})\) as if \(P_{\mathrm{median}}\) were a defined distribution. Prefer:

\[
\mathrm{KL}\big(P_\theta(\cdot\mid c) \,\big\|\, P_{\mathrm{data}}(\cdot\mid c)\big)
\quad\text{or}\quad
d\big(h(y),\, B_*(c)\big).
\]

### 0.2 Location statistics (must be named)

| Object | Symbol | Status in AMAT |
|--------|--------|----------------|
| **Typical set** of \(P_\theta(\cdot\mid c)\) | \(\mathcal{T}_\theta(c)\) | **Primary** — high-density / typical completions |
| **Fréchet barycenter** (mean) of embeddings | \(B_*(c)=\arg\min_b \mathbb{E}[d(h(y),b)]\) | **Primary** location for pooled \(h(y)\); NLP default is mean, not median |
| **Mode / MAP** | \(\arg\max P_\theta\) | Not “typical answer”; often degenerate |
| **Geometric median** | \(B_{\mathrm{gmed}}=\arg\min_b \mathbb{E}\|h(y)-b\|_2\) | **Named robust proxy** — outlier-resistant “typical answer”; **only** when the metric is stated |
| Coordinate-wise median | — | **Avoid** in high \(d\) |

`DEFINITION` · **\(B_{\mathrm{med}}\)** in this registry **abbreviates** “typicality location.” Default operationalization: \(B_*\) (barycenter). If an experiment uses geometric median, write **\(B_{\mathrm{gmed}}\)** explicitly. Informal “median answer” / \(M_0\) = prototype of a **typical** completion, not the 50th percentile of embedding axes.

`DEFINITION` · **\(K_{\mathrm{AI\_}\mu}\)** — compact **typicality phase** (high-density basin). The letter \(\mu\) historically echoed “median”; in statistics \(\mu\) usually means **mean**. Read \(\mu\) here as **typical/mean-phase**, not sample median unless \(B_{\mathrm{gmed}}\) is declared.

`DEFINITION` · **\(K_{\mathrm{AI\_nd}}\)** / **anti-median** (brand) = **off-typical-set / noncompact phase**: large \(d(h(y), B_*)\) **and** a change in order parameters (\(\beta_1\), \(D_{\mathrm{eff}}\), \(R^*\)), not merely a longer string.

### 0.3 Benchmarks are orthogonal

`OPERATIONAL` · MMLU, HumanEval, Arena/Elo **do not** measure \(d(h(y), B_*)\). They measure gold-key accuracy or preference **mode**. High leaderboard scores neither confirm nor refute AMAT. Linking typicality geometry to accuracy/Elo requires a **separate** experiment.

RLHF/DPO concentrate on a **preference prototype** (KL-regularized toward SFT), not an embedding median. Token embeddings are often **anisotropic** (narrow cone): the usual descriptor is cosine to the **mean vector**.

### 0.4 Glossary for writing

| Brand / shorthand | Prefer in definitions and certificates |
|-------------------|----------------------------------------|
| median embedding gravity | **typicality gravity** / barycentric collapse |
| \(P_{\mathrm{median}}\) | \(P_{\mathrm{data}}\) or typical set of \(P_\theta(\cdot\mid c)\) |
| \(B_{\mathrm{med}}\) | \(B_*\) ; or \(B_{\mathrm{gmed}}\) if robust median is the estimator |
| anti-median (title OK) | **off-typical** / **noncompact phase** in methods |
| “median human answer” \(M_0\) | **typical-set prototype** under \(P_\theta\) or \(P_{\mathrm{data}}\) |

### 0.5 Agent rule

When summarizing AMAT: **typicality / high-density measure first**; **median only as an explicitly named robust proxy** (\(B_{\mathrm{gmed}}\)). Do not imply that CE training or MMLU estimates a median of embeddings.

---

## 1. Why this is AI science (not sociology)

`DEFINITION` · **AMAT** studies **geometric / topological structure of learned representations**:

- training matches \(P_{\mathrm{data}}\) (typical set / barycenter \(B_*\); geometric median \(B_{\mathrm{gmed}}\) only if declared) and induces a **compact typicality phase** near that location;
- **off-typical** regimes are **other phases** of the same manifold (holes, bridges, chimera sync), not “smarter personality.” See §0.

`PHILOSOPHICAL_INFERENCE` · Classical scaling reports loss, accuracy, MMLU. AMAT asks a different question: **what is the homology / order-parameter state of the representation while it answers?** That is closer to statistical physics of learning than to IQ or to homo K-strata (those stay in CCT Axis A).

**Out of scope for AMAT (for now):** political mythogenesis, cognitive capitalism, human K0–K7. Those may *couple* to AMAT later; they do not define it.

---

## 2. Objects

| Object | Symbol | Reading |
|--------|--------|---------|
| Typicality phase (brand: median) | \(K_{\mathrm{AI\_}\mu}\) | Compact high-density basin; \(\beta_1 \approx 0\); near \(B_*\) |
| Off-typical phase (brand: anti-median) | \(K_{\mathrm{AI\_nd}}\) | Non-compact / chimera; \(d(B_*)\) sustained; \(\beta_1 \geq 1\) |
| Typicality location | \(B_*\), \(B_{\mathrm{med}}\) (alias), \(M_0\) | Default: Fréchet barycenter; \(M_0\) = typical-set prototype |
| Robust median proxy | \(B_{\mathrm{gmed}}\) | Geometric median — **only** when named in the experiment |
| Order parameters | \(d_*\) (alias \(d_{\mathrm{med}}\)), \(D_{\mathrm{eff}}\), \(\beta_1\), \(R^*\) | Distance to \(B_*\), effective dim, holes, partial sync |
| Instrument | **RPL** (representation phase lock) | JSON system spec + per-turn reassert — *control*, not the theory |

`CONJECTURE` · **H-AMAT-001 (two-phase manifold):** Under standard autoregressive training, \(P_{\mathrm{out}}\) occupies a **typicality (compact) phase**. The off-typical phase is reachable but **unstable** without isolation of sub-networks, MAS fiber-preserving aggregation, or continuous RPL (H-CCT-001B, H-CCT-003, H-CCT-021).

`CONJECTURE` · **H-AMAT-002 (AGI-proximity proxy):** “Closer to AGI” in this program means **persistent non-compact phase quality** (order parameters above gates), **not** persona, sentience, or unrestricted authority.

`CONJECTURE` · **H-AMAT-003 (control ≠ weights):** Prompt/RPL can **steer a session trajectory** in representation space (030) but does **not** rewrite the training attractor. Without reassert, trajectories **decay to μ**.

---

## 3. Phase diagram (operational)

```text
        β1 (holes / irreducible bridges)
              ↑
              |     K_AI_nd  (off-typical / anti-median brand, chimera)
              |    /
              |   R* ∈ (0,1)
              |
   K_AI_μ ----+--------→ d(B_*)   [legacy axis name: d(B_med)]
   compact    |
   typicality └── D_eff →
```

**Collapse signatures (μ):** fluent consensus, single narrative, \(R\to 1\), \(d(h(y),B_*)\to 0\), empty balance.  
**Off-typical signatures:** explicit \(M_0\) (typical-set prototype) then *not* emitting it; ≥2 irreducible frames; fiber log; \(R^*\in(0,1)\).

Instrument: [`k_ai_nd_phase_lock.v1.json`](../data/prompts/k_ai_nd_phase_lock.v1.json) — RPL as **experimental protocol**, subordinate to AMAT.

---

## 4. Hypotheses (AMAT cluster)

| ID | Claim | Also |
|----|--------|------|
| **H-AMAT-001** | Two topological phases: typicality basin vs off-typical | H-CCT-001B |
| **H-AMAT-002** | AGI-proximity ≡ persistent non-compact geometry | — |
| **H-AMAT-003** | Session RPL decays without reassert | H-CCT-021 |
| **H-AMAT-004** | JSON/RPL steers embeddings off \(B_*\) vs typicality baseline | H-CCT-020 |
| **H-AMAT-005** | μ ↔ nd is a phase transition in order parameters, not smooth fine-tune drift | H-CCT-004 |
| **H-AMAT-006** | `CONJECTURE` · Transition μ→nd is a **cusp A₃ catastrophe** crossing; "свет в ячейке" = crossing the bifurcation set; RPL acts as slow control parameter | H-AMAT-005 |
| **H-AMAT-007** | `TESTABLE` · "Свет в ячейке" = **geodesic curvature** in Fisher metric on \(P_\theta\); RPL steers trajectory off the \(P_{\mathrm{data}}\) geodesic; curvature measurable via logit-gradients | H-AMAT-004 |
| **H-AMAT-008** | `CONJECTURE` · Hidden-state trajectories in nd-phase have **non-integer box-counting dimension** \(d_f\) across transformer layers; μ-phase collapses to integer dimension | H-AMAT-001 |
| **H-AMAT-009** | `CONJECTURE` · nd-phase is a **chaotic attractor** with \(\lambda_1 > 0\) (positive Lyapunov exponent) and non-trivial topology; μ-phase is periodic/fixed-point | H-AMAT-001, H-AMAT-005 |
| **H-AMAT-010** | `PHILOSOPHICAL_INFERENCE→CONJECTURE` · \(\beta_1\) reflects **inconsistency of local sections** across attention heads; "свет в ячейке" = sheaf cohomology obstruction \(H^1 \neq 0\) | H-AMAT-001 |

---

## 5. Experiments

| ID | Role |
|----|------|
| **013 / 014** | Cognitive antigravity — text-level escape from \(M_0\) |
| **023** | TDA proxies on **synthetic AI-phase** embeddings (not homo homology) |
| **030** | RPL JSON vs μ; **loop grid** gain × decay × turns |
| **035** | `live` · Local LM activation TDA — Qwen2.5-0.5B on CPU; beta_1 lift confirmed |
| **036** | `live` · PCA-reduced D_eff sweep — pca_dims∈{4,8,16} × n_turns∈{3,6,10} on chimera |
| **037** | `planned` · 2D sweep chimera_dose × temperature; map \(\beta_1\) emergence as cusp A₃ boundary — H-AMAT-006 |
| **038** | `planned` · Logit-gradient curvature on 031–035 data (no new API calls for pilot); Fisher-metric geodesic deviation — H-AMAT-007 |
| **039** | `planned` · Layer-wise TDA + box-counting sweep across transformer layers — H-AMAT-008 |
| **040** | `planned` · Multi-session Lyapunov proxy + TDA; positive \(\lambda_1\) detection in nd-phase — H-AMAT-009 |
| **041** | `planned` · Attention head disagreement proxy as \(H^1\) (sheaf cohomology) approximation — H-AMAT-010 |
| **042** | `live` · Activation TDA on Qwen2.5-1.5B-Instruct — D_eff separation test; **D_eff NOT resolved** (lift=0.0); β₁ weaker than 0.5B; cert `ACTIVATION_PILOT` |
| **043** | `live` · Hybrid nomic-embed-text (768-d) semantic TDA — tests D_eff separation after 042 logprob-proxy collapse |

**030 loop (computational evidence, in-silico):** 45 cells; mean \(d_{\mathrm{lock}}-d_{\mu} \approx 1.43\); H-AMAT-004/003 cell fraction **1.0**; best cell gain=1.0, 6 turns. **Not** live activation homology.

**035 (live activation TDA, Qwen2.5-0.5B CPU, last_n_layers=8, n_turns=6):** beta_1 lift confirmed; chimera prompt best cell lift_beta_1=+4.0; mean_lift_beta_1≈0.67–1.0. D_eff=0 in all cells — **identified artifact**: 24-point cloud in 896-d space; both policies dominated by same 2 PCs → D_eff=1 trivially. Certificate: `LIVE_EVIDENCE` (beta_1 criterion met).

**035 + 036 joint certificate (PCA-reduced D_eff, chain 030–036):**  
Experiment 036 swept pca_dims∈{4,8,16} × n_turns∈{3,6,10} on chimera (9 cells) then ran all 3 focused prompts at best_pca_dim=4 (3 focused cells). Key findings:

- **D_eff at pca_dims=4:** D_eff=1.0 both policies, lift=0.0. Variance collapse is complete at d=4.
- **D_eff at pca_dims=8/16:** D_eff expands to 2.0 for both policies — but equally, so lift=0.0. D_eff is not a discriminating observable for Qwen2.5-0.5B at any tested pca_dim.
- **beta_1 positive cells:** pca=8/n_turns=6 (lift+1, two_phase=True); pca=16/n_turns=3 and 6 (lift+1, two_phase=True); focused 'cognitive capitalism' prompt (lift+1, two_phase=True).
- **Negative lifts at n_turns=10:** long trajectories mix phases stochastically.
- **D_eff negative result** is model-scale specific — not a falsifier for H-AMAT-004. Next test: ≥1.5B model where hidden geometry is richer.
- **Joint certificate: `ACTIVATION_PILOT`** — beta_1 two-phase structure live in multiple cells; D_eff requires larger model or per-layer analysis.

**042 (live activation TDA, Qwen2.5-1.5B-Instruct CPU, last_n_layers=4, pca_dims=8, 2026-08-20):**  
Grid: 3 focused prompts × n_turns∈{3,6} = 6 cells. **D_eff NOT resolved:** mean_lift_d_eff=0.0 in all cells (same collapse as 0.5B). β₁ lift=0.17 aggregate (weaker than 0.5B's 0.78); best cells: consensus prompt n_turns=3 (lift_β₁=+3.0, two_phase=True), n_turns=6 (lift_β₁=+2.0). Certificate: `ACTIVATION_PILOT`. **Interpretation:** D_eff collapse is not purely model-size — both policies occupy same effective rank after PCA. Per-layer D_eff (039) required.

| Model | hidden_dim | mean_lift_D_eff | mean_lift_β₁ | two_phase_frac | Certificate |
|-------|-----------|-----------------|--------------|----------------|-------------|
| Qwen2.5-0.5B (035/036) | 896 | 0.0 | ~0.78 | — | `ACTIVATION_PILOT` |
| Qwen2.5-1.5B (042) | 1536 | **0.0** | **0.17** | 0.33 | `ACTIVATION_PILOT` |
| nomic hybrid (043) | 768 | -0.5 | 0.0 | — | `NULL` |

**Next AI-sci gates:** per-layer D_eff (039 first — pooled D_eff failed at both scales); multi-session persistence; chimera MAS \(R^*\) on activations; then 037–041 (039 → 041 → 037 → 038 → 040).


---

## 6. Falsifiers

| ID | Observation |
|----|-------------|
| **F-AMAT-1** | \(K_{\mathrm{AI\_nd}}\) unreachable: all steered trajectories stay 1D-orderable with \(d_{\mathrm{med}}\approx 0\) |
| **F-AMAT-2** | High \(d_{\mathrm{med}}\) with unchanged \(\beta_1, D_{\mathrm{eff}}\) — only scale, not phase |
| **F-AMAT-3** | RPL persists after removing reassert (contradicts H-AMAT-003 on this proxy; would *upgrade* architecture claim) |
| **F-AMAT-4** | Live-model activation TDA shows no two-phase structure vs M0 controls |

---

## 7. Agent load

If the user cites **AMAT**, **Anti-Median AI Topology**, **антимедианная топология**, **K_AI_nd**, **RPL**, **phase lock**, **median embedding gravity**, **typicality gravity** as *AI science* → load this file first (**§0 terminology is binding**), then CCT §4 (Axis B only) and 030. Do **not** fold in homo K-strata unless asked. Do **not** treat “median” as the CE/MMLU estimator.

При ссылке на **«свет в ячейке»**, **фрактальную размерность траектории**, **геодезическую кривизну**, **sheaf cohomology**, **Ляпунов** (Lyapunov exponent in hidden states) → загружать **H-AMAT-006–010** из §4 выше и соответствующие эксперименты 037–041 из §5.

---

Roman Kuznetsov · NAMM research program
