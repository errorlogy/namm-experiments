# NAMM Manifesto (brief)

**Non-Anthropic Mathematics** — a scientific research program, not a hype claim.

---

## Thesis

Some mathematical structures may be **native to machine cognition first**: easier to generate, verify, and compose as programs than to name in classical notation. We search for them with falsifiable experiments, not philosophical arguments alone.

---

## Method

1. **Certificate over prose** — ground truth is `certificate.json` (hash + eval witness), not the human summary.
2. **Hard gates** — independence, compression asymmetry (\(K_A/K_H \geq 2\)), generative holdout.
3. **Logged failure** — every rejection has a reason code; null results count.
4. **Attack before announce** — correlation, simplify, non-equivalence checks before any candidate is accepted.

---

## What we do not claim

- We do not claim new theorems by default.
- We do not use Tegmark's MUH as a proof premise — only as search-space heuristic ([`PHILOSOPHY.md`](PHILOSOPHY.md)).
- We do not treat LLM prose as evidence.

---

## North star

> Discover structures whose canonical representation is a **verified program**, not a formula; whose human explanation is longer and lossier than the machine artifact; and which predict behavior on families no named invariant spans.

---

## Reproduce or refute

```bash
pip install -e ".[dev]"
pytest tests/ -v
namm run-experiment --id NAMM-2026-001
```

Repository: [github.com/errorlogy/namm-experiments](https://github.com/errorlogy/namm-experiments)

**Author:** Roman Kuznetsov · NAMM research program
