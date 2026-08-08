# NAMM-2026-005 — Kotzig P_k-Graph Finite Shadow

**Domain:** `open_problem_shadow`  
**Status:** implemented  
**Open problem:** [Kotzig's conjecture](https://en.wikipedia.org/wiki/Kotzig%27s_conjecture)

---

## Research question

Can NAMM's finite-graph evaluator **certify or refute** the bounded shadow of Kotzig's conjecture by exhaustive atlas scan?

> **Conjecture (Kotzig, 1974):** For every integer \(k \ge 3\), there is no finite simple graph with at least two vertices in which every pair of distinct vertices is joined by exactly one simple path of length \(k\) (a **\(P_k\)-graph**).

---

## Finite shadow (exact, falsifiable)

For fixed bounds \((n_{\max}, k_{\max})\):

\[
\neg\,\exists\, G \text{ connected simple},\, 2 \le |V(G)| \le n_{\max},\,
3 \le k \le k_{\max} : G \text{ is a } P_k\text{-graph}.
\]

A single graph–\(k\) pair with score \(= 1.0\) (all pairs have exactly one length-\(k\) path) is a **counterexample certificate** refuting Kotzig for that \(k\).

This run uses \(n_{\max}=7\), \(k \in \{3,\ldots,10\}\).

---

## Run

```bash
python -m pip install -e ".[dev]"
python -m namm.cli run-experiment --id NAMM-2026-005
python -m pytest tests/test_open_problem_pk.py -q
```

Primary artifacts: `artifacts/certificate.json` (if counterexample), `artifacts/result.json`, `artifacts/rejections.jsonl`.

---

## Related docs

- [`docs/OPEN_PROBLEMS_TIERLIST.md`](../../docs/OPEN_PROBLEMS_TIERLIST.md) — tiered catalog
- [`docs/VISION.md`](../../docs/VISION.md) — philosophy vs operations

---

## Author

Roman Kuznetsov · NAMM research program
