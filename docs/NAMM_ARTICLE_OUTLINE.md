# NAMM Article Outline (Draft)

**Status:** working outline for a methods + case-study paper  
**Author:** Roman Kuznetsov · NAMM research program  
**Date:** 2026-09-07  
**Scope:** Non-Anthropic Mathematics Mode (NAMM) as a verification-first research program; AMAT experiments 037–041 as primary empirical case study  
**Zenodo alignment:** sibling EIA deposit [record 22646895](https://zenodo.org/records/22646895) (Proto-AGI Horizon, v1.0.0); NAMM v0.2.0 bundle via [`docs/ZENODO_RELEASE.md`](ZENODO_RELEASE.md) and [`scripts/build_zenodo_bundle.ps1`](../scripts/build_zenodo_bundle.ps1).

**Epistemic rule for the paper:** distinguish **brand / philosophical framing** (Anthemium, AMAT, “anti-median”, MUH motivation) from **operational claims** (Protocol v2 gates, `certificate.json`, logged falsifiers, reproducible experiment IDs). Report null and partial certificates as first-class outcomes.

Related repo docs: [`PROTOCOL_V2.md`](PROTOCOL_V2.md) · [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md) · [`SCI_FLOW.md`](SCI_FLOW.md) · [`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) · [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`OPEN_SOURCE_LANDSCAPE.md`](OPEN_SOURCE_LANDSCAPE.md) · [`proactive-ai/INTEGRATION.md`](proactive-ai/INTEGRATION.md)

---

## 1. Working title (choose one)

1. **Non-Anthropic Mathematics Mode: Verification-First Discovery of Machine-Native Structure with Certificate-Gated Negative Results**
2. **Certificates Before Formulas: A Reproducible Protocol for Machine-Native Mathematical and Representation-Geometry Evidence**
3. **NAMM Protocol v2 and the AMAT Pilot Loop: Falsifiable AI-Science Metrics on Local LLM Hidden States**

*Subtitle option (any title):* “Case study: Anti-Median AI Topology experiments 037–041 under Sci Flow”

---

## 2. Abstract (bullet points for prose expansion)

- **Problem:** Automated discovery systems often optimize **human-readable outputs** (papers, formulas, benchmark scores) rather than **verified machine-native artifacts** whose ground truth is independent of anthropic projection \(\pi_H\).
- **Approach:** NAMM (Non-Anthropic Mathematics Mode) — a **verification-first** cycle with hard acceptance gates (Protocol v2), `certificate.json` witnesses, explicit falsifiers, and mandatory `rejections.jsonl` logging.
- **Domains:** Operational adapters span finite graphs, program AST synthesis, rewriting systems, TDA scaffolds, open-problem shadows, and **AI-science** (`ai_science`) via the AMAT (Anti-Median AI Topology) branch — routed declaratively by **Sci Flow**.
- **Case study:** Five linked AMAT pilots (NAMM-2026-037–041) on local Qwen2.5-0.5B hidden states test hypotheses H-AMAT-006–010 (cusp boundary, Fisher curvature, fractal dimension, Lyapunov proxy, attention H¹ proxy).
- **Positive partial evidence:** Relative cusp onset enrichment (037, `CUSP_EVIDENCE`); curvature lift under RPL vs μ (038, `CURVATURE_EVIDENCE`); non-integer fractal gap and layer-wise profile (039, `FRACTAL_EVIDENCE` with H-AMAT-008-a **false**); attention-head disagreement pilot (041, `H1_PILOT` deepen).
- **Honest nulls / partials:** **Effective dimension \(D_{\mathrm{eff}}\)** does **not** discriminate μ vs off-typical policies at 0.5B or 1.5B after PCA (035/036/042; lift ≈ 0); Lyapunov / chaos hypothesis **unsupported** (040, `CHAOS_PARTIAL`, Rosenstein λ₁ < 0); β₁–H¹ correlation absent in 041 deepen.
- **Claim boundary:** We claim **methodology, reproducible artifacts, and bounded computational evidence** — not AGI, not product readiness, not breakthrough theorems. Philosophical inference (MUH, sheaf metaphor) is labeled non-evidential.
- **Broader link:** Sci Flow + certificate discipline provide a verification substrate for sibling **Endogenous Initiative Architecture (EIA)** / proactive-AI governance (contact gating mirrors attack checklist).

---

## 3. Problem: verification-first machine-native math vs human projection

### 3.1 Motivation

- Classical automated discovery (symbolic regression, AI Scientist pipelines) targets **anthropic compression** \(K_H\): short formulas, readable papers, leaderboard accuracy.
- NAMM inverts the epistemic anchor: **ground truth = verified certificate** (AST hash, eval witness, metric bundle), with human projection \(\pi_H\) explicitly **secondary and lossy** ([`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md), [`VISION.md`](VISION.md)).
- **Testable falsifiable claim** (operational): machine-native search can surface structures with **compression asymmetry** \(K_A \ll K_H\), baseline **independence**, and **generative holdout** — *before* a compact human formula exists ([`README.md`](../README.md)).

### 3.2 Failure mode that motivated Protocol v2

- NAMM-2026-001 accepted a Wiener-dominated linear combination (\(r \approx 0.938\)) under weak non-equivalence — motivating **correlation**, **simplify**, and **novelty floor** gates ([`PROTOCOL_V2.md`](PROTOCOL_V2.md)).

### 3.3 Brand vs operational (must appear in §1–2 of paper)

| Layer | Examples | Paper treatment |
|-------|----------|-----------------|
| **Brand / naming** | “Non-Anthropic Mathematics”, “Anti-Median AI Topology (AMAT)”, Anthemium lineage | Attribution only; not evidentiary |
| **Philosophical inference** | MUH widens search space; “structure beyond \(\pi_H\)” | Motivation paragraph; **not** proof premise ([`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md)) |
| **Operational** | Protocol v2 gates, Sci Flow routes, certificate tiers, falsifier IDs | Methods + Results ground truth |
| **Conjecture** | H-AMAT-001–010, graph-invariant hypotheses | Label `CONJECTURE`; support only via cited experiment IDs |

### 3.4 AMAT as NAMM `ai_science` domain (not a separate product claim)

- AMAT studies **representation geometry / topology** of LLM hidden states: typicality phase \(K_{\mathrm{AI\_}\mu}\) vs off-typical phase \(K_{\mathrm{AI\_nd}}\) ([`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md)).
- **Terminology binding:** “anti-median” is **brand**; operational text uses **typicality / barycenter** \(B_*\), not coordinate-wise median or MMLU as geometry estimators.
- MMLU, HumanEval, Arena **do not** measure \(d(h(y), B_*)\); any link to accuracy requires a **separate** experiment (state explicitly in Related Work).

---

## 4. Method: Protocol v2, certificates, falsifiers, Sci Flow

### 4.1 NAMM cycle (Protocol v2 checklist)

Present as Figure 1 pipeline (from [`PROTOCOL_V2.md`](PROTOCOL_V2.md)):

`INPUT → ABSTRACT → META-LIFT (≥2) → GENERATE → FORMALIZE → ATTACK → VERIFY → COMPARE → PROJECT`

- **Status labels:** `DEFINITION`, `CONJECTURE`, `COMPUTATIONAL_EVIDENCE`, `PHILOSOPHICAL_INFERENCE` (excluded from evidence chain).
- **Artifact layout:** `config.yaml`, `artifacts/certificate.json`, `rejections.jsonl`, `HUMAN_PROJECTION.md`.

### 4.2 Hard acceptance gates (v2)

1. Non-equivalence vs primary baseline  
2. Correlation gate: Pearson \(r \leq \tau\) (default 0.95)  
3. Prior-art simplify gate (sympy vs known baselines)  
4. Novelty floor ≥ N2 ([`NOVELTY_LADDER.md`](NOVELTY_LADDER.md))  
5. Representation metrics \(K_A\) proxies logged  
6. Baselines under **same compute budget**  
7. All rejections in `rejections.jsonl`

*Math-discovery experiments (001–008, 003, 007):* emphasize gates 1–6.  
*AMAT pilots:* hypothesis-linked **certificate tiers** + falsifiers F-AMAT-1–4.

### 4.3 Certificate-first artifacts

- **`certificate.json`:** canonical serialization, eval/hash witnesses, seeds, representation metrics, hypothesis support flags, tier label.
- **`human_projection.md`:** optional, trust-only for humans; agents re-evaluate certificates ([`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md)).
- **Sci Flow unified output:** `sci_flow.json` + aggregated metrics ([`SCI_FLOW.md`](SCI_FLOW.md)).

### 4.4 Sci Flow (declarative routing)

- Registry: `data/sci_flow_registry.yaml` maps experiment / hypothesis → modules (`catastrophe`, `tda`, `entropy`, …).
- CLI: `namm sci-flow run NAMM-2026-037`
- Stages: load config → resolve modules → dependency check → handler dispatch → aggregate → certificate check (`PARTIAL_EVIDENCE` / `INCONCLUSIVE` / `FALSIFIER_TRIGGERED`).

### 4.5 Domain universe (frame selection)

- [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md): catalog of operational vs stub vs planned domains; AMAT registered under `ai_science` + TDA overlay.
- Escalation after null: e.g. 001 → program AST (003) → raw tensor (007); AMAT 035 β₁ signal → specialized metrics 037–041.

### 4.6 Falsifiers (explicit in Methods)

**Protocol-level:** correlation/simplify/novelty rejections (logged).  
**AMAT cluster** ([`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) §6):

| ID | Trigger |
|----|---------|
| F-AMAT-1 | Off-typical phase unreachable (1D-orderable, \(d \approx 0\)) |
| F-AMAT-2 | High distance without \(\beta_1, D_{\mathrm{eff}}\) change (scale only) |
| F-AMAT-3 | RPL persists without reassert (would upgrade control claim) |
| F-AMAT-4 | Live activation TDA shows no two-phase structure vs controls |

### 4.7 Reproducibility & governance

- Python 3.12+, pytest CI, experiment seeds in config.
- Human-set falsifiability gates; AI allocates search budget ([`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md)).
- CC BY 4.0; cite via [`CITATION.cff`](../CITATION.cff).

---

## 5. Results: AMAT loop as case study (037–041)

*Primary narrative thread for the paper’s Results section. Secondary thread (one subsection): graph/program domains 003/007 as proof-of-protocol outside AMAT.*

### 5.1 Experimental setup (common)

- **Model:** Qwen/Qwen2.5-0.5B-Instruct (CPU local HF), unless noted.
- **Policies:** `mu` (typicality baseline) vs `lock_reassert` (RPL / off-typical steering).
- **Prompts:** focused chimera / consensus-non-optimality set (shared across 035–041 chain).
- **Order parameters:** \(d(B_*)\), \(\beta_1\) (activation TDA), \(D_{\mathrm{eff}}\) (PCA-participation proxy), certificate tier per hypothesis.

### 5.2 Chain context (035–036 → 037–041)

Brief pointer: NAMM-2026-035 established live \(\beta_1\) lift; 036 swept PCA dims — **\(D_{\mathrm{eff}}\) lift = 0** at all tested dims (document before 037–041 table).

### 5.3 Experiment table (main Results Table 1)

| ID | Hypothesis | Certificate tier | Key metric | Supported? |
|----|------------|------------------|------------|------------|
| **037** | H-AMAT-006 cusp A₃ | `CUSP_EVIDENCE` | Relative β₁ onset enrichment **0.89** (vs absolute saturation 0) | **Yes** (relative onset) |
| **038** | H-AMAT-007 Fisher curvature | `CURVATURE_EVIDENCE` | Mean κ lift lock−μ **+0.79**; corr(κ, β₁)**≈0.79** | **Yes** |
| **039** | H-AMAT-008 fractal \(d_f\) | `FRACTAL_EVIDENCE` | Non-integer gap lift **+0.02**; H-AMAT-008-a (**mean \(d_f\)**) **false** | **Partial** |
| **040** | H-AMAT-009 chaos λ₁ | `CHAOS_PARTIAL` | Pair λ₁ mean lift **+0.03**; Rosenstein **< 0** both policies | **No** |
| **041** | H-AMAT-010 sheaf H¹ proxy | `H1_PILOT` (deepen) | mean_lift_h1 **≈0.047**; β₁ lift **0** | **Partial** (a yes, b no) |

### 5.4 Honest reporting: \(D_{\mathrm{eff}}\) null (mandatory subsection)

**Title suggestion:** “\(D_{\mathrm{eff}}\) collapse as a negative discriminant (not a program falsifier)”

| Source | Model | mean_lift \(D_{\mathrm{eff}}\) | Interpretation |
|--------|-------|-------------------------------|----------------|
| 035/036 | Qwen 0.5B | **0.0** | 24-point cloud in 896-d → shared rank after PCA |
| 042 | Qwen 1.5B | **0.0** | Not purely scale artifact; both policies same effective rank |
| 043 | nomic hybrid | **−0.5** | `NULL` certificate |
| 039 | per-layer \(d_f\) | mixed | Layer profile informative; **mean** \(d_f\) not higher in lock |

**Paper language:** “\(D_{\mathrm{eff}}\) under current PCA protocol **does not** separate phases; \(\beta_1\), curvature, and relative cusp onset **do** (under stated budgets).”

### 5.5 What we do **not** claim from 037–041

- Not evidence that RPL rewrites training attractor (H-AMAT-003 session-only).
- Not formal sheaf cohomology (041 = JS disagreement **proxy**).
- Not AGI-proximity (H-AMAT-002 operationalized as geometry gates only — report as conjecture).
- Not benchmark superiority (MMLU etc. orthogonal).

### 5.6 Optional compact math-domain results (short §5.7)

- **NAMM-2026-003:** program AST certificate discipline (evolutionary search + sympy checks).
- **NAMM-2026-007:** first operational signal in raw tensor frame (F3g).
- **NAMM-2026-001:** calibration **null** — exemplar of rejection logging.

---

## 6. Contribution to AI science + proactive AI (EIA link, brief)

### 6.1 Contribution to AI science (operational)

1. **Verification-first AI-science metrics** on **live activations**, not synthetic embedding toys only.
2. **Tiered certificates** (`CUSP_EVIDENCE`, `CURVATURE_EVIDENCE`, …) enabling partial progress without headline overclaim.
3. **Explicit falsifier registry** (F-AMAT-*) tied to observable order parameters.
4. **Sci Flow** as reusable routing layer for multi-hypothesis programs (037–041 share infrastructure).
5. **Negative-result culture:** \(D_{\mathrm{eff}}\) null, H-AMAT-008-a false, H-AMAT-009 unsupported — publishable constraints.

### 6.2 Proactive AI / EIA (one short § or Discussion paragraph)

- **EIA** (Endogenous Initiative Architecture): endogenous initiative with dual-controller governance ([`proactive-ai/INTEGRATION.md`](proactive-ai/INTEGRATION.md)).
- **Crosswalk** ([`proactive-ai/docs/NAMM_ARTIFACT_CROSSWALK.md`](../proactive-ai/docs/NAMM_ARTIFACT_CROSSWALK.md)): NAMM **ContactGovernor** ↔ Protocol v2 attack checklist; **SenseMaking** ↔ TDA / β₁ tension; **041 H1 pilot** flagged as signal for EIA crosswalk.
- **Claim boundary:** integration is **architectural research mapping**, not shipped proactive product. Shared Anthemium cognitive frame; NAMM supplies **verification instrument**, EIA supplies **agency instrument**.

---

## 7. Related work / positioning vs benchmarks

### 7.1 Positioning matrix (from [`OPEN_SOURCE_LANDSCAPE.md`](OPEN_SOURCE_LANDSCAPE.md))

| Family | NAMM overlap | NAMM gap filled |
|--------|--------------|-----------------|
| AI Scientist agents (Sakana, DeepScientist, …) | Hypothesis → experiment loop | Output = **`certificate.json`**, not LaTeX paper |
| Hypothesis + falsification (POPPER, PiEvo) | Popper-style rejection | Machine-native artifacts + \(K_A/K_H\) |
| Evolutionary program search (FunSearch, OpenEvolve) | Strong (003, 007) | Independence + novelty ladder + frame escalation |
| Symbolic regression (PySR) | Weak overlap | Anthropic formula target vs certificate target |
| Formal proving (LeanDojo, DeepSeek-Prover) | Rewriting (002) | Computational certificates at scale |
| Representation interpretability (activation patching, probing) | AMAT uses hidden states | **Phase diagram + falsifiers**, not single-metric probes |

### 7.2 Benchmarks explicitly **not** competing with

- MMLU, HumanEval, GSM8K, Arena/Elo — accuracy / preference modes, not \(d(h,B_*)\) or \(\beta_1\) ([`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) §0.3).

### 7.3 Adjacent technical literature (to cite)

- Persistent homology on neural representations / TDA for deep learning.
- Catastrophe theory / bifurcation in learning dynamics (careful: pilot-scale evidence only).
- Information geometry / Fisher metric on language models.
- Lyapunov / chaos metrics for RNN/Transformer trajectories (note Rosenstein negative result).
- AI4Science agent surveys (contrast end-to-end paper generation).

---

## 8. Target venues

### 8.1 Primary (methods + reproducibility emphasis)

| Venue | Fit | Notes |
|-------|-----|-------|
| **arXiv cs.AI** (or cs.LG + cs.AI cross-list) | Strong | Fast dissemination; attach Zenodo DOI + GitHub commit hash |
| **JAIR** | Medium–strong if expanded | Needs broader evaluation + longer related work; good for protocol permanence |
| **NeurIPS Datasets & Benchmarks** | Medium | If framed as **benchmark + certificate schema** for AI-science metrics |
| **NeurIPS / ICML AI4Science workshop** | Strong | AMAT case study fits; clearly label pilot scale (0.5B CPU) |

### 8.2 Secondary / specialized

| Venue | Fit |
|-------|-----|
| **TMLR** | Reproducibility certification track |
| **AAAI AI for Social Impact / AI4Science** | If proactive-AI governance subsection expanded |
| **Applied Category Theory / ACT workshop** | Only if sheaf section stays metaphor-free + proxy-only |
| **Journal of Open Source Software (JOSS)** | If contribution skews to Sci Flow + `namm` package tooling paper |

### 8.3 Not recommended for first submission

- Top-tier claim without larger models / independent replication of β₁ and cusp results.
- Philosophy-forward venues without operational separation of PI labels.

---

## 9. Figure and table plan

| # | Type | Content |
|---|------|---------|
| **Fig. 1** | Pipeline diagram | Protocol v2 cycle + Sci Flow overlay (mermaid from [`SCI_FLOW.md`](SCI_FLOW.md)) |
| **Fig. 2** | Phase diagram | AMAT order-parameter space: \(d(B_*)\), \(\beta_1\), \(D_{\mathrm{eff}}\) axes; μ vs nd regions ([`ANTI_MEDIAN_AI_TOPOLOGY.md`](ANTI_MEDIAN_AI_TOPOLOGY.md) §3) |
| **Fig. 3** | Heatmap | 037 cusp sweep: dose × T with relative β₁ onset contour vs theoretical cusp set |
| **Fig. 4** | Line plots | 038 per-turn Fisher curvature proxy μ vs lock |
| **Fig. 5** | Layer profile | 039 box-counting \(d_f\) by layer (highlight layers 19, 17, 4, 20, 3) |
| **Fig. 6** | Session trajectories | 040 λ₁ pair + Rosenstein panel (show partial / negative chaos claim) |
| **Fig. 7** | Scatter | 041 H¹ proxy vs β₁ (show **no** correlation — honest null) |
| **Table 1** | Main results | 037–041 summary (§5.3 above) |
| **Table 2** | \(D_{\mathrm{eff}}\) null | 035/036/042/043 comparison |
| **Table 3** | Protocol gates | v2 acceptance criteria vs NAMM-2026-001 failure |
| **Table 4** | Landscape positioning | Condensed from [`OPEN_SOURCE_LANDSCAPE.md`](OPEN_SOURCE_LANDSCAPE.md) |
| **Supp. Table S1** | Domain universe excerpt | Operational domains from [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) |
| **Supp. Fig. S1** | Certificate JSON schema | Annotated excerpt from 037 `artifacts/summary.json` |

---

## 10. Timeline to draft (realistic, single-author + agent-assisted)

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| **W1** | Outline freeze + Zenodo sync | This file finalized; verify record 22646895 metadata; pick title |
| **W2** | Methods draft | Protocol v2 + Sci Flow + AMAT definitions (§0 terminology box) |
| **W3** | Results draft | Tables 1–2 + Figures 3–7 from existing `artifacts/` (no new GPU runs required) |
| **W4** | Related work + positioning | Landscape table; benchmark non-overlap paragraph |
| **W5** | Discussion + limitations | \(D_{\mathrm{eff}}\) null, 0.5B scale, CPU budget, proxy epistemology (H¹, sheaf) |
| **W6** | Internal review | Run `pytest`; pin commit hash; consistency pass on certificate tiers |
| **W7** | arXiv v1 + Zenodo v0.2 | PDF + source tarball; DOI cross-link GitHub tag |
| **W8+** | Workshop / journal fork | Expand replication (≥1.5B, more prompts) **only if** needed for venue |

**Dependencies before submission:**

- [ ] Confirm Zenodo 22646895 title/abstract matches this outline (manual — API unavailable 2026-09-07).
- [ ] Generate publication figures from stored JSON (no LM re-run unless reviewer requests).
- [ ] One-pass legal/brand check: “anti-median” vs “off-typical” in abstract.
- [ ] Optional: independent re-run of 037 relative onset from `full_cusp_sweep.json` (offline reproducibility sentence).

---

## Appendix A. Suggested paper section map

1. Introduction (problem + claim boundary)  
2. Background (π_H / π_A, certificates vs papers)  
3. NAMM Protocol v2  
4. Sci Flow and domain universe  
5. Case study: AMAT hypotheses H-AMAT-006–010  
6. Results 037–041 + \(D_{\mathrm{eff}}\) null  
7. Discussion (AI science, EIA crosswalk, limitations)  
8. Related work  
9. Conclusion (methodology contribution, open gates)  
10. References  
Appendix: artifact schemas, attack checklist excerpt, reproduction commands  

---

## Appendix B. Reproduction commands (for paper §Reproducibility)

```bash
python -m pip install -e ".[dev,science,llm-local,nd]"
python -m pytest tests/ -q
namm sci-flow run NAMM-2026-037
namm sci-flow run NAMM-2026-040
python experiments/NAMM-2026-038/run_experiment.py
python experiments/NAMM-2026-039/run_experiment.py
python experiments/NAMM-2026-041/run_experiment.py
```

---

*Roman Kuznetsov · NAMM research program · CC BY 4.0*
