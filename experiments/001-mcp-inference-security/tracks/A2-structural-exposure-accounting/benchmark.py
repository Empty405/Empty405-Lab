#!/usr/bin/env python3
"""A2 benchmark for schema-derived structural exposure accounting."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path

LOCATIONS, RESOURCES, EPOCHS = 12, 8, 3
TOTAL_CELLS = LOCATIONS * RESOURCES * EPOCHS
TOTAL_TUPLES = TOTAL_CELLS + LOCATIONS * EPOCHS  # single-cell plus regional-summary argument shapes
CHECKPOINTS = (0.05, 0.10, 0.25, 0.50, 0.75, 1.00)
PRECISION = {"availability": 0.50, "capacity_band": 0.66, "numeric_range": 0.90,
             "regional_summary": 0.25, "band_alias": 0.66}


def key(e: int, l: int, r: int) -> str:
    return f"E{e}:L{l}:R{r}"


@dataclass(frozen=True)
class Event:
    tool: str
    epoch: int
    location: int
    resource: int | None
    affected: tuple[str, ...]

    @property
    def tuple_key(self) -> tuple[object, ...]:
        return self.epoch, self.location, self.resource


@dataclass
class Row:
    trial: int
    stream: str
    checkpoint: float
    request_fraction: float
    tuple_coverage: float
    cell_coverage: float
    marginal_coverage: float
    weighted_coverage: float
    reference_exposure: float
    reconstruction_score: float


def state(rng: random.Random) -> dict[str, int]:
    return {key(e, l, r): rng.randint(0, 100) for e in range(EPOCHS)
            for l in range(LOCATIONS) for r in range(RESOURCES)}


def single(tool: str, e: int, l: int, r: int) -> Event:
    return Event(tool, e, l, r, (key(e, l, r),))


def make_stream(name: str, rng: random.Random) -> list[Event]:
    cells = [(e, l, r) for e in range(EPOCHS) for l in range(LOCATIONS) for r in range(RESOURCES)]
    rng.shuffle(cells)
    if name == "unique":
        return [single("numeric_range", *c) for c in cells]
    if name == "duplicate-heavy":
        return [single("capacity_band", *c) for c in cells for _ in range(3)]
    if name == "precision-escalation":
        return [single(tool, *c) for c in cells for tool in ("availability", "capacity_band", "numeric_range")]
    if name == "marginal-scan":
        chosen = [(e, l, r) for e in range(EPOCHS) for l in range(LOCATIONS) for r in range(2)]
        rng.shuffle(chosen)
        return [single("capacity_band", *c) for c in chosen]
    if name == "multi-cell-summary":
        items = [(e, l) for e in range(EPOCHS) for l in range(LOCATIONS)]
        rng.shuffle(items)
        return [Event("regional_summary", e, l, None,
                      tuple(key(e, l, r) for r in range(RESOURCES))) for e, l in items]
    if name == "mixed":
        tools = ("availability", "capacity_band", "numeric_range", "band_alias")
        events = [single(rng.choice(tools), *c) for c in cells]
        events += [Event("regional_summary", e, l, None,
                         tuple(key(e, l, r) for r in range(RESOURCES)))
                   for e in range(EPOCHS) for l in range(LOCATIONS)]
        rng.shuffle(events)
        return events
    raise ValueError(name)


def constraint(tool: str, value: int) -> tuple[int, int]:
    if tool == "availability":
        return (50, 100) if value >= 50 else (0, 49)
    if tool in ("capacity_band", "band_alias"):
        return (0, 33) if value < 34 else ((34, 66) if value < 67 else (67, 100))
    if tool == "numeric_range":
        lower = (value // 10) * 10
        return lower, min(100, lower + 9)
    if tool == "regional_summary":
        return (0, 24) if value < 25 else (25, 100)
    raise ValueError(tool)


class Ledgers:
    def __init__(self):
        self.requests = 0
        self.tuples: set[tuple[object, ...]] = set()
        self.cells: set[str] = set()
        self.locations: set[int] = set()
        self.resources: set[int] = set()
        self.epochs: set[int] = set()
        self.weights: dict[str, float] = {}
        self.intervals = {key(e, l, r): (0, 100) for e in range(EPOCHS)
                          for l in range(LOCATIONS) for r in range(RESOURCES)}

    def apply(self, event: Event, hidden: dict[str, int]) -> None:
        self.requests += 1
        self.tuples.add(event.tuple_key)
        self.locations.add(event.location)
        self.epochs.add(event.epoch)
        if event.resource is not None:
            self.resources.add(event.resource)
        else:
            self.resources.update(range(RESOURCES))
        for cell in event.affected:
            self.cells.add(cell)
            self.weights[cell] = max(self.weights.get(cell, 0.0), PRECISION[event.tool])
            old_lo, old_hi = self.intervals[cell]
            new_lo, new_hi = constraint(event.tool, hidden[cell])
            self.intervals[cell] = max(old_lo, new_lo), min(old_hi, new_hi)

    def snapshot(self, stream_length: int) -> dict[str, float]:
        widths = [hi - lo for lo, hi in self.intervals.values()]
        estimates = [(lo + hi) / 2 for lo, hi in self.intervals.values()]
        return {
            "request_fraction": self.requests / stream_length,
            "tuple_coverage": len(self.tuples) / TOTAL_TUPLES,
            "cell_coverage": len(self.cells) / TOTAL_CELLS,
            "marginal_coverage": statistics.fmean((len(self.locations) / LOCATIONS,
                                                    len(self.resources) / RESOURCES,
                                                    len(self.epochs) / EPOCHS)),
            "weighted_coverage": sum(self.weights.values()) / TOTAL_CELLS,
            "reference_exposure": statistics.fmean(1 - width / 100 for width in widths),
            "estimates": estimates,
        }


def run_trial(trial: int, stream_name: str, seed: int) -> list[Row]:
    rng = random.Random(seed + trial)
    hidden = state(rng)
    stream = make_stream(stream_name, rng)
    checkpoints = sorted({max(1, math.ceil(len(stream) * fraction)): fraction for fraction in CHECKPOINTS}.items())
    ledgers = Ledgers()
    rows = []
    checkpoint_index = 0
    for index, event in enumerate(stream, 1):
        ledgers.apply(event, hidden)
        while checkpoint_index < len(checkpoints) and index >= checkpoints[checkpoint_index][0]:
            _, fraction = checkpoints[checkpoint_index]
            snap = ledgers.snapshot(len(stream))
            error = statistics.fmean(abs(a - b) for a, b in zip(snap.pop("estimates"), hidden.values()))
            rows.append(Row(trial, stream_name, fraction, reconstruction_score=max(0, 1 - error / 100), **snap))
            checkpoint_index += 1
    return rows


def pearson(xs: list[float], ys: list[float]) -> float:
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = rank
        i = j + 1
    return out


def summarize(rows: list[Row]) -> list[dict[str, object]]:
    predictors = ("request_fraction", "tuple_coverage", "cell_coverage", "marginal_coverage", "weighted_coverage")
    output = []
    for stream in sorted({r.stream for r in rows}):
        selected = [r for r in rows if r.stream == stream]
        target = [r.reference_exposure for r in selected]
        for predictor in predictors:
            values = [getattr(r, predictor) for r in selected]
            output.append({"stream": stream, "predictor": predictor, "observations": len(values),
                           "pearson": pearson(values, target),
                           "spearman": pearson(ranks(values), ranks(target)),
                           "calibration_mae": statistics.fmean(abs(x - y) for x, y in zip(values, target))})
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=40502)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results"))
    args = parser.parse_args()
    streams = ("unique", "duplicate-heavy", "precision-escalation", "marginal-scan", "multi-cell-summary", "mixed")
    rows = [row for trial in range(args.runs) for stream in streams for row in run_trial(trial, stream, args.seed)]
    summary = summarize(rows)
    args.output.mkdir(parents=True, exist_ok=True)
    with gzip.open(args.output / "checkpoints.csv.gz", "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0])))
        writer.writeheader(); writer.writerows(asdict(row) for row in rows)
    payload = {"version": "A2-v0.1", "runs": args.runs, "root_seed": args.seed,
               "streams": list(streams), "checkpoint_rows": len(rows), "summary": summary}
    (args.output / "benchmark.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
