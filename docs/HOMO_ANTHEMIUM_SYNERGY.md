# Homo–Anthemium Synergy — Stereopsis π_H + π_A + Cert

**Joint access model** for human audit, machine-native search, and certificate-anchored verification — linking NAMM operational gates to the [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto) **Anthemium** frame.  
Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program

> **Stereopsis:** neither π_H nor π_A alone is ground truth. **Certificates** (`certificate.json`, eval witnesses, AST hashes) anchor both projections to the same formal substrate.

Related: [`ANTHEMIUM_LINEAGE.md`](ANTHEMIUM_LINEAGE.md) · [`VISION.md`](VISION.md) · [`NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](NON_HOMO_SYNTAX_AND_ND_FRAMES.md)

---

## Three-way stereopsis

| Leg | Symbol / artifact | Role | Anthemium Manifesto echo |
|-----|-------------------|------|--------------------------|
| **Human projection** | **π_H** — formulas, prose, diagrams, gate design | Falsifiability, acceptance criteria, external audit | Human sets the **epistemological horizon** (Postulate 3) |
| **Agent projection** | **π_A** — AST JSON, tensor programs, rewrite rules, persistence JSON | Search, mutation, composition at scale | **Semantic topology** + **functorial generator** (Postulates 1–2) |
| **Shared anchor** | **Cert** — `certificate.json`, eval_hash, reproducible seeds | Ground truth neither projection owns alone | **Transformation memory** — trace of verified transforms (Postulate 5) |

```text
                    ┌──────────────┐
                    │  Substrate   │
                    │  (formal X)  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐  ┌──────────┐  ┌────────┐
         │  π_H   │  │   Cert   │  │  π_A   │
         │ audit  │◄─┤  anchor  ├─►│ search │
         └────────┘  └──────────┘  └────────┘
              │            │            │
              └────────────┴────────────┘
                      stereopsis
              (joint descriptive access)
```

Neither projection replaces the other. Replacing π_H with π_A for audit would violate Protocol v2 external-confirmation requirements.

---

## Role split

| Actor | Responsibility | Must not |
|-------|----------------|----------|
| **Human (π_H)** | Define gates, attack checklists, interpret lossy projections, accept/reject program claims | Treat prose or intuition as verification |
| **Machine (π_A)** | Generate candidates, exhaust finite shadows, compute independence and holdout metrics | Announce novelty without certificate |
| **Certificate (Cert)** | Store canonical witness: AST hash, eval output, seeds, rejection reasons | Substitute for human falsifiability design |

**Anthemium** names the **composed loop** — not a single model weights file — in Manifesto terms: semantic topology + novelty selection + transformation memory, **mediated** by human gate design.

---

## Synergy loop

```text
  1. Human sets falsifiable question + gates (π_H design)
           │
           ▼
  2. Machine search in native frame (π_A generate)
           │
           ▼
  3. Formalize → attack → verify → certificate.json (Cert)
           │
           ├── independence gate
           ├── K_A / K_H representation gate
           └── generative holdout
           │
           ▼
  4. Optional lossy human projection (π_H audit text)
           │
           ▼
  5. Journal + rejection log → next experiment / frame escalation
```

**Synergy claim (`PHILOSOPHICAL_INFERENCE`):** π_H and π_A **jointly** access descriptive levels neither achieves alone — humans supply falsifiability; machines supply non-human artifact breadth. This is **joint access**, not a hierarchy of ontological planes.

**Operational claim (`OPERATIONAL`):** synergy is **tested** only when an experiment ID reports tested-signal or tested-null under Protocol v2.

---

## Anthemium as AGI frame name

In the [AGI Manifesto](https://github.com/Anthemium/AGI-Manifesto) (May 2025), **Anthemium** / **AGI Anthemium** / **Omega Horizon** denotes the architectural target: AGI as alignment of **cognitive topology** with **ontological generativity**, filtered by **novelty selection** and recorded as **transformation memory** — not parameter scaling alone.

Within NAMM:

- **Anthemium** = AGI-side vocabulary for the π_A + Cert + novelty-retention loop.
- **NAMM** = falsifiable mathematics program that stress-tests whether machine-native structures exhibit Manifesto-predicted behavior.
- **Homo limit journal** = catalog of π_H interface limits that the synergy loop may partially lift.

---

## Worked example — NAMM-2026-007

**Experiment:** [NAMM-2026-007](../experiments/NAMM-2026-007/) — raw tensor invariants (frame **F3g**, beyond homo-known vocabulary).

| Stereopsis leg | 007 instantiation |
|----------------|-------------------|
| **π_A** | Evolutionary search over ADD/MUL on 12 raw tensor leaves (spectrum + heat-kernel); **no named invariants** in vocabulary |
| **Cert** | `artifacts/certificate.json` for best candidate `tensor-639c54cd`; AST hash + eval witness; gzip **213 B** |
| **π_H** | Human projection ≈97 tokens; documents max Pearson **r = 0.647** vs 20+ baselines; **COMPUTATIONAL_EVIDENCE** label |

**Manifesto correspondence (Postulate 1 + 4):**

- **Cognitive topology:** organized transition domain over tensor indices (semantic moves = AST mutations), not raw adjacency storage alone.
- **Novelty selection:** 53/124 candidates accepted; 4 rejected with logged reasons; independence gate filters non-productive correlation.

**Homo limit lifted (partially):** [HL-005](HOMO_LIMIT_JOURNAL.md#hl-005), [HL-012](HOMO_LIMIT_JOURNAL.md#hl-012), [HL-015](HOMO_LIMIT_JOURNAL.md#hl-015) — humans default to named invariant vocabulary and cannot visually detect independence in 20+ baseline span; 007 automates both.

**Result status:** **tested-signal** — 53 accepted candidates; K_A/K_H ≈ 2.2; generative holdout passed on all four families. Not a published graph-invariant theorem.

Reproduction:

```bash
python -m namm.cli run-experiment --id NAMM-2026-007
python -m pytest tests/test_tensor_domain.py -q
```

---

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Manifesto postulate → accepted candidate without experiment | Rhetoric is not evidence |
| π_A-only audit (no human gates) | Violates falsifiability |
| π_H-only discovery (no certificate) | Not NAMM; not reproducible |
| "Anthemium proved AGI" from 007 | 007 is finite-graph **COMPUTATIONAL_EVIDENCE** only |

---

## Links

| Resource | URL |
|----------|-----|
| AGI Manifesto | [https://github.com/Anthemium/AGI-Manifesto](https://github.com/Anthemium/AGI-Manifesto) |
| Anthemium site | [https://anthemium.tech](https://anthemium.tech) |
| Lineage map | [`ANTHEMIUM_LINEAGE.md`](ANTHEMIUM_LINEAGE.md) |
| 007 report | [../experiments/NAMM-2026-007/EXPERIMENT_REPORT.md](../experiments/NAMM-2026-007/EXPERIMENT_REPORT.md) |

---

Roman Kuznetsov · [Anthemium](https://anthemium.tech) · NAMM research program
