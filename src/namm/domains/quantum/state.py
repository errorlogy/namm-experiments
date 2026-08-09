"""Small quantum-system experiments — COMPUTATIONAL_EVIDENCE only."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

MAX_QUBITS = 3


@dataclass(frozen=True)
class BellStateWitness:
    """Witness for standard Bell-state preparation (2 qubits)."""

    fidelity: float
    entanglement_entropy: float
    n_qubits: int
    witness_hash: str
    status: str = "COMPUTATIONAL_EVIDENCE"

    def to_dict(self) -> dict:
        return {
            "fidelity": self.fidelity,
            "entanglement_entropy": self.entanglement_entropy,
            "n_qubits": self.n_qubits,
            "witness_hash": self.witness_hash,
            "status": self.status,
        }


def two_qubit_entanglement_entropy(rho) -> float:
    """Von Neumann entropy of reduced single-qubit state."""
    import numpy as np

    if rho.dims[0] != [2, 2]:
        raise ValueError("expected 2-qubit density matrix")
    rho_a = rho.ptrace(0)
    evals = np.array(rho_a.eigenenergies())
    evals = evals[evals > 1e-12]
    return float(-sum(e * np.log2(e) for e in evals))


def bell_state_witness() -> BellStateWitness:
    """Prepare |Φ+⟩ and measure fidelity + entanglement entropy."""
    import numpy as np
    import qutip as qt

    bell = (
        qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
        + qt.tensor(qt.basis(2, 1), qt.basis(2, 1))
    ).unit()
    rho = bell * bell.dag()
    target = qt.ket2dm(bell)
    fidelity = float((rho * target).tr().real)

    rho_reduced = rho.ptrace(0)
    evals = np.array(rho_reduced.eigenenergies())
    evals = evals[evals > 1e-12]
    entropy = float(-sum(e * np.log2(e) for e in evals))

    payload = f"{fidelity:.8f}:{entropy:.8f}:2"
    witness_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]

    return BellStateWitness(
        fidelity=fidelity,
        entanglement_entropy=entropy,
        n_qubits=2,
        witness_hash=witness_hash,
    )


def three_qubit_ghz_fidelity() -> float:
    """Optional 3-qubit GHZ witness — stays within MAX_QUBITS."""
    import qutip as qt

    ghz = (
        qt.tensor(qt.basis(2, 0), qt.basis(2, 0), qt.basis(2, 0))
        + qt.tensor(qt.basis(2, 1), qt.basis(2, 1), qt.basis(2, 1))
    ).unit()
    rho = ghz * ghz.dag()
    target = qt.ket2dm(ghz)
    return float((rho * target).tr().real)
