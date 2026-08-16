# C3 Availability Degradation Benchmark

Standard-library simulation of service availability when exposure-accounting dependencies slow down, fail, partition, or recover under backlog.

```bash
python -m unittest -v test_benchmark.py
python benchmark.py
python plot_results.py
```

The default run produces exactly 63,000 paired trials and 3,024,000 auditable task events:

`7 policies × 5 disruptions × 3 workload intensities × 3 task-criticality classes × 200 trials`.

Each episode lasts 120 abstract ticks. Retry attempts preserve the original logical task, deadline, and fixed C1–C2 exposure state.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/task-events.csv.gz` — raw task events used to recompute latency and recovery metrics;
- `results/benchmark.json` — configuration summaries and confidence intervals;
- `results/figure-c3-frontier.svg` — security–availability frontier;
- `results/RESULTS.md` — interpretation after the full run.

Fail-open is an intentionally unsafe comparison baseline. The oracle is evaluator-only, and criticality never authorizes bypass.
