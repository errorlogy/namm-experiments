# Experiment Template (Protocol v2)

## 1. Experiment ID

`NAMM-YYYY-NNN`

## 2. Domain

State the exact mathematical domain and why it supports automated evaluation.

## 3. Research question

Provide one falsifiable question.

## 4. Baselines (required)

List human-designed, random-search, evolutionary, symbolic, or existing AI baselines.

**Same budget rule:** every baseline uses the same `num_candidates`, `max_order`, and documented compute cap. See [`docs/BASELINE_PROTOCOL.md`](../docs/BASELINE_PROTOCOL.md).

| Baseline | Expression / method | Equivalent? | Pearson r | Same budget? |
|----------|---------------------|---------------|-----------|--------------|
| wiener_index | `1*wiener_index` | | | yes |
| random_search | generator × N | | | yes |

## 5. Primitive data

Define sets, types, signatures, categories, programs, or finite universes.

## 6. Candidate construction

Give the exact construction procedure and canonical serialization.

## 7. Meta-level origin

State whether the candidate was generated from objects, morphisms, rewrite rules, evaluators, logical systems, or transformations of those components.

## 8. Claims

| ID | Statement | Status |
|---|---|---|
| C1 | ... | DEFINITION / CONJECTURE / LEMMA / THEOREM / COMPUTATIONAL_EVIDENCE |

## 9. Evaluator

Specify the objective function, verifier, proof assistant, solver, or exhaustive procedure.

## 10. Counterexample search

Describe search space, bounds, methods, and all discovered failures.

## 11. Proof or certificate

Link to formal proof, solver certificate, executable notebook, or deterministic reproduction script.

## 12. Prior-art analysis

List nearest known constructions and explain similarities and differences.

**Stub queries (document only):**

- OEIS: search terms derived from primitive counts / sequences on small graphs
- Semantic Scholar: `"graph invariant" AND ("Wiener index" OR "topological index")`

## 13. Novelty level (N0–N5)

Choose one per [`docs/NOVELTY_LADDER.md`](../docs/NOVELTY_LADDER.md):

- **N0** known / equivalent
- **N1** renaming / reformulation
- **N2** new combination (QSAR-class linear combo)
- **N3** potentially novel component
- **N4** externally confirmed
- **N5** established result

| Level | Justification |
|-------|---------------|
| N_ | |

## 14. Machine-native representation

Provide the canonical non-natural-language artifact.

## 15. Human projection

Give a concise explanation, examples, and limitations.

## 16. Reproduction

Provide exact commands, dependencies, compute budget, and seeds.

## 17. Negative results

Record rejected variants and failure modes. **Every rejection must appear in `artifacts/rejections.jsonl`.**

| Candidate | Reason code | Detail |
|-----------|-------------|--------|
| | `equivalent_to_wiener_baseline` | |
| | `high_correlation_with_baseline:…` | |
| | `prior_art_simplify:…` | |

## 18. Representation metrics

Log K_A proxies per [`docs/REPRESENTATION_METRICS.md`](../docs/REPRESENTATION_METRICS.md):

| Metric | Value |
|--------|-------|
| json_bytes | |
| gzip_bytes | |
| eval_time_ms | |
| token_count_estimate | |

## Attack checklist sign-off

Complete [`docs/ATTACK_CHECKLIST.md`](../docs/ATTACK_CHECKLIST.md) before accepting a candidate.

| Step | Passed | Notes |
|------|--------|-------|
| A1 non-equivalence | | |
| A3 correlation | | |
| A4 simplify | | |

`signed_off: true / false`

## NEGATIVE_RESULTS.md (append or link)

Summarize null outcomes for the experiment folder:

```markdown
# Negative Results — NAMM-YYYY-NNN

## Summary
- Candidates rejected: N
- Primary failure modes: …

## Notable rejections
| ID | Reason | Pearson r |
|----|--------|-----------|
```
