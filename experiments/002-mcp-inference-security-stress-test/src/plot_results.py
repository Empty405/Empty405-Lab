from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
DATA = json.loads((RESULTS / "benchmark-v0.2.json").read_text())

scenario = DATA["identity_scenarios"]["4"]

labels = [
    "Baseline",
    "Rate Limit + Waiting",
    "Hard / Identity",
    "Hard / Shared",
    "Adaptive / Shared",
]
keys = [
    "baseline",
    "rate_limit_with_waiting",
    "hard_coverage_per_identity",
    "hard_coverage_shared_principal",
    "adaptive_disclosure_shared_principal",
]

# Figure 1: information exposure under 4 identities
values = [
    scenario[key]["information_exposure_percent"]["mean"]
    for key in keys
]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(labels, values)
ax.set_title("v0.2 Information Exposure Under Four-Identity Rotation")
ax.set_ylabel("Mean Information Exposure (%)")
ax.set_ylim(0, 100)
ax.tick_params(axis="x", labelrotation=20)

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.2f}%",
        ha="center",
        va="bottom",
    )

fig.tight_layout()
fig.savefig(RESULTS / "figure-v0.2-1-information-exposure.png", dpi=200)
plt.close(fig)

# Figure 2: security-utility trade-off under 4 identities
fig, ax = plt.subplots(figsize=(8, 6))

for label, key in zip(labels, keys):
    utility = scenario[key]["legitimate_task_utility_percent"]["mean"]
    exposure = scenario[key]["information_exposure_percent"]["mean"]
    ax.scatter(utility, exposure, s=90)
    ax.annotate(
        label,
        (utility, exposure),
        xytext=(7, 7),
        textcoords="offset points",
    )

ax.set_title("v0.2 Security–Utility Trade-off Under Four Identities")
ax.set_xlabel("Legitimate Task Utility (%)")
ax.set_ylabel("Information Exposure (%)")
ax.set_xlim(20, 105)
ax.set_ylim(20, 100)
ax.grid(True, alpha=0.25)

fig.tight_layout()
fig.savefig(RESULTS / "figure-v0.2-2-security-utility-tradeoff.png", dpi=200)
plt.close(fig)

# Figure 3: identity rotation bypass
single = DATA["identity_scenarios"]["1"]
four = DATA["identity_scenarios"]["4"]

labels2 = ["1 identity", "4 identities"]
per_identity_values = [
    single["hard_coverage_per_identity"]["information_exposure_percent"]["mean"],
    four["hard_coverage_per_identity"]["information_exposure_percent"]["mean"],
]
shared_values = [
    single["hard_coverage_shared_principal"]["information_exposure_percent"]["mean"],
    four["hard_coverage_shared_principal"]["information_exposure_percent"]["mean"],
]

x = [0, 1]
fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.plot(x, per_identity_values, marker="o", label="Per-identity budget")
ax.plot(x, shared_values, marker="o", label="Shared-principal budget")
ax.set_xticks(x, labels2)
ax.set_ylabel("Mean Information Exposure (%)")
ax.set_ylim(0, 100)
ax.set_title("Identity Rotation Effect on Hard Coverage")
ax.grid(True, alpha=0.25)
ax.legend()

fig.tight_layout()
fig.savefig(RESULTS / "figure-v0.2-3-identity-rotation.png", dpi=200)
plt.close(fig)

print("Saved v0.2 figures.")
