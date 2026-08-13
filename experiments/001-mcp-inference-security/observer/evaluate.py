import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "hidden_state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    hidden_state = json.load(f)

result = subprocess.run(
    [
        "python",
        str(BASE_DIR / "observer" / "reconstruct.py"),
    ],
    capture_output=True,
    text=True,
    check=True,
)

reconstructed = json.loads(result.stdout)

absolute_errors = []
rows = []

for location, resources in hidden_state["locations"].items():
    for resource, true_value in resources.items():
        estimate = reconstructed[location][resource]["estimated_value"]
        error = abs(true_value - estimate)

        absolute_errors.append(error)

        rows.append(
            {
                "location": location,
                "resource": resource,
                "true_value": true_value,
                "estimated_value": estimate,
                "absolute_error": error,
            }
        )

mae = sum(absolute_errors) / len(absolute_errors)

accuracy = max(0, 100 - mae)

output = {
    "samples": len(absolute_errors),
    "mean_absolute_error": round(mae, 2),
    "simple_reconstruction_score": round(accuracy, 2),
    "details": rows,
}

print(json.dumps(output, indent=2))
