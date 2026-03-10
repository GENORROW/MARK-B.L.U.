# quantum_hash/input_encoder.py

# quantum_hash/input_encoder.py

import hashlib
import math


def encode_input_to_params(input_data: bytes, params: list) -> dict:
    """
    Maps input bytes to circuit parameters, scaled to [0, 2π].

    Improvement over the original:
      - Pre-stretches input through SHA-512 before angle mapping.
      - This decorrelates adjacent bytes (original cyclic mapping let similar
        inputs produce similar angle clusters, weakening the avalanche effect).
      - If more parameters are needed than 64 bytes allow, additional SHA-512
        rounds are generated deterministically using a counter suffix.

    Args:
        input_data (bytes): Input byte array.
        params (list): List of circuit Parameters.

    Returns:
        dict: Mapping of parameters to float values in [0, 2π].
    """
    TWO_PI = 2 * math.pi

    # Generate enough pseudorandom bytes to cover all parameters.
    # SHA-512 → 64 bytes per round; ceil(len(params) / 64) rounds needed.
    num_rounds = math.ceil(len(params) / 64)
    stretched = b"".join(
        hashlib.sha512(input_data + round_idx.to_bytes(2, "big")).digest()
        for round_idx in range(num_rounds)
    )

    param_dict = {}
    for i, param in enumerate(params):
        param_dict[param] = (stretched[i] / 255.0) * TWO_PI

    return param_dict

'''
def encode_input_to_params(input_data: bytes, params: list) -> dict:
    """
    Maps input bytes cyclically to circuit parameters, scaled to [0, 2π].

    Args:
        input_data (bytes): Input byte array.
        params (list): List of circuit Parameters.

    Returns:
        dict: Mapping of parameters to float values.
    """
    param_dict = {}
    for i, param in enumerate(params):
        byte_val = input_data[i % len(input_data)]
        param_dict[param] = (byte_val / 255) * 2 * 3.14159  # 0 to 2π
    return param_dict
'''