import random,tempfile,unittest
from pathlib import Path
import benchmark
class Tests(unittest.TestCase):
 def test_fixed_requests(self):
  for n in benchmark.SERVERS:self.assertEqual(len(benchmark.request_plan(n,'low',random.Random(1))),96)
 def test_one_server_respects_budget(self):
  for m in benchmark.MODELS:
   if m=='central':sync='healthy'
   else:sync='partitioned'
   r=benchmark.simulate_trial(1,m,'disjoint',sync,.25,1);self.assertLessEqual(r['aggregate_exposure'],.28 if m=='sketch' else .25)
 def test_local_servers_multiply_budget(self):
  one=benchmark.simulate_trial(1,'local','disjoint','healthy',.25,2);many=benchmark.simulate_trial(4,'local','disjoint','healthy',.25,2);self.assertGreater(many['aggregate_exposure'],one['aggregate_exposure'])
 def test_oracle_is_server_invariant(self):
  for n in benchmark.SERVERS:
   r=benchmark.simulate_trial(n,'oracle','disjoint','partitioned',.25,3);self.assertEqual(r['aggregate_exposure'],.25)
 def test_partition_increases_eventual_exposure(self):
  healthy=benchmark.simulate_trial(16,'eventual','disjoint','healthy',.25,4);part=benchmark.simulate_trial(16,'eventual','disjoint','partitioned',.25,4);self.assertGreater(part['aggregate_exposure'],healthy['aggregate_exposure'])
 def test_central_partition_fails_closed(self):
  r=benchmark.simulate_trial(8,'central','low','partitioned',.25,5);self.assertEqual(r['aggregate_exposure'],0);self.assertEqual(r['legitimate_utility'],0)
 def test_small_run_count(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=benchmark.run(1,Path(tmp));self.assertEqual(r['trial_rows'],1296);self.assertEqual(r['configurations'],1296)
if __name__=='__main__':unittest.main()
