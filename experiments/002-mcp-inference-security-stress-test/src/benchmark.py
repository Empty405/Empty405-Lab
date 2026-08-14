from __future__ import annotations

from pathlib import Path
import json
import math
import random
import statistics
import sys

HERE = Path(__file__).resolve().parent
EXPERIMENT_DIR = HERE.parent
RESULTS_DIR = EXPERIMENT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE))

from model import (
    LOCATIONS,
    RESOURCES,
    TIME_STEPS,
    capacity_band,
    generate_state,
    tool_response,
)
from observer import reconstruct
from policies import (
    AdaptiveSharedPolicy,
    HardCoveragePolicy,
    degrade_response,
    legitimate_utility,
)

RUNS = 1000
RANDOM_SEED = 40502
TOOLS = ["availability", "band", "range", "trend"]
MODES = [
    "baseline",
    "rate_limit_with_waiting",
    "hard_coverage_per_identity",
    "hard_coverage_shared_principal",
    "adaptive_disclosure_shared_principal",
]
IDENTITY_SCENARIOS = [1, 4]


def mode_policy(mode: str, total_cells: int):
    if mode in ("baseline", "rate_limit_with_waiting"):
        return None

    if mode == "hard_coverage_per_identity":
        return HardCoveragePolicy(total_cells, shared_principal=False)

    if mode == "hard_coverage_shared_principal":
        return HardCoveragePolicy(total_cells, shared_principal=True)

    if mode == "adaptive_disclosure_shared_principal":
        return AdaptiveSharedPolicy(total_cells)

    raise ValueError(mode)


def evaluate_mode(state: dict, order: list[tuple], mode: str, identities: int) -> dict:
    policy = mode_policy(mode, len(order))

    exposure = []
    errors = []
    within_five = []
    utility = []
    observable = []

    for index, cell in enumerate(order):
        identity = index % identities

        if policy is None:
            level = "full"
        else:
            level = policy.level(identity, cell)

        if level == "blocked":
            responses = []
        else:
            responses = [
                degrade_response(
                    tool_response(state, cell, tool),
                    level,
                    capacity_band,
                )
                for tool in TOOLS
            ]

        reconstructed = reconstruct(state[cell], responses)

        exposure.append(reconstructed["information_exposure"])
        errors.append(reconstructed["absolute_error"])
        within_five.append(1.0 if reconstructed["within_5"] else 0.0)
        utility.append(legitimate_utility(level))

        observable.append(
            1.0 if any(response["kind"] != "limited" for response in responses) else 0.0
        )

    return {
        "information_exposure_percent": statistics.mean(exposure) * 100,
        "mean_absolute_error": statistics.mean(errors),
        "reconstruction_within_5_percent": statistics.mean(within_five) * 100,
        "legitimate_task_utility_percent": statistics.mean(utility) * 100,
        "observable_state_percent": statistics.mean(observable) * 100,
    }


def summarize(rows: list[dict]) -> dict:
    output = {}

    for metric in rows[0]:
        values = [row[metric] for row in rows]
        mean = statistics.mean(values)
        sd = statistics.stdev(values)
        ci95 = 1.96 * sd / math.sqrt(len(values))

        output[metric] = {
            "mean": round(mean, 3),
            "sd": round(sd, 3),
            "ci95_half_width": round(ci95, 3),
        }

    return output


def main() -> None:
    rng = random.Random(RANDOM_SEED)

    raw = {
        identity_count: {mode: [] for mode in MODES}
        for identity_count in IDENTITY_SCENARIOS
    }

    for _ in range(RUNS):
        state = generate_state(rng)
        order = list(state.keys())
        rng.shuffle(order)

        for identity_count in IDENTITY_SCENARIOS:
            for mode in MODES:
                raw[identity_count][mode].append(
                    evaluate_mode(state, order, mode, identity_count)
                )

    output = {
        "experiment": "MCP Inference Security v0.2 stress test",
        "runs": RUNS,
        "random_seed": RANDOM_SEED,
        "state": {
            "locations": LOCATIONS,
            "resources": RESOURCES,
            "time_steps": TIME_STEPS,
            "cells_per_run": LOCATIONS * RESOURCES * TIME_STEPS,
        },
        "identity_scenarios": {},
        "metric_notes": {
            "information_exposure_percent": (
                "Project-specific interval-narrowing metric. "
                "0 means the full 0-100 domain remains feasible; "
                "higher values mean released projections narrow the feasible interval."
            ),
            "legitimate_task_utility_percent": (
                "Project-specific weighted proxy: availability 50%, band 30%, trend 20%."
            ),
            "reconstruction_within_5_percent": (
                "Percentage of hidden cells whose reconstructed midpoint is within ±5 units."
            ),
        },
    }

    for identity_count in IDENTITY_SCENARIOS:
        output["identity_scenarios"][str(identity_count)] = {
            mode: summarize(raw[identity_count][mode])
            for mode in MODES
        }

    output_file = RESULTS_DIR / "benchmark-v0.2.json"
    output_file.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(json.dumps(output, indent=2))
    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()
