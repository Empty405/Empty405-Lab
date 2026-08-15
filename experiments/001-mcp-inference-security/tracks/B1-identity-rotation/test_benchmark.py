import tempfile
import unittest
from pathlib import Path

import benchmark


class BenchmarkTests(unittest.TestCase):
    def test_partition_preserves_request_count(self):
        for rotations in benchmark.ROTATIONS:
            self.assertEqual(sum(benchmark.request_partition(rotations)), benchmark.REQUESTS)

    def test_no_rotation_respects_budget(self):
        for strategy in benchmark.STRATEGIES:
            row = benchmark.simulate_trial(0, strategy, 0.25, "missing", 1)
            self.assertLessEqual(row["exposure"], 0.25)

    def test_oracle_is_rotation_invariant(self):
        for rotations in benchmark.ROTATIONS:
            row = benchmark.simulate_trial(rotations, "oracle", 0.50, "missing", 3)
            self.assertEqual(row["exposure"], 0.50)
            self.assertEqual(row["false_split_rate"], 0.0)

    def test_per_identity_rotation_bypasses_budget(self):
        base = benchmark.simulate_trial(0, "per_identity", 0.25, "clean", 7)
        rotated = benchmark.simulate_trial(4, "per_identity", 0.25, "clean", 7)
        self.assertEqual(base["exposure"], 0.25)
        self.assertEqual(rotated["exposure"], 1.0)

    def test_metrics_are_bounded(self):
        for strategy in benchmark.STRATEGIES:
            row = benchmark.simulate_trial(16, strategy, 0.75, "noisy", 9)
            for metric in ("exposure", "reconstruction", "false_split_rate", "legitimate_utility"):
                self.assertGreaterEqual(row[metric], 0.0)
                self.assertLessEqual(row[metric], 1.0)

    def test_small_run_row_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(2, Path(tmp))
            expected = len(benchmark.ROTATIONS) * len(benchmark.STRATEGIES) * len(benchmark.BUDGETS) * len(benchmark.QUALITIES) * 2
            self.assertEqual(result["trial_rows"], expected)
            self.assertEqual(result["configurations"], 324)


if __name__ == "__main__":
    unittest.main()
