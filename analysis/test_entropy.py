# analysis/test_entropy.py

# analysis/test_entropy.py

# analysis/test_entropy.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from quantum_hash.hash_core import quantum_hash_function


def calculate_entropy(byte_sequence: bytes) -> float:
    """
    Calculate Shannon entropy of a byte sequence in bits per byte.
    Max possible value is 8.0 (perfectly uniform over 256 values).
    NOTE: requires many bytes to approach 8.0 — a 32-byte sample is
    statistically capped around 4.9 even for a perfect hash.
    """
    if len(byte_sequence) == 0:
        return 0.0
    _, counts = np.unique(list(byte_sequence), return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log2(probs))
    return entropy


def test_entropy(num_samples=500, input_size=32):
    """
    Two measurement approaches:

    1. Per-sample entropy — averaged across individual 32-byte outputs.
       Statistically capped ~4.9 due to small sample size; not a true
       measure of hash quality on its own.

    2. Pooled entropy — all output bytes concatenated, then measured.
       This is the correct way to assess byte distribution quality.
       A good hash should score >= 7.9 / 8.0 here.
    """
    per_sample_entropies = []
    all_bytes = bytearray()

    print(f"[*] Hashing {num_samples} random inputs...\n")

    for i in range(num_samples):
        random_input = os.urandom(input_size)
        hash_output = quantum_hash_function(random_input)
        per_sample_entropies.append(calculate_entropy(hash_output))
        all_bytes.extend(hash_output)

        if (i + 1) % 100 == 0:
            print(f"    [{i+1}/{num_samples}] samples processed...")

    # --- Per-sample stats ---
    avg = np.mean(per_sample_entropies)
    mn  = np.min(per_sample_entropies)
    mx  = np.max(per_sample_entropies)

    print(f"\n[1] Per-sample Shannon entropy (32 bytes each):")
    print(f"    Average : {avg:.4f} / 8.00 bits per byte")
    print(f"    Min     : {mn:.4f} bits per byte")
    print(f"    Max     : {mx:.4f} bits per byte")
    print(f"    NOTE: A 32-byte sample is statistically capped ~4.9 even")
    print(f"          for a perfect uniform hash. This metric alone is misleading.")

    # --- Pooled stats ---
    pooled_entropy = calculate_entropy(bytes(all_bytes))
    total_bytes = len(all_bytes)

    print(f"\n[2] Pooled entropy ({total_bytes} bytes across all samples):")
    print(f"    Entropy : {pooled_entropy:.4f} / 8.00 bits per byte  ({pooled_entropy / 8.0 * 100:.1f}%)")

    if pooled_entropy >= 7.9:
        print("  Excellent — byte distribution is near-uniform.")
    elif pooled_entropy >= 7.5:
        print("  Good — very minor bias but pragmatically workable.")
    elif pooled_entropy >= 7.0:
        print("  Moderate — noticeable bias, consider improving mixing.")
    else:
        print("  Poor — significant bias in output distribution.")

    # --- Byte frequency histogram check ---
    byte_counts = np.bincount(list(all_bytes), minlength=256)
    expected = total_bytes / 256
    chi_sq = np.sum((byte_counts - expected) ** 2 / expected)
    print(f"\n[3] Chi-squared uniformity test:")
    print(f"    Chi² = {chi_sq:.2f}  (ideal ≈ 255, lower = more uniform)")
    if chi_sq < 300:
        print(" Output bytes are uniformly distributed.")
    elif chi_sq < 500:
        print(" Slight non-uniformity detected.")
    else:
        print(" Significant non-uniformity — hash has byte bias.")


if __name__ == "__main__":
    print("[*] Starting entropy test...")
    test_entropy(num_samples=500)


'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import os
from quantum_hash.hash_core import quantum_hash_function

def calculate_entropy(byte_sequence: bytes) -> float:
    """
    Calculate Shannon entropy of a byte sequence.
    """
    if len(byte_sequence) == 0:
        return 0.0
    _, counts = np.unique(list(byte_sequence), return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log2(probs))
    return entropy

def test_entropy(num_samples=100, input_size=32):
    """
    Tests entropy of quantum hash outputs across many random inputs.
    """
    entropies = []

    for _ in range(num_samples):
        random_input = os.urandom(input_size)
        hash_output = quantum_hash_function(random_input)
        entropy = calculate_entropy(hash_output)
        entropies.append(entropy)

    avg_entropy = np.mean(entropies)
    max_entropy = np.log2(len(hash_output)) * 8  # 256 bits of max entropy
    print(f"\n[*] Average entropy: {avg_entropy:.4f} / {max_entropy:.2f} bits")

if __name__ == "__main__":
    print("[*] Starting entropy test...")
    test_entropy(num_samples=100)
'''