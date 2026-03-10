import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.circuit import Parameter
from scipy.stats import entropy
from tqdm import tqdm

def build_parameterized_circuit(num_qubits=6, num_layers=3):
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

    qc.measure_all()
    return qc, params

def compute_entropy_from_counts(counts, num_shots):
    probs = np.array([v / num_shots for v in counts.values()])
    return entropy(probs, base=2)

def simulate_entropy_distribution(num_qubits=6, num_layers=3, num_inputs=300, shots=1024):
    simulator = Aer.get_backend("aer_simulator")
    entropy_values = []

    for _ in tqdm(range(num_inputs), desc="Simulating"):
        qc, params = build_parameterized_circuit(num_qubits, num_layers)
        param_values = np.random.uniform(0, 2 * np.pi, len(params))
        bound_qc = qc.bind_parameters({p: v for p, v in zip(params, param_values)})
        transpiled = transpile(bound_qc, simulator)
        qobj = assemble(transpiled, shots=shots)
        result = simulator.run(qobj).result()
        counts = result.get_counts()
        entropy_values.append(compute_entropy_from_counts(counts, shots))

    return entropy_values

# Run simulation
entropy_vals = simulate_entropy_distribution()

# Plot results
plt.figure(figsize=(8, 5))
plt.hist(entropy_vals, bins=30, edgecolor='black', color='skyblue')
plt.xlabel("Shannon Entropy (bits)")
plt.ylabel("Frequency")
plt.title("Entropy Distribution of Mark-1 Quantum Hash Function Outputs")
plt.grid(True)
plt.tight_layout()
plt.show()
