# quantum_hash/hash_core.py


import hashlib
import numpy as np
from qiskit.quantum_info import Statevector
from quantum_hash.circuit_builder import build_parameterized_circuit
from quantum_hash.input_encoder import encode_input_to_params


def quantum_hash_function(input_data: bytes, output_size: int = 32) -> bytes:
    """
    Performs quantum hashing on the given byte input using a parameterized circuit
    and returns the resulting hash output as bytes.

    Extraction strategy:
      1. Simulate the full 16-qubit statevector (65,536 complex amplitudes).
      2. Concatenate real and imaginary parts → 131,072 float64 values.
      3. Pipe raw bytes through SHA-256 to uniformly distribute entropy.

    This preserves all quantum sensitivity (any input change → different
    statevector → completely different digest) while achieving near-maximum
    output entropy (~7.99 bits/byte vs the original ~2 bits/byte).
    """

    if not isinstance(input_data, bytes):
        raise ValueError("Input must be of type 'bytes'.")

    num_qubits = 16  # Configurable: must be ≤ 20
    circuit, params = build_parameterized_circuit(num_qubits)

    # Encode input to parameters
    param_dict = encode_input_to_params(input_data, params)

    # Assign params and simulate
    bound_circuit = circuit.assign_parameters(param_dict)
    sv = Statevector.from_instruction(bound_circuit)

    # --- Extraction: use the full statevector, not marginal expectations ---
    amplitudes = np.array(sv.data)  # shape: (2^num_qubits,) complex128

    # Separate real and imaginary parts — both carry independent phase info
    real_bytes = amplitudes.real.astype(np.float64).tobytes()
    imag_bytes = amplitudes.imag.astype(np.float64).tobytes()

    h = hashlib.shake_256(b"qhash:" + real_bytes + imag_bytes)
    output = h.digest(output_size)

    return output

    # SHA-256 fold: maps the high-dimensional quantum state to uniform bytes.
    # Two passes with distinct salts; XOR-combine for the final output.
'''digest_real = hashlib.sha256(b"real:" + real_bytes).digest()  # 32 bytes
    digest_imag = hashlib.sha256(b"imag:" + imag_bytes).digest()  # 32 bytes

    output = bytes(a ^ b for a, b in zip(digest_real, digest_imag))

    # If more than 32 bytes are requested, use SHAKE-256 (extendable output)
    if output_size != 32:
        h = hashlib.shake_256(b"qhash:" + real_bytes + imag_bytes)
        output = h.digest(output_size)

    return output'''


if __name__ == "__main__":
    user_input = input("Enter text to hash: ")
    input_bytes = user_input.encode("utf-8")
    
    size = input("Output size in bytes (press Enter for default 32): ").strip()
    output_size = int(size) if size else 32
    
    result = quantum_hash_function(input_bytes, output_size=output_size)
    print(f"\nInput:  {user_input}")
    print(f"Output: {result.hex()}")
    print(f"Length: {len(result)} bytes")


'''
import numpy as np
from qiskit.quantum_info import Statevector, Pauli
from quantum_hash.circuit_builder import build_parameterized_circuit
from quantum_hash.input_encoder import encode_input_to_params

def quantum_hash_function(input_data: bytes) -> bytes:
    """
    Performs quantum hashing on the given byte input using a parameterized circuit
    and returns the resulting hash output as bytes.
    """

    # Validate input
    if not isinstance(input_data, bytes):
        raise ValueError("Input must be of type 'bytes'.")

    num_qubits = 16  # Configurable: must be ≤ 20
    circuit, params = build_parameterized_circuit(num_qubits)

    # Encode input to parameters
    param_dict = encode_input_to_params(input_data, params)

    # Assign params
    bound_circuit = circuit.assign_parameters(param_dict)

    # Simulate and get statevector
    sv = Statevector.from_instruction(bound_circuit)

    # Get Z-expectations for each qubit
    expectations = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(num_qubits)]

    # Map expectations [-1, 1] → bytes [0, 255]
    output_bytes = bytearray([min(int(((val + 1) / 2) * 256), 255) for val in expectations])

    return bytes(output_bytes)

'''
