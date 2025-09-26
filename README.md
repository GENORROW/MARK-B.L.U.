# MARK-B.L.U. 1.0: Part1: The Hashing Mechanism

## Overview

The MARK-B.L.U. Architecture is quantum encryption framework built using parameterized quantum circuits. It simulates a hash mechanism based on quantum circuit behavior, to safeguard autonomous & AI Infrastructure.

This mechanism demonstrates a first-step implementation that maps classical input data to quantum parameters, extracts measurement-based signatures, and secures agent identity & output communication logs.

## Features

- Parameterized quantum circuit with entangling layers
- Input encoding into continuous quantum gate parameters
- Statevector-based computation
- Tests for entropy, collisions, avalanche effect, and bit independence

## Installation

### Requirements

- Python 3.9+
- Qiskit
- NumPy

### Setup

Clone the repo:

```bash
git clone https://github.com/yourusername/quantum_hash_project.git
cd quantum_hash_project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python main.py
```

This hashes a 32-byte input using the quantum circuit and prints both input and output bytes.

## Hash Quality Analysis

### Entropy Test

- Average Entropy over 100 samples: **\~1.74 to 2.31 bits per byte**
- Maximum possible entropy: **4 bits per byte (32 bytes output)**

### Collision Test

- **0 collisions** found across **1000 randomly generated 32-byte inputs**

### Avalanche Effect

- **Bit Differences:** 72 / 128 (i.e., over **56%** bits flipped on 1-bit input change)

### Bit Independence

- **Average deviation from 50% distribution:** 6.21 bits
- **Maximum deviation:** 23 bits

These results indicate a moderate-to-strong diffusion and randomness profile, suitable for a prototype.

## Project Structure

```
quantum_hash_project/
├── analysis/
│   ├── test_entropy.py
│   ├── test_collisions.py
│   ├── test_avalanche.py
│   └── test_bit_independence.py
├── quantum_hash/
│   ├── circuit_builder.py
│   ├── hash_core.py
│   └── input_encoder.py
├── main.py
└── README.md
```

## Limitations

- Operates on simulated quantum circuits (limited scalability)
- Uses statevector output, which may contain biases
- Fixed number of qubits (16) and layers (3)

---

Feel free to contribute or reach out for collaboration!

=======
# MARK-B.L.U.
>>>>>>> 230c54c6328c41433cd53112e692b687682f0691
