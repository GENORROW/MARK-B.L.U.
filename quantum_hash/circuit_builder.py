# quantum_hash/circuit_builder.py

# quantum_hash/circuit_builder.py

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from typing import List, Tuple


def build_parameterized_circuit(num_qubits: int, num_layers: int = 6) -> Tuple[QuantumCircuit, List[Parameter]]:
    """
    Builds a layered parameterized quantum circuit with strong entanglement.

    Improvements over the original:
      - Increased default layers from 3 → 6 for deeper mixing.
      - Replaced single linear CX chain with a two-pass brick-wall pattern:
          Pass 1: even pairs  (0,1), (2,3), (4,5), ...
          Pass 2: odd pairs   (1,2), (3,4), (5,6), ...
        This ensures every qubit is entangled with both its neighbours each
        layer, eliminating the isolated qubits that caused bit-position bias.
      - Added RZ rotation after entanglement per layer for extra phase mixing.

    Args:
        num_qubits (int): Number of qubits. Must be <= 20.
        num_layers (int): Number of circuit layers. Default 6.

    Returns:
        qc (QuantumCircuit): The parameterized quantum circuit.
        params (List[Parameter]): Ordered list of all circuit parameters.
    """
    qc = QuantumCircuit(num_qubits)
    params = []

    for layer in range(num_layers):

        # --- RY rotation layer ---
        for i in range(num_qubits):
            theta = Parameter(f"ry_{layer}_{i}")
            qc.ry(theta, i)
            params.append(theta)

        # --- RZ rotation layer ---
        for i in range(num_qubits):
            phi = Parameter(f"rz_{layer}_{i}")
            qc.rz(phi, i)
            params.append(phi)

        # --- Brick-wall entanglement: even pairs ---
        for i in range(0, num_qubits - 1, 2):
            qc.cx(i, i + 1)

        # --- Brick-wall entanglement: odd pairs ---
        for i in range(1, num_qubits - 1, 2):
            qc.cx(i, i + 1)

    return qc, params

'''
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from typing import List, Tuple

def build_parameterized_circuit(num_qubits: int, num_layers: int = 3) -> Tuple[QuantumCircuit, List[Parameter]]:
    """
    Builds a layered parameterized quantum circuit with entanglement.

    Returns:
        qc (QuantumCircuit): The quantum circuit.
        params (List[Parameter]): List of parameters.
    """
    qc = QuantumCircuit(num_qubits)
    params = []

    for layer in range(num_layers):
        for i in range(num_qubits):
            theta = Parameter(f"theta_ry_{layer}_{i}")
            qc.ry(theta, i)
            params.append(theta)

        for i in range(num_qubits):
            phi = Parameter(f"theta_rz_{layer}_{i}")
            qc.rz(phi, i)
            params.append(phi)

        for i in range(num_qubits):
            qc.cx(i, (i + 1) % num_qubits)

    return qc, params
'''