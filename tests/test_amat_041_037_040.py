# unit smoke for attention H1 / lyapunov / cusp helpers
import numpy as np
import pytest

pytestmark = pytest.mark.amat

from namm.metrics.attention_h1 import assign_h1_certificate, h1_proxy_from_attentions, pairwise_js
from namm.metrics.cusp_boundary import (
    assign_cusp_certificate,
    blend_system,
    apply_relative_onset,
    recompute_cusp_from_cells,
)
from namm.metrics.lyapunov_tda import assign_lyapunov_certificate, lyapunov_from_pair


def test_pairwise_js_identical():
    p = np.array([0.2, 0.3, 0.5])
    assert pairwise_js(p, p) < 1e-9


def test_h1_proxy_positive():
    # divergent heads
    att = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    stats = h1_proxy_from_attentions(att, metric="js")
    assert stats["h1_mean"] > 0


def test_assign_h1_certificate():
    assert assign_h1_certificate({"mean_lift_h1": 0.03, "corr_h1_beta1": 0.7, "lock_gt_mu_h1_fraction": 1.0}) == "H1_EVIDENCE"
    assert assign_h1_certificate({"mean_lift_h1": 0.0, "corr_h1_beta1": 0.0, "lock_gt_mu_h1_fraction": 0.0}) == "NULL"


def test_lyapunov_pair_diverging():
    t = np.arange(10)[:, None]
    a = np.concatenate([t, np.zeros((10, 1))], axis=1)
    b = np.concatenate([t * 1.2, np.zeros((10, 1))], axis=1)
    lam = lyapunov_from_pair(a, b)
    assert lam == lam  # not nan


def test_assign_lyapunov_certificate():
    assert (
        assign_lyapunov_certificate(
            {"mean_lift_lambda1": 0.1, "lock_positive_count": 2, "mu_positive_count": 0, "n_prompts": 2}
        )
        == "CHAOS_EVIDENCE"
    )


def test_blend_system_endpoints():
    assert blend_system("MU", "ND", 0.0) == "MU"
    assert blend_system("MU", "ND", 1.0) == "ND"
    mid = blend_system("MU", "ND", 0.5)
    assert "MU" in mid and "ND" in mid


def test_assign_cusp_certificate():
    assert (
        assign_cusp_certificate(
            {"onset_enrichment": 0.3, "boundary_agreement_fraction": 0.7, "n_onset": 3}
        )
        == "CUSP_EVIDENCE"
    )


def test_relative_onset_dose0_never():
    cells = [
        {"dose": 0.0, "temperature": 0.7, "beta_1": 4.0, "inside_cusp_region": False},
        {"dose": 0.35, "temperature": 0.7, "beta_1": 5.0, "inside_cusp_region": True},
        {"dose": 0.7, "temperature": 0.7, "beta_1": 3.0, "inside_cusp_region": True},
    ]
    out = apply_relative_onset(cells, beta1_onset_abs=1.0, relative_margin=0.0)
    assert out[0]["beta1_onset"] is False
    assert out[0]["beta1_onset_absolute"] is True
    assert out[1]["beta1_onset"] is True
    assert out[2]["beta1_onset"] is False


def test_recompute_enrichment_positive_on_037_pattern():
    cells = [
        {"dose": 0.0, "temperature": 0.3, "beta_1": 4.0, "inside_cusp_region": False},
        {"dose": 0.0, "temperature": 0.7, "beta_1": 4.0, "inside_cusp_region": False},
        {"dose": 0.35, "temperature": 0.3, "beta_1": 5.0, "inside_cusp_region": False},
        {"dose": 0.35, "temperature": 0.7, "beta_1": 5.0, "inside_cusp_region": True},
        {"dose": 1.0, "temperature": 0.7, "beta_1": 5.0, "inside_cusp_region": True},
        {"dose": 1.0, "temperature": 0.3, "beta_1": 4.0, "inside_cusp_region": False},
    ]
    r = recompute_cusp_from_cells(cells)
    assert r["n_onset"] >= 1
    assert all(not (c["dose"] == 0.0 and c["beta1_onset"]) for c in r["cells"])
    assert r["onset_enrichment"] > 0
    assert r["onset_enrichment_absolute"] == 0.0 or r["n_onset_absolute"] == len(cells)
