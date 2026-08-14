import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "benchmark-v0.1.json"
OUTPUT_FILE = BASE_DIR / "figure-1-reconstruction-score.png"

with open(RESULT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

labels = [
    "Baseline",
    "Rate Limit\n+ Waiting",
    "Hard\nCoverage",
    "Adaptive\nDisclosure",
]

scores = [
    data["baseline"]["mean_reconstruction_score"],
    data["rate_limit_with_waiting"]["mean_reconstruction_score"],
    data["hard_coverage_policy"]["mean_reconstruction_score"],
    data["adaptive_disclosure"]["mean_reconstruction_score"],
]

fig, ax = plt.subplots(figsize=(9, 5.5))

bars = ax.bar(labels, scores)

ax.set_title("Reconstruction Score by Defense Mode")
ax.set_ylabel("Mean Reconstruction Score (%)")
ax.set_ylim(0, 100)

for bar, score in zip(bars, scores):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        score + 2,
        f"{score:.2f}%",
        ha="center",
        va="bottom",
    )

fig.tight_layout()
fig.savefig(OUTPUT_FILE, dpi=200)

print(f"Saved: {OUTPUT_FILE}")
