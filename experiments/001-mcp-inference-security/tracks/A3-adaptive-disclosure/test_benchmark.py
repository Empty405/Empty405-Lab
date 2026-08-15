import unittest
from benchmark import PROFILES, adaptive_level, answer, nested_interval, provenance, randomized_sampling_violation, run

class A3Tests(unittest.TestCase):
    def test_nested_intervals(self):
        widths=[]
        for level in ("L0","L1","L2","L3"):
            lo,hi=nested_interval(53,level); widths.append(hi-lo)
            self.assertTrue(lo<=53<=hi)
        self.assertEqual(widths,sorted(widths))

    def test_monotonic_levels(self):
        levels=[adaptive_level(i/100,PROFILES["adaptive_balanced"]) for i in range(101)]
        self.assertEqual(levels,sorted(levels))

    def test_deterministic_response(self):
        self.assertEqual(answer(53,50,"L2","test"),answer(53,50,"L2","test"))

    def test_provenance_complete(self):
        required={"level","freshness_epoch","transformed","synthetic","reason","policy_version"}
        self.assertTrue(required<=provenance("L3","test").keys())
        self.assertFalse(provenance("L3","test")["synthetic"])

    def test_randomized_negative_control_narrows(self):
        lo,hi=randomized_sampling_violation(40503)
        self.assertLess(hi-lo,19)

    def test_trial_metrics_bounded(self):
        row=run(0,"adaptive_balanced",40503)
        for value in row.__dict__.values():
            if isinstance(value,float): self.assertTrue(0<=value<=1)

if __name__=="__main__": unittest.main()
