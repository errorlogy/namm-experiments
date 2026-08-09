# NAMM-2026-006 — TDA Frame Search

**Domain:** `tda_frame`  
**Status:** scaffold — first ND frame experiment  
**Frame ladder:** F3f (see [`docs/FRAME_LADDER.md`](../../docs/FRAME_LADDER.md))

---

## Research question

Can search discover finite graphs whose **persistent homology signature** on the shortest-path metric differs nontrivially from a path-graph baseline?

- **Σ:** Rips filtration on geodesic distance matrix (Gudhi)
- **Eval:** H0/H1 persistence, Betti counts, entropy features
- **Cert:** `signature_hash`, persistence vector, eval_hash
- **κ (π_H):** "Has a hole" prose vs full persistence JSON

This is a **TDA frame** experiment — topology as machine-native artifact, not human geometric intuition.

---

## Prerequisites

```bash
pip install -e ".[dev,nd]"
```

Requires **gudhi** (optional `[nd]` extra).

---

## Run

```bash
python -m namm.cli run-experiment --id NAMM-2026-006
```

Primary artifact: `artifacts/certificate.json` (persistence signature, baseline comparison, eval hash).

---

## Design

| Component | Role |
|-----------|------|
| `src/namm/domains/tda/homology.py` | Gudhi Rips + persistence features |
| `src/namm/domains/tda/generator.py` | Random connected graph sampling |
| `src/namm/domains/tda/serializer.py` | Certificate-first artifacts |

Benchmark baseline: path graph on ⌊max_order/2⌋ nodes. Acceptance: L1 persistence distance ≥ 0.5 and β₁ > 0 (or nontrivial H¹ total persistence).

Graph order capped at 20 for tractability; config uses ≤ 8.

---

## Related docs

- [`docs/FRAME_LADDER.md`](../../docs/FRAME_LADDER.md) — F1–F∞ ladder
- [`docs/NON_HOMO_SYNTAX.md`](../../docs/NON_HOMO_SYNTAX.md) — non-homo syntax
- [`docs/RESEARCH_DIRECTION.md`](../../docs/RESEARCH_DIRECTION.md) — roadmap

---

## Author

Roman Kuznetsov · NAMM research program
