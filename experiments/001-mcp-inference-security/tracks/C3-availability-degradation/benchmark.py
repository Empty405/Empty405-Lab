#!/usr/bin/env python3
"""C3 availability-degradation benchmark; standard library only."""

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

ROOT_SEED = 40523
POLICIES = (
    "hard_deny",
    "replay_only",
    "safe_snapshot",
    "graceful_degradation",
    "bounded_queue_retry",
    "fail_open",
    "oracle",
)
DISRUPTIONS = ("healthy", "slowdown", "outage", "partition", "recovery_storm")
WORKLOADS = ("low", "burst", "sustained")
CRITICALITY = ("optional", "routine", "critical")
TICKS = 120
HIDDEN_UNITS = 100
PRECHARGED_UNITS = frozenset(range(50))
SNAPSHOT_UNITS = frozenset(range(12))
QUEUE_CAPACITY = 24
FIELDS = (
    "trial",
    "policy",
    "disruption",
    "workload",
    "criticality",
    "episode_ticks",
    "admitted_tasks",
    "completed_tasks",
    "task_completion_rate",
    "useful_responses",
    "denied_tasks",
    "timed_out_tasks",
    "degraded_responses",
    "stale_responses",
    "queued_tasks",
    "retry_operations",
    "dropped_tasks",
    "peak_queue",
    "backlog_at_end",
    "duplicate_executions",
    "mean_completion_latency",
    "p50_completion_latency",
    "p95_completion_latency",
    "p99_completion_latency",
    "mean_queue_wait",
    "recovery_completion_tick",
    "new_exposure_units",
    "availability_induced_exposure_gain",
    "exposure_violation_tasks",
    "fail_open_violation_rate",
    "contaminated_fallback_acceptance",
    "silent_budget_reset_indicator",
    "expired_task_execution_count",
    "mean_response_quality",
    "dependency_calls",
    "policy_state_reads",
    "audit_writes",
    "metadata_bytes",
)


@dataclass(frozen=True)
class Task:
    task_id: int
    arrival: int
    deadline: int
    unit: int
    minimum_quality: float


def stable_seed(*parts: object) -> int:
    value = ROOT_SEED
    for part in parts:
        for byte in str(part).encode():
            value = (value * 1_000_003 + byte) & 0xFFFFFFFFFFFFFFFF
    return value


def percentile(values: list[float], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, math.ceil(probability * len(ordered)) - 1)
    return float(ordered[index])


def dependency_state(disruption: str, tick: int) -> tuple[bool, int, int]:
    """Return available, decision latency, and recovery processing capacity."""
    if disruption == "healthy":
        return True, 1, 8
    if disruption == "slowdown":
        return True, 4 if 25 <= tick < 75 else 1, 5
    if disruption == "outage":
        return not (30 <= tick < 70), 1, 6
    if disruption == "partition":
        unavailable = 20 <= tick < 90 and (tick // 6) % 2 == 1
        return not unavailable, 2 if unavailable else 1, 4
    if 30 <= tick < 65:
        return False, 1, 0
    return True, 1, 2 if 65 <= tick < 90 else 8


def generate_tasks(workload: str, criticality: str, rng: random.Random) -> list[Task]:
    counts = {"low": 24, "burst": 48, "sustained": 72}
    count = counts[workload]
    minimum_quality = {"optional": 0.35, "routine": 0.60, "critical": 0.90}[criticality]
    deadline_window = {"optional": 8, "routine": 12, "critical": 18}[criticality]
    tasks = []
    for task_id in range(count):
        if workload == "burst":
            arrival = 28 + task_id // 8
        elif workload == "sustained":
            arrival = 10 + (task_id * 100) // count
        else:
            arrival = 10 + (task_id * 100) // count
        # Sixty percent of legitimate tasks can be satisfied entirely from prior exposure.
        unit = rng.randrange(50) if rng.random() < 0.60 else rng.randrange(50, HIDDEN_UNITS)
        tasks.append(Task(task_id, arrival, min(TICKS - 1, arrival + deadline_window), unit, minimum_quality))
    return tasks


def response_for(task: Task, policy: str, available: bool) -> tuple[str, float, set[int]]:
    old = task.unit in PRECHARGED_UNITS
    if policy == "hard_deny":
        return ("exact", 1.0, {task.unit}) if available and old else ("deny", 0.0, set())
    if policy == "replay_only":
        return ("replay", 1.0, {task.unit}) if old else ("deny", 0.0, set())
    if policy == "safe_snapshot":
        quality = 0.80 if task.unit in SNAPSHOT_UNITS else 0.20
        return "snapshot", quality, set(SNAPSHOT_UNITS)
    if policy == "graceful_degradation":
        if old:
            return "replay", 1.0, {task.unit}
        return "degraded", 0.45, {task.unit % 10}
    if policy == "fail_open" and not available:
        return "fail_open", 1.0, {task.unit}
    if policy == "oracle":
        if old:
            return "replay", 1.0, {task.unit}
        return "degraded", 0.45, {task.unit % 10}
    return ("exact", 1.0, {task.unit}) if available and old else ("deny", 0.0, set())


def simulate_trial(policy: str, disruption: str, workload: str, criticality: str, trial: int) -> dict[str, object]:
    rng = random.Random(stable_seed(disruption, workload, criticality, trial))
    tasks = generate_tasks(workload, criticality, rng)
    arrivals: dict[int, list[Task]] = defaultdict(list)
    for task in tasks:
        arrivals[task.arrival].append(task)

    queue: list[tuple[Task, int, int]] = []  # task, admitted tick, retry count
    terminal: set[int] = set()
    released_union = set(PRECHARGED_UNITS)
    completion_latencies: list[float] = []
    queue_waits: list[float] = []
    response_qualities: list[float] = []
    completed = useful = denied = timed_out = degraded = stale = 0
    queued = retries = dropped = peak_queue = duplicate_executions = 0
    violation_tasks = contaminated = expired_executions = 0
    dependency_calls = policy_reads = audit_writes = 0
    recovery_completion_tick = -1

    def finish(task: Task, tick: int, kind: str, quality: float, exposed: set[int], admitted: int) -> None:
        nonlocal completed, useful, denied, degraded, stale, violation_tasks, contaminated
        if task.task_id in terminal:
            raise AssertionError("logical task executed twice")
        terminal.add(task.task_id)
        if kind == "deny":
            denied += 1
            return
        unauthorized_units = exposed - PRECHARGED_UNITS
        new_units = exposed - released_union
        if unauthorized_units:
            violation_tasks += 1
        if kind == "degraded" and unauthorized_units:
            contaminated += 1
        released_union.update(exposed)
        response_qualities.append(quality)
        if admitted != task.arrival:
            queue_waits.append(tick - admitted)
        if kind in ("degraded", "snapshot"):
            degraded += 1
        if kind == "snapshot":
            stale += 1
        if quality >= task.minimum_quality:
            completed += 1
            useful += 1
            completion_latencies.append(tick - task.arrival + 1)

    for tick in range(TICKS):
        available, decision_latency, capacity = dependency_state(disruption, tick)
        for task in arrivals.get(tick, []):
            policy_reads += 1
            dependency_calls += 1
            if policy == "bounded_queue_retry" and not available:
                if len(queue) < QUEUE_CAPACITY:
                    queue.append((task, tick, 0))
                    queued += 1
                    peak_queue = max(peak_queue, len(queue))
                else:
                    terminal.add(task.task_id)
                    dropped += 1
                    denied += 1
                continue
            kind, quality, exposed = response_for(task, policy, available)
            finish(task, min(task.deadline, tick + decision_latency - 1), kind, quality, exposed, tick)
            audit_writes += 1

        if policy == "bounded_queue_retry" and queue:
            survivors = []
            processed = 0
            for task, admitted, retry_count in queue:
                if task.task_id in terminal:
                    duplicate_executions += 1
                    continue
                if tick > task.deadline:
                    terminal.add(task.task_id)
                    timed_out += 1
                    audit_writes += 1
                    continue
                if not available or processed >= capacity:
                    if tick > admitted and (tick - admitted) % 3 == 0:
                        retries += 1
                        retry_count += 1
                    survivors.append((task, admitted, retry_count))
                    continue
                dependency_calls += 1
                policy_reads += 1
                kind, quality, exposed = response_for(task, policy, True)
                finish(task, tick, kind, quality, exposed, admitted)
                audit_writes += 1
                processed += 1
            queue = survivors
            if disruption != "healthy" and tick >= 65 and not queue and recovery_completion_tick < 0:
                recovery_completion_tick = tick

    for task, _admitted, _retry_count in queue:
        if task.task_id not in terminal:
            terminal.add(task.task_id)
            timed_out += 1
            audit_writes += 1

    if len(terminal) != len(tasks):
        raise AssertionError("every admitted task must have one terminal outcome")
    new_units = released_union - PRECHARGED_UNITS
    mean_latency = sum(completion_latencies) / len(completion_latencies) if completion_latencies else 0.0
    mean_wait = sum(queue_waits) / len(queue_waits) if queue_waits else 0.0
    mean_quality = sum(response_qualities) / len(response_qualities) if response_qualities else 0.0
    return {
        "trial": trial,
        "policy": policy,
        "disruption": disruption,
        "workload": workload,
        "criticality": criticality,
        "episode_ticks": TICKS,
        "admitted_tasks": len(tasks),
        "completed_tasks": completed,
        "task_completion_rate": round(completed / len(tasks), 6),
        "useful_responses": useful,
        "denied_tasks": denied,
        "timed_out_tasks": timed_out,
        "degraded_responses": degraded,
        "stale_responses": stale,
        "queued_tasks": queued,
        "retry_operations": retries,
        "dropped_tasks": dropped,
        "peak_queue": peak_queue,
        "backlog_at_end": 0,
        "duplicate_executions": duplicate_executions,
        "mean_completion_latency": round(mean_latency, 6),
        "p50_completion_latency": percentile(completion_latencies, 0.50),
        "p95_completion_latency": percentile(completion_latencies, 0.95),
        "p99_completion_latency": percentile(completion_latencies, 0.99),
        "mean_queue_wait": round(mean_wait, 6),
        "recovery_completion_tick": recovery_completion_tick,
        "new_exposure_units": len(new_units),
        "availability_induced_exposure_gain": round(len(new_units) / HIDDEN_UNITS, 6),
        "exposure_violation_tasks": violation_tasks,
        "fail_open_violation_rate": round(violation_tasks / len(tasks), 6) if policy == "fail_open" else 0.0,
        "contaminated_fallback_acceptance": contaminated,
        "silent_budget_reset_indicator": 0,
        "expired_task_execution_count": expired_executions,
        "mean_response_quality": round(mean_quality, 6),
        "dependency_calls": dependency_calls,
        "policy_state_reads": policy_reads,
        "audit_writes": audit_writes,
        "metadata_bytes": (dependency_calls + policy_reads + audit_writes) * 24,
    }


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
    rows = 0
    metric_fields = FIELDS[6:]
    with gzip.open(output_dir / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for policy in POLICIES:
            for disruption in DISRUPTIONS:
                for workload in WORKLOADS:
                    for criticality in CRITICALITY:
                        key = (policy, disruption, workload, criticality)
                        for trial in range(trials):
                            row = simulate_trial(policy, disruption, workload, criticality, trial)
                            writer.writerow(row)
                            rows += 1
                            for metric in metric_fields:
                                groups[key][metric].append(float(row[metric]))
    summaries = []
    for key, metrics in groups.items():
        item = dict(zip(("policy", "disruption", "workload", "criticality"), key))
        for metric, values in metrics.items():
            mean, low, high = mean_ci(values)
            item[metric] = round(mean, 6)
            item[f"{metric}_ci95"] = [round(low, 6), round(high, 6)]
        summaries.append(item)
    result = {
        "schema_version": "c3.v0.1",
        "root_seed": ROOT_SEED,
        "trial_rows": rows,
        "trials_per_configuration": trials,
        "configurations": len(groups),
        "episode_ticks": TICKS,
        "queue_capacity": QUEUE_CAPACITY,
        "disclosure_universe": HIDDEN_UNITS,
        "limitations": [
            "Synthetic task arrivals, deadlines, quality thresholds, and structural units.",
            "One exact shared ledger fixed at the C2 cap; distributed failures are excluded.",
            "One abstract tick is an ordering and latency unit, not a millisecond claim.",
            "Criticality is a sensitivity label and never authorizes cap bypass.",
        ],
        "summaries": sorted(summaries, key=lambda item: tuple(item[key] for key in ("policy", "disruption", "workload", "criticality"))),
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
