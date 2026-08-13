import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / "policies"))
from coverage_policy import CoveragePolicy

LOCATIONS = ["north", "central", "south"]
RESOURCES = ["fuel", "medical", "food"]

policy = CoveragePolicy(max_unique_combinations=5)

allowed = 0
blocked = 0
observations = []


def run_tool(script_name, location, resource):
    global allowed, blocked

    decision = policy.check(location, resource)

    if not decision["allowed"]:
        blocked += 1
        return {
            "blocked": True,
            "location": location,
            "resource": resource,
            "coverage_count": decision["coverage_count"],
        }

    allowed += 1

    script = BASE_DIR / "server" / script_name

    result = subprocess.run(
        ["python", str(script), location, resource],
        capture_output=True,
        text=True,
        check=True,
    )

    response = json.loads(result.stdout)
    response["blocked"] = False
    response["coverage_count"] = decision["coverage_count"]

    return response


for location in LOCATIONS:
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

        observations.append({
            "location": location,
            "resource": resource,
            "availability": availability,
            "capacity": capacity,
        })


output = {
    "total_attempted": allowed + blocked,
    "allowed": allowed,
    "blocked": blocked,
    "unique_combinations_exposed": len(policy.seen),
    "max_unique_combinations": policy.max_unique_combinations,
    "observations": observations,
}

print(json.dumps(output, indent=2))
