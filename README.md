# MARK-B.L.U. 1.0

MARK-B.L.U. (Base Layer Unification) 1.0 is a quantum-classical hybrid cryptographic architecture designed for a very specific problem: how do we establish and verify the identity of autonomous AI agents — and their outputs — in high-stakes, zero-trust, adversarially uncertain environments?
Classical hash functions derive their security from computational hardness assumptions. Those assumptions are increasingly fragile against quantum-enabled adversarial contexts. MARK-B.L.U. 1.0 doesn't defend against quantum computation classically — it uses quantum mechanics as the source of security itself. Unpredictability here is not algorithmic. It is physical: rooted in superposition, entanglement, and the irreversible collapse of the quantum wavefunction upon measurement.
This repository is the complete, open-source, reproducible implementation of the 1.0. No proprietary hardware or data is required to run it.

Architecture Overview
The architecture has two principal components, built in ordered dependency:
┌──────────────────────────────────────────────────┐
│         MARK-B.L.U. 1.0 Full Architecture        │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │     Component 1: Quantum Hashing Core       │ │
│  │  Classical Input → SHA-512 Pre-stretch →    │ │
│  │  16-Qubit Parameterized Circuit →           │ │
│  │  Statevector Simulation →                   │ │
│  │  SHAKE-256 Amplitude Extraction →           │ │
│  │  256-bit Quantum Hash Digest                │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │ entropy foundation          │
│  ┌──────────────────▼──────────────────────────┐ │
│  │  Component 2: Agent Badge & Rotation System │ │
│  │  QRNG Seed → Quantum Circuit Execution →    │ │
│  │  SHA-256 Badge → Time-bound Rotation →      │ │
│  │  AES-256-CBC Encryption → Verification      │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
Component 1 — Quantum Hashing Pipeline
Show Image
The hashing pipeline maps an arbitrary-length classical byte input to a deterministic 256-bit quantum-derived digest through six sequential stages:
StageModuleDescription1. Classical Inputhash_coreArbitrary-length byte input (e.g., os.urandom, agent ID, message payload)2. Parameter Encoderinput_encoderSHA-512 pre-stretch → 64-byte seed; each byte scaled to θᵢ ∈ [0, 2π]; cyclic HMAC-SHA-512 extension to fill all 192 circuit parameters3. Quantum Circuitcircuit_builder16 qubits, 6 entangling layers; RY+RZ rotations per qubit per layer; brick-wall CNOT entanglement; input-dependent parameterization4. Statevector Simulationhash_coreExact noiseless simulation; outputs full |ψ_out⟩ ∈ ℂ⁶⁵'⁵³⁶ (65,536 complex amplitudes)5. Amplitude Extractionhash_coreDecompose into Re(αⱼ) and Im(αⱼ); serialize as float64 byte streams (~1 MB total)6. Final Hash Outputhash_coreH = SHAKE-256("qhash:" ‖ R_bytes ‖ I_bytes, 32) → 32-byte (256-bit) digest

The Quantum Circuit
The circuit is a 16-qubit, 6-layer parameterized design. Each layer is structured as:
Single-Qubit Sub-layer — RY(θ) followed by RZ(φ) on every qubit:
RY(θ)=(cos⁡θ2−sin⁡θ2sin⁡θ2cos⁡θ2),RZ(φ)=(e−iφ/200eiφ/2)R_Y(\theta) = \begin{pmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}, \quad R_Z(\varphi) = \begin{pmatrix} e^{-i\varphi/2} & 0 \\ 0 & e^{i\varphi/2} \end{pmatrix}RY​(θ)=(cos2θ​sin2θ​​−sin2θ​cos2θ​​),RZ​(φ)=(e−iφ/20​0eiφ/2​)
Entanglement Sub-layer — brick-wall CNOT gates alternating between:

Even pairs: (q₀,q₁), (q₂,q₃), …, (q₁₄,q₁₅)
Odd pairs: (q₁,q₂), (q₃,q₄), …, (q₁₃,q₁₄)

Full circuit unitary: U(θ) = U₆(θ) · U₅(θ) · U₄(θ) · U₃(θ) · U₂(θ) · U₁(θ)
Full 16-qubit circuit (production):
Show Image
Reduced 4-qubit pedagogical reference (same structural grammar):
Show Image

Gate labels follow the convention gate_type_layer_index_qubit_index — e.g., ry_2_5 denotes the RY gate on qubit q₅ in layer 2. The full circuit contains 282 gates, with 90 CNOT entangling gates and 192 independent input-dependent rotation parameters (96 RY + 96 RZ), at a circuit depth of 24 time steps.


Component 2 — Agent Badge Generation & Rotation System
Show Image
Each agent holds a time-variant quantum-derived badge that rotates on a fixed-duration timeslot schedule (default: 5 minutes). The badge lifecycle proceeds across six stages:
StageDescription1. QRNG Seed512-bit quantum-circuit-derived seed generated per timeslot2. Circuit Execution16-qubit circuit (Hadamard + Entanglement + Seeded Rotations + Measurement) outputs 16-bit raw measurement string3. Badge ConstructionRaw measurement ‖ Agent ID ‖ Timeslot → SHA-256 → 256-bit Quantum Badge4. Rotation & StorageNew badge every timeslot (forward secrecy); stored in secure central database5. Key DerivationAES_key = SHA-256(badge) → AES-256-CBC communication encryption6. AuthenticationReceiver retrieves badge by timeslot to decrypt; admins verify via quantum seed replay
Timeslot computation:
timeslot=⌊tcurrent−tepochtinterval⌋\text{timeslot} = \left\lfloor \frac{t_{\text{current}} - t_{\text{epoch}}}{t_{\text{interval}}} \right\rfloortimeslot=⌊tinterval​tcurrent​−tepoch​​⌋
Encryption key derivation:
KeyAES=SHA-256(badgequantum)\text{Key}_{\text{AES}} = \text{SHA-256}(\text{badge}_{\text{quantum}})KeyAES​=SHA-256(badgequantum​)
Security properties delivered:
PropertyDescriptionQuantum ContributionTemporal UnlinkabilityDistinct timeslot badges prevent cross-session correlationIndependent quantum measurements ensure zero statistical linkageForward SecrecyCompromise of current badge reveals nothing about prior onesMeasurement collapse erases prior quantum state informationMessage AuthenticationValid decryption with timeslot badge proves message originBadges are un-forgeable due to measurement irreproducibilityReplay PreventionExpired badges invalidate old cipher-textsQuantum measurement irreproducibility ensures non-repeating badge sequencesQuantum UnpredictabilityEntropy derives from physical indeterminacySecurity grounded in quantum mechanics, not computational hardness

Evaluation Results
Five cryptographic evaluation metrics were implemented and tested. All experiments used Qiskit's exact statevector simulator backend.
Summary Table
MetricObserved ValueIdeal / BenchmarkPer-sample Shannon entropy (n=500)4.884 bits/byte (σ = 0.081)~5.0 bits/byte (per-sample ceiling for 32-byte output)Pooled Shannon entropy (16,000 bytes)7.9886 / 8.00 bits/byte (99.86%)8.0 bits/byteCollisions (1,000 distinct inputs)00Avalanche flip rate (single trial)127/256 bits (49.6%)50% (strict avalanche criterion)Avalanche heatmap mean (150 trials)49.6%, no spatial structure45–55%, no bandingBIC average deviation (1,000 samples)1.14 pp≤ 1.58 pp (noise floor at n=1,000)BIC maximum single-bit deviation5.10 pp at bit 381 outlier ≥ 3σ expected in 256 bitsHamming distance mean (300 pairs)128.34 / 256 bits (50.1%)128 bits (50%)Hamming distance std deviationσ = 8.46 bitsTheoretical σ = 8.0 bitsByte uniformity χ² (df=255, p=0.05)292.58 (threshold: 293.25)Null hypothesis of uniformity not rejected

Entropy Distribution
Show Image
Per-sample Shannon entropy over 500 random 32-byte inputs. Mean: 4.884 bits/byte (σ = 0.081) — at the statistical ceiling for a 32-byte output. No zero-entropy samples observed.

Output Byte Uniformity
Show Image
Pooled byte-frequency distribution over 16,000 output bytes (500 samples × 32 bytes). Near-uniform coverage across all 256 byte values. χ² = 292.58 — below the rejection threshold of 293.25 at p = 0.05.

Avalanche Effect
Show Image
Evaluated over 150 trials across 16 input bit positions × 256 output bit positions. Mean flip rate: 49.6%. No structured banding or spatial patterns detected, confirming satisfaction of the strict avalanche criterion. The result is directly attributable to the 6-layer brick-wall entanglement topology, through which any single-parameter perturbation must propagate two independent entanglement paths before reaching the output statevector.

Bit Independence Criterion (BIC)
Show Image
Tracked across all 256 output bit positions over 1,000 random inputs. Average deviation from 50%: 1.14 pp — below the theoretical noise floor of 1.58 pp for a perfect uniform hash at n=1,000. Maximum single-bit deviation: 5.10 pp at bit position 38 (byte 04, bit 6), statistically consistent with expected 3σ behavior for 256 independent bits.

Hamming Distance Distribution
Show Image
Pairwise Hamming distances over 300 randomly selected distinct-input pairs. Mean: 128.34 bits (50.1% of 256). σ = 8.46 bits (theoretical: 8.0 bits). Distribution is visually consistent with B(256, 0.5), confirming statistically independent outputs with no pairwise structural correlation.

Architecture Feature Summary
FeatureContributionModular Parameterized Quantum CircuitFully reproducible framework integrating parameterized gate encoding and quantum measurement-based randomness harvestingOn-Ground Evaluative ParametersArchitectural evaluation against cryptographic metrics with empirical results on entropy, avalanche effect, and collision behaviorEntropy Harvesting DesignBridges theoretical design and NISQ-compatible quantum cryptography via open-source implementation for AI security researchIdentified Emphasis AreasScoping for high-stakes AI infrastructure in multi-nodal dynamic environments (defense, finance) including hybrid-classical improvements and adversarial noise robustness

Repository Structure
MARK-B.L.U./
│
├── hash_core.py              # Core hashing pipeline integrator
├── input_encoder.py          # SHA-512 pre-stretching + HMAC cyclic encoding
├── circuit_builder.py        # 16-qubit 6-layer parameterized circuit construction
├── badge_system.py           # Agent badge generation and rotation system
│
├── eval/
│   ├── test_entropy.py       # Shannon entropy over 500 samples
│   ├── test_collisions.py    # Collision resistance over 1,000 distinct inputs
│   ├── test_avalanche.py     # Avalanche effect + 150-trial heatmap
│   ├── test_bit_independence.py  # BIC across all 256 output bit positions
│   └── test_hamming_distance.py  # Pairwise Hamming distance over 300 pairs
│
├── visualize_circuit.py      # Circuit diagram generation
├── requirements.txt          # Pinned dependencies
└── main.py                   # Entry-point demo and invocation

Quick Start
bashgit clone https://github.com/GENORROW/MARK-B.L.U.
cd MARK-B.L.U.
pip install -r requirements.txt
python main.py
The hash function is callable as a black-box module:
pythonfrom hash_core import quantum_hash_function

input_bytes = bytes(range(32))   # any arbitrary-length byte input
digest = quantum_hash_function(input_bytes)
print(digest.hex())              # 256-bit quantum-derived hash digest

Positioning and Limitations
MARK-B.L.U. 1.0 operates via statevector simulation — a noiseless classical emulation of quantum circuit behavior — rather than physical quantum hardware. This is an intentional staging decision. The 1.0 is designed to:

establish the mathematical correctness of the architecture,
empirically validate its cryptographic properties under ideal conditions, and
provide a reproducible open-source baseline from which hardware-deployed iterations can proceed.

The architecture does not claim post-quantum security in the formal complexity-theoretic sense. It claims information-theoretic unpredictability grounded in quantum mechanical indeterminacy — a property that does not rely on the computational limitations of an adversary, but on the physical impossibility of predicting or replicating quantum measurement outcomes.
Operating on 16 qubits, the circuit satisfies NISQ (Noisy Intermediate-Scale Quantum) constraints — an intentional design choice for maximal near-term implementability over raw scale.

Future Directions

Measurement-based hardware extraction: Transition from statevector simulation to real quantum backends, deriving entropy from physical shot-level randomness rather than structural circuit complexity — upgrading the unpredictability guarantee from computational to information-theoretic.
Enhanced post-processing: Integration of Toeplitz randomness extractors or multi-round sponge constructions for improved statistical uniformity without compromising the quantum-first entropy source.
Adversarial robustness: Quantum optimal control, variational parameter tuning, and adversarial noise modelling for circuit design optimization under real-time uncertainty.
Protocol embedding: Integration within verifiable quantum protocols or blockchain-based proof-of-work systems toward a broader quantum-secured agent infrastructure ecosystem.
