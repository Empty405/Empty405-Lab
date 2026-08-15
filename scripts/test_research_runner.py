import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import research_runner


class RunnerTests(unittest.TestCase):
    def fixture(self, root: Path, declared=2):
        module = root / "experiments" / "program" / "tracks" / "X1-fixture"
        (module / "results").mkdir(parents=True)
        (module / "benchmark.py").write_text("print('ok')\n")
        (module / "test_benchmark.py").write_text("import unittest\n")
        (module / "results" / "benchmark.json").write_text(json.dumps({"trial_rows": declared}))
        with gzip.open(module / "results" / "trials.csv.gz", "wt", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["x"])
            writer.writerow([1])
            writer.writerow([2])
        return module

    def test_discovers_complete_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(Path(tmp))
            modules = research_runner.discover(Path(tmp))
            self.assertEqual([item.key for item in modules], ["X1-fixture"])

    def test_validates_declared_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = self.fixture(Path(tmp))
            result = research_runner.validate_results(research_runner.Module(module.name, module))
            self.assertEqual(result["raw_rows"], 2)

    def test_rejects_row_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = self.fixture(Path(tmp), declared=3)
            with self.assertRaisesRegex(RuntimeError, "row mismatch"):
                research_runner.validate_results(research_runner.Module(module.name, module))

    def test_fingerprint_changes_with_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = self.fixture(Path(tmp))
            item = research_runner.Module(module.name, module)
            before = research_runner.fingerprint(item)
            (module / "results" / "benchmark.json").write_text(json.dumps({"trial_rows": 2, "changed": True}))
            self.assertNotEqual(before, research_runner.fingerprint(item))


if __name__ == "__main__":
    unittest.main()
