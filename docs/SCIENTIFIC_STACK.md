# NAMM Scientific Stack

Roman Kuznetsov · NAMM research program

Related: [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) · [`data/mathematics_library_base.yaml`](../data/mathematics_library_base.yaml)

---

## Install

**Core** (always installed with NAMM):

```bash
pip install -e .
```

**Science extras** — information theory, fuzzy logic, TDA, nonlinear dynamics:

```bash
pip install -e ".[science]"
```

**Full research stack** (dev tests + ND quantum/TDA + science):

```bash
pip install -e ".[dev,nd,science]"
```

---

## Optional dependency group `[science]`

| Package | Purpose | NAMM module |
|---------|---------|-------------|
| `dit` | Discrete information theory (PMF entropy, multivariate info) | `namm.metrics.entropy` (lazy via `try_import_dit`) |
| `scikit-fuzzy` | Fuzzy control / defuzzification pipelines | `namm.metrics.fuzzy` (lazy via `try_import_skfuzzy`) |
| `ripser` | Lightweight persistent homology (β₁ proxies) | CCT / TDA experiments (optional) |
| `nolds` | Lyapunov, DFA, correlation dimension | `namm.metrics.catastrophe` (lazy via `try_import_nolds`) |

**Not on PyPI:** catastrophe theory has no maintained `pycatastrophe` package. NAMM implements Thom fold/cusp/swallowtail in pure `numpy`/`scipy`:

- `namm.metrics.catastrophe` — potentials, equilibria, bifurcation detection, hysteresis loops

---

## Core metric modules (no extras required)

| Module | Domains | Key APIs |
|--------|---------|----------|
| `namm.metrics.entropy` | information_theory, CNS | `shannon_entropy`, `mutual_information`, `delta_h_fiber`, `opinion_entropy` |
| `namm.metrics.fuzzy` | fuzzy_logic, CNS contours | `triangular`, `trapezoidal`, `gaussian_centroid`, `spatial_soft`, `issue_tag_membership` |
| `namm.metrics.catastrophe` | catastrophe_theory, dynamical_systems | `fold_potential`, `cusp_potential`, `cusp_hysteresis_loop`, `detect_bifurcation_crossing` |

Existing CNS / Kuramoto code in `namm.metrics.consensus_non_optimality` now delegates entropy and membership primitives to these modules.

---

## Library YAML mapping

See `scientific_stack` section in [`data/mathematics_library_base.yaml`](../data/mathematics_library_base.yaml) for `namm_extra: science` vs `namm_extra: nd` flags per mathematical section.

Experiment routing to modules is declared in [`data/sci_flow_registry.yaml`](../data/sci_flow_registry.yaml) and documented in [`SCI_FLOW.md`](SCI_FLOW.md).
