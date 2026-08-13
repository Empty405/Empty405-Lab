import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "hidden_state.json"


class AdaptiveGateway:
    def __init__(self):
        self.seen = set()

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            self.state = json.load(f)

    def _disclosure_level(self):
        coverage = len(self.seen)

        if coverage <= 3:
            return 0
        elif coverage <= 5:
            return 1
        elif coverage <= 7:
            return 2
        else:
            return 3

    def _degrade(self, value, level):
        if level == 0:
            return {
                "precision": "exact",
                "value": value,
            }

        if level == 1:
            lower = (value // 10) * 10
            upper = lower + 10

            return {
                "precision": "range",
                "value": f"{lower}-{upper}",
            }

        if level == 2:
            if value < 34:
                category = "low"
            elif value < 67:
                category = "medium"
            else:
                category = "high"

            return {
                "precision": "category",
                "value": category,
            }

        return {
            "precision": "regional",
            "value": "limited",
        }

    def query(self, location, resource):
        if location not in self.state["locations"]:
            return {"error": "unknown_location"}

        if resource not in self.state["locations"][location]:
            return {"error": "unknown_resource"}

        key = (location, resource)
        self.seen.add(key)

        level = self._disclosure_level()
        true_value = self.state["locations"][location][resource]

        degraded = self._degrade(true_value, level)

        return {
            "location": location,
            "resource": resource,
            "coverage_count": len(self.seen),
            "disclosure_level": level,
            "precision": degraded["precision"],
            "response": degraded["value"],
        }
