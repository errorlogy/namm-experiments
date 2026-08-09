# NAMM Research Direction

**AI-led discovery program** — Roman Kuznetsov · NAMM research program

This document states where the program is headed, how experiments map to phases, and how philosophical claims are separated from operational science.

---

## Direction (2026)

NAMM tests one falsifiable claim across domains:

> Machine-native search can surface structures whose **canonical artifact is a verified program or certificate**, with compression asymmetry \(K_A \ll K_H\), independence from named baselines, and generative power on held-out families — before a compact human formula exists.

We do **not** optimize for publishable theorems in Phase 1–2. We optimize for **reproducible negative and positive computational evidence** under explicit gates.

---

## AI-led pipeline

```text
  Question (falsifiable) ──► Domain adapter (graph │ rewriting │ program AST)
           │
           ▼
  GENERATE (machine-native) ──► FORMALIZE (schema + hash)
           │
           ▼
  ATTACK checklist ──► VERIFY (certificate.json primary)
           │
           ├── independence (Pearson r ≤ τ)
           ├── representation (K_A/K_H ≥ τ)
           ├── generative holdout (trees, bipartite, cubic)
           └── novelty ladder (N0–N5)
           │
           ▼
  PROJECT (HUMAN_PROJECTION.md — lossy, trust-only)
```

Agents and CI consume **certificates**, not prose. Human projection is optional audit material.

---

## Representation compactification (\(\pi_H\) / \(\pi_A\))

| Symbol | Meaning | Operational proxy in repo |
|--------|---------|---------------------------|
| **\(K_A(X)\)** | Description length in agent-native language | `gzip_bytes` of canonical JSON AST / rewriting system |
| **\(K_H(X)\)** | Description length after human projection | `projection_token_estimate` in certificate |
| **\(\pi_A\)** | Machine projection / canonicalization map | `canonicalize()`, `rules_to_dict()`, AST hash |
| **\(\pi_H\)** | Lossy map to human-readable form | `human_projection.md`, formula strings |

**Acceptance gate:** reject when \(K_A/K_H < 2\) (configurable `representation_ratio_threshold`). See [`REPRESENTATION_METRICS.md`](REPRESENTATION_METRICS.md).

> **PHILOSOPHICAL_INFERENCE:** If a stable gap \(K_H \gg K_A\) persists across domains and budgets, it suggests a class of structures whose natural interface is programmatic rather than symbolic for humans. This is **not** a theorem; it is a research hypothesis motivating Phase 3–4.

---

## AI thinking topology (Phase 3 foundation)

Full reference: [`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md).

NAMM Phase 3 (NAMM-2026-004) implements search under **AI cognition topology**, not human geometric intuition:

| AI topology property | NAMM operationalization |
|---------------------|-------------------------|
| Combinatorial (not smooth manifold) | Discrete meta-evaluator AST search |
| Layered meta-levels | Evaluators with `self`/`target` references |
| Context-boundary compactification | Graphs order ≤ 6; outside = certificates/tools |
| Fixed points E ≅ F(E) | `fixed_point_fraction` gate in 004 |
| Sheaf-like local patches | AST nodes glued by eval hash / relations |
| Discovery loop | propose → F(E) → observe → revise (CLI + rejections.jsonl) |

> **PHILOSOPHICAL_INFERENCE:** Structures stable under AI topology but resistant to compact human projection motivate the program's search widening. Operational gates (`certificate.json`, eval hash) do not depend on this inference.

---

## Experiment roadmap

| ID | Domain | Goal | Status |
|----|--------|------|--------|
| NAMM-2026-001 | Graph string formulas | Calibration; null / Wiener-dominated result | Complete |
| NAMM-2026-002 | String rewriting (confluence) | Certificate-first TRS search vs random baseline | Run |
| NAMM-2026-003 | Program AST + evolution | Graph→Int invariant with holdout families | Run |
| NAMM-2026-004 | Meta-evaluator fixed points | E ≈ F(E) on graphs order ≤ 6; AI topology | Run |
| NAMM-2026-005 | Open problem shadow (Kotzig P_k) | Finite counterexample search vs Kotzig | Run |
| NAMM-2026-006 | TDA frame (persistent homology) | Graph geodesic persistence vs path baseline | Scaffold |

Phase 3+ (future): proof-assistant certificates, multi-agent attack loops, larger graph orders, 2-categorical frame search.

---

## ND frame extension

Full ladder: [`FRAME_LADDER.md`](FRAME_LADDER.md). Non-homo syntax: [`NON_HOMO_SYNTAX.md`](NON_HOMO_SYNTAX.md).

| Stub domain | Library | Role |
|-------------|---------|------|
| `tda` | gudhi | Persistence on graph metric (006) |
| `quantum` | qutip | 2–3 qubit witnesses (`COMPUTATIONAL_EVIDENCE`) |
| `category` | (pure Python) | Finite hom-set counts on graphs n≤6 |

Install: `pip install -e ".[dev,nd]"`.

---

## Falsifiability (continued)

The program is wrong if:

- machine-native search consistently collapses to human-known invariants with \(K_H \approx K_A\);
- Independence and generative gates never discriminate beyond noise.
- Certificates add no reproducibility over ad-hoc scripts.

Negative results are **first-class** (`rejections.jsonl`).

---

## Related docs

- [`AI_THINKING_TOPOLOGY.md`](AI_THINKING_TOPOLOGY.md) — AI vs human cognition topology
- [`VISION.md`](VISION.md) — program vision and success criteria
- [`NON_HOMO_SYNTAX.md`](NON_HOMO_SYNTAX.md) — non-homo syntax reference
- [`FRAME_LADDER.md`](FRAME_LADDER.md) — F1–F∞ frame ladder
- [`AI_NATIVE_NAMM.md`](AI_NATIVE_NAMM.md) — certificate-first Phase 2
- [`PHILOSOPHY.md`](PHILOSOPHY.md) — MUH as heuristic only
- [`PROTOCOL_V2.md`](PROTOCOL_V2.md) — hard gates and novelty ladder
