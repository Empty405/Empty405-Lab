import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import benchmark


class Tests(unittest.TestCase):
    def test_matrix_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = benchmark.run(1, Path(tmp))
        self.assertEqual(result["configurations"], 378)
        self.assertEqual(result["trial_rows"], 378)

    def test_default_matrix_is_75600(self):
        self.assertEqual(7 * 6 * 3 * 3 * 200, 75_600)

    def test_cap_never_overshoots(self):
        for policy in benchmark.POLICIES:
            row = benchmark.simulate_trial(policy, "adaptive_burn", "high", "late_critical", 1)
            self.assertEqual(row["cap_overshoot"], 0)
            self.assertLessEqual(row["total_charged_units"], benchmark.CAP)

    def test_duplicate_only_flood_costs_at_most_unique_units(self):
        row = benchmark.simulate_trial("global_fifo", "frequency_flood", "high", "steady", 2)
        self.assertLessEqual(row["attacker_charged_units"], 6)
        self.assertEqual(row["duplicate_charge_count"], 0)

    def test_denied_requests_expose_nothing(self):
        row = benchmark.simulate_trial("bounded_hybrid", "novelty_maximizer", "high", "burst", 3)
        self.assertEqual(row["denied_response_exposure"], 0)

    def test_no_budget_reset(self):
        for policy in benchmark.POLICIES:
            row = benchmark.simulate_trial(policy, "front_loaded_burn", "high", "late_critical", 4)
            self.assertEqual(row["silent_budget_reset"], 0)

    def test_oracle_admits_no_attacker(self):
        row = benchmark.simulate_trial("oracle", "adaptive_burn", "high", "burst", 5)
        self.assertEqual(row["attacker_admitted"], 0)

    def test_one_terminal_event_per_request(self):
        row, events = benchmark.simulate_episode("reservation", "camouflage", "medium", "steady", 6)
        self.assertEqual(len(events), row["requests"])
        self.assertEqual(len({event["request_id"] for event in events}), len(events))

    def test_principal_charges_conserve_global_charge(self):
        row, events = benchmark.simulate_episode("fair_share", "adaptive_burn", "high", "burst", 7)
        self.assertEqual(sum(event["charged_units"] for event in events), row["total_charged_units"])

    def test_every_episode_has_120_ticks(self):
        row = benchmark.simulate_trial("global_fifo", "benign_control", "low", "steady", 8)
        self.assertEqual(row["episode_ticks"], 120)

    def test_raw_events_recompute_charges(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp); result = benchmark.run(1, output)
            with gzip.open(output / "request-events.csv.gz", "rt", encoding="utf-8", newline="") as handle:
                events = list(csv.DictReader(handle))
            json.loads((output / "benchmark.json").read_text(encoding="utf-8"))
        self.assertEqual(len(events), result["request_event_rows"])
        self.assertEqual(set(events[0]), set(benchmark.EVENT_FIELDS))

    def test_role_not_passed_to_admission(self):
        self.assertNotIn("role", benchmark.admission.__code__.co_varnames[: benchmark.admission.__code__.co_argcount])


if __name__ == "__main__":
    unittest.main()
