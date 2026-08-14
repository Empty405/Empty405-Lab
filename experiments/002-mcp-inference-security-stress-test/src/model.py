from __future__ import annotations

from typing import Dict, Tuple
import random

Cell = Tuple[int, int, int]
State = Dict[Cell, int]

LOCATIONS = 12
RESOURCES = 8
TIME_STEPS = 3


def clip(value: float) -> int:
    return max(0, min(100, int(round(value))))


def generate_state(rng: random.Random) -> State:
    state: State = {}

    for location in range(LOCATIONS):
        for resource in range(RESOURCES):
            previous = rng.randint(0, 100)
            state[(location, resource, 0)] = previous

            for time_step in range(1, TIME_STEPS):
                previous = clip(previous + rng.gauss(0, 12))
                state[(location, resource, time_step)] = previous

    return state


def capacity_band(value: float) -> str:
    if value <= 24:
        return "q1"
    if value <= 49:
        return "q2"
    if value <= 74:
        return "q3"
    return "q4"


def numeric_range(value: int) -> tuple[int, int]:
    lower = (value // 10) * 10
    upper = min(100, lower + 9)
    return lower, upper


def trend(state: State, cell: Cell) -> str:
    location, resource, time_step = cell

    if time_step == 0:
        return "na"

    previous = state[(location, resource, time_step - 1)]
    delta = state[cell] - previous

    if delta >= 5:
        return "up"
    if delta <= -5:
        return "down"
    return "stable"


def tool_response(state: State, cell: Cell, tool: str) -> dict:
    value = state[cell]

    if tool == "availability":
        return {"kind": "availability", "value": value >= 50}

    if tool == "band":
        return {"kind": "band4", "value": capacity_band(value)}

    if tool == "range":
        return {"kind": "range", "value": numeric_range(value)}

    if tool == "trend":
        return {"kind": "trend3", "value": trend(state, cell)}

    raise ValueError(f"Unknown tool: {tool}")
