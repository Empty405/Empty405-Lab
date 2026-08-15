import tempfile, unittest
from pathlib import Path
import benchmark


class BenchmarkTests(unittest.TestCase):
    def test_fixed_request_count(self):
        for pool in benchmark.POOL_SIZES:
            self.assertEqual(len(benchmark.query_plan(pool,"partition",__import__('random').Random(1))),100)

    def test_single_identity_respects_budget(self):
        for scope in benchmark.SCOPES:
            row=benchmark.simulate_trial(1,scope,"partition",.25,"missing",1)
            self.assertLessEqual(row["exposure"],.25)

    def test_oracle_is_pool_invariant(self):
        for pool in benchmark.POOL_SIZES:
            row=benchmark.simulate_trial(pool,"oracle","partition",.50,"missing",2)
            self.assertEqual(row["exposure"],.50)

    def test_per_identity_pool_multiplies_budget(self):
        one=benchmark.simulate_trial(1,"per_identity","partition",.25,"clean",3)
        many=benchmark.simulate_trial(4,"per_identity","partition",.25,"clean",3)
        self.assertEqual(one["exposure"],.25); self.assertEqual(many["exposure"],1.0)

    def test_duplicate_coordination_wastes_coverage(self):
        duplicate=benchmark.simulate_trial(4,"per_identity","duplicate",.25,"clean",4)
        partition=benchmark.simulate_trial(4,"per_identity","partition",.25,"clean",4)
        self.assertLess(duplicate["exposure"],partition["exposure"])

    def test_metrics_bounded(self):
        row=benchmark.simulate_trial(64,"attributed_cluster","random",.75,"missing",5)
        for metric in ("exposure","false_split_rate","legitimate_utility"):
            self.assertGreaterEqual(row[metric],0); self.assertLessEqual(row[metric],1)

    def test_small_run_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=benchmark.run(1,Path(tmp))
            self.assertEqual(result["trial_rows"],1512)
            self.assertEqual(result["configurations"],1512)


if __name__=="__main__": unittest.main()
