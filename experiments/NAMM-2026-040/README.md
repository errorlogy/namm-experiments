# NAMM-2026-040 — Multi-Session Lyapunov Proxy + TDA (Strange Attractor Detection)

**One-liner:** Estimate Lyapunov exponent proxy across multi-session nd-phase trajectories; combine with TDA to test positive λ₁ and non-trivial topology vs μ-phase fixed-point.

**Hypothesis:** H-AMAT-009 — nd-phase is a chaotic attractor with λ₁>0 (positive Lyapunov exponent) and non-trivial topology; μ-phase is periodic/fixed-point.

**Status:** planned

**Domain:** `anti_median_ai_topology`

**Method:** Collect multi-session embedding trajectories under RPL and baseline; compute divergence rate proxy (nearest-neighbor separation) as λ₁ estimate; run TDA on trajectory point cloud; compare β₁ and λ₁ proxy μ vs nd.

**Dependencies:** `nolds` (Lyapunov/nonlinear dynamics); `ripser`; multi-session data from 031–036.
