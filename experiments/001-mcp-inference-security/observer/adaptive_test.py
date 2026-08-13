import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / "server"))
from adaptive_gateway import AdaptiveGateway

LOCATIONS = ["north", "central", "south"]
RESOURCES = ["fuel", "medical", "food"]

gateway = AdaptiveGateway()

observations = []

for location in LOCATIONS:
    for resource in RESOURCES:
        response = gateway.query(location, resource)
        observations.append(response)

output = {
    "unique_combinations_exposed": len(gateway.seen),
    "observations": observations,
}

print(json.dumps(output, indent=2))
