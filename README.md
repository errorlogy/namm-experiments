# NAMM Experiments

> **Non-Anthropic Mathematics:** discovering structures whose canonical form is a verified program, not a human formula.

**Research governance:** AI-led direction — the human author sets falsifiability and gates; the AI researcher allocates search budget across domains. See [`docs/RESEARCH_DIRECTION.md`](docs/RESEARCH_DIRECTION.md).

---

## Hypothesis

Mathematical structures may exist that are natural for **machine cognition before human projection** — easier to search, verify, and compose as certificates or AST programs than to name in classical notation. Max Tegmark's Mathematical Universe Hypothesis (MUH) is used **only as philosophy** to widen the search space; it is not a proof premise. See [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md).

---

## What this repo does

| Phase | Focus | Priority | Status |
|-------|-------|----------|--------|
| **Phase 1** | Finite graph invariant search (string formulas, baselines) | Closed | [`NAMM-2026-001`](experiments/NAMM-2026-001/) — calibration null result |
| **Phase 2b** | Program AST synthesis (Graph → Int), evolutionary search | **P1** | [`NAMM-2026-003`](experiments/NAMM-2026-003/) |
| **Phase 2a** | String rewriting systems, confluence search, certificate-first | **P2** | [`NAMM-2026-002`](experiments/NAMM-2026-002/) |
| **Phase 3** | Trans-level meta-evaluators (reflective agents) | **P3** | [`NAMM-2026-004`](experiments/NAMM-2026-004/) — scaffold only |
| **Protocol v2** | Hard acceptance gates, rejection logging, attack checklist | — | [`docs/PROTOCOL_V2.md`](docs/PROTOCOL_V2.md) |
| **CI** | pytest + smoke search on every push to `main` | — | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) |

Full vision, falsifiability, and pipeline diagram: [`docs/VISION.md`](docs/VISION.md).  
Research direction and roadmap: [`docs/RESEARCH_DIRECTION.md`](docs/RESEARCH_DIRECTION.md).  
Brief manifesto: [`docs/MANIFESTO.md`](docs/MANIFESTO.md).

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

**Author:** Roman Kuznetsov · NAMM research program

---

## Clone and run

Requires **Python 3.12+**. From the project root (after cloning):

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
```

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
