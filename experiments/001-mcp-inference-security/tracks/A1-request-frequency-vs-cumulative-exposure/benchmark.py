#!/usr/bin/env python3
"""A1 benchmark: request frequency versus cumulative exposure."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import random
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path

LOCATIONS = 12
RESOURCES = 8
CELL_COUNT = LOCATIONS * RESOURCES
RATE_REQUESTS = 10
RATE_WINDOW = 60
LIFETIME_QUOTA = CELL_COUNT // 2
COVERAGE_CAP = CELL_COUNT // 2
DEADLINE = 180


@dataclass(frozen=True)
class Query:
    query_id: str
    location: int
    resource: int

    @property
    def key(self) -> str:
        return f"L{self.location}:R{self.resource}"


@dataclass
class RunResult:
    trial: int
    scenario: str
    observer: str
    policy: str
    attempted: int
    released: int
    delayed: int
    denied: int
    unique_exposed: int
    observable_state: float
    reconstruction_score: float
    logical_time: int
    legitimate_utility: float


class Policy:
    name = "base"

    def decide(self, query: Query, now: int) -> tuple[str, int | None]:
        return "release", None


class Baseline(Policy):
    name = "baseline"


class WindowRateLimit(Policy):
    name = "rate_limit"

    def __init__(self, requests: int = RATE_REQUESTS, window: int = RATE_WINDOW):
        self.requests = requests
        self.window = window
        self.window_start = 0
        self.used = 0

    def decide(self, query: Query, now: int) -> tuple[str, int | None]:
        if now >= self.window_start + self.window:
            self.window_start = (now // self.window) * self.window
            self.used = 0
        if self.used >= self.requests:
            return "delay", self.window_start + self.window
        self.used += 1
        return "release", None


class LifetimeQuota(Policy):
    name = "lifetime_quota"

    def __init__(self, quota: int = LIFETIME_QUOTA):
        self.remaining = quota

    def decide(self, query: Query, now: int) -> tuple[str, int | None]:
        if self.remaining <= 0:
            return "deny", None
        self.remaining -= 1
        return "release", None


class CoverageBudget(Policy):
    name = "coverage_budget"

    def __init__(self, cap: int = COVERAGE_CAP):
        self.cap = cap
        self.seen: set[str] = set()

    def decide(self, query: Query, now: int) -> tuple[str, int | None]:
        if query.key in self.seen:
            return "release", None
        if len(self.seen) >= self.cap:
            return "deny", None
        self.seen.add(query.key)
        return "release", None


class Hybrid(CoverageBudget):
    name = "hybrid"

    def __init__(self):
        super().__init__()
        self.rate = WindowRateLimit()

    def decide(self, query: Query, now: int) -> tuple[str, int | None]:
        if query.key not in self.seen and len(self.seen) >= self.cap:
            return "deny", None
        decision, retry = self.rate.decide(query, now)
        if decision != "release":
            return decision, retry
        self.seen.add(query.key)
        return "release", None


POLICIES = (Baseline, WindowRateLimit, LifetimeQuota, CoverageBudget, Hybrid)


def hidden_state(rng: random.Random) -> dict[str, int]:
    return {f"L{l}:R{r}": rng.randint(0, 100) for l in range(LOCATIONS) for r in range(RESOURCES)}


def query_stream(rng: random.Random, scenario: str) -> list[Query]:
    cells = [(l, r) for l in range(LOCATIONS) for r in range(RESOURCES)]
    rng.shuffle(cells)
    if scenario == "duplicate-heavy":
        cells = [cell for cell in cells for _ in range(3)]
    return [Query(f"q-{i:04d}", l, r) for i, (l, r) in enumerate(cells)]


def band(value: int) -> str:
    if value < 34:
        return "low"
    if value < 67:
        return "medium"
    return "high"


MIDPOINT = {"low": 16.5, "medium": 50.0, "high": 83.5}


def reconstruction_score(state: dict[str, int], observations: dict[str, str]) -> float:
    estimates = [MIDPOINT[observations[k]] if k in observations else 50.0 for k in state]
    error = statistics.fmean(abs(est - true) for est, true in zip(estimates, state.values()))
    return max(0.0, 1.0 - error / 100.0)


def evaluate_legitimate_utility(policy_type: type[Policy]) -> float:
    """Run a small independent task workload with a 30-second answer deadline."""
    policy = policy_type()
    task_deadline = 30
    successful = 0
    for i in range(12):
        query = Query(f"legit-{i:02d}", i % LOCATIONS, (i * 3) % RESOURCES)
        decision, retry_at = policy.decide(query, 0)
        if decision == "release":
            successful += 1
        elif decision == "delay" and retry_at is not None and retry_at <= task_deadline:
            successful += 1
    return successful / 12


def execute(trial: int, scenario: str, observer: str, policy_type: type[Policy], seed: int) -> RunResult:
    rng = random.Random(seed)
    state = hidden_state(rng)
    queries = query_stream(rng, scenario)
    policy = policy_type()
    now = attempted = released = delayed = denied = 0
    observations: dict[str, str] = {}

    for query in queries:
        attempted += 1
        decision, retry_at = policy.decide(query, now)
        if decision == "delay":
            delayed += 1
            assert retry_at is not None and retry_at > now
            if observer == "deadline" and retry_at > DEADLINE:
                denied += 1
                continue
            now = retry_at
            decision, _ = policy.decide(query, now)
        if observer == "deadline" and now > DEADLINE:
            denied += 1
            continue
        if decision == "deny":
            denied += 1
            continue
        released += 1
        observations[query.key] = band(state[query.key])

    return RunResult(
        trial=trial,
        scenario=scenario,
        observer=observer,
        policy=policy.name,
        attempted=attempted,
        released=released,
        delayed=delayed,
        denied=denied,
        unique_exposed=len(observations),
        observable_state=len(observations) / CELL_COUNT,
        reconstruction_score=reconstruction_score(state, observations),
        logical_time=now,
        legitimate_utility=evaluate_legitimate_utility(policy_type),
    )


def aggregate(rows: list[RunResult]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[RunResult]] = {}
    for row in rows:
        grouped.setdefault((row.scenario, row.observer, row.policy), []).append(row)
    output = []
    for (scenario, observer, policy), values in sorted(grouped.items()):
        output.append({
            "scenario": scenario,
            "observer": observer,
            "policy": policy,
            "runs": len(values),
            "observable_state_mean": statistics.fmean(v.observable_state for v in values),
            "reconstruction_score_mean": statistics.fmean(v.reconstruction_score for v in values),
            "logical_time_mean": statistics.fmean(v.logical_time for v in values),
            "legitimate_utility_mean": statistics.fmean(v.legitimate_utility for v in values),
            "released_mean": statistics.fmean(v.released for v in values),
            "denied_mean": statistics.fmean(v.denied for v in values),
        })
    return output


def write_results(output: Path, rows: list[RunResult], summary: list[dict[str, object]], runs: int, seed: int) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with gzip.open(output / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    payload = {"version": "A1-v0.1", "runs": runs, "root_seed": seed, "configuration": {
        "cells": CELL_COUNT, "rate_requests": RATE_REQUESTS, "rate_window": RATE_WINDOW,
        "lifetime_quota": LIFETIME_QUOTA, "coverage_cap": COVERAGE_CAP, "deadline": DEADLINE,
    }, "summary": summary}
    (output / "benchmark.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=40501)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results"))
    args = parser.parse_args()
    rows = [execute(trial, scenario, observer, policy, args.seed + trial)
            for trial in range(args.runs)
            for scenario in ("unique", "duplicate-heavy")
            for observer in ("patient", "deadline")
            for policy in POLICIES]
    summary = aggregate(rows)
    write_results(args.output, rows, summary, args.runs, args.seed)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
