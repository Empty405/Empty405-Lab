from __future__ import annotations

from collections import defaultdict
import math

HARD_COVERAGE_FRACTION = 0.30
ADAPTIVE_FULL_FRACTION = 0.30
ADAPTIVE_COARSE_FRACTION = 0.40


class HardCoveragePolicy:
    def __init__(self, total_cells: int, shared_principal: bool):
        self.limit = max(1, math.floor(total_cells * HARD_COVERAGE_FRACTION))
        self.shared_principal = shared_principal
        self.identity_seen = defaultdict(set)
        self.global_seen = set()

    def level(self, identity: int, cell: tuple) -> str:
        if self.shared_principal:
            if cell in self.global_seen:
                return "full"

            if len(self.global_seen) >= self.limit:
                return "blocked"

            self.global_seen.add(cell)
            return "full"

        seen = self.identity_seen[identity]

        if cell in seen:
            return "full"

        if len(seen) >= self.limit:
            return "blocked"

        seen.add(cell)
        return "full"


class AdaptiveSharedPolicy:
    def __init__(self, total_cells: int):
        self.total_cells = total_cells
        self.full_limit = math.floor(total_cells * ADAPTIVE_FULL_FRACTION)
        self.coarse_limit = math.floor(
            total_cells * (ADAPTIVE_FULL_FRACTION + ADAPTIVE_COARSE_FRACTION)
        )
        self.level_by_cell = {}

    def level(self, identity: int, cell: tuple) -> str:
        # Identity is accepted deliberately but does not partition exposure state.
        if cell in self.level_by_cell:
            return self.level_by_cell[cell]

        count = len(self.level_by_cell) + 1

        if count <= self.full_limit:
            level = "full"
        elif count <= self.coarse_limit:
            level = "coarse"
        else:
            level = "minimal"

        self.level_by_cell[cell] = level
        return level


def degrade_response(response: dict, level: str, capacity_band_fn) -> dict:
    if level == "full":
        return response

    if level == "blocked":
        return {"kind": "limited", "value": None}

    kind = response["kind"]
    value = response["value"]

    if level == "coarse":
        if kind == "availability":
            return response

        if kind == "band4":
            return {
                "kind": "band2",
                "value": "below_50" if value in ("q1", "q2") else "at_least_50",
            }

        if kind == "range":
            lower, upper = value
            midpoint = (lower + upper) / 2
            return {"kind": "band4", "value": capacity_band_fn(midpoint)}

        if kind == "trend3":
            return response

    if level == "minimal":
        if kind == "availability":
            return response

        if kind in ("band4", "range"):
            return {"kind": "limited", "value": None}

        if kind == "trend3":
            if value == "na":
                return response

            return {
                "kind": "trend2",
                "value": "stable" if value == "stable" else "changed",
            }

    return {"kind": "limited", "value": None}


def legitimate_utility(level: str) -> float:
    """
    Project-specific task utility proxy.

    Task weighting:
      availability = 50%
      band         = 30%
      trend        = 20%

    full:
      all tasks retain full resolution -> 1.00

    coarse:
      availability full (0.50)
      band binary rather than quartile (0.15 partial credit)
      trend full (0.20)
      total = 0.85

    minimal:
      availability full (0.50)
      band unavailable (0.00)
      trend stable/changed partial credit (0.10)
      total = 0.60
    """
    return {
        "full": 1.00,
        "coarse": 0.85,
        "minimal": 0.60,
        "blocked": 0.00,
    }[level]
