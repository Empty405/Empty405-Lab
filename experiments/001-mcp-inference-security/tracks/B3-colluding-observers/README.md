# B3 Colluding Observers Benchmark

Standard-library simulation of independent authenticated observers that receive individually permitted disclosures and combine them through full post-hoc exchange.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
```

The default run creates 648,000 raw trial rows across 1,296 configurations while holding total coalition traffic to 96 requests.

Server-side policies never receive coalition ground truth or future exchange information. Detector and false-suspicion probabilities are synthetic model inputs, not empirical claims.
