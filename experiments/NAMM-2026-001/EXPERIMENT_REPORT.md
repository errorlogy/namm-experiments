# NAMM-2026-001 — Full Experiment Report

**Status:** computationally supported  
**Cycle:** INPUT → ABSTRACT → META-LIFT → GENERATE → FORMALIZE → ATTACK → VERIFY → COMPARE → PROJECT  
**Date:** 2026-08-08

---

## NAMM Research Cycle

### INPUT

- **Domain:** finite connected simple graphs, order \(n \leq 8\)
- **Base object:** graph statistic primitives drawn from NetworkX (`wiener_index`, `num_edges`, `avg_degree`, `clustering`, etc.)
- **Baseline:** Wiener index \(W(G) = \sum_{\{u,v\}} d(u,v)\)
- **Seed:** 42; **Candidates generated:** 50

### ABSTRACT

Objects: connected graphs \(G=(V,E)\), \(|V|\leq 8\).  
Relations: graph isomorphism.  
Transformations: random linear composition of primitive statistics.  
Invariants: candidate expressions \(f(G)\) evaluated by deterministic Python AST interpreter.  
Constraints: reject candidates identical to Wiener baseline on the test graph set.

### META-LIFT

| Level | Object |
|-------|--------|
| L0 | Individual graphs and their statistics |
| L1 | Morphism-level: `evaluate_formula` as a graph → ℝ map |
| L2 | Meta-level: `random_invariant_formula` generator composing statistics with coefficients |
| L3 | Evaluation criterion: variance score + baseline non-equivalence filter |

The generator operates on the **space of composition rules** (coefficients, primitive selection), not on human-motivated graph families.

### GENERATE

Machine-native generator: `random_invariant_formula(seed)` → linear combination of 2–4 primitives with integer coefficients in \(\{1,\ldots,5\}\).

**Best candidate (by variance score):**

```
2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering
```

- **ID:** `inv-a6fe843a`
- **Score:** 289.44 (max − min over 40 test graphs)
- **Meta-origin:** `random_composition_of_graph_statistics`

### FORMALIZE

**Definition (DEFINITION).** For a connected graph \(G\), define

\[
I(G) = 2\bar{d}(G) + 5W(G) + 4|E| + \kappa(G)
\]

where \(\bar{d}(G)=2|E|/|V|\) is average degree, \(W\) is Wiener index, and \(\kappa(G)\) is transitivity (global clustering coefficient).

All primitives are **DEFINITION**-level graph invariants under isomorphism.

### ATTACK

Adversarial checks applied:

1. **Baseline non-equivalence:** candidate must differ from `1*wiener_index` on at least one test graph — **passed** (all 50 candidates differ).
2. **Exhaustive atlas search (order ≤ 6):** 143 connected graphs from NetworkX graph atlas — **counterexample found** at \(K_2\): \(I(K_2)=11\), \(W(K_2)=1\).
3. **Known-invariant equivalence:** compared against 10 standard baselines on order ≤ 6 — **none equivalent**.
4. **Degeneracy:** \(I\) is highly correlated with Wiener (\(r \approx 0.938\) on 143 atlas graphs \(n\leq 6\)) — candidate is Wiener-dominated, not structurally independent.
5. **Redundancy:** `avg_degree = 2*num_edges/num_nodes` — expression reduces to a rational combination of \((W, |E|, \kappa, |V|)\), a standard form in chemical graph theory.

### VERIFY

| Check | Result |
|-------|--------|
| Exhaustive vs Wiener, order ≤ 5 (atlas) | Not equivalent; CE: \(K_2\) |
| Exhaustive vs Wiener, order ≤ 6 (full atlas, 143 graphs) | Not equivalent; CE: \(K_2\) |
| Z3 stub | SAT (stub only; no invariant encoding) |
| Python evaluator agreement | Verified on all test graphs |

**Evidence artifacts:** `artifacts/result.json`, `artifacts/extended_analysis.json`

### COMPARE (Prior Art)

| Known invariant | Relationship to candidate |
|-----------------|-------------------------|
| **Wiener index** (1947) | Dominant term (coefficient 5); Pearson \(r \approx 0.938\) on order ≤ 6 atlas (143 graphs) |
| **Degree sum** \(2|E|\) | Present via `4*num_edges` and `2*avg_degree` |
| **Clustering / transitivity** | Present with coefficient 1 |
| **Spectral (algebraic connectivity)** | Not used in best candidate; other candidates in pool used it |
| **Linear combinations in QSAR/CGT** | Same structural class: weighted sums of topological indices |

**Novelty status:** **new combination** (not equivalent to tested singles or simple pairs), but **not potentially novel** as mathematics — this is a random linear combination of well-known statistics, a standard heuristic in computational chemistry and graph enumeration.

### PROJECT

See `artifacts/HUMAN_PROJECTION.md` for human-readable summary.

---

## Template Sections 1–17

### 1. Experiment ID

`NAMM-2026-001`

### 2. Domain

Finite connected simple graphs with \(1 \leq |V| \leq 8\).  
Supports automated evaluation via NetworkX statistics and a deterministic AST formula evaluator.

### 3. Research question

**Can machine-native random search discover a graph invariant expression that differs from the Wiener index baseline while remaining nontrivial on tested graphs?**

**Answer (falsifiable):** Yes — random search produces many candidates differing from Wiener with nontrivial value range. However, none appear mathematically novel; the best candidate is a Wiener-dominated linear combination.

### 4. Baselines

| Baseline | Role |
|----------|------|
| `1*wiener_index` | Primary non-equivalence target |
| `1*algebraic_connectivity` | Listed in config; used in other candidates |
| Random search (50 candidates, seed 42) | Generator baseline |
| Known singles: degree sum, clustering, diameter, radius | Compared in extended analysis |

### 5. Primitive data

- **Graph universe (search):** 40 graphs — NetworkX atlas for \(n \leq 5\), 3 random connected graphs per \(n \in \{6,7,8\}\)
- **Graph universe (verification):** 143 connected atlas graphs for \(n \leq 6\)
- **Primitives:** `num_nodes`, `num_edges`, `avg_degree`, `diameter`, `radius`, `clustering`, `algebraic_connectivity`, `wiener_index`
- **Serialization:** JSONL candidate records + JSON result bundle

### 6. Candidate construction

```python
chosen = rng.sample(PRIMITIVES, k=rng.randint(2, 4))
coeffs = [rng.randint(1, 5) for _ in chosen]
expression = " + ".join(f"{c}*{p}" for c, p in zip(coeffs, chosen))
```

Canonical form: `InvariantFormula(id, expression, primitives, meta_origin)`.

### 7. Meta-level origin

Generated from **L2 meta-operator** `random_composition_of_graph_statistics`: selection and weighting of L0 statistics without human structural priors.

### 8. Claims

| ID | Statement | Status |
|----|-----------|--------|
| C1 | Random linear combinations of graph statistics may differ from Wiener index on connected graphs | **COMPUTATIONAL_EVIDENCE** (50/50 candidates differ on test set) |
| C2 | Best candidate \(I(G)=2\bar{d}+5W+4|E|+\kappa\) is not equivalent to Wiener index | **COMPUTATIONAL_EVIDENCE** (counterexample \(K_2\), verified on 143 atlas graphs \(n\leq 6\)) |
| C3 | \(I(G)\) is not equivalent to any of 10 tested standard invariants on order ≤ 6 | **COMPUTATIONAL_EVIDENCE** |
| C4 | \(I(G)\) is strongly correlated with Wiener index (\(r \approx 0.938\) on 143 atlas graphs) | **COMPUTATIONAL_EVIDENCE** |
| C5 | \(I(G)\) constitutes a novel graph invariant in the mathematical literature | **CONJECTURE** — **rejected** by prior-art analysis; see novelty status |
| C6 | `avg_degree`, `wiener_index`, `num_edges`, `clustering` are graph isomorphism invariants | **DEFINITION** (standard) |
| C7 | Exhaustive non-equivalence on order ≤ 5 detects baseline separation | **COMPUTATIONAL_EVIDENCE** |

### 9. Evaluator

- **Objective:** maximize value range \(\max_G f(G) - \min_G f(G)\) subject to \(f \not\equiv W\)
- **Verifier:** `exhaustive_equivalence_check` on NetworkX atlas
- **Implementation:** `namm.domains.graph.evaluator.evaluate_formula` (AST, no LLM)

### 10. Counterexample search

| Search | Space | Method | Outcome |
|--------|-------|--------|---------|
| vs Wiener, \(n\leq 5\) | Atlas connected graphs | Exhaustive | CE: \(K_2=(\{0,1\},\{01\})\), \(I=11\), \(W=1\) |
| vs Wiener, \(n\leq 6\) | 143 atlas connected graphs | Exhaustive | Same CE; no graph found where \(I=W\) |
| vs 10 known invariants, \(n\leq 6\) | Same 143 graphs | Pairwise exhaustive | No equivalence to any tested baseline |

### 11. Proof or certificate

Deterministic reproduction:

```powershell
cd c:\Users\Public\NAMM
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m namm.cli run-experiment --id NAMM-2026-001
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m namm.cli verify --expr "2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering" --baseline "1*wiener_index" --max-order 6
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe experiments\analyze_namm_2026_001.py
C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe -m pytest -q
```

### 12. Prior-art analysis

- **Wiener index (1947):** Sum of shortest-path distances; foundational topological index in chemistry. Our candidate uses \(5W\) as dominant term.
- **Degree-based indices:** Zagreb indices, degree sum \(2m\); our `4*num_edges + 2*avg_degree` encodes degree information redundantly.
- **Clustering coefficient:** Transitivity measures triangle density; standard in network science (Watts-Strogatz, etc.).
- **Spectral invariants:** Algebraic connectivity (Fiedler value) appears in other candidates but not the best one; Laplacian eigenvalues are a distinct classical family.
- **Linear combinations:** Weighted sums of topological indices are standard in QSAR; no claim of novelty is warranted.

**Difference from prior art:** Specific coefficient tuple \((2,5,4,1)\) for \((\bar{d}, W, m, \kappa)\) — arbitrary from random search, not derived from theory.

### 13. Novelty status

**new combination** — not equivalent to tested singles or simple pairs, but **not potentially novel** as a mathematical result. Honest assessment: this is a **reformulation-class** object (linear combo of known invariants), unlikely to interest graph theorists without further structural characterization.

### 14. Machine-native representation

```json
{
  "candidate_id": "inv-a6fe843a",
  "expression": "2*avg_degree + 5*wiener_index + 4*num_edges + 1*clustering",
  "primitives": ["avg_degree", "wiener_index", "num_edges", "clustering"],
  "meta_origin": "random_composition_of_graph_statistics",
  "score": 289.44444444444446,
  "verification": {
    "equivalent_to_wiener_atlas_n6": false,
    "counterexample": {"order": 2, "edges": [[0, 1]], "value_a": 11.0, "value_b": 1.0}
  }
}
```

Full bundle: `artifacts/result.json`, `artifacts/candidates.jsonl`, `artifacts/extended_analysis.json`

### 15. Human projection

The best discovered expression is essentially “mostly Wiener index, plus some edge-count and clustering adjustments.” On a path graph \(P_4\), it produces values in a wider range than Wiener alone (hence high score), but this reflects **coefficient tuning**, not discovery of a new structural invariant.

**Limitation:** The search space is restricted to small-integer linear combinations of 8 primitives — a narrow, human-adjacent space despite the “non-anthropic” framing.

### 16. Reproduction

| Parameter | Value |
|-----------|-------|
| Python | 3.12 (`C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe`) |
| Seed | 42 |
| Candidates | 50 |
| Max order | 8 |
| Compute | < 15 s on local machine |

Install: `pip install -e .` from workspace root.

### 17. Negative results

| Result | Detail |
|--------|--------|
| Zero rejections | All 50 random candidates differed from Wiener — filter may be too weak (non-equivalence is trivial for random combos) |
| No novel invariant | Best candidate is Wiener-dominated (\(r \approx 0.938\)) |
| Z3 verification stub | Full SMT encoding of graph invariants not implemented |
| Incomplete exhaustivity for \(n > 5\) | Search uses 3 random graphs per order for \(n \in \{6,7,8\}\), not full atlas |
| No candidates using `max`/`min` | Generator samples linear combos only in practice (operators defined but unused in this run) |
| Research question partially answered | “Differs from Wiener” yes; “nontrivial new invariant” no |

---

## Protocol Section 13 Summary

| Field | Value |
|-------|-------|
| **A. Object ID** | `inv-a6fe843a` |
| **B. Status** | computationally supported |
| **C. Primitive Data** | Connected graphs, NetworkX statistics |
| **D. Construction** | Random linear combination, seed 42 |
| **E. Meta-Level Origin** | L2 composition of L0 statistics |
| **F. Axioms** | Standard graph definitions (NetworkX) |
| **G. Semantics** | Connected simple graphs, order ≤ 8 |
| **H. Invariants** | \(I(G) = 2\bar{d} + 5W + 4m + \kappa\) |
| **I. Main Claims** | See table §8 |
| **J. Proof/Evidence** | Exhaustive atlas check, 143 graphs |
| **K. Known Analogues** | Wiener-type linear topological indices |
| **L. Novel Component** | Coefficient tuple only — minimal, likely uninteresting |
| **M. Human Projection** | `artifacts/HUMAN_PROJECTION.md` |
| **N. Machine Representation** | `artifacts/result.json`, `candidates.jsonl` |
| **O. Open Problems** | Can search escape the Wiener-correlated subspace? Can Z3 encode invariant equivalence? Full atlas for \(n=7,8\)? |
