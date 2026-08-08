# Novelty Ladder (N0–N5)

Operational definitions for assigning novelty level to a NAMM candidate. Levels are **ordinal**; higher is more novel. Publication-style claims require **N3+** with evidence.

| Level | Name | Definition | v2 rule |
|-------|------|------------|---------|
| **N0** | Known / equivalent | Pointwise equivalent to a known invariant or baseline on the test universe | **Reject** for candidate status |
| **N1** | Renaming / reformulation | Same function, different syntax; or sympy-simplifies to known form | **Reject** |
| **N2** | New combination | Weighted sum or composition of known primitives not equivalent to any single tested baseline, but no new primitive or theorem | Accept as *computational artifact* only; not “novel mathematics” |
| **N3** | Potentially novel component | Contains a term, operator, or structural feature not reducible to tested baselines; distance \(N(X) > \varepsilon\) supported | Requires attack + prior-art sign-off |
| **N4** | Externally confirmed | Independent agent or literature search confirms novelty of minimal component | Required for `THEOREM`-level claims |
| **N5** | Established result | Peer-reviewed or proof-assistant verified new mathematics | Out of scope for Phase 1 automation |

---

## Assignment procedure

1. Run equivalence checks vs all baselines in [`BASELINE_PROTOCOL.md`](BASELINE_PROTOCOL.md).
2. Run `prior_art.simplify` — if match, assign **N0** or **N1**.
3. Compute max Pearson \(r\) vs baselines — if \(r > 0.95\) and structure is linear-combination class, cap at **N2** regardless of non-equivalence.
4. Document minimal novel component (section L in protocol output).
5. Record level in experiment template §13 and `result.json`.

---

## NAMM-2026-001 retrospective

Best candidate `2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering`:

| Criterion | v1 assessment | v2 assessment |
|-----------|---------------|---------------|
| Non-equivalence vs Wiener | Pass | Pass |
| Correlation vs Wiener (\(r \approx 0.938\)) | Not gated | Pass at \(\tau=0.95\); flagged as Wiener-dominated |
| Simplify / redundancy | Noted in prose | **N1** (avg_degree = 2·num_edges/num_nodes) |
| Honest ladder level | “new combination” | **N2** capped (linear QSAR-class combo); reject for “novel invariant” claims |

Under v2 with stricter \(\tau = 0.90\), the candidate would be **rejected at search time** for high correlation.
