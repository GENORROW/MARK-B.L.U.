"""
visualize_results.py
Generates all evaluation plots for the quantum hash function.
Run from the project root:
    python visualize_results.py

Outputs (saved next to this script):
    1. plot_entropy_distribution.png
    2. plot_avalanche_heatmap.png
    3. plot_byte_frequency.png
    4. plot_hamming_distribution.png
    5. plot_bit_bias_heatmap.png
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Resolve project root whether script is in root or a subfolder (e.g. visualizations/)
_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, ".."))
for _p in (_PROJECT_ROOT, _SCRIPT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from quantum_hash.hash_core import quantum_hash_function

OUTPUT_DIR = _SCRIPT_DIR   # PNGs saved next to this script

# ── Shared style ─────────────────────────────────────────────────────────────
DARK_BG    = "#0f1117"
PANEL_BG   = "#1a1d27"
ACCENT     = "#00d4ff"
ACCENT2    = "#7c3aed"
TEXT_WHITE = "#e8eaf0"
TEXT_GREY  = "#8b8fa8"
GRID_COL   = "#2a2d3a"

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    PANEL_BG,
    "axes.edgecolor":    GRID_COL,
    "axes.labelcolor":   TEXT_WHITE,
    "axes.titlecolor":   TEXT_WHITE,
    "xtick.color":       TEXT_GREY,
    "ytick.color":       TEXT_GREY,
    "grid.color":        GRID_COL,
    "grid.linewidth":    0.6,
    "text.color":        TEXT_WHITE,
    "font.family":       "monospace",
    "axes.titlesize":    14,
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
})

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  [+] Saved: {path}")


# ═════════════════════════════════════════════════════════════════════════════
# 1. ENTROPY DISTRIBUTION HISTOGRAM
# ═════════════════════════════════════════════════════════════════════════════
def plot_entropy_distribution(num_samples=500):
    print(f"\n[1/5] Entropy distribution ({num_samples} samples)...")
    entropies = []
    for i in range(num_samples):
        out = quantum_hash_function(os.urandom(32))
        vals, cnts = np.unique(list(out), return_counts=True)
        p = cnts / cnts.sum()
        entropies.append(-np.sum(p * np.log2(p)))
        if (i + 1) % 100 == 0:
            print(f"    {i+1}/{num_samples}")

    entropies = np.array(entropies)
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.suptitle("Entropy Distribution Across Hash Outputs",
                 fontsize=16, fontweight="bold", color=TEXT_WHITE, y=1.02)

    ax.hist(entropies, bins=30, color=ACCENT, edgecolor=DARK_BG,
            linewidth=0.5, alpha=0.85, label="Per-sample entropy")
    ax.axvline(entropies.mean(), color="#ff6b6b", linewidth=2,
               linestyle="--", label=f"Mean = {entropies.mean():.4f} bits/byte")
    ax.axvline(5.0, color="#ffd166", linewidth=1.5, linestyle=":",
               label="Statistical cap for 32-byte output (~5.0)")

    ax.set_xlabel("Shannon Entropy  (bits per byte)", labelpad=10)
    ax.set_ylabel("Number of Samples", labelpad=10)
    ax.set_xlim(4.3, 5.15)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(fontsize=9, framealpha=0.15, labelcolor=TEXT_WHITE,
              facecolor=PANEL_BG, edgecolor=GRID_COL)

    fig.text(0.5, -0.03,
             f"n={num_samples}   mean={entropies.mean():.4f}   "
             f"std={entropies.std():.4f}   "
             f"min={entropies.min():.4f}   max={entropies.max():.4f}",
             ha="center", fontsize=8.5, color=TEXT_GREY)

    save(fig, "plot_entropy_distribution.png")


# ═════════════════════════════════════════════════════════════════════════════
# 2. AVALANCHE HEATMAP
# ═════════════════════════════════════════════════════════════════════════════
def plot_avalanche_heatmap(num_trials=150):
    print(f"\n[2/5] Avalanche heatmap ({num_trials} trials)...")
    import random
    flip_counts = np.zeros(256, dtype=int)

    for i in range(num_trials):
        inp = bytearray(os.urandom(32))
        bi, bit = random.randint(0, 31), random.randint(0, 7)
        inp[bi] ^= (1 << bit)
        o1 = quantum_hash_function(bytes(inp))
        inp[bi] ^= (1 << bit)
        o2 = quantum_hash_function(bytes(inp))
        for byte_idx, (b1, b2) in enumerate(zip(o1, o2)):
            xor = b1 ^ b2
            for bit_idx in range(8):
                if xor & (1 << bit_idx):
                    flip_counts[byte_idx * 8 + bit_idx] += 1
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{num_trials}")

    flip_pct = flip_counts / num_trials * 100
    grid = flip_pct.reshape(16, 16)

    cmap = LinearSegmentedColormap.from_list(
        "avalanche", ["#1a0533", "#7c3aed", "#00d4ff", "#ffffff"])

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.suptitle("Avalanche Effect — Output Bit Flip Frequency\n"
                 "(single input bit flipped per trial)",
                 fontsize=15, fontweight="bold", color=TEXT_WHITE, y=1.03)

    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=100, aspect="auto")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Flip frequency  (%)", color=TEXT_WHITE, fontsize=10)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_GREY)
    cbar.ax.yaxis.set_tick_params(color=TEXT_GREY)
    cbar.ax.axhline(50, color="#ff6b6b", linewidth=1.5, linestyle="--")

    ax.set_xlabel("Bit column  (0–15 within each row of 16 bits)", labelpad=10)
    ax.set_ylabel("Bit row  (each row covers 16 consecutive output bits)", labelpad=10)
    ax.set_xticks(range(16))
    ax.set_yticks(range(16))
    ax.set_xticklabels([str(i) for i in range(16)])
    ax.set_yticklabels([f"bits {r*16}–{r*16+15}" for r in range(16)], fontsize=8)

    fig.text(0.5, -0.02,
             f"n={num_trials} trials   |   "
             f"mean flip rate = {flip_pct.mean():.1f}%   |   "
             f"ideal = 50%   |   bright = high flip rate",
             ha="center", fontsize=8.5, color=TEXT_GREY)

    save(fig, "plot_avalanche_heatmap.png")


# ═════════════════════════════════════════════════════════════════════════════
# 3. BYTE FREQUENCY BAR CHART
# ═════════════════════════════════════════════════════════════════════════════
def plot_byte_frequency(num_samples=500):
    print(f"\n[3/5] Byte frequency chart ({num_samples} samples)...")
    all_bytes = []
    for i in range(num_samples):
        all_bytes.extend(quantum_hash_function(os.urandom(32)))
        if (i + 1) % 100 == 0:
            print(f"    {i+1}/{num_samples}")

    counts   = np.bincount(all_bytes, minlength=256)
    expected = len(all_bytes) / 256

    fig, ax = plt.subplots(figsize=(14, 5))
    fig.suptitle("Output Byte Value Frequency  (Uniformity Check)",
                 fontsize=16, fontweight="bold", color=TEXT_WHITE, y=1.02)

    ax.bar(range(256), counts, width=1.0, color=ACCENT, alpha=0.7, linewidth=0)
    ax.axhline(expected, color="#ff6b6b", linewidth=2, linestyle="--",
               label=f"Expected (uniform) = {expected:.0f}")
    ax.axhspan(expected * 0.95, expected * 1.05, color="#ffd166",
               alpha=0.08, label="±5% tolerance band")

    ax.set_xlabel("Byte Value  (0 = 0x00,  255 = 0xFF)", labelpad=10)
    ax.set_ylabel("Occurrence Count", labelpad=10)
    ax.set_xlim(-1, 256)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(fontsize=9, framealpha=0.15, labelcolor=TEXT_WHITE,
              facecolor=PANEL_BG, edgecolor=GRID_COL)

    chi_sq = np.sum((counts - expected) ** 2 / expected)
    fig.text(0.5, -0.03,
             f"Total bytes = {len(all_bytes):,}   |   "
             f"Chi² = {chi_sq:.2f}  (ideal ≈ 255, lower = more uniform)   |   "
             f"n = {num_samples} samples",
             ha="center", fontsize=8.5, color=TEXT_GREY)

    save(fig, "plot_byte_frequency.png")


# ═════════════════════════════════════════════════════════════════════════════
# 4. HAMMING DISTANCE DISTRIBUTION
# ═════════════════════════════════════════════════════════════════════════════
def plot_hamming_distribution(num_pairs=300):
    print(f"\n[4/5] Hamming distance distribution ({num_pairs} pairs)...")
    distances = []
    for i in range(num_pairs):
        o1 = quantum_hash_function(os.urandom(32))
        o2 = quantum_hash_function(os.urandom(32))
        distances.append(sum(bin(a ^ b).count("1") for a, b in zip(o1, o2)))
        if (i + 1) % 100 == 0:
            print(f"    {i+1}/{num_pairs}")

    distances = np.array(distances)
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.suptitle("Hamming Distance Between Independent Hash Outputs",
                 fontsize=16, fontweight="bold", color=TEXT_WHITE, y=1.02)

    ax.hist(distances, bins=30, color=ACCENT2, edgecolor=DARK_BG,
            linewidth=0.5, alpha=0.85)
    ax.axvline(128, color="#ffd166", linewidth=2, linestyle="--",
               label="Ideal mean = 128 bits  (50% of 256)")
    ax.axvline(distances.mean(), color="#ff6b6b", linewidth=2, linestyle="-",
               label=f"Observed mean = {distances.mean():.1f} bits")

    ax.set_xlabel("Hamming Distance  (number of differing bits out of 256)", labelpad=10)
    ax.set_ylabel("Number of Pairs", labelpad=10)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(fontsize=9, framealpha=0.15, labelcolor=TEXT_WHITE,
              facecolor=PANEL_BG, edgecolor=GRID_COL)

    fig.text(0.5, -0.03,
             f"n={num_pairs} random pairs   |   "
             f"mean={distances.mean():.2f}   std={distances.std():.2f}   "
             f"min={distances.min()}   max={distances.max()}",
             ha="center", fontsize=8.5, color=TEXT_GREY)

    save(fig, "plot_hamming_distribution.png")


# ═════════════════════════════════════════════════════════════════════════════
# 5. BIT BIAS HEATMAP  (32 bytes × 8 bits)
# ═════════════════════════════════════════════════════════════════════════════
def plot_bit_bias_heatmap(num_samples=1000):
    print(f"\n[5/5] Bit bias heatmap ({num_samples} samples)...")
    bit_counts = np.zeros(256, dtype=int)

    for i in range(num_samples):
        out = quantum_hash_function(os.urandom(32))
        for byte_idx, byte in enumerate(out):
            for bit_idx in range(8):
                if byte & (1 << bit_idx):
                    bit_counts[byte_idx * 8 + bit_idx] += 1
        if (i + 1) % 200 == 0:
            print(f"    {i+1}/{num_samples}")

    deviation = np.abs(bit_counts / num_samples * 100 - 50.0)
    grid = deviation.reshape(32, 8)

    cmap = LinearSegmentedColormap.from_list(
        "bias", ["#0d2137", "#00d4ff", "#ffd166", "#ff4444"])

    fig, ax = plt.subplots(figsize=(9, 13))
    fig.suptitle("Bit Bias Heatmap\nDeviation from 50% per Output Bit Position",
                 fontsize=15, fontweight="bold", color=TEXT_WHITE, y=1.02)

    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=10, aspect="auto")
    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label("Absolute deviation from 50%  (pp)", color=TEXT_WHITE, fontsize=10)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_GREY)
    cbar.ax.yaxis.set_tick_params(color=TEXT_GREY)

    ax.set_xlabel("Bit position within byte\n(0 = LSB / least significant,  7 = MSB / most significant)",
                  labelpad=12)
    ax.set_ylabel("Output byte index  (byte 0 = leftmost output byte)", labelpad=10)
    ax.set_xticks(range(8))
    ax.set_xticklabels([f"bit {i}" for i in range(8)], fontsize=9)
    ax.set_yticks(range(32))
    ax.set_yticklabels([f"byte {i:02d}" for i in range(32)], fontsize=7.5)

    worst_bit = deviation.argmax()
    fig.text(0.5, -0.02,
             f"n={num_samples} samples   |   "
             f"avg deviation = {deviation.mean():.2f}pp   |   "
             f"max deviation = {deviation.max():.2f}pp  (bit {worst_bit})   |   "
             f"blue = unbiased,  red = biased",
             ha="center", fontsize=8.5, color=TEXT_GREY)

    save(fig, "plot_bit_bias_heatmap.png")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  Quantum Hash Evaluation Visualizer")
    print("=" * 60)
    print(f"  Output directory: {OUTPUT_DIR}")

    plot_entropy_distribution(num_samples=500)
    plot_avalanche_heatmap(num_trials=150)
    plot_byte_frequency(num_samples=500)
    plot_hamming_distribution(num_pairs=300)
    plot_bit_bias_heatmap(num_samples=1000)

    print("\n" + "=" * 60)
    print("  All 5 plots saved.")
    print("=" * 60)