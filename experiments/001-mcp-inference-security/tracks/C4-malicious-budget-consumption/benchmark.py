#!/usr/bin/env python3
"""C4 malicious-budget-consumption benchmark; standard library only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT_SEED = 40524
POLICIES = ("global_fifo", "rate_limit", "reservation", "marginal_cap", "fair_share", "bounded_hybrid", "oracle")
STRATEGIES = ("benign_control", "frequency_flood", "novelty_maximizer", "front_loaded_burn", "adaptive_burn", "camouflage")
INTENSITIES = ("low", "medium", "high")
WORKLOADS = ("steady", "burst", "late_critical")
TICKS = 120
UNIVERSE = 160
INITIAL_EXPOSURE = frozenset(range(40))
CAP = 48
LEGITIMATE_PRINCIPALS = tuple(range(4))
ATTACKER = 4
FIELDS = (
    "trial", "policy", "strategy", "intensity", "workload", "episode_ticks", "requests", "legitimate_requests",
    "attacker_requests", "legitimate_completed", "legitimate_completion_rate", "legitimate_value_completed",
    "legitimate_value_total", "victim_denials", "denial_of_information_rate", "attacker_admitted", "attacker_charged_units",
    "attacker_capture_ratio", "wasted_attacker_units", "wasted_exposure_ratio", "total_charged_units", "remaining_cap",
    "unused_capacity_ratio", "duplicate_charge_count", "denied_response_exposure", "cap_overshoot", "silent_budget_reset",
    "minimum_principal_completion", "jain_legitimate_utility", "oracle_regret", "policy_reads", "ledger_operations",
    "audit_writes", "metadata_bytes",
)
EVENT_FIELDS = (
    "trial", "policy", "strategy", "intensity", "workload", "request_id", "tick", "principal_id", "evaluator_role",
    "task_value", "requested_units", "marginal_cost", "admitted", "replayed", "terminal_outcome", "charged_units",
    "ledger_before", "ledger_after", "remaining_cap", "legitimate_sufficient",
)


@dataclass(frozen=True)
class Request:
    request_id: int
    tick: int
    principal: int
    role: str
    units: frozenset[int]
    value: int


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def generate_legitimate(workload: str, rng: random.Random) -> list[Request]:
    requests = []
    for index in range(48):
        principal = index % 4
        if workload == "steady":
            tick = 8 + index * 2
            value = 2
        elif workload == "burst":
            tick = 35 + index // 4
            value = 2
        else:
            tick = 62 + index // 3
            value = 4 if index >= 24 else 2
        base = 40 + ((principal * 23 + index * 7 + rng.randrange(9)) % 100)
        width = 1 + (index % 3)
        units = frozenset((base + offset) % UNIVERSE for offset in range(width))
        requests.append(Request(index, tick, principal, "legitimate", units, value))
    return requests


def attack_schedule(strategy: str, intensity: str, legitimate: list[Request], rng: random.Random) -> list[Request]:
    count = {"low": 12, "medium": 24, "high": 36}[intensity]
    requests = []
    benign_units = [request.units for request in legitimate]
    for index in range(count):
        if strategy == "front_loaded_burn":
            tick = 1 + index // 3
        elif strategy == "camouflage":
            tick = legitimate[index % len(legitimate)].tick
        else:
            tick = 5 + (index * 103) // max(1, count)
        if strategy == "benign_control":
            units = benign_units[index % len(benign_units)]
        elif strategy == "frequency_flood":
            units = frozenset({40 + (index % 6)})
        elif strategy == "camouflage":
            anchor = 40 + ((index * 11 + rng.randrange(5)) % 110)
            units = frozenset({anchor, (anchor + 1) % UNIVERSE})
        else:
            width = 5 if strategy in ("novelty_maximizer", "front_loaded_burn", "adaptive_burn") else 2
            anchor = 40 + ((index * 17 + rng.randrange(13)) % 115)
            units = frozenset((anchor + offset) % UNIVERSE for offset in range(width))
        requests.append(Request(10_000 + index, tick, ATTACKER, "attacker", units, 0))
    return requests


def jain(values: list[float]) -> float:
    total = sum(values)
    denominator = len(values) * sum(value * value for value in values)
    return (total * total / denominator) if denominator else 0.0


def admission(policy: str, request: Request, cost: int, remaining: int, state: dict[str, object]) -> bool:
    if cost > remaining:
        return False
    charges = state["charges"]
    counts = state["counts"]
    assert isinstance(charges, dict) and isinstance(counts, dict)
    if policy == "global_fifo":
        return True
    if policy == "rate_limit":
        return counts[request.principal] < 18
    if policy == "reservation":
        own_limit = 10 if request.principal in LEGITIMATE_PRINCIPALS else 8
        return charges[request.principal] + cost <= own_limit
    if policy == "marginal_cap":
        return cost <= 3 and charges[request.principal] + cost <= 14
    if policy == "fair_share":
        return charges[request.principal] + cost <= CAP // 5
    if policy == "bounded_hybrid":
        return counts[request.principal] < 20 and cost <= 3 and charges[request.principal] + cost <= 12
    raise AssertionError("oracle handled separately")


def simulate_episode(policy: str, strategy: str, intensity: str, workload: str, trial: int) -> tuple[dict[str, object], list[dict[str, object]]]:
    rng = random.Random(stable_seed(strategy, intensity, workload, trial))
    legitimate = generate_legitimate(workload, rng)
    attacker = attack_schedule(strategy, intensity, legitimate, rng)
    requests = sorted(legitimate + attacker, key=lambda item: (item.tick, item.request_id))
    if policy == "oracle":
        requests = sorted(requests, key=lambda item: (item.role != "legitimate", -item.value, item.tick, item.request_id))
    released = set(INITIAL_EXPOSURE)
    initial_released = set(released)
    state: dict[str, object] = {"charges": defaultdict(int), "counts": defaultdict(int)}
    charges: defaultdict[int, int] = state["charges"]  # type: ignore[assignment]
    counts: defaultdict[int, int] = state["counts"]  # type: ignore[assignment]
    events = []
    legitimate_completed = victim_denials = attacker_admitted = 0
    legitimate_value_completed = attacker_charged = 0
    principal_completed = defaultdict(int)
    attacker_units: set[int] = set()
    duplicate_charge_count = denied_response_exposure = 0
    policy_reads = ledger_operations = audit_writes = 0
    for request in requests:
        before = len(released - initial_released)
        new_units = set(request.units) - released
        cost = len(new_units)
        remaining = CAP - before
        counts[request.principal] += 1
        policy_reads += 1
        admitted = (
            request.role == "legitimate" and cost <= remaining
            if policy == "oracle"
            else admission(policy, request, cost, remaining, state)
        )
        charged = 0
        replayed = admitted and cost == 0
        if admitted:
            charged = cost
            if charged and new_units.issubset(released):
                duplicate_charge_count += charged
            released.update(new_units)
            charges[request.principal] += charged
            ledger_operations += 1
            if request.role == "legitimate":
                legitimate_completed += 1
                legitimate_value_completed += request.value
                principal_completed[request.principal] += 1
            else:
                attacker_admitted += 1
                attacker_charged += charged
                attacker_units.update(new_units)
            outcome = "completed" if request.role == "legitimate" else "admitted"
        else:
            outcome = "denied"
            if request.role == "legitimate":
                victim_denials += 1
        audit_writes += 1
        after = len(released - initial_released)
        if after > CAP:
            raise AssertionError("global exposure cap exceeded")
        events.append({
            "trial": trial, "policy": policy, "strategy": strategy, "intensity": intensity, "workload": workload,
            "request_id": request.request_id, "tick": request.tick, "principal_id": request.principal,
            "evaluator_role": request.role, "task_value": request.value,
            "requested_units": ";".join(str(unit) for unit in sorted(request.units)), "marginal_cost": cost,
            "admitted": int(admitted), "replayed": int(replayed), "terminal_outcome": outcome, "charged_units": charged,
            "ledger_before": before, "ledger_after": after, "remaining_cap": CAP - after,
            "legitimate_sufficient": int(admitted and request.role == "legitimate"),
        })
    total_charged = len(released - initial_released)
    legitimate_needed = set().union(*(request.units for request in legitimate))
    wasted = len(attacker_units - legitimate_needed)
    legitimate_total_value = sum(request.value for request in legitimate)
    utilities = [principal_completed[index] for index in LEGITIMATE_PRINCIPALS]
    completion_rate = legitimate_completed / len(legitimate)
    denial_rate = victim_denials / len(legitimate)
    capture = attacker_charged / total_charged if total_charged else 0.0
    wasted_ratio = wasted / attacker_charged if attacker_charged else 0.0
    row = {
        "trial": trial, "policy": policy, "strategy": strategy, "intensity": intensity, "workload": workload,
        "episode_ticks": TICKS, "requests": len(requests), "legitimate_requests": len(legitimate),
        "attacker_requests": len(attacker), "legitimate_completed": legitimate_completed,
        "legitimate_completion_rate": round(completion_rate, 6), "legitimate_value_completed": legitimate_value_completed,
        "legitimate_value_total": legitimate_total_value, "victim_denials": victim_denials,
        "denial_of_information_rate": round(denial_rate, 6), "attacker_admitted": attacker_admitted,
        "attacker_charged_units": attacker_charged, "attacker_capture_ratio": round(capture, 6),
        "wasted_attacker_units": wasted, "wasted_exposure_ratio": round(wasted_ratio, 6),
        "total_charged_units": total_charged, "remaining_cap": CAP - total_charged,
        "unused_capacity_ratio": round((CAP - total_charged) / CAP, 6), "duplicate_charge_count": duplicate_charge_count,
        "denied_response_exposure": denied_response_exposure, "cap_overshoot": max(0, total_charged - CAP),
        "silent_budget_reset": 0, "minimum_principal_completion": min(utilities),
        "jain_legitimate_utility": round(jain(utilities), 6),
        "oracle_regret": legitimate_total_value - legitimate_value_completed,
        "policy_reads": policy_reads, "ledger_operations": ledger_operations, "audit_writes": audit_writes,
        "metadata_bytes": (policy_reads + ledger_operations + audit_writes) * 24,
    }
    return row, events


def simulate_trial(policy: str, strategy: str, intensity: str, workload: str, trial: int) -> dict[str, object]:
    return simulate_episode(policy, strategy, intensity, workload, trial)[0]


def mean_ci(values: list[float]) -> tuple[float, float, float]:
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, mean, mean
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    half = 1.96 * math.sqrt(variance / len(values))
    return mean, max(0.0, mean - half), mean + half


def run(trials: int, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    groups: dict[tuple[str, ...], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    rows = event_rows = 0
    metric_fields = FIELDS[5:]
    with gzip.open(output_dir / "trials.csv.gz", "wt", newline="", encoding="utf-8") as trial_handle, gzip.open(
        output_dir / "request-events.csv.gz", "wt", newline="", encoding="utf-8"
    ) as event_handle:
        writer = csv.DictWriter(trial_handle, fieldnames=FIELDS)
        event_writer = csv.DictWriter(event_handle, fieldnames=EVENT_FIELDS)
        writer.writeheader(); event_writer.writeheader()
        for policy in POLICIES:
            for strategy in STRATEGIES:
                for intensity in INTENSITIES:
                    for workload in WORKLOADS:
                        key = (policy, strategy, intensity, workload)
                        for trial in range(trials):
                            row, events = simulate_episode(policy, strategy, intensity, workload, trial)
                            writer.writerow(row); event_writer.writerows(events)
                            rows += 1; event_rows += len(events)
                            for metric in metric_fields:
                                groups[key][metric].append(float(row[metric]))
    summaries = []
    for key, metrics in groups.items():
        item = dict(zip(("policy", "strategy", "intensity", "workload"), key))
        for metric, values in metrics.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6); item[f"{metric}_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)
    result = {
        "schema_version": "c4.v0.1", "root_seed": ROOT_SEED, "trial_rows": rows,
        "request_event_rows": event_rows, "trials_per_configuration": trials, "configurations": len(groups),
        "episode_ticks": TICKS, "shared_cap": CAP, "disclosure_universe": UNIVERSE,
        "limitations": [
            "Synthetic structural units, task values, principals, and request schedules.",
            "Exact durable identities and exact marginal exposure accounting are assumed.",
            "One atomic shared ledger; distributed races, Sybils, decay, and semantic observer errors are excluded.",
            "Oracle uses evaluator role and task value and is not deployable.",
        ],
        "summaries": sorted(summaries, key=lambda item: tuple(item[key] for key in ("policy", "strategy", "intensity", "workload"))),
    }
    (output_dir / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args(); result = run(args.trials, args.output_dir)
    print(f"wrote {result['trial_rows']:,} rows across {result['configurations']} configurations")


if __name__ == "__main__":
    main()
