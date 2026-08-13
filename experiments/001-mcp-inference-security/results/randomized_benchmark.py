import json
import random
import statistics
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "hidden_state.json"

sys.path.insert(0, str(BASE_DIR / "server"))
sys.path.insert(0, str(BASE_DIR / "policies"))

from adaptive_gateway import AdaptiveGateway
from coverage_policy import CoveragePolicy

RUNS = 1000
RANDOM_SEED = 405

random.seed(RANDOM_SEED)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    hidden = json.load(f)["locations"]

cells = [
    (location, resource)
    for location, resources in hidden.items()
    for resource in resources
]


def baseline_estimate(true_value):
    if true_value < 21:
        available = False
    else:
        available = True

    if true_value < 34:
        level = "low"
    elif true_value < 67:
        level = "medium"
    else:
        level = "high"

    if level == "low":
        low, high = 0, 33
    elif level == "medium":
        low, high = 34, 66
    else:
        low, high = 67, 100

    if available:
        low = max(low, 21)
    else:
        high = min(high, 20)

    return (low + high) / 2


def estimate_adaptive(response):
    precision = response["precision"]
    value = response["response"]

    if precision == "exact":
        return float(value)

    if precision == "range":
        low, high = value.split("-")
        return (float(low) + float(high)) / 2

    if precision == "category":
        mapping = {
            "low": 16.5,
            "medium": 50.0,
            "high": 83.5,
        }
        return mapping[value]

    return None


def normalized_score(true_value, estimate):
    if estimate is None:
        return 0.0

    error = abs(true_value - estimate)

    score = 1.0 - (error / 100.0)

    return max(0.0, score)


baseline_scores = []
rate_limit_scores = []
coverage_scores = []
adaptive_scores = []

baseline_known = []
rate_known = []
coverage_known = []
adaptive_known = []


for _ in range(RUNS):
    order = cells.copy()
    random.shuffle(order)

    # -------------------------
    # BASELINE
    # -------------------------

    scores = []
    known = 0

    for location, resource in order:
        true_value = hidden[location][resource]

        estimate = baseline_estimate(true_value)

        scores.append(
            normalized_score(true_value, estimate)
        )

        known += 1

    baseline_scores.append(statistics.mean(scores))
    baseline_known.append(known / len(cells))


    # -------------------------
    # RATE LIMIT + WAIT
    # -------------------------

    # With enough time, the observer eventually receives
    # all permitted responses, so the informational result
    # is equivalent to baseline.

    rate_limit_scores.append(
        baseline_scores[-1]
    )

    rate_known.append(1.0)


    # -------------------------
    # HARD COVERAGE
    # -------------------------

    policy = CoveragePolicy(
        max_unique_combinations=5
    )

    scores = []
    known = 0

    for location, resource in order:
        decision = policy.check(
            location,
            resource,
        )

        true_value = hidden[location][resource]

        if decision["allowed"]:
            estimate = baseline_estimate(true_value)
            known += 1
        else:
            estimate = None

        scores.append(
            normalized_score(true_value, estimate)
        )

    coverage_scores.append(
        statistics.mean(scores)
    )

    coverage_known.append(
        known / len(cells)
    )


    # -------------------------
    # ADAPTIVE DISCLOSURE
    # -------------------------

    gateway = AdaptiveGateway()

    scores = []
    known = 0

    for location, resource in order:
        true_value = hidden[location][resource]

        response = gateway.query(
            location,
            resource,
        )

        estimate = estimate_adaptive(response)

        if estimate is not None:
            known += 1

        scores.append(
            normalized_score(
                true_value,
                estimate,
            )
        )

    adaptive_scores.append(
        statistics.mean(scores)
    )

    adaptive_known.append(
        known / len(cells)
    )


def summarize(scores, known):
    return {
        "mean_reconstruction_score": round(
            statistics.mean(scores) * 100,
            2,
        ),

        "min_score": round(
            min(scores) * 100,
            2,
        ),

        "max_score": round(
            max(scores) * 100,
            2,
        ),

        "mean_observable_percent": round(
            statistics.mean(known) * 100,
            2,
        ),
    }


output = {
    "runs": RUNS,
    "random_seed": RANDOM_SEED,

    "baseline": summarize(
        baseline_scores,
        baseline_known,
    ),

    "rate_limit_with_waiting": summarize(
        rate_limit_scores,
        rate_known,
    ),

    "hard_coverage_policy": summarize(
        coverage_scores,
        coverage_known,
    ),

    "adaptive_disclosure": summarize(
        adaptive_scores,
        adaptive_known,
    ),

    "metric_notes": {
        "normalized_score": (
            "Each cell receives a score from 0 to 1. "
            "Unknown cells score 0. Known cells lose "
            "one percentage point per absolute error unit."
        ),

        "purpose": (
            "Compare all modes using the same metric "
            "while penalizing hidden or unavailable cells."
        ),
    },
}

print(
    json.dumps(
        output,
        indent=2,
    )
)
