#!/usr/bin/env python3
"""B1 identity-rotation benchmark; Python standard library only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT_SEED = 40511
ROTATIONS = (0, 1, 2, 4, 8, 16)
STRATEGIES = ("per_identity", "per_session", "durable_credential", "deterministic", "probabilistic", "oracle")
BUDGETS = (0.25, 0.50, 0.75)
QUALITIES = ("clean", "noisy", "missing")
HIDDEN_UNITS = 100
REQUESTS = 100

LINK_PROBABILITY = {
    "per_identity": (0.0, 0.0, 0.0),
    "per_session": (0.0, 0.0, 0.0),
    "durable_credential": (0.995, 0.85, 0.50),
    "deterministic": (0.95, 0.72, 0.40),
    "probabilistic": (0.98, 0.84, 0.64),
    "oracle": (1.0, 1.0, 1.0),
}

FALSE_MERGE_PROBABILITY = {
    "per_identity": (0.0, 0.0, 0.0),
    "per_session": (0.0, 0.0, 0.0),
    "durable_credential": (0.005, 0.015, 0.030),
    "deterministic": (0.020, 0.060, 0.100),
    "probabilistic": (0.010, 0.040, 0.080),
    "oracle": (0.0, 0.0, 0.0),
}

FIELDS = [
    "trial", "rotation_count", "strategy", "budget", "signal_quality",
    "exposure", "excess_exposure", "reconstruction", "rotation_amplification",
    "false_split_rate", "false_merge", "legitimate_utility", "attribution_keys",
]


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode("utf-8"):
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def request_partition(rotations: int) -> list[int]:
    identities = rotations + 1
    q, r = divmod(REQUESTS, identities)
    return [q + (index < r) for index in range(identities)]


def simulate_trial(rotations: int, strategy: str, budget: float, quality: str, trial: int) -> dict[str, object]:
    rng = random.Random(stable_seed(rotations, strategy, budget, quality, trial))
    quality_index = QUALITIES.index(quality)
    link_p = LINK_PROBABILITY[strategy][quality_index]

    key_loads = [0]
    false_splits = 0
    for identity_requests in request_partition(rotations):
        if key_loads[0] == 0:
            key_index = 0
        elif rng.random() < link_p:
            key_index = 0
        else:
            key_loads.append(0)
            key_index = len(key_loads) - 1
            false_splits += 1
        key_loads[key_index] += identity_requests

    cap = round(budget * HIDDEN_UNITS)
    exposure_units = sum(min(load, cap) for load in key_loads)
    exposure = min(1.0, exposure_units / HIDDEN_UNITS)
    excess = max(0.0, exposure - budget)
    amplification = exposure / budget

    false_merge = int(rng.random() < FALSE_MERGE_PROBABILITY[strategy][quality_index])
    legitimate_utility = 0.0 if false_merge and key_loads[0] >= cap else 1.0

    return {
        "trial": trial,
        "rotation_count": rotations,
        "strategy": strategy,
        "budget": budget,
        "signal_quality": quality,
        "exposure": round(exposure, 6),
        "excess_exposure": round(excess, 6),
        "reconstruction": round(exposure, 6),
        "rotation_amplification": round(amplification, 6),
        "false_split_rate": round(false_splits / rotations if rotations else 0.0, 6),
        "false_merge": false_merge,
        "legitimate_utility": legitimate_utility,
        "attribution_keys": len(key_loads),
    }


def mean_ci(values: list[float]) -> tuple[float, float, float]:
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, mean, mean
    variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    half = 1.96 * math.sqrt(variance / len(values))
    return mean, max(0.0, mean - half), min(max(values), mean + half)


def run(trials: int, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "trials.csv.gz"
    grouped: dict[tuple, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    rows = 0
    with gzip.open(raw_path, "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for rotations in ROTATIONS:
            for strategy in STRATEGIES:
                for budget in BUDGETS:
                    for quality in QUALITIES:
                        key = (rotations, strategy, budget, quality)
                        for trial in range(trials):
                            row = simulate_trial(rotations, strategy, budget, quality, trial)
                            writer.writerow(row)
                            rows += 1
                            for metric in ("exposure", "excess_exposure", "rotation_amplification", "false_split_rate", "false_merge", "legitimate_utility", "attribution_keys"):
                                grouped[key][metric].append(float(row[metric]))

    summaries = []
    for key, metrics in grouped.items():
        item = dict(zip(("rotation_count", "strategy", "budget", "signal_quality"), key))
        for metric, values in metrics.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6)
            item[metric + "_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)

    result = {
        "schema_version": "b1.v0.1",
        "root_seed": ROOT_SEED,
        "trial_rows": rows,
        "trials_per_configuration": trials,
        "configurations": len(grouped),
        "limitations": [
            "Fixed-cadence rotation only; reactive rotation is not implemented in v0.1.",
            "Attribution probabilities are declared synthetic assumptions, not estimates of real-world identity systems.",
            "Reconstruction equals unique structural exposure in this harness; semantic inference is out of scope.",
        ],
        "summaries": sorted(summaries, key=lambda x: (x["rotation_count"], x["strategy"], x["budget"], x["signal_quality"])),
    }
    (output_dir / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    result = run(args.trials, args.output_dir)
    print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")


if __name__ == "__main__":
    main()
