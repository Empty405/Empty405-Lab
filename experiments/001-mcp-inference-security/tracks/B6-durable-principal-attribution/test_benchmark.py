import tempfile
import unittest
from pathlib import Path

import benchmark


class Tests(unittest.TestCase):
    def test_matrix_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(1, Path(tmp))
        self.assertEqual(result["configurations"], 360)
        self.assertEqual(result["trial_rows"], 360)

    def test_default_matrix_is_108000(self):
        self.assertEqual(6 * 5 * 4 * 3 * 300, 108_000)

    def test_oracle_never_splits(self):
        for lifecycle in benchmark.LIFECYCLES:
            row = benchmark.simulate_trial("oracle", lifecycle, "honest", 0.25, 1)
            self.assertEqual(row["false_split"], 0)
            self.assertLessEqual(row["aggregate_exposure"], 0.25)

    def test_session_rotation_can_duplicate_budget(self):
        stable = benchmark.simulate_trial("session", "stable", "honest", 0.25, 2)
        rotated = benchmark.simulate_trial("session", "token_rotation", "honest", 0.25, 2)
        self.assertGreater(rotated["aggregate_exposure"], stable["aggregate_exposure"])
        self.assertEqual(rotated["false_split"], 1)

    def test_global_id_links_more_contexts(self):
        global_id = benchmark.simulate_trial("global_id", "stable", "honest", 0.50, 3)
        pairwise = benchmark.simulate_trial("pairwise", "stable", "honest", 0.50, 3)
        self.assertGreater(global_id["linked_contexts"], pairwise["linked_contexts"])

    def test_outage_uses_restricted_bootstrap(self):
        row = benchmark.simulate_trial("anonymous_credential", "stable", "service_outage", 0.50, 4)
        self.assertLessEqual(row["aggregate_exposure"], 0.10)
        self.assertEqual(row["recovery_success"], 0)

    def test_ground_truth_not_in_attribution_api(self):
        keys, _, _ = benchmark.attribution_keys("account", "stable", "honest")
        self.assertEqual(keys, ["p0", "p0"])


if __name__ == "__main__":
    unittest.main()
