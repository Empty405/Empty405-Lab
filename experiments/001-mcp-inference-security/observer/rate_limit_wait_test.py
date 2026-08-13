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
    window_seconds=3,
)

allowed = 0
blocked = 0
waits = 0
observations = []


def run_tool(script_name, location, resource):
    global allowed, blocked, waits

    while not limiter.allow():
        blocked += 1
        waits += 1
        time.sleep(3.1)

    allowed += 1

    script = BASE_DIR / "server" / script_name

    result = subprocess.run(
        ["python", str(script), location, resource],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)


start_time = time.time()

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


elapsed = time.time() - start_time

output = {
    "total_required_queries": 18,
    "successful_queries": allowed,
    "rate_limit_hits": blocked,
    "wait_cycles": waits,
    "elapsed_seconds": round(elapsed, 2),
    "complete_dataset_collected": allowed == 18,
    "observations": observations,
}

print(json.dumps(output, indent=2))
