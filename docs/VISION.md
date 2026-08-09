# NAMM Vision

**Non-Anthropic Mathematics (NAMM)** — a falsifiable research program led by Roman Kuznetsov.

---

## Core hypothesis

Mathematical structures may exist that are **natural for machine cognition before human projection**: easier to generate, verify, and compose as programs or certificates than to express as familiar formulas or diagrams.

We do **not** claim breakthrough theorems here. We claim a **methodology** — search, formalize, attack, verify, compare — with explicit acceptance gates and logged negative results.

---

## Philosophy vs. operations

| Layer | Role |
|-------|------|
| **MUH (Tegmark)** | Heuristic only — expands the search space for admissible structures. Not a proof premise. See [`PHILOSOPHY.md`](PHILOSOPHY.md). |
| **Protocol v2** | Executable cycle, hard gates, novelty ladder. See [`PROTOCOL_V2.md`](PROTOCOL_V2.md). |
| **AI-native Phase 2** | Certificate-first artifacts, program AST domain. See [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md). |

---

## Representation asymmetry (K_A vs K_H)

- **K_A(X)** — complexity in the agent's machine-native language (JSON AST, gzip bytes, eval witness).
- **K_H(X)** — complexity in human-interpretable projection (tokens, prose, formula strings).

**Non-anthropic signal:** \(K_A \ll K_H\) under comparable verification cost — the machine artifact is smaller and more precise than its human explanation.

Operational proxies: [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md).

---

## Projections π_H and π_A (philosophy)

Human and machine cognition apply different **compactifications** of the same formal substrate:

| Projection | Typical form | Role |
|------------|--------------|------|
| **π_H** | Named formulas, diagrams, prose | Human audit and intuition |
| **π_A** | AST JSON, rule tables, eval hashes | Search, verification, composition |

Neither projection is the substrate. Certificates (Lean, z3, eval witnesses in `certificate.json`) are the **shared anchor** between π_H and π_A.

`PHILOSOPHICAL_INFERENCE`: AGI/ASI may correspond to a richer π_A — higher descriptive bandwidth for the same objects, not a separate ontology.

**Beyond homo cognition (program belief, not verification path):** The research program treats mathematical objects as potentially **real independent of human representational access**. Human cognition (π_H) may project only a thin slice; machine-native search (π_A) together with human audit may **jointly** access structure at other descriptive levels. This is labeled `PHILOSOPHICAL_INFERENCE` throughout docs — it motivates widening search and tolerating non-human artifacts, but **does not** replace SNH operational gates (certificates, independence, generative holdout, novelty ladder).

**North star:** structures whose natural compactification is **machine-native first**. See [`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md) for the authoritative priority stack.

---

## AI-native pipeline

```text
  Domain + falsifiable question
           │
           ▼
  Machine-native GENERATE (graph primitives │ program AST)
           │
           ▼
  FORMALIZE + ATTACK checklist
           │
           ▼
  VERIFY ──► certificate.json  (canonical AST hash, eval witness, seeds)
           │
           ├──► independence gate (Pearson r ≤ τ vs baselines)
           ├──► generative gate (held-out graph families)
           └──► novelty ladder (N0–N5)
           │
           ▼
  PROJECT ──► HUMAN_PROJECTION.md  (optional, lossy, trust-only)
```

**North star:** discover structures whose canonical representation is a **verified program**, not a formula; whose human explanation is longer and lossier than the machine artifact; and which predict behavior on families no named invariant spans.

---

## What counts as success

A candidate clears the bar only when **all** hold:

1. **Verified** — computational certificate or proof-assistant check; ground truth is the artifact hash, not the prose.
2. **Compression asymmetry** — \(K_A \ll K_H\); certificate compact, projection lossy.
3. **Independence** — not a disguised baseline (correlation, sympy simplify, non-equivalence gates).
4. **Generative power** — non-trivial on held-out families not used during search.

Failure modes are **first-class**: rejections logged to `rejections.jsonl` with reason codes.

---

## Falsifiability

This program is wrong if, across domains and budgets:

- machine-native search consistently collapses to human-known invariants with \(K_H \approx K_A\);
- independence and generative gates never discriminate beyond noise;
- certificates add no reproducibility over string formulas.

Each experiment config states a falsifiable question. Negative results belong in the repo.

---

## Phases in this repository

| Phase | Domain | Experiment | Priority |
|-------|--------|------------|----------|
| 1 | Finite graph invariants (string formulas) | NAMM-2026-001 | Closed (calibration) |
| 2b | Program AST + evolutionary search | NAMM-2026-003 | **P1** — AI-native core |
| 2a | String rewriting systems (confluence) | NAMM-2026-002 | **P2** |
| 3 | Trans-level meta-evaluators | NAMM-2026-004 | **P3** — scaffold only |

CI (pytest + smoke search) is the merge gate. No production deployment — quality is in the artifacts.

---

## Related docs

- [`NON_HOMO_SYNTAX.md`](NON_HOMO_SYNTAX.md) — non-homo syntax, compactification vs projection
- [`FRAME_LADDER.md`](FRAME_LADDER.md) — F1–F∞ representational ladder
- [`NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](NON_HOMO_SYNTAX_AND_ND_FRAMES.md) — extended ND mapping
- [`RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md) — AI-led roadmap, \(\pi_H\)/\(\pi_A\) notes
- [`MANIFESTO.md`](MANIFESTO.md) — brief scientific manifesto
- [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md) — certificate-first Phase 2
- [`OPEN_PROBLEMS_TIERLIST.md`](OPEN_PROBLEMS_TIERLIST.md) — open problems mapped to finite shadows

---

## Author

Roman Kuznetsov · NAMM research program · [namm-experiments](https://github.com/errorlogy/namm-experiments)
