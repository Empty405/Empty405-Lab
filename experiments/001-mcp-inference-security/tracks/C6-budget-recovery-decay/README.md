# C6 Budget Recovery / Decay Benchmark

Standard-library paired simulation of disclosure-budget recovery across versioned hidden state while an evaluator preserves append-only lifetime history.

The default run produces exactly 84,000 trials:

`7 policies × 5 state regimes × 4 request cadences × 3 horizons × 200 trials`.

Outputs are `results/trials.csv.gz`, `results/request-events.csv.gz`, and `results/benchmark.json`. The oracle is evaluator-only. Synthetic evidence is deliberately separated from state-change ground truth.
