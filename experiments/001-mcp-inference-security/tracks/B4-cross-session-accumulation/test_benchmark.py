import random,tempfile,unittest
from pathlib import Path
import benchmark
class Tests(unittest.TestCase):
 def test_fixed_requests(self):
  for n in benchmark.SESSIONS:self.assertEqual(sum(benchmark.partition_requests(n)),96)
 def test_one_session_reset_respects_budget(self):
  r=benchmark.simulate_trial(1,'session_reset','long',.25,'partitioned',1);self.assertEqual(r['observer_known_exposure'],.25)
 def test_persistent_is_session_invariant(self):
  for n in benchmark.SESSIONS:
   r=benchmark.simulate_trial(n,'persistent','long',.25,'partitioned',2);self.assertEqual(r['observer_known_exposure'],.25)
 def test_session_reset_accumulates(self):
  one=benchmark.simulate_trial(1,'session_reset','short',.25,'partitioned',3);many=benchmark.simulate_trial(8,'session_reset','short',.25,'partitioned',3);self.assertGreater(many['observer_known_exposure'],one['observer_known_exposure'])
 def test_decay_does_not_erase_observer_memory(self):
  r=benchmark.simulate_trial(8,'exponential_decay','long',.25,'partitioned',4);self.assertGreaterEqual(r['observer_known_exposure'],r['policy_accounted_exposure'])
 def test_duplicate_workload_limits_accumulation(self):
  d=benchmark.simulate_trial(32,'session_reset','long',.25,'duplicate_heavy',5);p=benchmark.simulate_trial(32,'session_reset','long',.25,'partitioned',5);self.assertLess(d['observer_known_exposure'],p['observer_known_exposure'])
 def test_small_run_count(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=benchmark.run(1,Path(tmp));self.assertEqual(r['trial_rows'],1080);self.assertEqual(r['configurations'],1080)
if __name__=='__main__':unittest.main()
