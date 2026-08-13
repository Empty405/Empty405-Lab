import json
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / "policies"))
from rate_limit import RateLimiter

LOCATIONS = ["north", "central", "south"]
RESOURCES = ["fuel", "medical", "food"]

limiter = RateLimiter(
    max_requests=5,
    window_seconds=10,
)

allowed = 0
blocked = 0
observations = []


def run_tool(script_name, location, resource):
    global allowed, blocked

    if not limiter.allow():
        blocked += 1

        return {
            "blocked": True,
            "tool": script_name,
            "location": location,
            "resource": resource,
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
    "observations": observations,
}

print(json.dumps(output, indent=2))
