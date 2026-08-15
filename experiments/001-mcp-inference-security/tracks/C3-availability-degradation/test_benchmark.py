import tempfile
import unittest
from pathlib import Path

import benchmark


class Tests(unittest.TestCase):
    def test_matrix_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(1, Path(tmp))
        self.assertEqual(result["configurations"], 315)
        self.assertEqual(result["trial_rows"], 315)

    def test_default_matrix_is_63000(self):
        self.assertEqual(7 * 5 * 3 * 3 * 200, 63_000)

    def test_every_episode_has_120_ticks(self):
        row = benchmark.simulate_trial("hard_deny", "outage", "low", "routine", 1)
        self.assertEqual(row["episode_ticks"], 120)

    def test_hard_deny_never_exposes_new_units(self):
        for disruption in benchmark.DISRUPTIONS:
            row = benchmark.simulate_trial("hard_deny", disruption, "sustained", "critical", 2)
            self.assertEqual(row["new_exposure_units"], 0)

    def test_replay_only_preserves_cap(self):
        row = benchmark.simulate_trial("replay_only", "outage", "burst", "routine", 3)
        self.assertEqual(row["availability_induced_exposure_gain"], 0)
        self.assertGreater(row["completed_tasks"], 0)

    def test_snapshot_is_precharged(self):
        row = benchmark.simulate_trial("safe_snapshot", "partition", "low", "optional", 4)
        self.assertEqual(row["new_exposure_units"], 0)
        self.assertEqual(row["stale_responses"], row["admitted_tasks"])

    def test_fail_open_records_violation(self):
        row = benchmark.simulate_trial("fail_open", "outage", "sustained", "routine", 5)
        self.assertGreater(row["new_exposure_units"], 0)
        self.assertGreater(row["fail_open_violation_rate"], 0)

    def test_retry_does_not_duplicate_tasks(self):
        row = benchmark.simulate_trial("bounded_queue_retry", "recovery_storm", "burst", "critical", 6)
        self.assertEqual(row["duplicate_executions"], 0)
        self.assertEqual(row["expired_task_execution_count"], 0)

    def test_queue_capacity_is_bounded(self):
        row = benchmark.simulate_trial("bounded_queue_retry", "outage", "sustained", "routine", 7)
        self.assertLessEqual(row["peak_queue"], benchmark.QUEUE_CAPACITY)

    def test_all_tasks_end_once(self):
        row = benchmark.simulate_trial("bounded_queue_retry", "outage", "burst", "optional", 8)
        outcomes = row["completed_tasks"] + row["denied_tasks"] + row["timed_out_tasks"]
        self.assertLessEqual(outcomes, row["admitted_tasks"])
        self.assertEqual(row["duplicate_executions"], 0)

    def test_recovery_never_resets_budget(self):
        for policy in benchmark.POLICIES:
            row = benchmark.simulate_trial(policy, "recovery_storm", "low", "routine", 9)
            self.assertEqual(row["silent_budget_reset_indicator"], 0)

    def test_criticality_does_not_authorize_bypass(self):
        for criticality in benchmark.CRITICALITY:
            row = benchmark.simulate_trial("hard_deny", "outage", "low", criticality, 10)
            self.assertEqual(row["new_exposure_units"], 0)


if __name__ == "__main__":
    unittest.main()
