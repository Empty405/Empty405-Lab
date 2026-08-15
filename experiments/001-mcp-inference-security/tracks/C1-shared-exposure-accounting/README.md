# C1 Shared Exposure Accounting Benchmark

Standard-library simulation of one structural exposure budget shared by four decision replicas under concurrency, delayed synchronization, and network partition.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
python plot_results.py
```

The default run produces exactly 54,000 paired trials:

`6 mechanisms × 5 workloads × 3 synchronization conditions × 3 budgets × 200 trials`.

## Compared mechanisms

- independent local ledgers;
- synchronous central exact ledger;
- eventual merge ledger;
- hierarchical fixed reservations;
- escrow rights;
- evaluator-only oracle.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/benchmark.json` — configuration summaries and confidence intervals;
- `results/figure-c1-frontier.svg` — security–coordination frontier;
- `results/RESULTS.md` — interpretation, falsification status, and limitations.

Budget-domain membership is fixed evaluator input from the B6 scope. C1 tests accounting conservation, not identity attribution, semantic equivalence, fair allocation, or temporal recovery.
