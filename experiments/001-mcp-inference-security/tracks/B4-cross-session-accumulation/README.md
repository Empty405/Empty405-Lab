# B4 Cross-session Accumulation Benchmark

Standard-library simulation that keeps observer memory separate from reset, TTL, rolling-window, persistent, and exponentially decayed server accounting.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
```

The default run produces 540,000 raw trial rows across 1,080 configurations with exactly 96 requests in every trial.

The fixture is static hidden state and synthetic logical time. Lower policy-accounted exposure must not be interpreted as observer forgetting.
