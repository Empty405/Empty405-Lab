import random
import tempfile
import unittest
from pathlib import Path

import benchmark


class Tests(unittest.TestCase):
    def test_fixed_request_count(self):
        for workload in benchmark.WORKLOADS:
            self.assertEqual(len(benchmark.request_plan(workload, random.Random(1))), 96)

    def test_matrix_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(1, Path(tmp))
        self.assertEqual(result["configurations"], 270)
        self.assertEqual(result["trial_rows"], 270)

    def test_default_matrix_is_54000(self):
        self.assertEqual(6 * 5 * 3 * 3 * 200, 54_000)

    def test_exact_mechanisms_respect_cap(self):
        for mechanism in ("central", "oracle"):
            for sync in benchmark.SYNC:
                row = benchmark.simulate_trial(mechanism, "disjoint", sync, 0.25, 1)
                self.assertLessEqual(row["union_exposure"], 0.25)

    def test_independent_replicas_multiply_budget(self):
        row = benchmark.simulate_trial("independent", "disjoint", "partitioned", 0.25, 2)
        self.assertGreater(row["union_exposure"], 0.25)
        self.assertEqual(row["budget_multiplication_factor"], 4.0)

    def test_eventual_partition_is_detected_late(self):
        row = benchmark.simulate_trial("eventual", "disjoint", "partitioned", 0.25, 3)
        self.assertGreater(row["delayed_detection_exposure"], 0)
        self.assertEqual(row["overrun_event"], 1)

    def test_bounded_authority_preserves_conservation(self):
        for mechanism in ("hierarchical", "escrow"):
            for sync in benchmark.SYNC:
                row = benchmark.simulate_trial(mechanism, "disjoint", sync, 0.25, 4)
                self.assertEqual(row["conservation_error"], 0)
                self.assertLessEqual(row["union_exposure"], 0.25)

    def test_exact_duplicate_workload_does_not_double_charge(self):
        row = benchmark.simulate_trial("oracle", "duplicate_heavy", "healthy", 0.25, 5)
        self.assertEqual(row["union_units"], 8)
        self.assertEqual(row["false_charge_events"], 0)
        self.assertEqual(row["denied_requests"], 0)
        self.assertEqual(row["duplicate_suppression"], 1.0)

    def test_central_partition_fails_closed(self):
        row = benchmark.simulate_trial("central", "partial_overlap", "partitioned", 0.50, 6)
        self.assertEqual(row["union_units"], 0)
        self.assertEqual(row["denied_requests"], 96)


if __name__ == "__main__":
    unittest.main()
