# Attack Checklist (mandatory)

Every candidate must survive adversarial review before promotion from `candidate` to `promising` or `accepted`. Sign off each item in the experiment template and in `attack_checklist` JSON.

## Required steps

| # | Attack | Method | Fail condition |
|---|--------|--------|----------------|
| A1 | **Baseline non-equivalence** | Pairwise values on test graph set | Identical to primary baseline on all graphs |
| A2 | **Exhaustive small-order check** | Atlas graphs, order ≤ configured max | Equivalent on full atlas when claimed exhaustive |
| A3 | **Correlation redundancy** | Pearson \(r\) vs each known baseline on atlas | \(r > \tau\) (default 0.95) without structural justification |
| A4 | **Algebraic simplify** | `prior_art.simplify` vs wiener, degree_sum, clustering, num_edges, avg_degree | Simplifies to known form |
| A5 | **Degenerate graphs** | \(K_1\), \(K_2\), path, star, cycle | Division by zero, NaN, or trivial collapse |
| A6 | **Counterexample hunt** | Swap equivalent pairs, single-edge perturbations | Unexpected equality class merge |
| A7 | **Coefficient sensitivity** | Perturb coefficients ±1 where applicable | Claim breaks under minimal perturbation (document only) |
| A8 | **Known analogue search** | Manual + stub OEIS/Semantic Scholar notes in template | Closest analogue not documented |

## Sign-off

```yaml
attack_checklist:
  signed_off: true
  items:
    - step: A1
      passed: true
      notes: "Differs on K_2"
    - step: A3
      passed: false
      notes: "r=0.938 vs wiener — Wiener-dominated"
```

**Rule:** Any failed **A1, A3, or A4** → candidate goes to `rejections.jsonl`, not `candidates.jsonl`.

## Multi-agent roles

Map to agents in `prompts/MULTI_AGENT_PROTOCOL.md`:

- A1–A2: Agent-3 (Counterexample Engine)
- A3–A4: Agent-2 (Analogy Searcher) + Agent-7 (Meta-Critic)
- A5–A6: Agent-3
- A7–A8: Agent-2 + Agent-7

Generator (Agent-0) must not self-certify attack pass.
