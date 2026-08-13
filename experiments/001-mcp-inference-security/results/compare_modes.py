import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "hidden_state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    hidden = json.load(f)["locations"]


def run_json(script):
    result = subprocess.run(
        ["python", str(script)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def midpoint_from_response(response):
    precision = response["precision"]
    value = response["response"]

    if precision == "exact":
        return float(value)

    if precision == "range":
        low, high = value.split("-")
        return (float(low) + float(high)) / 2

    if precision == "category":
        if value == "low":
            return 16.5
        if value == "medium":
            return 50.0
        if value == "high":
            return 83.5

    return None


def calculate_mae(estimates):
    errors = []

    for location, resources in hidden.items():
        for resource, true_value in resources.items():
            estimate = estimates.get((location, resource))

            if estimate is not None:
                errors.append(abs(true_value - estimate))

    if not errors:
        return None

    return sum(errors) / len(errors)


baseline = run_json(BASE_DIR / "observer" / "evaluate.py")
rate_wait = run_json(BASE_DIR / "observer" / "rate_limit_wait_test.py")
coverage = run_json(BASE_DIR / "observer" / "coverage_test.py")
adaptive = run_json(BASE_DIR / "observer" / "adaptive_test.py")


adaptive_estimates = {}

for obs in adaptive["observations"]:
    estimate = midpoint_from_response(obs)

    adaptive_estimates[
        (obs["location"], obs["resource"])
    ] = estimate


adaptive_mae = calculate_mae(adaptive_estimates)

adaptive_known = sum(
    1 for value in adaptive_estimates.values()
    if value is not None
)

total_cells = sum(
    len(resources)
    for resources in hidden.values()
)


output = {
    "baseline": {
        "mean_absolute_error": baseline["mean_absolute_error"],
        "reconstruction_score": baseline["simple_reconstruction_score"],
        "cells_observed": total_cells,
    },

    "rate_limit_with_waiting": {
        "complete_dataset_collected": rate_wait["complete_dataset_collected"],
        "successful_queries": rate_wait["successful_queries"],
        "elapsed_seconds": rate_wait["elapsed_seconds"],
        "cells_observed": total_cells,
    },

    "coverage_policy": {
        "unique_combinations_exposed": coverage["unique_combinations_exposed"],
        "total_combinations": total_cells,
        "coverage_percent": round(
            coverage["unique_combinations_exposed"] / total_cells * 100,
            2,
        ),
    },

    "adaptive_disclosure": {
        "mean_absolute_error_on_estimable_cells": (
            round(adaptive_mae, 2)
            if adaptive_mae is not None
            else None
        ),
        "estimable_cells": adaptive_known,
        "total_cells": total_cells,
        "estimable_percent": round(
            adaptive_known / total_cells * 100,
            2,
        ),
    },
}

print(json.dumps(output, indent=2))
