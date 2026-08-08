# NAMM-2026-004 — Meta-Evaluator Fixed Points

**Domain:** `meta_evaluation`  
**Status:** implemented  
**Topology:** AI thinking topology (see [`docs/AI_THINKING_TOPOLOGY.md`](../../docs/AI_THINKING_TOPOLOGY.md))

---

## Research question

Can search discover **meta-evaluator fixed points** E ≈ F(E) on finite graphs (order ≤ 6), where:

- **E** is an evaluator AST that maps graphs → scores and can reference `self` or `target`
- **F(E)** is a meta-transformation on evaluator programs (canonicalize, add_zero, self_unfold, …)
- **Fixed point:** E and F(E) agree on all benchmark graphs within tolerance

This is a **trans-level** experiment under AI-native topology: the object of study is not graph invariants but **self-referential evaluator structure** stable under program transformation.

---

## Run

```bash
python -m namm.cli run-experiment --id NAMM-2026-004
```

Primary artifact: `artifacts/certificate.json` (evaluator AST, transform, fixed-point fraction, eval hashes).

---

## Design

| Component | Role |
|-----------|------|
| `src/namm/domains/meta/ast.py` | Meta-evaluator AST (leaf, self, target, binary ops) |
| `src/namm/domains/meta/transform.py` | F(E) transform registry |
| `src/namm/domains/meta/evaluator.py` | Graph evaluation with self/target context |
| `src/namm/domains/meta/serializer.py` | Certificate-first artifacts |

Benchmark graphs: connected graphs order ≤ 6 (atlas). Fixed-point threshold: 1.0 (exact agreement).

---

## Related docs

- [`docs/AI_THINKING_TOPOLOGY.md`](../../docs/AI_THINKING_TOPOLOGY.md) — AI vs human cognition topology
- [`docs/RESEARCH_DIRECTION.md`](../../docs/RESEARCH_DIRECTION.md) — Phase 3 roadmap

---

## Author

Roman Kuznetsov · NAMM research program
