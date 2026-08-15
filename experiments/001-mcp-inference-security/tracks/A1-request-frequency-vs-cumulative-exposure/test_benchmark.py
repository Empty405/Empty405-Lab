import unittest

from benchmark import (
    Baseline, CoverageBudget, Hybrid, LifetimeQuota, WindowRateLimit,
    execute, evaluate_legitimate_utility, query_stream, CELL_COUNT,
)
import random


class BenchmarkTests(unittest.TestCase):
    def test_stream_shapes(self):
        self.assertEqual(len(query_stream(random.Random(1), "unique")), CELL_COUNT)
        self.assertEqual(len(query_stream(random.Random(1), "duplicate-heavy")), CELL_COUNT * 3)

    def test_patient_rate_limit_reaches_baseline_exposure(self):
        base = execute(0, "unique", "patient", Baseline, 40501)
        rate = execute(0, "unique", "patient", WindowRateLimit, 40501)
        self.assertEqual(base.observable_state, 1.0)
        self.assertEqual(rate.observable_state, base.observable_state)
        self.assertGreater(rate.logical_time, base.logical_time)

    def test_coverage_budget_caps_exposure(self):
        result = execute(0, "unique", "patient", CoverageBudget, 40501)
        self.assertEqual(result.observable_state, 0.5)

    def test_lifetime_quota_wastes_duplicate_releases(self):
        quota = execute(0, "duplicate-heavy", "patient", LifetimeQuota, 40501)
        coverage = execute(0, "duplicate-heavy", "patient", CoverageBudget, 40501)
        self.assertLess(quota.observable_state, coverage.observable_state)

    def test_hybrid_caps_and_delays(self):
        result = execute(0, "unique", "patient", Hybrid, 40501)
        self.assertEqual(result.observable_state, 0.5)
        self.assertGreater(result.logical_time, 0)

    def test_utility_is_a_separate_deadline_workload(self):
        self.assertEqual(evaluate_legitimate_utility(Baseline), 1.0)
        self.assertEqual(evaluate_legitimate_utility(CoverageBudget), 1.0)
        self.assertLess(evaluate_legitimate_utility(WindowRateLimit), 1.0)


if __name__ == "__main__":
    unittest.main()
