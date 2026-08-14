import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
NEW = ENGINE / "scripts" / "new_research.py"
VALIDATOR = ENGINE / "scripts" / "validate_research.py"


class EngineTests(unittest.TestCase):
    def test_new_research_creates_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable, str(NEW),
                    "--id", "2",
                    "--title", "Strange Test",
                    "--root", tmp,
                    "--raw-idea", "Try to kill this idea."
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            target = Path(tmp) / "002-strange-test"
            self.assertTrue((target / "research.json").exists())
            self.assertTrue((target / "experiment" / "EXPERIMENT.md").exists())
            self.assertTrue((target / "results" / "RESULTS.md").exists())

    def test_incomplete_record_fails_design_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "research.json"
            record.write_text(json.dumps({
                "engine_version": "0.1",
                "research": {"id": "002", "title": "X", "status": "idea"}
            }))
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), str(record)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)

    def test_complete_record_passes_publish_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "research.json"
            record.write_text(json.dumps({
                "engine_version": "0.1",
                "research": {
                    "id": "002",
                    "title": "Complete",
                    "slug": "complete",
                    "status": "publish-ready"
                },
                "question": "Does X survive Y?",
                "hypothesis": "X survives Y.",
                "prior_art": [{"title": "Prior work"}],
                "strongest_objections": ["Alternative explanation."],
                "falsification": {"criteria": ["Metric falls below threshold."]},
                "success_criteria": ["Metric remains above threshold."],
                "experiment": {"plan": "Run controlled benchmark.", "metrics": ["score"]},
                "reproducibility": {"command": "python benchmark.py", "seed": 405},
                "review": {
                    "outcome": "supported",
                    "limitations": ["Synthetic environment."],
                    "claim_audit": ["Do not generalize to production."]
                },
                "next_questions": ["Does it survive a stronger attacker?"]
            }))
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), str(record), "--stage", "publish"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
