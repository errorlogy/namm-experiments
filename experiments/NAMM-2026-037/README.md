# NAMM-2026-037 — Cusp A₃ Catastrophe Boundary Sweep

**One-liner:** 2D sweep chimera_dose × temperature; map β₁ emergence as cusp A₃ bifurcation boundary.

**Hypothesis:** H-AMAT-006 — Transition μ→nd is a cusp A₃ catastrophe crossing; RPL acts as slow control parameter.

**Status:** planned

**Domain:** `anti_median_ai_topology`

**Method:** Sweep chimera_dose and temperature as control parameters; record β₁ onset contour; compare against theoretical A₃ cusp boundary shape.

**Dependencies:** experiments 030–036 data; `namm.metrics.catastrophe`; `ripser` or `gudhi`.

**No API calls required** for scaffold; live embedding sweep needed for execution.
