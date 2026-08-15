# B2 Coordinated Sybil Benchmark

Standard-library simulation of one controller coordinating many parallel visible identities while total attacker request volume remains fixed.

## Run

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
```

The default matrix contains 1,512 configurations and 500 trials each: 756,000 compressed raw rows.

## Interpretation boundary

Linkage, false-merge and proof-cost parameters are synthetic model inputs. They are not empirical estimates and do not justify production fingerprinting or proof-of-personhood.
