# NAMM-2026-013 — Cognitive Antigravity Prompt Protocol (scaffold)

**Domain:** cross-cutting — `meta_evaluation` + inference protocol (not a NAMM search frame)  
**Status:** **scaffold only** — not yet implemented  
**Hypothesis:** [`docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md`](../../docs/COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md) · H-CA-001  
**Branch:** `hypothesis/cognitive-antigravity`

## Planned research question

Does the **cognitive antigravity v1** instruction template measurably increase **distance from median homo-answer** (\(D_{\mathrm{med}}\)) and **falsifiability** (\(S_{\mathrm{fals}}\)) on a fixed task battery, without increasing hallucination rate, compared to a default system prompt?

## Planned design

| Arm | Prompt |
|-----|--------|
| `control` | Default assistant system prompt |
| `antigravity-v1` | Template from `COGNITIVE_ANTIGRAVITY_HYPOTHESIS.md` §5 |

**Metrics:** \(D_{\mathrm{med}}\), pipeline compliance, \(S_{\mathrm{fals}}\), \(F_{\mathrm{form}}\), \(H_{\mathrm{hall}}\), task accuracy.

**Optional bridge:** correlate antigravity scores with NAMM SNH gate pass rates on graph/tensor prompts (007-style).

## Falsifiers

1. No significant \(D_{\mathrm{med}}\) lift vs control.
2. Lift only via decorative symbolism (\(D_{\mathrm{sym}}\)) without \(F_{\mathrm{form}}\).
3. Accuracy drop > 5% at equal token budget.

## Dependencies

- Embedding model or same-LLM \(M_0(q_H)\) rollout
- Task battery YAML (to be added)
- Rubric for pipeline section parsing

## Not run in this session

Implementation deferred; see hypothesis doc §10.

---

Roman Kuznetsov · NAMM research program
