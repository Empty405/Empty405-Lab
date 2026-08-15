# C2 Budget Exhaustion Benchmark

Standard-library simulation of immediate policy behavior after a shared structural exposure budget reaches its exact cap.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
python plot_results.py
```

The default run produces exactly 54,000 paired trials:

`6 policies × 5 post-cap workloads × 3 budgets × 3 task-criticality classes × 200 trials`.

## Compared policies

- hard deny;
- replay-only;
- coarse fallback with an explicitly uncharged structural namespace;
- pre-charged safe snapshot;
- bounded five-unit override;
- evaluator-only cap-aware oracle.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/benchmark.json` — configuration summaries and confidence intervals;
- `results/figure-c2-frontier.svg` — post-cap security–utility frontier;
- `results/RESULTS.md` — interpretation, falsification status, and limitations.

Every trial begins with an exact C1 ledger at cap. Criticality is a synthetic sensitivity label, not authorization, emergency-access policy, or legal priority.
