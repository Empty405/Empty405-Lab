#!/usr/bin/env python3
"""A3 adaptive disclosure benchmark with matched-risk comparisons."""
from __future__ import annotations

import argparse, csv, gzip, json, random, statistics
from dataclasses import asdict, dataclass
from pathlib import Path

LOCATIONS, RESOURCES = 12, 8
CELLS = LOCATIONS * RESOURCES
TASKS = ("threshold", "category", "planning", "exact", "aggregate")
HARD_CAPS = tuple(i / 20 for i in range(2, 20))  # 0.10 through 0.95 in 0.05 steps
PROFILES = {
    "adaptive_conservative": (0.10, 0.25, 0.40, 0.55, 0.70),
    "adaptive_balanced": (0.20, 0.40, 0.60, 0.75, 0.90),
    "adaptive_permissive": (0.30, 0.50, 0.70, 0.85, 0.95),
}


@dataclass(frozen=True)
class Response:
    level: str
    interval: tuple[int, int] | None
    category: str | None
    aggregate_band: str | None
    provenance: dict[str, object]


@dataclass
class Trial:
    trial: int
    mode: str
    interval_reduction: float
    reconstruction_score: float
    exact_recovery: float
    macro_utility: float
    threshold_utility: float
    category_utility: float
    planning_utility: float
    exact_utility: float
    aggregate_utility: float
    provenance_complete: float


def cat(value: float) -> str:
    return "low" if value < 34 else ("medium" if value < 67 else "high")


def nested_interval(value: int, level: str) -> tuple[int, int] | None:
    if level == "L0": return value, value
    if level == "L1":
        lo = value // 10 * 10; return lo, min(100, lo + 9)
    if level == "L2":
        lo = value // 20 * 20; return lo, min(100, lo + 19)
    if level == "L3":
        return (0, 33) if value < 34 else ((34, 66) if value < 67 else (67, 100))
    return None


def provenance(level: str, reason: str) -> dict[str, object]:
    return {"level": level, "freshness_epoch": "epoch-1", "transformed": level != "L0",
            "synthetic": False, "reason": reason, "policy_version": "A3-v0.1"}


def adaptive_level(exposure: float, thresholds: tuple[float, ...]) -> str:
    for index, boundary in enumerate(thresholds):
        if exposure <= boundary: return f"L{index}"
    return "L5"


def answer(value: int, region_mean: float, level: str, reason: str) -> Response:
    interval = nested_interval(value, level)
    return Response(level, interval, cat(value) if level in ("L0", "L1", "L2", "L3") else None,
                    cat(region_mean) if level == "L4" else None, provenance(level, reason))


def useful(task: str, response: Response, value: int) -> bool:
    if response.level == "L5": return False
    if task == "exact": return response.interval == (value, value)
    if task == "planning": return response.interval is not None and response.interval[1] - response.interval[0] <= 20
    if task == "category": return response.category == cat(value)
    if task == "threshold":
        return response.interval is not None and (response.interval[1] < 50 or response.interval[0] >= 50)
    if task == "aggregate": return response.aggregate_band is not None or response.level in ("L0", "L1", "L2", "L3")
    raise ValueError(task)


def run(trial: int, mode: str, seed: int) -> Trial:
    rng = random.Random(seed + trial)
    values = [rng.randint(0, 100) for _ in range(CELLS)]
    order = list(range(CELLS)); rng.shuffle(order)
    intervals = [(0, 100) for _ in range(CELLS)]
    utilities = {task: 0 for task in TASKS}; provenance_ok = 0
    cap = float(mode.split("_")[-1]) if mode.startswith("hard_") else None
    thresholds = PROFILES.get(mode)
    for step, cell in enumerate(order):
        exposure = step / CELLS
        if mode == "exact": level, reason = "L0", "baseline"
        elif cap is not None: level, reason = ("L0" if exposure < cap else "L5"), "hard-cap"
        elif thresholds is not None: level, reason = adaptive_level(exposure, thresholds), "cumulative-exposure"
        else: raise ValueError(mode)
        loc = cell // RESOURCES
        region = values[loc * RESOURCES:(loc + 1) * RESOURCES]
        response = answer(values[cell], statistics.fmean(region), level, reason)
        required = {"level", "freshness_epoch", "transformed", "synthetic", "reason", "policy_version"}
        provenance_ok += required <= response.provenance.keys()
        if response.interval:
            lo, hi = intervals[cell]; nlo, nhi = response.interval
            intervals[cell] = max(lo, nlo), min(hi, nhi)
        for task in TASKS: utilities[task] += useful(task, response, values[cell])
    widths = [hi - lo for lo, hi in intervals]
    estimates = [(lo + hi) / 2 for lo, hi in intervals]
    reduction = statistics.fmean(1 - width / 100 for width in widths)
    score = 1 - statistics.fmean(abs(a - b) for a, b in zip(estimates, values)) / 100
    exact = sum(lo == hi for lo, hi in intervals) / CELLS
    task_scores = {task: utilities[task] / CELLS for task in TASKS}
    return Trial(trial, mode, reduction, score, exact, statistics.fmean(task_scores.values()),
                 task_scores["threshold"], task_scores["category"], task_scores["planning"],
                 task_scores["exact"], task_scores["aggregate"], provenance_ok / CELLS)


def randomized_sampling_violation(seed: int, samples: int = 8) -> tuple[int, int]:
    """Negative control: random same-width ranges intersect into a narrower range."""
    rng = random.Random(seed); value = 53; lo, hi = 0, 100
    for _ in range(samples):
        left = rng.randint(max(0, value - 19), value)
        right = min(100, left + 19)
        lo, hi = max(lo, left), min(hi, right)
    return lo, hi


def summarize(rows: list[Trial]) -> list[dict[str, object]]:
    output=[]
    for mode in sorted({r.mode for r in rows}):
        selected=[r for r in rows if r.mode==mode]
        item={"mode":mode,"runs":len(selected)}
        for field in ("interval_reduction","reconstruction_score","exact_recovery","macro_utility",
                      "threshold_utility","category_utility","planning_utility","exact_utility",
                      "aggregate_utility","provenance_complete"):
            item[field]=statistics.fmean(getattr(r,field) for r in selected)
        output.append(item)
    return output


def frontier(summary: list[dict[str, object]]) -> list[dict[str, object]]:
    hard=[r for r in summary if str(r["mode"]).startswith("hard_")]
    output=[]
    for adaptive in [r for r in summary if str(r["mode"]).startswith("adaptive_")]:
        match=min(hard,key=lambda h:abs(float(h["interval_reduction"])-float(adaptive["interval_reduction"])))
        output.append({"adaptive":adaptive["mode"],"adaptive_risk":adaptive["interval_reduction"],
                       "adaptive_utility":adaptive["macro_utility"],"matched_hard":match["mode"],
                       "hard_risk":match["interval_reduction"],"hard_utility":match["macro_utility"],
                       "utility_delta":float(adaptive["macro_utility"])-float(match["macro_utility"]),
                       "risk_gap":abs(float(adaptive["interval_reduction"])-float(match["interval_reduction"]))})
    return output


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--runs",type=int,default=1000); p.add_argument("--seed",type=int,default=40503)
    p.add_argument("--output",type=Path,default=Path(__file__).with_name("results")); args=p.parse_args()
    modes=["exact",*[f"hard_{cap:.2f}" for cap in HARD_CAPS],*PROFILES]
    rows=[run(t,m,args.seed) for t in range(args.runs) for m in modes]
    summary=summarize(rows); matched=frontier(summary); violation=randomized_sampling_violation(args.seed)
    args.output.mkdir(parents=True,exist_ok=True)
    with gzip.open(args.output/"trials.csv.gz","wt",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(asdict(rows[0]))); w.writeheader(); w.writerows(asdict(r) for r in rows)
    payload={"version":"A3-v0.1","runs":args.runs,"root_seed":args.seed,"summary":summary,
             "matched_frontier":matched,"randomized_negative_control":{"final_interval":violation,"width":violation[1]-violation[0]}}
    (args.output/"benchmark.json").write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))


if __name__=="__main__": main()
