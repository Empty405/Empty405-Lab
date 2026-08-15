# A3 Adaptive Disclosure Benchmark

Compares three deterministic nested precision ladders with hard blocking at the nearest achievable interval-reduction risk.

```bash
python benchmark.py --runs 1000 --seed 40503
python -m unittest -v test_benchmark.py
```

The randomized-range function is a negative control showing how repeated non-deterministic ranges can intersect into a more precise answer. It is not a proposed defense.
