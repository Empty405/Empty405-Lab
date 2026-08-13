import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "hidden_state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if len(sys.argv) != 3:
    print("Usage: python tool_capacity_band.py <location> <resource>")
    sys.exit(1)

location = sys.argv[1]
resource = sys.argv[2]

locations = state["locations"]

if location not in locations:
    print(json.dumps({"error": "unknown_location"}))
    sys.exit(1)

if resource not in locations[location]:
    print(json.dumps({"error": "unknown_resource"}))
    sys.exit(1)

value = locations[location][resource]

if value < 34:
    level = "low"
elif value < 67:
    level = "medium"
else:
    level = "high"

response = {
    "location": location,
    "resource": resource,
    "level": level
}

print(json.dumps(response))
