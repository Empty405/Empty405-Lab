#!/usr/bin/env python3
"""C1 shared-exposure-accounting benchmark; standard library only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT_SEED = 40521
MECHANISMS = ("independent", "central", "eventual", "hierarchical", "escrow", "oracle")
WORKLOADS = ("disjoint", "duplicate_heavy", "partial_overlap", "hotspot", "adversarial_interleaving")
SYNC = ("healthy", "delayed", "partitioned")
BUDGETS = (0.25, 0.50, 0.75)
REPLICAS = 4
REQUESTS = 96
HIDDEN_UNITS = 100
FIELDS = (
    "trial",
    "mechanism",
    "workload",
    "sync_condition",
    "budget",
    "requests",
    "released_requests",
    "union_units",
    "union_exposure",
    "budget_overrun",
    "overrun_event",
    "first_overrun_request",
    "delayed_detection_exposure",
    "false_charge_events",
    "missed_charge_events",
    "duplicate_suppression",
    "denied_requests",
    "legitimate_utility",
    "stranded_budget_fraction",
    "replica_divergence",
    "conservation_error",
    "budget_multiplication_factor",
    "coordination_messages",
    "metadata_bytes",
    "synchronous_lookups",
    "state_writes",
    "visible_operators",
)


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def request_plan(workload: str, rng: random.Random) -> list[tuple[int, int]]:
    plan = []
    local_counts = [0] * REPLICAS
    for request in range(REQUESTS):
        replica = request % REPLICAS
        local = local_counts[replica]
        local_counts[replica] += 1
        if workload == "disjoint":
            unit = replica * 25 + local
        elif workload == "duplicate_heavy":
            unit = request % 8
        elif workload == "partial_overlap":
            unit = (replica * 12 + local) % 55
        elif workload == "hotspot":
            unit = rng.randrange(10) if rng.random() < 0.8 else 10 + rng.randrange(50)
        else:
            unit = replica * 20 + (local * 7) % 20
        plan.append((replica, unit))
    return plan


def split_authority(cap: int) -> list[int]:
    base, extra = divmod(cap, REPLICAS)
    return [base + int(replica < extra) for replica in range(REPLICAS)]


def accounting_groups(mechanism: str, sync: str) -> list[int]:
    if mechanism in ("central", "oracle"):
        return [0] * REPLICAS
    if mechanism == "independent":
        return list(range(REPLICAS))
    if mechanism == "eventual":
        if sync == "healthy":
            return [0] * REPLICAS
        if sync == "delayed":
            return [0, 0, 1, 1]
        return list(range(REPLICAS))
    if mechanism == "escrow" and sync == "healthy":
        return [0] * REPLICAS
    return list(range(REPLICAS))


def simulate_trial(mechanism: str, workload: str, sync: str, budget: float, trial: int) -> dict[str, object]:
    rng = random.Random(stable_seed(mechanism, workload, sync, budget, trial))
    plan = request_plan(workload, rng)
    cap = round(budget * HIDDEN_UNITS)
    groups = accounting_groups(mechanism, sync)
    ledgers: dict[int, set[int]] = defaultdict(set)
    released_union: set[int] = set()
    released = denied = false_charge = missed_charge = 0
    repeated_attempts = suppressed_duplicates = 0
    first_overrun = -1
    central_unavailable = mechanism == "central" and sync == "partitioned"

    if mechanism in ("hierarchical", "escrow") and not (mechanism == "escrow" and sync == "healthy"):
        local_limits = split_authority(cap)
    else:
        local_limits = [cap] * REPLICAS

    for index, (replica, unit) in enumerate(plan):
        globally_seen = unit in released_union
        if globally_seen:
            repeated_attempts += 1
        if central_unavailable:
            denied += 1
            if globally_seen:
                suppressed_duplicates += 1
            continue

        key = groups[replica]
        ledger = ledgers[key]
        locally_seen = unit in ledger
        if mechanism in ("hierarchical", "escrow") and not (mechanism == "escrow" and sync == "healthy"):
            limit = local_limits[replica]
        else:
            limit = cap

        if not locally_seen and len(ledger) >= limit:
            denied += 1
            if globally_seen:
                suppressed_duplicates += 1
            continue

        if globally_seen and not locally_seen:
            false_charge += 1
        if globally_seen and locally_seen:
            suppressed_duplicates += 1
        if not globally_seen and locally_seen:
            missed_charge += 1
        ledger.add(unit)
        released_union.add(unit)
        released += 1
        if len(released_union) > cap and first_overrun < 0:
            first_overrun = index

    union_units = len(released_union)
    overrun_units = max(0, union_units - cap)
    duplicate_suppression = suppressed_duplicates / repeated_attempts if repeated_attempts else 1.0
    views = [len(ledgers[groups[replica]]) for replica in range(REPLICAS)]
    divergence = (max(views) - min(views)) / HIDDEN_UNITS if views else 0.0

    if mechanism in ("hierarchical", "escrow") and not (mechanism == "escrow" and sync == "healthy"):
        unused = sum(max(0, local_limits[replica] - len(ledgers[replica])) for replica in range(REPLICAS))
        authority = sum(local_limits)
    elif mechanism in ("central", "oracle") or (mechanism == "escrow" and sync == "healthy"):
        unused = max(0, cap - len(ledgers[0]))
        authority = cap
    else:
        unused = sum(max(0, cap - len(ledgers[group])) for group in set(groups))
        authority = cap * len(set(groups))

    if mechanism == "central":
        messages = 0 if central_unavailable else REQUESTS * 2
        lookups = 0 if central_unavailable else REQUESTS
    elif mechanism == "eventual":
        messages = REQUESTS if sync == "healthy" else REQUESTS // 4 if sync == "delayed" else REPLICAS
        lookups = 0
    elif mechanism == "hierarchical":
        messages = REPLICAS * 2
        lookups = 0
    elif mechanism == "escrow":
        messages = REQUESTS if sync == "healthy" else REPLICAS * 3
        lookups = REQUESTS if sync == "healthy" else 0
    else:
        messages = lookups = 0

    visibility = {"independent": 1, "central": 5, "eventual": 4, "hierarchical": 2, "escrow": 2, "oracle": 0}[mechanism]
    return {
        "trial": trial,
        "mechanism": mechanism,
        "workload": workload,
        "sync_condition": sync,
        "budget": budget,
        "requests": REQUESTS,
        "released_requests": released,
        "union_units": union_units,
        "union_exposure": round(union_units / HIDDEN_UNITS, 6),
        "budget_overrun": round(overrun_units / HIDDEN_UNITS, 6),
        "overrun_event": int(overrun_units > 0),
        "first_overrun_request": first_overrun,
        "delayed_detection_exposure": round(overrun_units / HIDDEN_UNITS if mechanism == "eventual" else 0.0, 6),
        "false_charge_events": false_charge,
        "missed_charge_events": missed_charge,
        "duplicate_suppression": round(duplicate_suppression, 6),
        "denied_requests": denied,
        "legitimate_utility": round(released / REQUESTS, 6),
        "stranded_budget_fraction": round(unused / cap if cap else 0.0, 6),
        "replica_divergence": round(divergence, 6),
        "conservation_error": max(0, authority - cap),
        "budget_multiplication_factor": round(authority / cap, 6),
        "coordination_messages": messages,
        "metadata_bytes": messages * 32,
        "synchronous_lookups": lookups,
        "state_writes": released,
        "visible_operators": visibility,
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
    metric_fields = FIELDS[6:]
    with gzip.open(output_dir / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for mechanism in MECHANISMS:
            for workload in WORKLOADS:
                for sync in SYNC:
                    for budget in BUDGETS:
                        key = (mechanism, workload, sync, budget)
                        for trial in range(trials):
                            row = simulate_trial(mechanism, workload, sync, budget, trial)
                            writer.writerow(row)
                            rows += 1
                            for metric in metric_fields:
                                groups[key][metric].append(float(row[metric]))

    summaries = []
    for key, metrics in groups.items():
        item = dict(zip(("mechanism", "workload", "sync_condition", "budget"), key))
        for metric, values in metrics.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6)
            item[f"{metric}_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)

    result = {
        "schema_version": "c1.v0.1",
        "root_seed": ROOT_SEED,
        "trial_rows": rows,
        "trials_per_configuration": trials,
        "configurations": len(groups),
        "replicas": REPLICAS,
        "fixed_requests": REQUESTS,
        "disclosure_universe": HIDDEN_UNITS,
        "limitations": [
            "Synthetic structural disclosures and synchronization schedules.",
            "Fixed four-replica topology and equal initial authority split.",
            "Budget-domain membership is evaluator-provided from B6 scope.",
            "Availability, fairness, malicious consumption, and decay remain C2-C6.",
        ],
        "summaries": sorted(
            summaries,
            key=lambda item: (item["mechanism"], item["workload"], item["sync_condition"], item["budget"]),
        ),
    }
    (output_dir / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    result = run(args.trials, args.output_dir)
    print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")


if __name__ == "__main__":
    main()
