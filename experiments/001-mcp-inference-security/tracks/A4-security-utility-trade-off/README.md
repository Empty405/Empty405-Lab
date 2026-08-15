# A4 Unified Pareto Benchmark

Runs release, deny, rate, quota, coverage, hybrid, and adaptive configurations on identical paired trials across six visible workload profiles and four deadlines.

```bash
python benchmark.py --runs 1000 --seed 40504
python -m unittest -v test_benchmark.py
```

Frontier membership applies only to tested configurations and declared metrics. Toy operation counts and ledger bytes are not production performance claims.
