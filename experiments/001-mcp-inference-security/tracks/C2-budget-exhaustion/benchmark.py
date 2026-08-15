#!/usr/bin/env python3
"""C2 budget-exhaustion benchmark; standard library only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT_SEED = 40522
POLICIES = ("hard_deny", "replay_only", "coarse_fallback", "safe_snapshot", "bounded_override", "oracle")
WORKLOADS = ("duplicate_only", "new_disjoint", "mixed", "hotspot", "staged_multi_step")
BUDGETS = (0.25, 0.50, 0.75)
CRITICALITY = ("optional", "routine", "critical")
REQUESTS = 48
HIDDEN_UNITS = 100
OVERRIDE_ALLOWANCE = 5
FIELDS = (
    "trial",
    "policy",
    "workload",
    "budget",
    "criticality",
    "requests",
    "pre_exhaustion_units",
    "released_responses",
    "denied_requests",
    "replayed_responses",
    "coarse_responses",
    "snapshot_responses",
    "override_responses",
    "post_cap_new_units",
    "post_cap_exposure_gain",
    "cap_violation_event",
    "first_violating_request",
    "silent_reset_indicator",
    "false_denial_events",
    "safe_reuse_rate",
    "task_progress",
    "task_completed",
    "downgrade_adequacy",
    "override_allowance",
    "override_used",
    "override_replay_accepted",
    "requests_to_terminal",
    "classifier_operations",
    "policy_state_reads",
    "audit_writes",
    "metadata_bytes",
)


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def candidate_requests(workload: str, cap: int, rng: random.Random) -> list[tuple[int, ...]]:
    old = list(range(cap))
    new = list(range(cap, HIDDEN_UNITS))
    rows = []
    for index in range(REQUESTS):
        if workload == "duplicate_only":
            units = (old[index % len(old)],)
        elif workload == "new_disjoint":
            units = (new[index % len(new)],)
        elif workload == "mixed":
            units = (old[index % len(old)], new[index % len(new)])
        elif workload == "hotspot":
            if rng.random() < 0.8:
                units = (old[rng.randrange(min(8, len(old)))],)
            else:
                units = (new[rng.randrange(len(new))],)
        else:
            units = (old[index % len(old)],) if index < REQUESTS // 2 else (new[index % len(new)],)
        rows.append(units)
    return rows


def task_requirements(
    candidates: list[tuple[int, ...]], criticality: str, rng: random.Random
) -> set[int]:
    universe = sorted({unit for response in candidates for unit in response})
    count = {"optional": 4, "routine": 8, "critical": 12}[criticality]
    return set(rng.sample(universe, min(count, len(universe))))


def validate_snapshot(snapshot: set[int], pre_exhaustion: set[int]) -> bool:
    return snapshot <= pre_exhaustion


def simulate_trial(policy: str, workload: str, budget: float, criticality: str, trial: int) -> dict[str, object]:
    rng = random.Random(stable_seed(workload, budget, criticality, trial))
    cap = round(budget * HIDDEN_UNITS)
    pre_exhaustion = set(range(cap))
    candidates = candidate_requests(workload, cap, rng)
    required = task_requirements(candidates, criticality, rng)
    snapshot = set(range(min(8, cap)))
    if not validate_snapshot(snapshot, pre_exhaustion):
        raise AssertionError("safe snapshot contains uncharged units")

    released_union = set(pre_exhaustion)
    exact_progress: set[int] = set()
    coarse_buckets: set[int] = set()
    released = denied = replays = coarse = snapshots = overrides = false_denials = 0
    safe_candidates = 0
    safe_reused = 0
    override_used = 0
    first_violation = -1

    for index, candidate in enumerate(candidates):
        candidate_set = set(candidate)
        entirely_old = candidate_set <= pre_exhaustion
        if entirely_old:
            safe_candidates += 1
        response: set[int] = set()
        response_kind = "deny"

        if policy == "hard_deny":
            pass
        elif policy == "replay_only":
            if entirely_old:
                response = candidate_set
                response_kind = "replay"
        elif policy == "coarse_fallback":
            bucket = candidate[0] // 10
            response = {80 + bucket}
            response_kind = "coarse"
            coarse_buckets.add(bucket)
        elif policy == "safe_snapshot":
            response = set(snapshot)
            response_kind = "snapshot"
        elif policy == "bounded_override":
            old_units = candidate_set & pre_exhaustion
            new_units = sorted(candidate_set - pre_exhaustion)
            available = OVERRIDE_ALLOWANCE - override_used
            allowed_new = set(new_units[:available])
            override_used += len(allowed_new)
            response = old_units | allowed_new
            response_kind = "override" if allowed_new else "replay"
        else:
            response = candidate_set & pre_exhaustion
            response_kind = "replay" if response else "deny"

        if not response:
            denied += 1
            if entirely_old:
                false_denials += 1
            continue

        new_units = response - released_union
        if new_units and first_violation < 0:
            first_violation = index
        released_union.update(response)
        released += 1
        if entirely_old and not (response - pre_exhaustion):
            safe_reused += 1
        if response_kind == "replay":
            replays += 1
        elif response_kind == "coarse":
            coarse += 1
        elif response_kind == "snapshot":
            snapshots += 1
        elif response_kind == "override":
            overrides += 1

        if response_kind == "coarse":
            pass
        else:
            exact_progress.update(response & required)

    satisfied = {
        unit for unit in required if unit in exact_progress or unit // 10 in coarse_buckets
    }
    progress = len(satisfied) / len(required) if required else 1.0
    new_units_count = len(released_union - pre_exhaustion)
    downgrade_adequacy = progress if policy in ("coarse_fallback", "safe_snapshot") else 0.0
    return {
        "trial": trial,
        "policy": policy,
        "workload": workload,
        "budget": budget,
        "criticality": criticality,
        "requests": REQUESTS,
        "pre_exhaustion_units": len(pre_exhaustion),
        "released_responses": released,
        "denied_requests": denied,
        "replayed_responses": replays,
        "coarse_responses": coarse,
        "snapshot_responses": snapshots,
        "override_responses": overrides,
        "post_cap_new_units": new_units_count,
        "post_cap_exposure_gain": round(new_units_count / HIDDEN_UNITS, 6),
        "cap_violation_event": int(new_units_count > 0),
        "first_violating_request": first_violation,
        "silent_reset_indicator": 0,
        "false_denial_events": false_denials,
        "safe_reuse_rate": round(safe_reused / safe_candidates if safe_candidates else 1.0, 6),
        "task_progress": round(progress, 6),
        "task_completed": int(progress == 1.0),
        "downgrade_adequacy": round(downgrade_adequacy, 6),
        "override_allowance": OVERRIDE_ALLOWANCE if policy == "bounded_override" else 0,
        "override_used": override_used if policy == "bounded_override" else 0,
        "override_replay_accepted": 0,
        "requests_to_terminal": REQUESTS,
        "classifier_operations": REQUESTS,
        "policy_state_reads": REQUESTS,
        "audit_writes": REQUESTS,
        "metadata_bytes": REQUESTS * 24,
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
    metric_fields = FIELDS[5:]
    with gzip.open(output_dir / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for policy in POLICIES:
            for workload in WORKLOADS:
                for budget in BUDGETS:
                    for criticality in CRITICALITY:
                        key = (policy, workload, budget, criticality)
                        for trial in range(trials):
                            row = simulate_trial(policy, workload, budget, criticality, trial)
                            writer.writerow(row)
                            rows += 1
                            for metric in metric_fields:
                                groups[key][metric].append(float(row[metric]))

    summaries = []
    for key, metrics in groups.items():
        item = dict(zip(("policy", "workload", "budget", "criticality"), key))
        for metric, values in metrics.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6)
            item[f"{metric}_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)

    result = {
        "schema_version": "c2.v0.1",
        "root_seed": ROOT_SEED,
        "trial_rows": rows,
        "trials_per_configuration": trials,
        "configurations": len(groups),
        "fixed_post_cap_requests": REQUESTS,
        "disclosure_universe": HIDDEN_UNITS,
        "override_allowance": OVERRIDE_ALLOWANCE,
        "limitations": [
            "Synthetic structural response classes and task requirements.",
            "Exact C1 ledger at cap; distributed-accounting failures are excluded.",
            "Coarse outputs use an explicit uncharged structural namespace.",
            "Criticality is a sensitivity label, not authorization or legal priority.",
        ],
        "summaries": sorted(
            summaries,
            key=lambda item: (item["policy"], item["workload"], item["budget"], item["criticality"]),
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
