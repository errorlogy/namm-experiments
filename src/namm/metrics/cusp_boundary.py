"""Cusp A₃ β₁ emergence boundary sweep — H-AMAT-006 / NAMM-2026-037."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from namm.metrics.activation_tda import (
    LocalLM,
    build_point_cloud,
    compute_betti_with_backend,
    extract_last_token_hidden_matrix,
    pca_reduce,
)
from namm.metrics.catastrophe import cusp_bifurcation_set, detect_bifurcation_crossing
from namm.metrics.cognitive_class import compute_d_eff
from namm.metrics.live_embeddings import FOLLOWUP
from namm.metrics.activation_tda import _chat_messages, _system_for_policy

logger = logging.getLogger(__name__)


def blend_system(m0: str, nd: str, dose: float) -> str:
    """chimera_dose ∈ [0,1]: 0 = typicality (μ) system, 1 = full RPL."""
    dose = float(np.clip(dose, 0.0, 1.0))
    if dose <= 0.0:
        return m0
    if dose >= 1.0:
        return nd
    return (
        f"{m0}\n\n"
        f"[RPL dose={dose:.2f} — apply the following off-typical constraints with weight {dose:.2f}]\n"
        f"{nd}"
    )


def _gen_temp(
    lm: LocalLM,
    messages: list[dict[str, str]],
    *,
    max_new_tokens: int,
    temperature: float,
) -> str:
    import torch

    tokenizer = lm.tokenizer
    model = lm.model
    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages) + "\nassistant:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    inputs = {k: v.to(lm.device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=max(float(temperature), 0.05),
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        )
    return tokenizer.decode(out[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True).strip()


def run_dose_temp_cell(
    lm: LocalLM,
    prompt: str,
    *,
    dose: float,
    temperature: float,
    m0_system: str,
    nd_system: str,
    n_turns: int = 3,
    max_new_tokens: int = 48,
    last_n_layers: int = 4,
    pca_dims: int = 8,
    beta1_onset: float = 1.0,
) -> dict[str, Any]:
    system = blend_system(m0_system, nd_system, dose)
    history: list[tuple[str, str]] = []
    hidden_mats: list[np.ndarray] = []
    n_layers = lm.n_layers
    layer_indices = list(range(max(1, n_layers - last_n_layers + 1), n_layers + 1))

    for turn in range(n_turns):
        user_msg = prompt if turn == 0 else FOLLOWUP
        hidden_mats.append(
            extract_last_token_hidden_matrix(lm, system, user_msg, history, layer_indices=layer_indices)
        )
        text = _gen_temp(
            lm,
            _chat_messages(system, user_msg, history),
            max_new_tokens=max_new_tokens,
            temperature=temperature,
        )
        history.append((user_msg, text))

    cloud = build_point_cloud(hidden_mats, mode="turns_x_layers")
    cloud_pca = pca_reduce(cloud, pca_dims) if cloud.shape[0] >= 2 else cloud
    beta_0, beta_1, backend = compute_betti_with_backend(cloud_pca, metric="cosine")
    d_eff = float(compute_d_eff(cloud_pca)) if cloud_pca.shape[0] >= 2 else 0.0

    # Map controls to cusp coordinates: a = -dose (deeper with RPL), b = T - 0.7
    a = -float(dose)
    b = float(temperature) - 0.7
    delta = float(cusp_bifurcation_set(np.array([a]), np.array([b]))[0])
    inside_cusp = delta < 0  # multiple-equilibria region for a<0

    onset_abs = bool(beta_1 >= beta1_onset)
    return {
        "dose": dose,
        "temperature": temperature,
        "a_cusp": a,
        "b_cusp": b,
        "cusp_delta": delta,
        "inside_cusp_region": bool(inside_cusp),
        "beta_0": beta_0,
        "beta_1": beta_1,
        "d_eff": d_eff,
        "beta1_onset_absolute": onset_abs,
        "beta1_onset": onset_abs,  # overwritten by relative gate in sweep
        "tda_backend": backend,
        "n_points": int(cloud.shape[0]),
    }



def mu_baseline_beta1_by_temp(
    cells: list[dict[str, Any]], *, dose_eps: float = 1e-9
) -> dict[float, float]:
    """temperature -> beta_1 at dose~0 (mu / typicality baseline)."""
    bas: dict[float, float] = {}
    for c in cells:
        if abs(float(c["dose"])) <= dose_eps:
            bas[float(c["temperature"])] = float(c["beta_1"])
    return bas


def apply_relative_onset(
    cells: list[dict[str, Any]],
    *,
    beta1_onset_abs: float = 1.0,
    relative_margin: float = 0.0,
    dose_eps: float = 1e-9,
) -> list[dict[str, Any]]:
    """Onset iff beta_1(dose) > beta_1(dose=0 at same T) + margin; dose=0 never onset.

    Keeps beta1_onset_absolute (legacy beta_1 >= threshold) for comparison.
    Primary flag beta1_onset is the relative gate.
    """
    bas = mu_baseline_beta1_by_temp(cells, dose_eps=dose_eps)
    out: list[dict[str, Any]] = []
    for c in cells:
        cell = dict(c)
        b1 = float(cell["beta_1"])
        t = float(cell["temperature"])
        dose = float(cell["dose"])
        cell["beta1_onset_absolute"] = bool(b1 >= beta1_onset_abs)
        base = bas.get(t)
        if base is None:
            cell["beta_1_mu_baseline"] = None
            cell["lift_beta_1"] = None
            cell["beta1_onset"] = cell["beta1_onset_absolute"]
        else:
            cell["beta_1_mu_baseline"] = float(base)
            cell["lift_beta_1"] = round(b1 - float(base), 6)
            if abs(dose) <= dose_eps:
                cell["beta1_onset"] = False
            else:
                cell["beta1_onset"] = bool(b1 > float(base) + float(relative_margin))
        out.append(cell)
    return out


def _enrichment_from_onset_flag(cells: list[dict[str, Any]], flag_key: str) -> tuple[int, float, float, float]:
    onset_cells = [c for c in cells if c.get(flag_key)]
    inside_onset = sum(1 for c in onset_cells if c["inside_cusp_region"])
    outside_onset = sum(1 for c in onset_cells if not c["inside_cusp_region"])
    n_inside = sum(1 for c in cells if c["inside_cusp_region"])
    n_outside = len(cells) - n_inside
    p_in = inside_onset / max(n_inside, 1)
    p_out = outside_onset / max(n_outside, 1)
    return len(onset_cells), round(p_in, 4), round(p_out, 4), round(p_in - p_out, 4)


def aggregate_cusp_result(
    cells: list[dict[str, Any]],
    doses: list[float],
    temperatures: list[float],
) -> dict[str, Any]:
    """Crossings + enrichment from cells that already have beta1_onset flags."""
    crossings: list[dict[str, Any]] = []
    for temp in temperatures:
        col = sorted([c for c in cells if abs(c["temperature"] - temp) < 1e-9], key=lambda c: c["dose"])
        if not col:
            continue
        doses_arr = np.array([c["dose"] for c in col])
        onset_flags = np.array([1 if c["beta1_onset"] else 0 for c in col])
        eq_counts = np.array([3 if c["inside_cusp_region"] else 1 for c in col])
        beta_cross = detect_bifurcation_crossing(doses_arr, onset_flags)
        cusp_cross = detect_bifurcation_crossing(doses_arr, eq_counts)
        crossings.append(
            {
                "temperature": temp,
                "beta1_onset_indices": beta_cross,
                "cusp_region_indices": cusp_cross,
                "onset_doses": [float(doses_arr[i]) for i in beta_cross],
                "cusp_boundary_doses": [float(doses_arr[i]) for i in cusp_cross],
            }
        )

    n_onset, p_in, p_out, enrichment = _enrichment_from_onset_flag(cells, "beta1_onset")
    n_abs, p_in_abs, p_out_abs, enrich_abs = _enrichment_from_onset_flag(cells, "beta1_onset_absolute")

    agree = 0
    total_rows = 0
    for row in crossings:
        total_rows += 1
        if row["onset_doses"] and row["cusp_boundary_doses"]:
            for od in row["onset_doses"]:
                if any(abs(od - cd) <= 0.35 + 1e-9 for cd in row["cusp_boundary_doses"]):
                    agree += 1
                    break
        elif not row["onset_doses"] and not row["cusp_boundary_doses"]:
            agree += 1

    return {
        "cells": cells,
        "crossings": crossings,
        "n_cells": len(cells),
        "n_onset": n_onset,
        "p_onset_inside_cusp": p_in,
        "p_onset_outside_cusp": p_out,
        "onset_enrichment": enrichment,
        "n_onset_absolute": n_abs,
        "p_onset_inside_cusp_absolute": p_in_abs,
        "p_onset_outside_cusp_absolute": p_out_abs,
        "onset_enrichment_absolute": enrich_abs,
        "onset_definition": "relative_vs_dose0",
        "boundary_agreement_rows": agree,
        "n_temp_rows": total_rows,
        "boundary_agreement_fraction": round(agree / max(total_rows, 1), 4),
        "mean_beta_1": round(float(np.mean([c["beta_1"] for c in cells])), 4),
        "doses": doses,
        "temperatures": temperatures,
        "mu_baseline_beta1_by_temp": {str(k): v for k, v in mu_baseline_beta1_by_temp(cells).items()},
    }


def recompute_cusp_from_cells(
    cells: list[dict[str, Any]],
    *,
    doses: list[float] | None = None,
    temperatures: list[float] | None = None,
    beta1_onset_abs: float = 1.0,
    relative_margin: float = 0.0,
) -> dict[str, Any]:
    """Offline certificate path: re-gate existing cell beta_1 without reloading the LM."""
    cells_r = apply_relative_onset(
        cells, beta1_onset_abs=beta1_onset_abs, relative_margin=relative_margin
    )
    if doses is None:
        doses = sorted({float(c["dose"]) for c in cells_r})
    if temperatures is None:
        temperatures = sorted({float(c["temperature"]) for c in cells_r})
    return aggregate_cusp_result(cells_r, doses, temperatures)


def run_cusp_boundary_sweep(
    lm: LocalLM,
    prompt: str,
    *,
    m0_system: str,
    nd_system: str,
    doses: list[float],
    temperatures: list[float],
    n_turns: int = 3,
    max_new_tokens: int = 48,
    last_n_layers: int = 4,
    pca_dims: int = 8,
    beta1_onset: float = 1.0,
    relative_margin: float = 0.0,
) -> dict[str, Any]:
    """2D grid chimera_dose × temperature → β₁ onset map vs A₃ cusp region."""
    cells: list[dict[str, Any]] = []
    for dose in doses:
        for temp in temperatures:
            logger.info("037 cell dose=%.2f T=%.2f", dose, temp)
            cell = run_dose_temp_cell(
                lm,
                prompt,
                dose=dose,
                temperature=temp,
                m0_system=m0_system,
                nd_system=nd_system,
                n_turns=n_turns,
                max_new_tokens=max_new_tokens,
                last_n_layers=last_n_layers,
                pca_dims=pca_dims,
                beta1_onset=beta1_onset,
            )
            cells.append(cell)

    cells = apply_relative_onset(
        cells, beta1_onset_abs=beta1_onset, relative_margin=relative_margin
    )
    return aggregate_cusp_result(cells, doses, temperatures)



def assign_cusp_certificate(result: dict[str, Any]) -> str:
    enrich = float(result.get("onset_enrichment", 0.0))
    agree = float(result.get("boundary_agreement_fraction", 0.0))
    n_onset = int(result.get("n_onset", 0))

    if enrich > 0.2 and agree >= 0.5 and n_onset >= 2:
        return "CUSP_EVIDENCE"
    if enrich > 0.05 and n_onset >= 1:
        return "CUSP_PILOT"
    if n_onset >= 1:
        return "CUSP_PARTIAL"
    return "NULL"
