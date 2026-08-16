# C4 Malicious Budget Consumption Benchmark

Standard-library simulation of strategic exhaustion of a shared structural-disclosure budget.

```bash
python -m unittest -v test_benchmark.py
python benchmark.py
```

The default run produces exactly 75,600 paired trials:

`7 policies × 6 traffic strategies × 3 attack intensities × 3 legitimate workloads × 200 trials`.

Each 120-tick episode uses four legitimate principals, one adversarial principal, one atomic shared ledger, a fixed cap, and exact structural marginal cost. Deployable policies never receive evaluator role labels or future task value.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/request-events.csv.gz` — auditable request-level decisions and ledger transitions;
- `results/benchmark.json` — configuration summaries and confidence intervals;
- `results/RESULTS.md` — interpretation after the full run.

The oracle is evaluator-only. Identity rotation, Sybils, budget decay, distributed races, and semantic observer error are intentionally excluded.
