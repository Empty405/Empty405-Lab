# A2 Metrics

## Request fraction

```text
released requests / total requests in canonical stream
```

Traffic baseline; not an exposure claim.

## Exact cell coverage

```text
unique released cell keys / total cell keys
```

## Tuple coverage

Unique normalized dimension tuples divided by the declared tuple universe.

## Marginal coverage

Weighted mean of per-dimension and configured pairwise coverage. Weights must be fixed before running the benchmark.

## Precision-weighted coverage

For each cell, retain the maximum released precision:

```text
weighted_coverage = mean(max_precision_per_cell)
```

Precision values are adapter declarations and must be audited separately.

## Reference interval reduction

```text
mean(1 - remaining_candidate_width / 100)
```

Experiment-only target; not available to enforcement.

## Prediction quality

For every proxy:

- Pearson correlation with reference interval reduction;
- Spearman rank correlation;
- mean absolute calibration error;
- worst-stream calibration error;
- checkpoint-level residuals.

## Operational metrics

- unique ledger entries;
- serialized ledger bytes;
- event-processing time;
- adapter mapping coverage;
- number of unmapped responses.

## Invariants

Automated tests must verify:

- all normalized exposure metrics remain in `[0, 1]`;
- exposure never decreases within a static epoch;
- identical repeats do not increase exact or weighted coverage;
- higher precision cannot reduce weighted coverage;
- a multi-cell event updates every declared key;
- unknown mappings never silently produce zero exposure;
- replaying the same immutable event log produces identical snapshots.

## Success threshold

No universal threshold is claimed. For the first benchmark, a structural proxy is considered promising if it materially and consistently exceeds request-count correlation across all declared streams and has no catastrophic calibration failure hidden by the aggregate mean.
