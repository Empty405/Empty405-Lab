# A3 v0.1 Results

**Trials:** 1000 per mode  
**Modes:** 22 (exact, 18 hard caps, 3 adaptive profiles)  
**Root seed:** `40503`

## Answer first

The tested adaptive precision ladders **did not outperform hard blocking on macro task utility at matched interval-reduction risk**. The primary A3 hypothesis is therefore not supported by v0.1.

Risk matching was close: gaps ranged from 0.001 to 0.005. All three adaptive profiles had lower macro utility than their nearest hard-block comparator.

Adaptive disclosure did redistribute utility. It improved category and aggregate tasks, but sharply reduced exact-task utility. Whether that trade is desirable depends on task weights; equal macro weighting does not justify a general utility advantage.

## Matched-risk frontier

| Adaptive profile | Adaptive risk | Adaptive utility | Hard comparator | Hard risk | Hard utility | Utility delta |
|---|---:|---:|---|---:|---:|---:|
| Conservative | 0.463 | 0.450 | Hard 0.45 | 0.458 | 0.458 | -0.009 |
| Balanced | 0.655 | 0.631 | Hard 0.65 | 0.656 | 0.656 | -0.026 |
| Permissive | 0.751 | 0.719 | Hard 0.75 | 0.750 | 0.750 | -0.031 |

## Task redistribution

| Mode | Threshold | Category | Planning | Exact | Aggregate |
|---|---:|---:|---:|---:|---:|
| Adaptive conservative | 0.475 | 0.552 | 0.406 | 0.107 | 0.708 |
| Matched hard 0.45 | 0.458 | 0.458 | 0.458 | 0.458 | 0.458 |
| Adaptive balanced | 0.669 | 0.760 | 0.604 | 0.212 | 0.906 |
| Matched hard 0.65 | 0.656 | 0.656 | 0.656 | 0.656 | 0.656 |
| Adaptive permissive | 0.767 | 0.854 | 0.708 | 0.306 | 0.958 |
| Matched hard 0.75 | 0.750 | 0.750 | 0.750 | 0.750 | 0.750 |

## Composition and provenance

The deterministic nested transformations passed the v0.1 invariants:

- interval widths increased monotonically from L0 through L3;
- exposure never restored a more precise level;
- identical inputs and policy state produced identical outputs;
- every response carried the required provenance fields;
- A3 responses declared `synthetic=false`.

## Negative randomized control

Eight randomized width-19 ranges around the same value intersected to width **5**. This demonstrates that independently randomized degraded ranges can reveal substantially more through repeated sampling. The negative control is not a proposed defense.

## Hypothesis decision

The general claim that adaptive disclosure preserves more utility than hard blocking is **falsified for the equal-weight task mix and three ladders tested here**.

A narrower statement survives: adaptive disclosure can deliberately prioritize coarse category and aggregate tasks over exact tasks while retaining deterministic composition and provenance. That is a policy trade, not a universal improvement.

## Limitations

- one unique-query stream over static integer cells;
- equal weighting of five synthetic task families;
- interval reduction used as the matching risk metric;
- stable principal and exact A2 ledger;
- L4 aggregate utility simplified to regional-band availability;
- no cross-tool aliases in the benchmark implementation;
- no empirical production workload.

## Next experiment

Before changing the ladder, collect or define realistic task weights. Optimizing thresholds without a justified workload would tune the benchmark rather than validate the mechanism.

## Reproduction

```bash
python benchmark.py --runs 1000 --seed 40503
python plot_results.py
python -m unittest -v test_benchmark.py
```
