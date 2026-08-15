# A2 v0.1 Results

**Trials:** 1000 per stream  
**Streams:** 6  
**Checkpoints:** 6 per trial  
**Checkpoint rows:** 36,000  
**Root seed:** `40502`

## Answer first

The narrow A2 hypothesis received **mixed support**.

Precision-weighted coverage was the best-calibrated proxy in all six synthetic streams. Its mean absolute calibration error ranged from 0.0015 to 0.0562, compared with 0.0354 to 0.3696 for request fraction.

However, request fraction remained almost perfectly correlated with interval reduction in five controlled streams because both increased monotonically with stream progress. Correlation alone therefore did not distinguish a good exposure proxy from a clock-like progress counter. The stronger A2 result is improved **calibration**, duplicate invariance, precision escalation, and multi-cell representation—not a universal correlation advantage.

## Predictor comparison

| Stream | Request Pearson | Weighted Pearson | Request MAE | Weighted MAE |
|---|---:|---:|---:|---:|
| Unique | 1.0000 | 1.0000 | 0.0394 | 0.0048 |
| Duplicate-heavy | 1.0000 | 1.0000 | 0.1443 | 0.0059 |
| Precision escalation | 1.0000 | 1.0000 | 0.0354 | 0.0088 |
| Marginal scan | 1.0000 | 1.0000 | 0.3696 | 0.0015 |
| Multi-cell summary | 0.9976 | 0.9976 | 0.2772 | 0.0562 |
| Mixed | 0.9926 | 0.9994 | 0.0775 | 0.0383 |

## What worked

- identical repeats did not increase cell or weighted coverage;
- later higher-precision projections increased weighted exposure without increasing cell coverage;
- a regional response updated all eight declared affected cells;
- declared tool aliases shared the same cell keys;
- weighted coverage had the lowest calibration error in every stream;
- all normalized metrics remained bounded and monotonic after correcting the tuple universe.

## What failed or remained weak

### Correlation was insufficient

Request fraction achieved Pearson correlation near one even when its absolute exposure estimate was badly wrong. A monotonically advancing counter can correlate with a monotonically advancing target without measuring the same quantity.

### Marginal coverage overestimated knowledge

The marginal-scan stream quickly covered every location and epoch while touching only two of eight resources. Marginal coverage therefore reported broad coverage despite limited cell-level knowledge. Its calibration MAE reached 0.5867.

### Regional summaries exposed adapter sensitivity

The regional-summary adapter declared precision 0.25 per affected cell, but actual interval reduction depended on whether the hidden value fell below the scarcity threshold. Weighted coverage remained useful but its MAE rose to 0.0562. The precision weight is policy configuration, not an objective fact.

## Required counterexamples

### Overestimate

Dimension-marginal coverage overestimates knowledge when a stream touches all locations but only a small resource subset.

### Underestimate

Exact cell coverage underestimates added knowledge during precision escalation: availability, band, and numeric range all touch the same cell, so cell coverage stays constant while the candidate interval shrinks.

## Hypothesis decision

The claim that structural proxies universally correlate better than request count is **not supported** by this benchmark. The narrower claim that precision-weighted structural coverage is better calibrated and represents duplicates, precision escalation, and multi-cell disclosures more faithfully is **provisionally supported** for declared synthetic adapters.

## Limitations

- adapter mappings and precision weights are declared manually;
- deterministic interval observer;
- synthetic state and schemas;
- no semantic equivalence beyond one declared alias;
- no observer priors, identity rotation, collusion, or distributed ledgers;
- checkpoint correlation is influenced by monotonic stream progress.

## Reproduction

```bash
python benchmark.py --runs 1000 --seed 40502
python plot_results.py
python -m unittest -v test_benchmark.py
```

Raw checkpoints are stored in `checkpoints.csv.gz`; aggregate metrics are in `benchmark.json`.
