# C5 Fair Allocation Between Clients Benchmark

Standard-library simulation of fair allocation of one shared structural-disclosure budget among legitimate clients.

The default run produces exactly 84,000 paired trials:

`7 policies × 5 demand profiles × 4 weight profiles × 3 scarcity levels × 200 trials`.

Each 120-tick episode contains five durable principals, one atomic shared ledger, exact marginal exposure cost, heterogeneous demand, declared weights, and synthetic task value.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/request-events.csv.gz` — auditable request and allocation events;
- `results/benchmark.json` — summaries and confidence intervals;
- `results/figure-c5-frontier.svg` — utility–fairness–utilization frontier;
- `results/RESULTS.md` — interpretation.

The oracle is evaluator-only. Malicious behavior, Sybils, budget decay, semantic observer errors, and real-world moral priority are excluded.
