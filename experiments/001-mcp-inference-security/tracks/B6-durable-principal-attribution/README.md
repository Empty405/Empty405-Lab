# B6 Durable Principal Attribution Benchmark

Standard-library simulation of exposure-budget continuity when a principal rotates tokens, accounts, devices, or credentials. It compares session, account, global-ID, pairwise-pseudonym, anonymous-credential, and evaluator-only oracle attribution.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
python plot_results.py
```

The default run produces exactly 108,000 paired trials:

`6 mechanisms × 5 lifecycle conditions × 4 adversarial/failure conditions × 3 budgets × 300 trials`.

Ground-truth principal identifiers remain evaluator-only. The deployable attribution function receives synthetic credential evidence, never evaluator truth.

## Outputs

- `results/trials.csv.gz` — raw trial rows;
- `results/benchmark.json` — configuration summaries and confidence intervals;
- `results/figure-b6-frontier.svg` — security–privacy frontier summary;
- `results/RESULTS.md` — interpretation, limits, and falsification status.

This is a synthetic structural benchmark, not proof of legal identity, production readiness, or semantic privacy protection.
