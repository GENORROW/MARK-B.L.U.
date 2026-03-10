

import sys
import os

# Save output next to this script, wherever it lives
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def build_parameterized_circuit(num_qubits: int, num_layers: int = 6):
    qc = QuantumCircuit(num_qubits)
    params = []

    for layer in range(num_layers):
        for i in range(num_qubits):
            theta = Parameter(f"ry_{layer}_{i}")
            qc.ry(theta, i)
            params.append(theta)

        for i in range(num_qubits):
            phi = Parameter(f"rz_{layer}_{i}")
            qc.rz(phi, i)
            params.append(phi)

        for i in range(0, num_qubits - 1, 2):
            qc.cx(i, i + 1)

        for i in range(1, num_qubits - 1, 2):
            qc.cx(i, i + 1)

    return qc, params


# --- Full 16-qubit circuit ---
print("[*] Building full 16-qubit circuit...")
qc_full, _ = build_parameterized_circuit(num_qubits=16, num_layers=6)

fig_full = qc_full.draw(output='mpl', fold=40, style='iqp')
fig_full.set_size_inches(28, 14)
out_full = os.path.join(OUTPUT_DIR, 'circuit_diagram_full.png')
fig_full.savefig(out_full, dpi=150, bbox_inches='tight')
print(f"[✓] Saved: {out_full}")

# --- Compact 4-qubit, 2-layer architecture diagram ---
print("[*] Building compact 4-qubit architecture diagram...")
qc_small, _ = build_parameterized_circuit(num_qubits=4, num_layers=2)

fig_small = qc_small.draw(output='mpl', fold=-1, style='iqp')
fig_small.set_size_inches(18, 5)
out_small = os.path.join(OUTPUT_DIR, 'circuit_diagram_architecture.png')
fig_small.savefig(out_small, dpi=150, bbox_inches='tight')
print(f"[✓] Saved: {out_small}")

print("\n[*] Done.")


'''
from quantum_hash.circuit_builder import build_parameterized_circuit
from quantum_hash.input_encoder import encode_input_to_params

sample_input = b"QuantumHashInputData1234567890!!"

num_qubits = 8  # or infer from the input length if needed
num_layers = 3  # same as in your builder

# Build the parameterized circuit structure
qc, param_list = build_parameterized_circuit(num_qubits, num_layers)

# Encode input to parameter values
param_value_dict = encode_input_to_params(sample_input, param_list)

# Bind actual parameter values
qc = qc.assign_parameters(param_value_dict)

# Visualize
fig = qc.draw(output="mpl")
fig.savefig("visualizations/mark1_quantum_hash_circuit.png", dpi=300, bbox_inches='tight')
print("\n Circuit image saved as mark1_quantum_hash_circuit.png")
'''