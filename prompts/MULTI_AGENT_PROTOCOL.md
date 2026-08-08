# Multi-Agent Protocol

Use separate agents or isolated model passes so that generation and validation are not performed by the same unchallenged process.

## Roles

### Generator
Produces candidate definitions, constructions, invariants, and conjectures.

### Formalizer
Converts a candidate into explicit syntax, types, axioms, semantics, and machine-readable form.

### Prior-Art Analyst
Searches for known equivalents, special cases, renamings, and established terminology.

### Counterexample Agent
Attempts to falsify every conjecture through finite search, model construction, edge cases, and adversarial interpretation.

### Proof Agent
Constructs a proof or a proof-assistant artifact. It does not assess novelty.

### Independent Verifier
Receives only the formal statement and certificate, not the Generator's explanatory reasoning.

### Human Projection Agent
Creates examples, diagrams, analogies, and concise explanations only after the object is stabilized.

### Meta-Reviewer
Audits evaluator design, search leakage, circularity, duplicated roles, and unsupported novelty claims.

## Acceptance gate

A candidate proceeds only if it satisfies all applicable gates:

```text
well-typed
AND semantically defined
AND nontrivial
AND survives counterexample search
AND has proof or stated evidence level
AND has prior-art analysis
AND is independently reproducible
```

## Recordkeeping

Persist:

- model and version;
- prompts;
- random seeds;
- search budget;
- evaluator code;
- generated candidates, including rejected ones;
- formal proof files;
- counterexamples;
- prior-art search notes;
- final human projection.
