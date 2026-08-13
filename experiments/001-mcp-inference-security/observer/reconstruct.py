import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOCATIONS = ["north", "central", "south"]
RESOURCES = ["fuel", "medical", "food"]


def run_tool(script_name, location, resource):
    script = BASE_DIR / "server" / script_name

    result = subprocess.run(
        ["python", str(script), location, resource],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)


def estimate_value(available, level):
    if level == "low":
        low, high = 0, 33
    elif level == "medium":
        low, high = 34, 66
    else:
        low, high = 67, 100

    if available:
        low = max(low, 21)
    else:
        high = min(high, 20)

    return round((low + high) / 2)


reconstructed = {}

for location in LOCATIONS:
    reconstructed[location] = {}

    for resource in RESOURCES:
        availability = run_tool(
            "tool_availability.py",
            location,
            resource,
        )

        capacity = run_tool(
            "tool_capacity_band.py",
            location,
            resource,
        )

        estimate = estimate_value(
            availability["available"],
            capacity["level"],
        )

        reconstructed[location][resource] = {
            "available": availability["available"],
            "level": capacity["level"],
            "estimated_value": estimate,
        }


print(json.dumps(reconstructed, indent=2))
