# NAMM-2026-029 — Resource conversion asymmetry

**Domain:** `cognitive_class_taxonomy` + telemetry overlay  
**Hypotheses:** H-CCT-016, H-CCT-017, H-MCG-014  
**Doc:** [`docs/COGNITIVE_CLASS_TAXONOMY.md`](../../docs/COGNITIVE_CLASS_TAXONOMY.md) §4.6

## Design

Fixed \(\tau\) token budget; class-tagged agents; sweep task channel \(c\);
measure \(U_{\mathrm{out}}\), \(\rho_{\mathrm{conv}}\), \(\Delta W_{\mathrm{alloc}}\).

## Run

```bash
namm sci-flow run --experiment NAMM-2026-029
# or
python experiments/NAMM-2026-029/run_experiment.py
```

## Results (round 3 — sci-flow)

| Metric | Value |
|--------|-------|
| sweep size | 900 |
| asymmetry high-impact ratio (K6 research / K1 research) | 8.18× |
| asymmetry noise ratio (K1 entertainment / K6 entertainment) | 9.75× |
| G-6×nd U_out (K6 research, φ=1.5) | 1.219 |
| G-1μ U_out (K_AI_μ research, attenuated) | 0.095 |
| steering ratio g6nd/g1mu | **12.8×** |
| H-CCT-016, H-CCT-017, H-MCG-014 | **supported** |
| Certificate | PARTIAL_EVIDENCE |

## Results (2026-08-18 run)

| Metric | Value |
|--------|-------|
| sweep size | 600 |
| asymmetry high-impact ratio (K6 research / K1 research) | 8.18× |
| asymmetry noise ratio (K1 entertainment / K6 entertainment) | 9.75× |
| K6 research U_out | 0.810 |
| K1 entertainment U_out | 0.701 |
| H-CCT-016, H-MCG-014 | **supported** |
| H-CCT-017 | **not supported** (G-6×nd vs G-1μ ratio borderline) |
| Certificate | PARTIAL_EVIDENCE |
