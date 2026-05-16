# analysis/test_bit_independence.py

# analysis/test_bit_independence.py

import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quantum_hash.hash_core import quantum_hash_function


def test_bit_independence(num_samples=1000):
    """
    Tests whether each output bit is independently and uniformly distributed.
    Each bit should be 1 approximately 50% of the time across many samples.
    """
    # Determine output size dynamically from a test hash
    sample_output = quantum_hash_function(os.urandom(32))
    num_bits = len(sample_output) * 8  # 32 bytes = 256 bits

    bit_counts = np.zeros(num_bits, dtype=int)

    for _ in range(num_samples):
        input_data = os.urandom(32)
        output = quantum_hash_function(input_data)

        for byte_idx, byte in enumerate(output):
            for bit_idx in range(8):
                if byte & (1 << bit_idx):
                    bit_counts[byte_idx * 8 + bit_idx] += 1

    expected = num_samples / 2
    deviations = np.abs(bit_counts - expected)
    avg_deviation = np.mean(deviations)
    max_deviation = np.max(deviations)
    max_bit = np.argmax(deviations)

    print(f"\n[*] Bit independence results over {num_samples} samples ({num_bits} bits tracked):")
    print(f"    Expected count per bit : {expected:.0f} (50%)")
    print(f"    Average deviation      : {avg_deviation:.2f} ({avg_deviation / expected * 100:.1f}%)")
    print(f"    Max deviation          : {max_deviation} at bit {max_bit} ({bit_counts[max_bit] / num_samples * 100:.1f}% ones)")

    if avg_deviation / expected <= 0.05:
        print(" Excellent — all bits are near-uniformly distributed.")
    elif avg_deviation / expected <= 0.10:
        print(" Good — minor bit bias present but acceptable.")
    else:
        print(" Poor — significant bit bias detected.")


if __name__ == "__main__":
    test_bit_independence(num_samples=1000)


'''
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quantum_hash.hash_core import quantum_hash_function

def test_bit_independence(num_samples=200):
    bit_counts = np.zeros(8 * 16, dtype=int)  # 16 bytes * 8 bits

    for _ in range(num_samples):
        input_data = os.urandom(32)
        output = quantum_hash_function(input_data)

        for byte_idx, byte in enumerate(output):
            for bit_idx in range(8):
                if byte & (1 << bit_idx):
                    bit_counts[byte_idx * 8 + bit_idx] += 1

    # Expectation is ~num_samples / 2 for each bit
    deviations = [abs(count - num_samples / 2) for count in bit_counts]
    avg_deviation = np.mean(deviations)
    max_deviation = np.max(deviations)

    print(f"Average deviation from balanced bit (50%): {avg_deviation:.2f}")
    print(f"Max deviation: {max_deviation}")

if __name__ == "__main__":
    test_bit_independence()
'''