import csv,gzip,json,tempfile,unittest
from pathlib import Path
import c6_benchmark as benchmark
class Tests(unittest.TestCase):
 def test_matrix(self):
  with tempfile.TemporaryDirectory() as tmp:r=benchmark.run(1,Path(tmp))
  self.assertEqual((r["configurations"],r["trial_rows"]),(420,420))
 def test_default_matrix(self):self.assertEqual(7*5*4*3*200,84000)
 def test_cap(self):
  for p in benchmark.POLICIES:self.assertEqual(benchmark.simulate_trial(p,"abrupt_replacement","burst","long",1)["cap_overshoot"],0)
 def test_append_only(self):
  _,e=benchmark.simulate_episode("fixed_window_reset","static","steady","long",2);self.assertTrue(all(b["lifetime_after"]>=a["lifetime_after"] for a,b in zip(e,e[1:])))
 def test_deceptive_no_evidence_recovery(self):self.assertEqual(benchmark.simulate_trial("evidence_based_recovery","deceptive_version_bump","burst","long",3)["recovered_units"],0)
 def test_reset_keeps_history(self):
  r=benchmark.simulate_trial("fixed_window_reset","static","burst","long",4);self.assertGreater(r["reset_events"],0);self.assertGreater(r["lifetime_distinct_facts"],0)
 def test_cyclic_repeat(self):self.assertGreater(benchmark.simulate_trial("fixed_window_reset","cyclic_return","adaptive_revisit","long",5)["repeat_releases"],0)
 def test_denied_exposure(self):self.assertEqual(benchmark.simulate_trial("no_recovery","static","burst","long",6)["denied_response_exposure"],0)
 def test_duplicate_zero_cost(self):
  _,e=benchmark.simulate_episode("no_recovery","static","adaptive_revisit","long",7);self.assertTrue(any(x["admitted"] and x["marginal_cost"]==0 for x in e))
 def test_reconciliation(self):
  for p in benchmark.POLICIES:self.assertEqual(benchmark.simulate_trial(p,"slow_drift","steady","medium",8)["reconciliation_error"],0)
 def test_one_outcome(self):
  r,e=benchmark.simulate_episode("linear_decay","slow_drift","steady","medium",9);self.assertEqual(len(e),r["requests"]);self.assertTrue(all(x["terminal_outcome"] in ("completed","denied") for x in e))
 def test_raw_recomputes(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);r=benchmark.run(1,out)
   with gzip.open(out/"request-events.csv.gz","rt",newline="",encoding="utf-8") as f:e=list(csv.DictReader(f))
   json.loads((out/"benchmark.json").read_text())
  self.assertEqual(len(e),r["request_event_rows"]);self.assertEqual(set(e[0]),set(benchmark.EVENT_FIELDS))
if __name__=="__main__":unittest.main()
