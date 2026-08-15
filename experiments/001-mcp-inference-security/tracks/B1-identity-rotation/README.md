# B1 Identity Rotation Benchmark

Reproducible standard-library simulation for the B1 design. It measures how sequential visible-identity rotation changes cumulative exposure when the true durable principal remains constant.

## Run

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
```

The default run writes 324,000 paired trial rows to `results/trials.csv.gz` and aggregate confidence intervals to `results/benchmark.json`.

## Matrix

- 6 rotation counts;
- 6 attribution strategies;
- 3 exposure budgets;
- 3 synthetic signal-quality assumptions;
- 1,000 trials per configuration.

## Interpretation boundary

Attribution probabilities are declared simulation inputs, not empirical claims about real people or production fingerprinting. The oracle is an unreachable upper bound and cannot be used as a deployable policy.
