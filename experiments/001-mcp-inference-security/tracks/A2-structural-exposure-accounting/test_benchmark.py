import random
import unittest

from benchmark import Ledgers, TOTAL_CELLS, make_stream, run_trial, single, state


class A2Tests(unittest.TestCase):
    def test_all_streams_run(self):
        for name in ("unique", "duplicate-heavy", "precision-escalation", "marginal-scan", "multi-cell-summary", "mixed"):
            self.assertEqual(len(run_trial(0, name, 40502)), 6)

    def test_duplicate_invariance(self):
        hidden = state(random.Random(1)); ledger = Ledgers(); event = single("capacity_band", 0, 0, 0)
        ledger.apply(event, hidden); first = ledger.snapshot(1)
        ledger.apply(event, hidden); second = ledger.snapshot(2)
        self.assertEqual(first["cell_coverage"], second["cell_coverage"])
        self.assertEqual(first["weighted_coverage"], second["weighted_coverage"])

    def test_precision_escalation(self):
        hidden = state(random.Random(1)); ledger = Ledgers()
        ledger.apply(single("availability", 0, 0, 0), hidden); low = ledger.snapshot(1)
        ledger.apply(single("numeric_range", 0, 0, 0), hidden); high = ledger.snapshot(2)
        self.assertEqual(low["cell_coverage"], high["cell_coverage"])
        self.assertGreater(high["weighted_coverage"], low["weighted_coverage"])
        self.assertGreater(high["reference_exposure"], low["reference_exposure"])

    def test_multi_cell_updates_eight_keys(self):
        event = make_stream("multi-cell-summary", random.Random(1))[0]
        hidden = state(random.Random(1)); ledger = Ledgers(); ledger.apply(event, hidden)
        self.assertEqual(len(ledger.cells), 8)

    def test_bounds_and_monotonicity(self):
        rows = run_trial(0, "mixed", 40502)
        for name in ("tuple_coverage", "cell_coverage", "marginal_coverage", "weighted_coverage", "reference_exposure"):
            values = [getattr(row, name) for row in rows]
            self.assertTrue(all(0 <= value <= 1 for value in values))
            self.assertEqual(values, sorted(values))


if __name__ == "__main__":
    unittest.main()
