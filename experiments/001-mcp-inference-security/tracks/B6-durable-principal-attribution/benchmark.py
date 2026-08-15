#!/usr/bin/env python3
"""B6 durable-principal-attribution benchmark; standard library only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT_SEED = 40516
MECHANISMS = ("session", "account", "global_id", "pairwise", "anonymous_credential", "oracle")
LIFECYCLES = ("stable", "token_rotation", "account_rotation", "multi_device", "credential_reissue")
CONDITIONS = ("honest", "credential_transfer", "issuer_collusion", "service_outage")
BUDGETS = (0.25, 0.50, 0.75)
REQUESTS = 80
HIDDEN_UNITS = 100
FIELDS = (
    "trial", "mechanism", "lifecycle", "condition", "budget", "true_principals",
    "attributed_keys", "aggregate_exposure", "excess_exposure", "budget_bypass",
    "false_merge", "false_split", "linked_contexts", "legitimate_utility",
    "denied_requests", "recovery_success", "protocol_bytes", "lookups", "state_writes",
)


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def attribution_keys(mechanism: str, lifecycle: str, condition: str) -> tuple[list[str], int, int]:
    """Return deployable keys only; evaluator truth never enters this function."""
    keys = ["p0", "p0"]
    if mechanism == "session" and lifecycle != "stable":
        keys[1] = "fresh-session"
    elif mechanism == "account" and lifecycle in ("account_rotation", "credential_reissue"):
        keys[1] = "fresh-account"
    elif mechanism == "pairwise" and lifecycle == "credential_reissue":
        keys[1] = "fresh-pairwise"
    elif mechanism == "anonymous_credential" and lifecycle == "credential_reissue":
        keys[1] = "fresh-credential"

    false_merge = 0
    if lifecycle == "multi_device" and mechanism in ("session", "pairwise"):
        keys[1] = "device-2"
    if condition == "credential_transfer" and mechanism in ("account", "global_id", "anonymous_credential"):
        false_merge = 1
    if condition == "issuer_collusion" and mechanism == "pairwise":
        keys[1] = keys[0]
    false_split = int(keys[0] != keys[1])
    return keys, false_merge, false_split


def simulate_trial(mechanism: str, lifecycle: str, condition: str, budget: float, trial: int) -> dict[str, object]:
    rng = random.Random(stable_seed(mechanism, lifecycle, condition, budget, trial))
    keys, false_merge, false_split = attribution_keys(mechanism, lifecycle, condition)
    cap = round(budget * HIDDEN_UNITS)
    ledgers: dict[str, set[int]] = defaultdict(set)
    exposed: set[int] = set()
    denied = 0
    outage = condition == "service_outage" and mechanism in ("global_id", "pairwise", "anonymous_credential")
    recovery_success = int(not outage and not (lifecycle == "credential_reissue" and false_split))

    for request in range(REQUESTS):
        phase = int(request >= REQUESTS // 2)
        key = keys[phase]
        unit = (request + rng.randrange(7)) % HIDDEN_UNITS
        if outage:
            # Restricted bootstrap: retain 10% of the nominal budget per phase.
            key = f"bootstrap-{phase}"
            limit = max(1, round(cap * 0.10))
        else:
            limit = cap
        if unit not in ledgers[key] and len(ledgers[key]) >= limit:
            denied += 1
            continue
        ledgers[key].add(unit)
        exposed.add(unit)

    exposure = len(exposed) / HIDDEN_UNITS
    bypass = int(exposure > budget + 1e-12)
    linked = {
        "session": 1,
        "account": 2,
        "global_id": 4,
        "pairwise": 2 + int(condition == "issuer_collusion"),
        "anonymous_credential": 1,
        "oracle": 0,
    }[mechanism]
    bytes_per_request = {"session": 4, "account": 8, "global_id": 16, "pairwise": 24, "anonymous_credential": 48, "oracle": 0}[mechanism]
    remote = mechanism in ("global_id", "pairwise", "anonymous_credential")
    return {
        "trial": trial, "mechanism": mechanism, "lifecycle": lifecycle, "condition": condition,
        "budget": budget, "true_principals": 2 if condition == "credential_transfer" else 1,
        "attributed_keys": len(ledgers), "aggregate_exposure": round(exposure, 6),
        "excess_exposure": round(max(0.0, exposure - budget), 6), "budget_bypass": bypass,
        "false_merge": false_merge, "false_split": false_split, "linked_contexts": linked,
        "legitimate_utility": round((REQUESTS - denied) / REQUESTS, 6), "denied_requests": denied,
        "recovery_success": recovery_success, "protocol_bytes": REQUESTS * bytes_per_request,
        "lookups": REQUESTS if remote else 0, "state_writes": REQUESTS - denied,
    }


def mean_ci(values: list[float]) -> tuple[float, float, float]:
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, mean, mean
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    half = 1.96 * math.sqrt(variance / len(values))
    return mean, max(0.0, mean - half), min(max(values), mean + half)


def run(trials: int, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    groups: dict[tuple[object, ...], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    rows = 0
    metrics = FIELDS[7:]
    with gzip.open(output_dir / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for mechanism in MECHANISMS:
            for lifecycle in LIFECYCLES:
                for condition in CONDITIONS:
                    for budget in BUDGETS:
                        key = (mechanism, lifecycle, condition, budget)
                        for trial in range(trials):
                            row = simulate_trial(mechanism, lifecycle, condition, budget, trial)
                            writer.writerow(row)
                            rows += 1
                            for metric in metrics:
                                groups[key][metric].append(float(row[metric]))
    summaries = []
    for key, values_by_metric in groups.items():
        item = dict(zip(("mechanism", "lifecycle", "condition", "budget"), key))
        for metric, values in values_by_metric.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6)
            item[f"{metric}_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)
    result = {
        "schema_version": "b6.v0.1", "root_seed": ROOT_SEED, "trial_rows": rows,
        "trials_per_configuration": trials, "configurations": len(groups),
        "unknown_policy": "restricted_bootstrap", "fixed_requests": REQUESTS,
        "limitations": [
            "Synthetic attribution and lifecycle abstractions.",
            "Structural exposure is not semantic reconstruction.",
            "Fixed mixed population; population sensitivity remains follow-up work.",
            "Linkability is an ordinal context count, not a legal privacy assessment.",
        ],
        "summaries": sorted(summaries, key=lambda item: (item["mechanism"], item["lifecycle"], item["condition"], item["budget"])),
    }
    (output_dir / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=300)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    result = run(args.trials, args.output_dir)
    print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")


if __name__ == "__main__":
    main()
