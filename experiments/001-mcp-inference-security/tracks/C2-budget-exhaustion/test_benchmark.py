import random
import tempfile
import unittest
from pathlib import Path

import benchmark


class Tests(unittest.TestCase):
    def test_fixed_request_count(self):
        for workload in benchmark.WORKLOADS:
            rows = benchmark.candidate_requests(workload, 25, random.Random(1))
            self.assertEqual(len(rows), 48)

    def test_matrix_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(1, Path(tmp))
        self.assertEqual(result["configurations"], 270)
        self.assertEqual(result["trial_rows"], 270)

    def test_default_matrix_is_54000(self):
        self.assertEqual(6 * 5 * 3 * 3 * 200, 54_000)

    def test_every_trial_starts_at_cap(self):
        for budget in benchmark.BUDGETS:
            row = benchmark.simulate_trial("hard_deny", "mixed", budget, "routine", 1)
            self.assertEqual(row["pre_exhaustion_units"], round(budget * benchmark.HIDDEN_UNITS))

    def test_hard_deny_has_zero_gain(self):
        row = benchmark.simulate_trial("hard_deny", "new_disjoint", 0.25, "routine", 2)
        self.assertEqual(row["post_cap_exposure_gain"], 0)
        self.assertEqual(row["released_responses"], 0)
        self.assertEqual(row["safe_candidate_requests"], 0)
        self.assertEqual(row["safe_reuse_rate"], 0)

    def test_hard_deny_does_not_claim_safe_reuse(self):
        row = benchmark.simulate_trial("hard_deny", "duplicate_only", 0.25, "routine", 2)
        self.assertEqual(row["safe_candidate_requests"], 48)
        self.assertEqual(row["safe_reused_requests"], 0)
        self.assertEqual(row["safe_reuse_rate"], 0)

    def test_replay_only_reuses_without_gain(self):
        row = benchmark.simulate_trial("replay_only", "duplicate_only", 0.25, "routine", 3)
        self.assertEqual(row["post_cap_exposure_gain"], 0)
        self.assertEqual(row["released_responses"], 48)
        self.assertEqual(row["safe_reuse_rate"], 1.0)

    def test_replay_only_denies_new_units(self):
        row = benchmark.simulate_trial("replay_only", "new_disjoint", 0.25, "critical", 4)
        self.assertEqual(row["denied_requests"], 48)
        self.assertEqual(row["cap_violation_event"], 0)

    def test_safe_snapshot_is_precharged(self):
        row = benchmark.simulate_trial("safe_snapshot", "new_disjoint", 0.25, "routine", 5)
        self.assertEqual(row["post_cap_exposure_gain"], 0)
        self.assertEqual(row["snapshot_responses"], 48)

    def test_contaminated_snapshot_is_invalid(self):
        self.assertFalse(benchmark.validate_snapshot({0, 1, 25}, set(range(25))))

    def test_bounded_override_cannot_exceed_allowance(self):
        row = benchmark.simulate_trial("bounded_override", "new_disjoint", 0.25, "critical", 6)
        self.assertLessEqual(row["post_cap_new_units"], benchmark.OVERRIDE_ALLOWANCE)
        self.assertEqual(row["override_replay_accepted"], 0)

    def test_no_policy_silently_resets(self):
        for policy in benchmark.POLICIES:
            row = benchmark.simulate_trial(policy, "mixed", 0.50, "optional", 7)
            self.assertEqual(row["silent_reset_indicator"], 0)


if __name__ == "__main__":
    unittest.main()
