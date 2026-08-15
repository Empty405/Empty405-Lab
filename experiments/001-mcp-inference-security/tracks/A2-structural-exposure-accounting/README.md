# A2 Structural Exposure Accounting Benchmark

This dependency-free benchmark compares request fraction, normalized tuple coverage, exact cell coverage, marginal coverage, and precision-weighted coverage against deterministic observer interval reduction.

```bash
python benchmark.py --runs 1000 --seed 40502
python -m unittest -v test_benchmark.py
```

The benchmark includes unique, duplicate-heavy, precision-escalation, marginal-scan, multi-cell-summary, and mixed streams. Structural scores are experimental proxies, not semantic knowledge or privacy guarantees.
