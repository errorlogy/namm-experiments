# Open-Source Landscape — Automated Scientific Discovery vs NAMM

**Date:** 2026-08-11  
**Scope:** GitHub and adjacent open-source projects in automated discovery, hypothesis pipelines, program synthesis, symbolic regression, and formal math — compared to **NAMM** (Non-Anthropic Mathematics Mode).  
Roman Kuznetsov · NAMM research program

Related: [`README.md`](../README.md) · [`FRAME_LADDER.md`](FRAME_LADDER.md) · [`PROTOCOL_V2.md`](PROTOCOL_V2.md) · [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) · [`MATH_OBJECT_CANDIDATES.md`](MATH_OBJECT_CANDIDATES.md)

> **Star counts** are approximate snapshots from public GitHub metadata (Aug 2026). Treat as order-of-magnitude activity signals, not quality rankings.

---

## Executive summary

The open-source ecosystem clusters into **six families**:

| Family | Typical output | Verification style | Closest to NAMM? |
|--------|----------------|-------------------|------------------|
| **AI Scientist agents** | ML papers, LaTeX, plots | LLM review + experiment logs | Partial (003 program AST) |
| **Hypothesis + falsification** | Ranked hypotheses, stats tests | Sequential testing, Popper-style | Partial (005/008 shadows) |
| **Evolutionary program search** | Code heuristics, equations | Automated evaluator | **Strong** (003, 007) |
| **Symbolic regression** | Closed-form formulas | Fit error, parsimony | Weak (anthropic target) |
| **Formal proving / conjecture** | Lean proofs, Mathlib | Kernel check | Partial (002 rewriting) |
| **Closed industrial systems** | Hypothesis reports | Trusted tester only | Gap (no certificates) |

**NAMM's niche:** verification-first discovery of **machine-native mathematical artifacts** (AST programs, certificates, config shadows) under explicit **SNH gates**, **frame ladder** escalation (F3a–F3h), **K_A/K_H compression asymmetry**, and **open-problem finite shadows** — not end-to-end paper generation.

---

## Categories overview

| Category | Representative projects | Primary artifact | License mix |
|----------|-------------------------|------------------|-------------|
| End-to-end AI Scientist | Sakana AI Scientist, AutoResearchClaw, DeepScientist, InternAgent, Arbor | PDF/LaTeX paper + code | Other, MIT, Apache-2.0 |
| Hypothesis generation + verification | Google AI Co-Scientist (closed), Kaimen Co-Scientist, POPPER, PiEvo, OpenScientist | Hypothesis list + report | Apache-2.0, MIT, closed |
| Program synthesis for science | FunSearch, OpenEvolve, NAMM F3c/F3g | Evolved program / AST | Apache-2.0 |
| Symbolic regression | PySR, SymbolicRegression.jl, Eureqa (proprietary) | Human-readable formula | Apache-2.0 / commercial |
| Theorem proving / conjecture | LeanDojo, DeepSeek-Prover, Goedel-Prover, formal-conjectures, Germinal, LeanConjecturer | Lean proof / `sorry` conjecture | Apache-2.0, MIT, model licenses |
| Domain-specific discovery | Sparks (materials), AllenAI CodeScientist/AutoDiscovery | Domain report / benchmark result | Apache-2.0 |

---

## 1. End-to-end “AI Scientist” pipelines

These systems automate **literature → hypothesis → experiment → manuscript**. Success is measured by paper quality, benchmark gains, or peer review — not by compact machine certificates.

### Sakana AI Scientist (v1)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/SakanaAI/AI-Scientist |
| **Stars** | ~14.3k |
| **License** | Other (custom; check repo) |
| **Activity** | High; Nature paper (2025); community templates |

**What it does:** Fully autonomous ML research loop — idea generation, code execution, plotting, LaTeX paper draft, automated peer review. Ships templates for NanoGPT, 2D diffusion, grokking.

**vs NAMM**

| Overlap | Gap |
|---------|-----|
| Hypothesis → experiment → artifact loop | Output is **human paper**, not `certificate.json` |
| Open rejection of bad ideas via experiment failure | No **frame ladder**, no **K_A/K_H** gate |
| Program/code mutation in templates | No **non-anthropic** vocabulary (F3g raw tensor) |
| | No **open-problem shadows** (Kotzig, Graceful Tree) |
| | Independence vs named baselines not SNH-hardened |

---

### Sakana AI Scientist v2

| Field | Value |
|-------|-------|
| **URL** | https://github.com/SakanaAI/AI-Scientist-v2 |
| **Stars** | ~7.0k |
| **License** | Other |
| **Activity** | High; ICLR 2025 workshop acceptance milestone |

**What it does:** Template-free agentic **tree search** over experiments; ideation via Semantic Scholar; experiment manager agent; VLM figure feedback; generalized ML domains.

**vs NAMM:** Same family as v1. Adds structured search (tree) closer to NAMM's evolutionary frames, but still optimizes **publishable ML narrative**, not machine-native graph/tensor programs with holdout families and sympy baseline gates.

---

### AutoResearchClaw (ResearchClaw)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/aiming-lab/AutoResearchClaw |
| **Stars** | ~14.0k |
| **License** | MIT |
| **Activity** | Very high (2026); 23-stage pipeline |

**What it does:** OpenClaw-integrated **full paper factory** — literature (OpenAlex, S2, arXiv), multi-agent debate, hardware-aware sandbox experiments, citation verification, peer review, LaTeX, HITL co-pilot modes.

**vs NAMM:** Strong on **auditability** (verification reports, claim checking) — nearest AI Scientist cousin to NAMM's falsifiability ethos. Still targets **conference papers**, not mathematical objects whose canonical form is an AST. No moduli/config shadows or representation bottleneck metrics.

---

### DeepScientist

| Field | Value |
|-------|-------|
| **URL** | https://github.com/ResearAI/DeepScientist |
| **Stars** | ~3.2k |
| **License** | Apache-2.0 |
| **Activity** | Active; local-first research studio |

**What it does:** Long-horizon autonomous research workspace — baselines, Bayesian optimization, findings memory, experiment rounds, paper outputs; compares itself explicitly to AI Scientist.

**vs NAMM:** Persistent research state and failure retention align with NAMM's `rejections.jsonl` philosophy. Missing: explicit **Protocol v2 gates**, **frame escalation**, certificate-first ground truth.

---

### InternAgent

| Field | Value |
|-------|-------|
| **URL** | https://github.com/InternScience/InternAgent |
| **Stars** | ~1.4k |
| **License** | Other |
| **Activity** | Active; multi-domain (physical, bio, earth, life) |

**What it does:** Unified agentic framework — hypothesis to verification across 12+ task types; paper reproduction; MLEvolve submodule for algorithm design (#1 MLEBench open-source claim).

**vs NAMM:** Breadth over depth in **pure math structure**. No certificate schema, no anthropic/compression asymmetry measurement.

---

### Arbor

| Field | Value |
|-------|-------|
| **URL** | https://github.com/RUC-NLPIR/Arbor |
| **Stars** | ~1.0k |
| **License** | Apache-2.0 |
| **Activity** | Active; strong MLE-Bench results |

**What it does:** **Hypothesis tree** with held-out dev/test discipline, git worktrees per experiment, literature novelty checks (alphaXiv), coordinator/executor agents.

**vs NAMM:** Closest **search discipline** among AI Scientist forks — explicit held-out validation mirrors NAMM generative holdout. Still ML-benchmark-centric; no machine-native math frames or Lean/certificate pipeline.

---

### AllenAI CodeScientist

| Field | Value |
|-------|-------|
| **URL** | https://github.com/allenai/codescientist |
| **Stars** | ~346 |
| **License** | Apache-2.0 |
| **Activity** | Stable; ACL Findings 2025 |

**What it does:** Genetic **LLM-as-mutator** over (paper, codeblock) pairs; containerized experiment builder; meta-analysis across replication attempts; agent/virtual-environment discoveries.

**vs NAMM:** Shared **evolutionary program** DNA with NAMM-2026-003. Differs: mutates research **code artifacts for NLP agents**, not graph invariants; evaluation is external review + replication, not SNH + `certificate.json`.

---

### AllenAI AutoDiscovery

| Field | Value |
|-------|-------|
| **URL** | https://github.com/allenai/autodiscovery |
| **Stars** | ~196 |
| **License** | Check repo (NeurIPS 2025 release) |
| **Activity** | Moderate; MCTS + Bayesian surprise |

**What it does:** Open-ended discovery on DiscoveryBench via **MCTS hypothesis search** and belief updates (Bayesian surprise).

**vs NAMM:** Hypothesis tree + surprise ≈ exploration policy. Tabular/social-science datasets, not graph AST certificates or config shadows.

---

### Sparks (MIT LAMM)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/lamm-mit/Sparks |
| **Stars** | ~23 |
| **License** | Apache-2.0 |
| **Activity** | Niche; peptide mechanics demo |

**What it does:** Multi-modal multi-agent loop (hypothesis → test → refine → report) with user-defined Python tools; demonstrated scaling laws in materials.

**vs NAMM:** Domain-specific **scientific principle** discovery; user supplies eval tools. No general math frame ladder or compression metrics.

---

## 2. Hypothesis generation + verification (without full paper factories)

### Google AI Co-Scientist (closed)

| Field | Value |
|-------|-------|
| **URL** | https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ |
| **Open source** | **No** — Trusted Tester Program only |
| **Paper** | arXiv:2502.18864; Nature 2026 |

**What it does:** Multi-agent Gemini system — generation, reflection, ranking, tournament evolution of **biomedical/scientific hypotheses**; test-time compute scaling.

**vs NAMM:** High-level hypothesis ranking without executable math certificates. Community reimplementations below.

---

### Kaimen-Inc / Co-Scientist

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Kaimen-Inc/Co-Scientist |
| **Stars** | ~191 |
| **License** | Apache-2.0 |

**What it does:** Independent open reimplementation — tournament-ranked research overview from natural-language goals; pluggable LLM providers.

**vs NAMM:** Hypothesis **text** output; no evolved graph programs or moduli enumeration certificates.

---

### POPPER (Stanford)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/snap-stanford/popper |
| **Stars** | ~281 |
| **License** | Check repo |

**What it does:** **Agentic sequential falsification** of free-form hypotheses with Type-I error control; designs experiments targeting measurable implications (biology, economics, sociology).

**vs NAMM:** Philosophically aligned with **falsifiability** (Popper). Statistical hypothesis testing, not machine-native AST discovery or open-problem finite shadows.

---

### PiEvo

| Field | Value |
|-------|-------|
| **URL** | https://github.com/amair-lab/PiEvo |
| **Stars** | ~31 |
| **License** | MIT |

**What it does:** Evolves **scientific principles** (not just hypotheses) via Bayesian optimization; principle / hypothesis / experiment agents.

**vs NAMM:** Meta-level belief update resembles NAMM **meta-evaluator** (004) thematically; no executable certificate artifacts.

---

### OpenScientist

| Field | Value |
|-------|-------|
| **URL** | https://github.com/openscientist-io/openscientist |
| **Stars** | ~44 |
| **License** | Apache-2.0 |

**What it does:** Domain-agnostic iterative hypothesis loop over uploaded scientific data; PubMed grounding; MCP tools.

**vs NAMM:** Omics/statistics focus; sandbox Python analysis — not combinatorial math search frames.

---

## 3. Program synthesis & evolutionary code search (science-adjacent)

### Google DeepMind FunSearch

| Field | Value |
|-------|-------|
| **URL** | https://github.com/google-deepmind/funsearch |
| **Stars** | ~1.1k |
| **License** | Apache-2.0 (code); CC BY 4.0 (materials) |

**What it does:** LLM + evolutionary database discovers **single Python functions** for cap sets, admissible sets, bin packing, etc. Reference implementation without bundled LLM/sandbox.

**vs NAMM**

| Overlap | Gap |
|---------|-----|
| **Program search** over compositional code | Single-function heuristics vs **AST programs** (F3c) |
| Automated evaluator as ground truth | No **independence** vs named graph baselines |
| Mathematical discoveries (Nature 2023) | No **K_A/K_H**, no **human_projection.md** split |
| | No **open-problem shadows** or **11D config** frame |

**NAMM-2026-003/007** are the closest in-repo analogues with stricter acceptance gates.

---

### OpenEvolve (AlphaEvolve open implementation)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/algorithmicsuperintelligence/openevolve |
| **Stars** | ~6.9k |
| **License** | Apache-2.0 |

**What it does:** Evolutionary LLM coding agent — multi-language, self-modifying prompts, **symbolic regression** examples (LLM-SRBench), GPU kernel optimization, circle packing.

**vs NAMM:** Strongest open **AlphaEvolve** lineage. Optimizes arbitrary code against user metrics; lacks NAMM's **frame ladder**, **novelty ladder N0–N5**, and **certificate.json** schema. Symbolic regression path targets **human-readable formulas** (anthropic projection), opposite of F3g raw tensor.

---

### AlphaEvolve (DeepMind — results only)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/google-deepmind/alphaevolve_results |
| **Stars** | ~282 |
| **License** | Apache-2.0 |
| **Code** | **Not released** — Colab verification notebooks only |

**What it does:** Evolves **entire code files** (hundreds of lines) for matrix multiplication, datacenter scheduling, etc.

**vs NAMM:** Superset of FunSearch expressiveness. Closed runner means community cannot replicate gate protocols; NAMM remains auditable end-to-end.

---

## 4. Symbolic regression & equation discovery

### PySR / SymbolicRegression.jl

| Field | Value |
|-------|-------|
| **URL** | https://github.com/MilesCranmer/PySR (also `astroautomata/PySR` fork) |
| **Backend** | https://github.com/MilesCranmer/SymbolicRegression.jl |
| **Stars** | ~3.6k (PySR) |
| **License** | Apache-2.0 |

**What it does:** High-performance **symbolic regression** — evolutionary + simplify-optimize loop; sklearn API; distributed Julia backend.

**vs NAMM:** Discovers **compact human formulas** from numeric data — explicitly the **π_H (anthropic) target** NAMM tests whether one can bypass. PySR lacks AST holdout on graph families, config shadows, or certificate hashes. Useful **baseline** for "already compressible to named math."

---

### Eureqa / Nutonian (commercial)

| Field | Value |
|-------|-------|
| **URL** | https://www.creativemachineslab.com/eureqa.html (historical) |
| **Open source** | **No** — merged into proprietary online service |

**What it does:** Pioneering GUI symbolic regression (circa 2009). PySR documentation cites Eureqa as motivation for an open replacement.

**vs NAMM:** Same category as PySR — anthropic equation discovery. Listed for historical lineage only.

---

## 5. Formal verification, conjecture generation, theorem proving

### google-deepmind / formal-conjectures

| Field | Value |
|-------|-------|
| **URL** | https://github.com/google-deepmind/formal-conjectures |
| **Stars** | ~1.0k |
| **License** | Apache-2.0 |

**What it does:** Large Lean 4 library of **formalized conjectures** (Erdős, OEIS, etc.) for Mathlib — corpus for AlphaProof / Nexus, not a search loop.

**vs NAMM:** **Static conjecture database** vs NAMM's **dynamic search + computational evidence**. Complementary: NAMM open-problem shadows could seed formal-conjecture-style statements after finite witness search.

---

### DeepSeek-Prover-V2

| Field | Value |
|-------|-------|
| **URL** | https://github.com/deepseek-ai/DeepSeek-Prover-V2 |
| **Stars** | ~1.3k |
| **License** | Model license (check `LICENSE-MODEL`) |

**What it does:** RL-trained LLM for **Lean 4 proof generation**; recursive subgoal decomposition; 7B and 671B models; ProverBench dataset.

**vs NAMM:** Proves stated theorems; does not **discover** graph/tensor programs or moduli fibers. Lean certificates are proof scripts — different schema from NAMM `certificate.json` (AST hash + eval witness on finite graphs).

---

### Goedel-Prover-V2 (Princeton et al.)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Goedel-LM/Goedel-Prover-V2 |
| **Stars** | ~181 |
| **License** | Check repo |

**What it does:** Open ATP with scaffolded data synthesis + verifier-guided self-correction; SOTA MiniF2F / PutnamBench claims at small model sizes.

**vs NAMM:** Proof search, not structure discovery in non-Lean frames (F3g raw tensor, F3h config shadow).

---

### LeanDojo / LeanDojo-v2

| Field | Value |
|-------|-------|
| **URL** | https://github.com/lean-dojo/LeanDojo-v2 (v1: `LeanDojo` ~789★) |
| **Stars** | ~68–111 (v2) |
| **License** | Apache-2.0 |

**What it does:** Trace Mathlib repos, build RL/gym environments, train retrieval-augmented provers (ReProver, LeanCopilot ecosystem).

**vs NAMM:** **Infrastructure** for ML on proofs — not a discovery protocol. NAMM F3b (rewriting) and future proof-assistant certificates (`FRAME_LADDER.md` CONJECTURE) could integrate LeanDojo-style tooling.

---

### LeanConjecturer

| Field | Value |
|-------|-------|
| **URL** | https://github.com/auto-res/LeanConjecturer |
| **Stars** | ~9 |
| **License** | MIT |

**What it does:** LLM + Mathlib context → Lean 4 conjectures; filters trivial/`aesop`-provable; GRPO training data generation (12k+ conjectures paper).

**vs NAMM:** Conjecture **statements** in Lean; NAMM seeks **computational witnesses** (e.g., AMFW fiber 729) with JSON certificates before formal promotion.

---

### ProofX + Germinal

| Field | Value |
|-------|-------|
| **URL** | https://github.com/MohammedAlkindi/ProofX (Germinal: `packages/germinal`) |
| **Stars** | ~0 (root repo) |
| **License** | MIT |

**What it does:** ProofX — directed search ledgers for Collatz/Goldbach; bounded Lean certificates. **Germinal** — Claude conjecture gen → Lean formalization → tactic race → counterexample ensemble; Git snapshot reproducibility.

**vs NAMM:** Nearest neighbor on **certificate + falsification** in number theory. ProofX certificates are **bounded finite checks**; NAMM adds **frame ladder**, **K_A/K_H**, and **machine-native AST** targets beyond human conjecture text. Germinal is LLM+Lean pipeline; NAMM minimizes anthropic vocabulary in search (F3g).

---

### Perqed

| Field | Value |
|-------|-------|
| **URL** | https://github.com/bneb/perqed |
| **Stars** | ~1 (early) |
| **License** | Check repo |

**What it does:** Neuro-symbolic Lean 4 lab — literature ingest, conjecture gen, MCTS tactics, Z3 witnesses, XState orchestration.

**vs NAMM:** Full autonomous proof **orchestration**; Ramsey/Torus targets. Less explicit about non-anthropic representation metrics or open-problem shadow calibration.

---

### conjectureextraction (sorgfresser)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/sorgfresser/conjectureextraction |
| **Stars** | Small / early |
| **License** | Check repo |

**What it does:** Distributed pipeline — informal conjecture gen, online autoformalization, ATP in Lean 4 via RabbitMQ workers.

**vs NAMM:** Engineering-heavy formal loop; no graph-domain evolutionary frames.

---

### AlphaProof / Nexus (DeepMind — partial open)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/google-deepmind/alphaproof-nexus-results |
| **Stars** | ~282 |
| **License** | Apache-2.0 |

**What it does:** Published Lean proofs + prose for solved Erdős/OEIS subsets; training code **not** fully open.

**vs NAMM:** Olympiad-grade **proof artifacts**; closed training loop. NAMM publishes **full experiment reproduction** (`python -m namm.cli run-experiment`).

---

## 6. Cross-project comparison matrix

| Project | Stars≈ | Synthesis / search | Hard verification | Certificate artifact | Non-anthropic frame | Open-problem shadow |
|---------|--------|-------------------|---------------------|----------------------|---------------------|---------------------|
| **NAMM** | — | AST / tensor / config evolution | SNH + sympy + holdout | `certificate.json` | **Core (F3g, F4)** | **Kotzig, Graceful Tree** |
| AI Scientist v1/v2 | 7–14k | LLM + tree search | Experiment logs | Paper + code | No | No |
| AutoResearchClaw | 14k | 23-stage agent pipeline | Citation + claim verify | LaTeX bundle | No | No |
| FunSearch | 1.1k | Evolution + LLM functions | Python evaluator | Discovered `.py` | Partial | Cap sets only |
| OpenEvolve | 6.9k | Evolution + LLM code | User metric | Best program snapshot | Optional SR path | User-defined |
| PySR | 3.6k | Genetic regression | Fit error | Formula string | No (targets formulas) | No |
| POPPER | 281 | Falsification experiments | Sequential testing | Stats report | No | No |
| formal-conjectures | 1k | Static corpus | Lean typecheck | `.lean` statements | No | Erdős list |
| DeepSeek-Prover-V2 | 1.3k | RL tactic search | Lean kernel | Proof script | No | Benchmarks |
| ProofX/Germinal | ~0 | Directed + LLM conjecture | Lean + ledgers | Bounded cert / Git exp | Partial | Collatz/Goldbach |
| Google Co-Scientist | — | Multi-agent tournament | Closed | None public | No | No |

---

## NAMM differentiation

### What NAMM is *not*

- Not an **AI paper writer** (contrast Sakana, AutoResearchClaw, DeepScientist).
- Not **symbolic regression** optimizing for human-readable formulas (contrast PySR, OpenEvolve SR examples).
- Not a **Lean prover** or static conjecture library (contrast DeepSeek-Prover, formal-conjectures).
- Not a **closed** trusted-tester demo (contrast Google AI Co-Scientist).

### What NAMM uniquely combines (open source)

1. **Non-anthropic mathematics mode** — searches frames where the canonical object is a **verified program or certificate** before compact human notation exists (`README.md`, `AI_NATIVE_NAMM.md`).

2. **Certificate-first ground truth** — `certificate.json` (AST hash, eval hash, holdout witness) beats prose claims; human explanation is **separate** and often lossier (`HUMAN_PROJECTION.md`).

3. **Frame ladder (F1→F∞)** — explicit representational rungs (`FRAME_LADDER.md`): string formulas (F3a) → rewriting (F3b) → program AST (F3c) → meta-evaluator (F3d) → open-problem shadows (F3e) → TDA (F3f) → raw tensor (F3g) → 11D config shadow (F3h). Most AI Scientist repos have **flat** agent loops.

4. **SNH gates (Protocol v2)** — correlation ceiling, sympy simplify, novelty floor N2+, generative holdout, equal compute vs baselines, mandatory `rejections.jsonl`.

5. **K_A / K_H compression asymmetry** — operational proxy for anthropic projection bottleneck (F4); success requires machine artifact **smaller/preciser** than human projection.

6. **Open-problem shadows** — finite calibration against named conjectures (Kotzig \(P_k\), Graceful Tree) without claiming full proofs (`OPEN_PROBLEMS_TIERLIST.md`).

7. **Negative results as first-class** — NAMM-2026-001 closed as valid null; contrasts with paper-pipeline positivity bias.

8. **Fully reproducible CLI** — `python -m namm.cli run-experiment --id NAMM-2026-00X`; CI pytest + smoke on every push.

### Strategic positioning

| If you need… | Use… | NAMM adds… |
|--------------|------|------------|
| Publish ML paper autonomously | AI Scientist v2, AutoResearchClaw | — |
| Evolve heuristics / algorithms | FunSearch, OpenEvolve | Graph/tensor **independence gates** + certificates |
| Discover \(y = f(x)\) formula | PySR | **Anti-goal** unless testing compressibility |
| Prove Lean theorems | DeepSeek-Prover, Goedel-Prover | **Discovery** in pre-formal frames |
| Falsify verbal hypothesis | POPPER | **Executable** finite shadows |
| Test "structure before human name" | — | **NAMM** |

### Integration opportunities (not implemented)

- **FunSearch/OpenEvolve** as F3c/F3g search backends under SNH gates.
- **LeanDojo + Germinal** for promoting `COMPUTATIONAL_EVIDENCE` to Lean `CONJECTURE`.
- **formal-conjectures** as target list for shadow experiments.
- **POPPER-style** sequential tests on implications of NAMM conjectures (H-001–H-007).

---

## References & further reading

| Resource | Link |
|----------|------|
| NAMM protocol | [`NAMM_PROTOCOL.md`](../NAMM_PROTOCOL.md) |
| Vision & falsifiability | [`VISION.md`](VISION.md) |
| Sakana AI Scientist Nature | https://sakana.ai/ai-scientist-nature/ |
| FunSearch Nature 2023 | https://www.nature.com/articles/s41586-023-06924-6 |
| AlphaEvolve report | https://arxiv.org/abs/2506.13131 |
| Google AI Co-Scientist | https://arxiv.org/abs/2502.18864 |
| PySR paper | https://arxiv.org/abs/2305.01582 |
| LeanConjecturer | https://arxiv.org/abs/2506.22005 |
| POPPER | https://github.com/snap-stanford/popper |

---

## Краткое резюме (RU)

**Ландшафт:** экосистема делится на «AI Scientist» (статьи и ML-эксперименты), эволюционный синтез программ (FunSearch, OpenEvolve), символическую регрессию (PySR), формальные доказательства/конjectуры (Lean-стек) и закрытые industrial-системы (Google Co-Scientist).

**NAMM** занимает отдельную нишу: **verification-first** поиск **машинно-нативных** математических артефактов (AST, тензорные программы, config shadows) с **`certificate.json`**, лестницей фреймов **F3a–F3h**, метрикой **K_A/K_H**, калибровкой на **тенях открытых проблем** и явным журналом отказов — без автогенерации статей.

**Топ проектов для сравнения:** Sakana AI Scientist (~14k★), AutoResearchClaw (~14k★), OpenEvolve (~7k★), AI Scientist v2 (~7k★), PySR (~3.6k★), DeepScientist (~3.2k★), FunSearch (~1.1k★), formal-conjectures (~1k★), InternAgent (~1.4k★), Arbor (~1k★), DeepSeek-Prover-V2 (~1.3k★), POPPER (~281★), Kaimen Co-Scientist (~191★).

Roman Kuznetsov · NAMM research program
