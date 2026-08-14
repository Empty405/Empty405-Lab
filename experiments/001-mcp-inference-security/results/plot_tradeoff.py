import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "benchmark-v0.1.json"
OUTPUT_FILE = BASE_DIR / "figure-2-security-utility-tradeoff.png"

with open(RESULT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

points = [
    (
        "Baseline",
        data["baseline"]["mean_observable_percent"],
        data["baseline"]["mean_reconstruction_score"],
    ),
    (
        "Rate Limit + Waiting",
        data["rate_limit_with_waiting"]["mean_observable_percent"],
        data["rate_limit_with_waiting"]["mean_reconstruction_score"],
    ),
    (
        "Hard Coverage",
        data["hard_coverage_policy"]["mean_observable_percent"],
        data["hard_coverage_policy"]["mean_reconstruction_score"],
    ),
    (
        "Adaptive Disclosure",
        data["adaptive_disclosure"]["mean_observable_percent"],
        data["adaptive_disclosure"]["mean_reconstruction_score"],
    ),
]

fig, ax = plt.subplots(figsize=(8, 6))

for label, observable, reconstruction in points:
    ax.scatter(observable, reconstruction, s=90)

    ax.annotate(
        label,
        (observable, reconstruction),
        xytext=(7, 7),
        textcoords="offset points",
    )

ax.set_title("Security–Utility Trade-off")
ax.set_xlabel("Observable State (%)")
ax.set_ylabel("Reconstruction Score (%)")

ax.set_xlim(45, 105)
ax.set_ylim(45, 100)

ax.grid(True, alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, dpi=200)

print(f"Saved: {OUTPUT_FILE}")
