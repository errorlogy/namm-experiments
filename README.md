# NAMM Experiments

> **Non-Anthropic Mathematics (NAMM):** a verification-first research program testing whether machine-native artifacts can certify mathematical structure before compact human projection exists.

**Research governance:** AI-led search under human-set falsifiability gates — the author defines acceptance criteria and attack checklists; the AI researcher allocates search budget across domains. See [`docs/RESEARCH_DIRECTION.md`](docs/RESEARCH_DIRECTION.md).

**Author:** Roman Kuznetsov · [NAMM research program](https://github.com/errorlogy/namm-experiments)

**Project updates:** [@AGIminister on X](https://x.com/AGIminister)

---

## Research program

NAMM tests a **falsifiable claim**, not a metaphysical proof:

> Machine-native search can surface structures whose **canonical form is a verified program or certificate**, with compression asymmetry \(K_A \ll K_H\), independence from named baselines, and generative power on held-out families — before a compact human formula exists.

We report **computational evidence** under explicit gates. Negative and null results are first-class (`rejections.jsonl`). We claim methodology and reproducible experiments — not breakthrough theorems.

---

## Epistemic stance

| Layer | Content | Status |
|-------|---------|--------|
| **Operational** | SNH gates, `certificate.json`, independence checks, generative holdout, novelty ladder | Executable; see [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md) |
| **Philosophical** | Structure as discovery, not invention; MUH widens search space; ND frames as **metaphors mapped to formal math** | `PHILOSOPHICAL_INFERENCE` — **non-evidential**; not a proof premise |

> **PHILOSOPHICAL_INFERENCE** (philosophical motivation — not a proof premise): Math structures are not human constructions but observer-independent objects. Human formalism is a cognitively bounded coordinate system over this space. AI may discover verifiable invariants and representations that are non-intuitive to us.

**Operational falsifiability** — SNH gates and [Protocol v2](docs/PROTOCOL_V2.md) — does not depend on this inference; it is what makes claims testable. This stance only widens the search space.

Humans access structure through **constrained projections** (\(\pi_H\)): formulas, diagrams, prose. Machine search operates in different representational frames (\(\pi_A\)): AST programs, rewrite systems, relation tensors. Whether AI accesses descriptive levels humans compress away is **empirically testable** via \(K_A/K_H\) and certificate reproducibility — not settled by metaphysics alone.

Consolidated concept reference: [`docs/NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](docs/NON_HOMO_SYNTAX_AND_ND_FRAMES.md). Philosophy detail: [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md).

---

## Hypothesis

Mathematical structures may exist that are natural for **machine cognition before human projection** — easier to search, verify, and compose as certificates or AST programs than to name in classical notation. Max Tegmark's Mathematical Universe Hypothesis (MUH) is used **only as philosophical motivation** to widen the search space; it is not a proof premise.

---

## Experiments and phases

| Phase | Focus | Priority | Status |
|-------|-------|----------|--------|
| **001** | Finite graph invariant search (string formulas, baselines) | Closed | [`NAMM-2026-001`](experiments/NAMM-2026-001/) — calibration null result |
| **002** | String rewriting systems, confluence search, certificate-first | **P2** | [`NAMM-2026-002`](experiments/NAMM-2026-002/) |
| **003** | Program AST synthesis (Graph → Int), evolutionary search | **P1** | [`NAMM-2026-003`](experiments/NAMM-2026-003/) |
| **004** | Meta-evaluator fixed points under AI thinking topology | **P3** | [`NAMM-2026-004`](experiments/NAMM-2026-004/) |
| **005** | Open-problem finite shadow — Kotzig \(P_k\)-graph counterexample search | **P2** | [`NAMM-2026-005`](experiments/NAMM-2026-005/) |
| **006** | ND frame — TDA persistence on graph geodesic metric | **P4** | [`NAMM-2026-006`](experiments/NAMM-2026-006/) — TDA frame scaffold |
| **Protocol v2** | Hard acceptance gates, rejection logging, attack checklist | — | [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md) |
| **CI** | pytest + smoke search on every push to `main` | — | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) |

Domain libraries (optional `[nd]` extra): **gudhi** (TDA), **qutip** (quantum frame stubs), pure-Python category hom-set counts. Install: `pip install -e ".[dev,nd]"`.

---

## Documentation

| Topic | Document |
|-------|----------|
| Vision, falsifiability, pipeline | [`docs/VISION.md`](docs/VISION.md) |
| Research direction and roadmap | [`docs/RESEARCH_DIRECTION.md`](docs/RESEARCH_DIRECTION.md) |
| AI thinking topology (Phase 004 foundation) | [`docs/AI_THINKING_TOPOLOGY.md`](docs/AI_THINKING_TOPOLOGY.md) |
| Non-homo syntax + ND frames (concept, consolidated) | [`docs/NON_HOMO_SYNTAX_AND_ND_FRAMES.md`](docs/NON_HOMO_SYNTAX_AND_ND_FRAMES.md) |
| Non-homo syntax (reference) | [`docs/NON_HOMO_SYNTAX.md`](docs/NON_HOMO_SYNTAX.md) |
| ND frame ladder (F1–F∞) | [`docs/FRAME_LADDER.md`](docs/FRAME_LADDER.md) |
| Open problems tierlist (finite shadows) | [`docs/OPEN_PROBLEMS_TIERLIST.md`](docs/OPEN_PROBLEMS_TIERLIST.md) |
| Certificate-first Phase 2 | [`docs/AI_NATIVE_NAMM.md`](docs/AI_NATIVE_NAMM.md) |
| Brief manifesto | [`docs/MANIFESTO.md`](docs/MANIFESTO.md) |

---

## North star

> Discover structures whose canonical representation is a verified program, not a formula; whose human explanation is longer and lossier than the machine artifact; and which predict behavior on families no named invariant spans.

From [`docs/AI_NATIVE_NAMM.md`](docs/AI_NATIVE_NAMM.md).

---

## What counts as success

A result is interesting only when **all** of the following hold (not when it merely sounds novel):

1. **Verified** — ground truth is the certificate (AST hash, eval witness), not the human projection.
2. **Compression asymmetry** — \(K_A \ll K_H\): machine artifact smaller and more precise than its human explanation.
3. **Independence** — passes correlation, simplify, and non-equivalence gates vs known baselines.
4. **Generative power** — non-trivial on held-out graph families not used during search.

Negative results are logged to `rejections.jsonl`. We claim methodology and falsifiable experiments — not breakthroughs.

---

## Clone and run

Requires **Python 3.12+**. From the project root (after cloning):

```bash
python -m pip install -e ".[dev,nd]"
python -m pytest tests/ -v
```

The `[nd]` extra installs **gudhi** (TDA) and **qutip** (quantum frame stubs). Core experiments run without it; NAMM-2026-006 requires `[nd]`.

On Windows you can use `py -3.12` instead of `python` if multiple versions are installed.

## Run program synthesis experiment (NAMM-2026-003) — Priority 1

```bash
python -m namm.cli run-experiment --id NAMM-2026-003
```

Evolutionary AST search with sympy equivalence checks only. Held-out families: trees, bipartite, cubic.

## Run rewriting experiment (NAMM-2026-002) — Priority 2

```bash
python -m namm.cli run-experiment --id NAMM-2026-002
```

Produces `certificate.json` for confluent rewriting systems.

## Run open-problem shadow (NAMM-2026-005) — Kotzig P_k

```bash
python -m namm.cli run-experiment --id NAMM-2026-005
```

Exhaustive finite shadow counterexample search for Kotzig's conjecture. See [`docs/OPEN_PROBLEMS_TIERLIST.md`](docs/OPEN_PROBLEMS_TIERLIST.md).

## Run meta-evaluator experiment (NAMM-2026-004) — Priority 3

```bash
python -m namm.cli run-experiment --id NAMM-2026-004
```

Searches for meta-evaluator fixed points E ≈ F(E) on graphs order ≤ 6. See [`docs/AI_THINKING_TOPOLOGY.md`](docs/AI_THINKING_TOPOLOGY.md).

## Run TDA frame experiment (NAMM-2026-006) — ND frame

```bash
pip install -e ".[dev,nd]"
python -m namm.cli run-experiment --id NAMM-2026-006
```

Persistent homology on graph geodesic metric via Gudhi. See [`docs/FRAME_LADDER.md`](docs/FRAME_LADDER.md).

## Run calibration experiment (NAMM-2026-001) — closed

```bash
python -m namm.cli run-experiment --id NAMM-2026-001
```

Valid null result; no further search budget allocated per [`docs/RESEARCH_DIRECTION.md`](docs/RESEARCH_DIRECTION.md).

## Health loop (Cursor)

Re-run tests + smoke experiment on a schedule:

```text
/loop 30m Run scripts/health.ps1 from the project root; fix any failures.
```

Or manually (Windows PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/health.ps1
```

Cross-platform equivalent:

```bash
python -m pytest tests/ -q
python -m namm.cli run-experiment --id NAMM-2026-001
```

## Verify a candidate

```bash
namm verify --expr "2*num_edges + 1*clustering" --baseline "1*wiener_index"
```

## Project layout

```
src/namm/           Core library (schemas, graph domain, verifiers, baselines, CLI)
experiments/        Per-experiment config and artifacts
tests/              pytest suite
prompts/            NAMM protocol prompts (from research repo)
```

See `NAMM_PROTOCOL.md`, [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md), and `prompts/` for the discovery protocol.

## CI/CD (GitHub Actions)

Every push and pull request to `main` runs CI:

- `pip install -e ".[dev]"`
- `pytest tests/ -v`
- Lightweight smoke search (10 candidates)

A weekly scheduled workflow re-runs pytest on `main`. There is no production deployment — CI is the quality gate before merge.

**Run the same checks locally:**

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

Details: [`.github/workflows/README.md`](.github/workflows/README.md)
