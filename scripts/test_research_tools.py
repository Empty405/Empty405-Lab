import csv
import gzip
import json
import math
import tempfile
import unittest
from pathlib import Path

from maintenance import env_doctor
from processing import metric_aggregator
from validation import integrity_checker, schema_enforcer


class ResearchToolsTests(unittest.TestCase):
    def fixture(self, root: Path, declared: int = 2, header: str = "value") -> Path:
        results = root / "experiments" / "program" / "tracks" / "X1-fixture" / "results"
        results.mkdir(parents=True)
        (results / "benchmark.json").write_text(
            json.dumps({"trial_rows": declared, "configuration_count": 1}),
            encoding="utf-8",
        )
        with gzip.open(results / "trials.csv.gz", "wt", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow([header] if header else [])
            writer.writerow([1])
            writer.writerow([2])
        return results

    def test_schema_accepts_positive_row_count(self):
        metadata = schema_enforcer.validate_metadata({"trial_rows": 2})
        self.assertEqual(schema_enforcer.declared_rows(metadata), 2)

    def test_schema_rejects_missing_or_conflicting_rows(self):
        with self.assertRaises(schema_enforcer.SchemaError):
            schema_enforcer.validate_metadata({"name": "missing"})
        with self.assertRaises(schema_enforcer.SchemaError):
            schema_enforcer.validate_metadata({"trial_rows": 2, "rows": 3})

    def test_schema_rejects_non_finite_numbers(self):
        with self.assertRaises(schema_enforcer.SchemaError):
            schema_enforcer.validate_metadata({"trial_rows": 2, "metric": math.nan})

    def test_integrity_checks_rows_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = integrity_checker.validate_results_dir(self.fixture(Path(tmp)))
            self.assertEqual(report["raw_rows"], 2)
            self.assertEqual(len(report["sha256"]["trials.csv.gz"]), 64)

    def test_integrity_checks_multiple_raw_artifacts_independently(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = self.fixture(Path(tmp))
            metadata_path = results / "benchmark.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["task_event_rows"] = 3
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            with gzip.open(results / "task-events.csv.gz", "wt", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["event"])
                writer.writerows([[1], [2], [3]])

            report = integrity_checker.validate_results_dir(results)

            self.assertEqual(report["raw_rows"], 5)
            self.assertEqual(
                report["declared_raw_files"],
                {"task-events.csv.gz": 3, "trials.csv.gz": 2},
            )

    def test_integrity_rejects_row_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "row mismatch"):
                integrity_checker.validate_results_dir(self.fixture(Path(tmp), declared=3))

    def test_integrity_rejects_invalid_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "header"):
                integrity_checker.validate_results_dir(self.fixture(Path(tmp), header=""))

    def test_aggregator_builds_validated_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            rows = metric_aggregator.collect(root)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["module"], "X1-fixture")
            self.assertEqual(rows[0]["raw_rows"], 2)

    def test_env_doctor_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            (root / "experiments").mkdir()
            (root / "scripts").mkdir()
            checks = env_doctor.diagnose(root, min_free_mb=0)
            self.assertTrue(all(check["ok"] for check in checks), checks)


if __name__ == "__main__":
    unittest.main()
