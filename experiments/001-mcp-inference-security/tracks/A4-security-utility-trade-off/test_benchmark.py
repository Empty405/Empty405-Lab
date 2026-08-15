import unittest
from benchmark import CONFIGS, DEADLINES, PROFILES, dominates, policy_decision, run

class A4Tests(unittest.TestCase):
 def test_metric_bounds(self):
  for policy in CONFIGS:
   row=run(0,"balanced","medium",policy,40504)
   for f in ("risk","exact_recovery","macro_utility","minimum_task_utility","weighted_utility","deadline_success"):
    self.assertTrue(0<=getattr(row,f)<=1,(policy,f,getattr(row,f)))
 def test_release_and_deny_sanity(self):
  release=run(0,"balanced","patient","release_all",40504);deny=run(0,"balanced","patient","deny_all",40504)
  self.assertGreater(release.risk,deny.risk);self.assertGreater(release.weighted_utility,deny.weighted_utility)
 def test_rate_deadline_boundary(self):
  patient=run(0,"balanced","patient","rate_10",40504);short=run(0,"balanced","short","rate_10",40504)
  self.assertGreater(patient.risk,short.risk);self.assertGreater(patient.p95_delay,short.p95_delay)
 def test_dominance(self):
  a={"risk":.2,"p95_delay":0,"ledger_bytes":1,"decision_ops":1,"weighted_utility":.8,"minimum_task_utility":.5,"deadline_success":.8}
  b={"risk":.3,"p95_delay":1,"ledger_bytes":2,"decision_ops":2,"weighted_utility":.7,"minimum_task_utility":.4,"deadline_success":.7}
  self.assertTrue(dominates(a,b));self.assertFalse(dominates(b,a))
 def test_adaptive_monotonic(self):
  levels=[policy_decision("adaptive_balanced",i,float("inf"))[0] for i in range(96)]
  self.assertEqual(levels,sorted(levels))

if __name__=="__main__":unittest.main()
