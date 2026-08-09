"""Tests for quantum domain stub."""

import pytest

pytest.importorskip("qutip")

from namm.domains.quantum.state import bell_state_witness, three_qubit_ghz_fidelity


def test_bell_state_witness():
    w = bell_state_witness()
    assert w.n_qubits == 2
    assert w.fidelity > 0.99
    assert w.entanglement_entropy > 0.9
    assert w.status == "COMPUTATIONAL_EVIDENCE"
    assert len(w.witness_hash) == 16


def test_ghz_three_qubit():
    fid = three_qubit_ghz_fidelity()
    assert fid > 0.99
