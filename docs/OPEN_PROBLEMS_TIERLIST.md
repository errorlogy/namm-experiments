# Open Problems Tierlist for NAMM Finite Shadows

**As of:** 2026-08-08  
**Purpose:** Catalog open mathematical problems mappable to NAMM **finite shadow** experiments (exact, falsifiable bounds).  
**Tier key:**

| Tier | Meaning |
|------|---------|
| **T0** | Ready now — existing NAMM graph/combinatorics evaluator + counterexample search |
| **T1** | Needs Lean — shadow defined; certificate-grade verification needs Mathlib / Formal Conjectures |
| **T2** | Shadow only — finite formulation exists but search space or domain adapter not yet in repo |
| **T3** | Motivation only — Wikipedia-tier; no crisp bounded falsifier without major reformulation |

Sources consulted: [Open Problem Garden](https://www.openproblemgarden.org/), [Douglas B. West open problems](https://dwest.web.illinois.edu/openp/), [OEIS](https://oeis.org/), [Formal Conjectures (DeepMind)](https://github.com/google-deepmind/formal-conjectures), [Wikipedia list of unsolved problems](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics) (tiering only).

---

## Top 3 recommended for NAMM (T0)

1. **Kotzig's conjecture (P_k-graphs)** → **NAMM-2026-005**  
   Exhaustive atlas counterexample search; immediate falsifier if any P_k-graph appears.

2. **Graceful Tree Conjecture (finite shadow)**  
   All trees of order ≤ n admit a graceful labeling; extend n computationally.

3. **Graph Reconstruction Conjecture (deck uniqueness shadow)**  
   No pair of non-isomorphic connected graphs of order ≤ n share the same deck.

---

## Full tierlist (≥10 problems)

### 1. Kotzig's conjecture (P_k-graphs)

| Field | Value |
|-------|-------|
| **Source** | [Wikipedia — Kotzig's conjecture](https://en.wikipedia.org/wiki/Kotzig%27s_conjecture); Bondy & Murty (1976); Kostochka verified k≤20 |
| **Tier** | **T0** |
| **Finite shadow** | ∃ connected simple G, \|V\|≥2, k≥3: every distinct pair has exactly one simple path of length k |
| **NAMM-ready** | Exact path-count evaluator on NetworkX atlas; counterexample = certificate |
| **Prior-art risk** | **Medium** — verified k≤20 (Kostochka); extending order bound is incremental, disproving conjecture would be major |
| **Experiment** | `NAMM-2026-005` |

### 2. Graceful Tree Conjecture

| Field | Value |
|-------|-------|
| **Source** | [Open Problem Garden — Graceful labeling](https://www.openproblemgarden.org/op/graceful_labeling); Rosa (1967) |
| **Tier** | **T0** |
| **Finite shadow** | ∀ trees T with \|V(T)\|≤n, ∃ graceful labeling f: V→{0,…,m} with distinct edge sums |
| **NAMM-ready** | Backtracking label search per tree; falsified by one tree of order ≤n |
| **Prior-art risk** | **Low–medium** — verified to large n; bounded extension is computational, not novel if negative |

### 3. Graph Reconstruction Conjecture

| Field | Value |
|-------|-------|
| **Source** | [Douglas B. West — Reconstruction Conjecture](https://dwest.web.illinois.edu/openp/reconstruct.shtml); Kelly (1957) |
| **Tier** | **T0** |
| **Finite shadow** | ∃ non-isomorphic connected G,H with \|V\|=n≤n_max and isomorphic decks |
| **NAMM-ready** | Deck builder + isomorphism check on atlas; counterexample pair is certificate |
| **Prior-art risk** | **High if positive** — would be breakthrough; negative bounded results well studied to n≈11 |

### 4. Unit Vector Flows (Jain conjecture 2) — **refuted 2026**

| Field | Value |
|-------|-------|
| **Source** | [Open Problem Garden — Unit vector flows](http://www.openproblemgarden.org/op/unit_vector_flows); [arXiv:2603.23328](https://doi.org/10.48550/arxiv.2603.23328) |
| **Tier** | **T1** (SAT + Lean replay) |
| **Finite shadow** | Finite S² point set requiring ±5 in {±4,…,±4} labeling with great-circle triple sums zero |
| **NAMM-ready** | SAT encoding + certificate; **prior art disproof exists** |
| **Prior-art risk** | **Very high** — use as methodology reference only, not discovery target |

### 5. WOWII Conjecture 200 (Hamiltonian path vs neighborhood independence)

| Field | Value |
|-------|-------|
| **Source** | [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures); [OpenMikasa counterexample](https://github.com/OpenMikasa/wowii-conjecture-200) |
| **Tier** | **T1** |
| **Finite shadow** | Connected G with ⌈1+λ_avg(G)⌉ ≤ tree(G) but no Hamiltonian path |
| **NAMM-ready** | 14-vertex verifier pattern; **refuted with Lean certificate** |
| **Prior-art risk** | **Very high** — closed problem as of 2026 |

### 6. Hedetniemi's conjecture

| Field | Value |
|-------|-------|
| **Source** | [Open Problem Garden — Hedetniemi](https://www.openproblemgarden.org/op/hedetniemis_conjecture) |
| **Tier** | **T2** |
| **Finite shadow** | χ(G×H) < min(χ(G),χ(H)) for small G,H |
| **NAMM-ready** | Product coloring search; **disproved in general (2019)** — finite shadows still useful for strength of counterexamples |
| **Prior-art risk** | **High** — main conjecture false; finite cases largely settled |

### 7. Hamiltonian paths in vertex-transitive graphs

| Field | Value |
|-------|-------|
| **Source** | [Open Problem Garden](https://openproblemgarden.org/op/hamiltonian_paths_and_cycles_in_vertex_transitive_graphs) |
| **Tier** | **T2** |
| **Finite shadow** | Connected vertex-transitive G of order ≤n without Hamiltonian path |
| **NAMM-ready** | Needs vertex-transitive generator + H-path DP; only 5 known exceptions |
| **Prior-art risk** | **Medium** — positive result would be huge; computational sweeps exist |

### 8. Turán number of 4-cycles (Verstraëte conjecture)

| Field | Value |
|-------|-------|
| **Source** | [Open Problem Garden — Turán number](https://www.openproblemgarden.org/op/turan_number_of_a_finite_family); Kühn–Osthus |
| **Tier** | **T2** |
| **Finite shadow** | C_4-free graph on n vertices with no C_4-free subgraph on ≥cn edges |
| **NAMM-ready** | Extremal search at fixed n; heavy but finite |
| **Prior-art risk** | **Medium** — active extremal literature |

### 9. OEIS gnu(n) iteration to 1 (Conway et al.)

| Field | Value |
|-------|-------|
| **Source** | [OEIS A000001](https://oeis.org/A000001) |
| **Tier** | **T2** |
| **Finite shadow** | ∃n: iterated a(n)=gnu(n) does not reach 1 within bounded steps |
| **NAMM-ready** | GAP/OEIS values to 500+; needs group-count oracle, not graph domain |
| **Prior-art risk** | **Low** for bounded checks; conjecture still open |

### 10. OEIS A053403 — missing gnu values

| Field | Value |
|-------|-------|
| **Source** | [OEIS A053403](https://oeis.org/A053403) |
| **Tier** | **T2** |
| **Finite shadow** | Find (a,b) in P with b≤B not generated by gnu rules, or prove none for bound B |
| **NAMM-ready** | Integer iteration from A000001 table; falsifiable at each B |
| **Prior-art risk** | **Medium** — 508 terms known; extensions are incremental |

### 11. Sombor index maximum on n-vertex trees

| Field | Value |
|-------|-------|
| **Source** | Chemical graph theory literature; OEIS cross-refs from [Encyclopedia of Finite Graphs](https://github.com/thoppe/encyclopedia-of-finite-graphs) |
| **Tier** | **T0** |
| **Finite shadow** | Tree T of order n with Sombor index exceeding conjectured maximum f(n) |
| **NAMM-ready** | Tree enumerator + invariant evaluator (extend graph statistics) |
| **Prior-art risk** | **Medium** — many bounds proved; counterexample would be publishable |

### 12. Total domination vs matching (Haynes–Hedetniemiet al.)

| Field | Value |
|-------|-------|
| **Source** | [Douglas B. West — domination problems](https://dwest.web.illinois.edu/openp/); open surveys |
| **Tier** | **T0** |
| **Finite shadow** | Connected G of order ≤n with γ_t(G) > f(δ(G)) for stated conjectured f |
| **NAMM-ready** | NetworkX + exact γ_t search on atlas |
| **Prior-art risk** | **Medium** — many cases resolved |

### 13. Riemann Hypothesis

| Field | Value |
|-------|-------|
| **Source** | [Wikipedia — unsolved problems](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics) |
| **Tier** | **T3** |
| **Finite shadow** | No standard finite checkable shadow without analytic reformulation |
| **NAMM-ready** | Motivation / complexity tiering only |
| **Prior-art risk** | N/A |

### 14. P vs NP

| Field | Value |
|-------|-------|
| **Source** | Wikipedia list |
| **Tier** | **T3** |
| **Finite shadow** | Cannot cast as bounded graph search without trivialization |
| **NAMM-ready** | Motivation only |
| **Prior-art risk** | N/A |

---

## Selection rationale for NAMM-2026-005

**Kotzig's conjecture** wins T0 selection because:

1. Shadow maps **directly** to existing graph infrastructure (path enumeration, atlas).
2. Falsifier is **exact** — one graph certificate refutes for a given k.
3. Negative results (no counterexample to order 7) are **logged and reproducible**.
4. Aligns with NAMM certificate culture without requiring Lean for first pass.
5. Prior-art is **bounded verification** (k≤20), not closed — room for bounded-order extension.

---

## Related

- [`experiments/NAMM-2026-005/README.md`](../experiments/NAMM-2026-005/README.md)
- [`docs/RESEARCH_DIRECTION.md`](RESEARCH_DIRECTION.md)
- [`docs/VISION.md`](VISION.md)

---

Roman Kuznetsov · NAMM research program
