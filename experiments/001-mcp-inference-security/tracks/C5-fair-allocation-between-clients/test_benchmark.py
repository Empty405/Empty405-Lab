import csv,gzip,json,tempfile,unittest
from pathlib import Path
import benchmark

class Tests(unittest.TestCase):
    def test_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:r=benchmark.run(1,Path(tmp))
        self.assertEqual(r["configurations"],420);self.assertEqual(r["trial_rows"],420)
    def test_default_matrix(self):self.assertEqual(7*5*4*3*200,84_000)
    def test_cap(self):
        for p in benchmark.POLICIES:
            r=benchmark.simulate_trial(p,"asymmetric_heavy","misspecified","severe",1);self.assertEqual(r["cap_overshoot"],0)
    def test_reconciliation(self):
        for p in benchmark.POLICIES:
            r=benchmark.simulate_trial(p,"balanced_burst","equal","moderate",2);self.assertEqual(r["reconciliation_error"],0)
    def test_denied_exposure(self):
        r=benchmark.simulate_trial("equal_reservation","asymmetric_heavy","equal","severe",3);self.assertEqual(r["denied_response_exposure"],0)
    def test_no_reset(self):
        r=benchmark.simulate_trial("bounded_borrowing","late_high_value","equal","moderate",4);self.assertEqual(r["silent_budget_reset"],0)
    def test_borrowing_bounded(self):
        _,events=benchmark.simulate_episode("bounded_borrowing","asymmetric_heavy","equal","moderate",5);self.assertTrue(all(e["borrowed_units"]<=4 for e in events))
    def test_inactive_not_starved(self):
        r=benchmark.simulate_trial("equal_reservation","sparse_clients","equal","moderate",6);self.assertLessEqual(r["starved_principals"],3)
    def test_one_event(self):
        r,e=benchmark.simulate_episode("progressive_max_min","balanced_steady","equal","moderate",7);self.assertEqual(len(e),r["requests"]);self.assertEqual(len({x["request_id"] for x in e}),len(e))
    def test_120_ticks(self):self.assertEqual(benchmark.simulate_trial("global_fifo","balanced_steady","equal","mild",8)["episode_ticks"],120)
    def test_raw_recomputes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);r=benchmark.run(1,out)
            with gzip.open(out/"request-events.csv.gz","rt",encoding="utf-8",newline="") as h:e=list(csv.DictReader(h))
            json.loads((out/"benchmark.json").read_text())
        self.assertEqual(len(e),r["request_event_rows"]);self.assertEqual(set(e[0]),set(benchmark.EVENT_FIELDS))
    def test_non_oracle_no_value_argument(self):self.assertNotIn("value",benchmark.decide.__code__.co_varnames[:benchmark.decide.__code__.co_argcount])
if __name__=="__main__":unittest.main()
