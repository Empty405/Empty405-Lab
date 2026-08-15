import random,tempfile,unittest
from pathlib import Path
import benchmark

class Tests(unittest.TestCase):
 def test_fixed_total_requests(self):
  for n in benchmark.COALITIONS:self.assertEqual(len(benchmark.query_plan(n,'low','independent',random.Random(1))),96)
 def test_one_observer_has_zero_coalition_gain(self):
  for p in benchmark.POLICIES:
   r=benchmark.simulate_trial(1,'low','partitioned',p,.25,1);self.assertAlmostEqual(r['coalition_gain'],0)
 def test_oracle_union_respects_budget(self):
  for n in benchmark.COALITIONS:
   r=benchmark.simulate_trial(n,'disjoint','partitioned','oracle',.25,2);self.assertLessEqual(r['coalition_reconstruction'],.25)
 def test_per_client_collusion_exceeds_individual(self):
  r=benchmark.simulate_trial(8,'disjoint','partitioned','per_client',.25,3);self.assertGreater(r['coalition_reconstruction'],r['max_individual_reconstruction'])
 def test_overlap_reduces_union(self):
  low=benchmark.simulate_trial(8,'disjoint','overlapping','per_client',.25,4)
  high=benchmark.simulate_trial(8,'high','overlapping','per_client',.25,4)
  self.assertGreater(low['coalition_reconstruction'],high['coalition_reconstruction'])
 def test_metrics_bounded(self):
  r=benchmark.simulate_trial(32,'medium','independent','behavioral_cohort',.75,5)
  for m in ('coalition_reconstruction','max_individual_reconstruction','complementarity_efficiency','legitimate_group_utility'):
   self.assertGreaterEqual(r[m],0);self.assertLessEqual(r[m],1)
 def test_small_run_count(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=benchmark.run(1,Path(tmp));self.assertEqual(r['trial_rows'],1296);self.assertEqual(r['configurations'],1296)
if __name__=='__main__':unittest.main()
