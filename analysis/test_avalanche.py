# analysis/test_avalanche.py

# analysis/test_avalanche.py

import os
import random
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quantum_hash.hash_core import quantum_hash_function


def count_bit_differences(b1: bytes, b2: bytes) -> int:
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))


def test_avalanche(num_trials=50):
    """
    Runs avalanche test across many trials for statistical reliability.
    Ideal: ~128/256 bits flipped (50%) per single-bit input change.
    """
    diffs = []
    total_bits = None

    print(f"[*] Running {num_trials} avalanche trials...\n")

    for i in range(num_trials):
        input_data = bytearray(os.urandom(32))

        # Flip a single random bit
        byte_index = random.randint(0, 31)
        bit_index = random.randint(0, 7)
        input_data[byte_index] ^= (1 << bit_index)
        output_1 = quantum_hash_function(bytes(input_data))

        # Revert the bit
        input_data[byte_index] ^= (1 << bit_index)
        output_2 = quantum_hash_function(bytes(input_data))

        diff = count_bit_differences(output_1, output_2)
        total_bits = len(output_1) * 8
        diffs.append(diff)

        if (i + 1) % 10 == 0:
            print(f"    [{i+1}/{num_trials}] Running avg: {np.mean(diffs):.1f} / {total_bits} bits flipped")

    avg   = np.mean(diffs)
    mn    = np.min(diffs)
    mx    = np.max(diffs)
    std   = np.std(diffs)
    pct   = avg / total_bits * 100

    print(f"\n[*] Avalanche results over {num_trials} trials:")
    print(f"    Average : {avg:.1f} / {total_bits} bits flipped  ({pct:.1f}%)")
    print(f"    Std dev : {std:.1f} bits")
    print(f"    Min     : {mn} bits  ({mn/total_bits*100:.1f}%)")
    print(f"    Max     : {mx} bits  ({mx/total_bits*100:.1f}%)")
    print(f"    Ideal   : 128 / 256 bits (50.0%)")

    if 45 <= pct <= 55:
        print(f"\n Excellent avalanche effect — near-ideal 50% bit diffusion.")
    elif 40 <= pct <= 60:
        print(f"\n Good avalanche effect — acceptable diffusion.")
    else:
        print(f"\n Weak avalanche effect — output is too correlated with input.")


if __name__ == "__main__":
    test_avalanche(num_trials=50)


'''
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quantum_hash.hash_core import quantum_hash_function

def count_bit_differences(b1: bytes, b2: bytes) -> int:
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))

def test_avalanche():
    input_data = bytearray(os.urandom(32))
    
    # Flip a single bit
    byte_index = random.randint(0, 31)
    bit_index = random.randint(0, 7)
    input_data[byte_index] ^= 1 << bit_index

    output_1 = quantum_hash_function(bytes(input_data))
    input_data[byte_index] ^= 1 << bit_index  # revert bit
    output_2 = quantum_hash_function(bytes(input_data))

    diff = count_bit_differences(output_1, output_2)

    print(f"Avalanche Effect Bit Differences: {diff} / {len(output_1) * 8}")

if __name__ == "__main__":
    test_avalanche()
'''