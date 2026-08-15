# A4 Metrics and Pareto Rules

## Oriented metric vector

```text
(min risk, max macro utility, max minimum-task utility,
 min p95 delay, max deadline success, min ledger bytes, min evaluation time)
```

## Dominance

Configuration A dominates B within tolerance `ε` when A is no worse than B on every selected metric and better on at least one beyond `ε`.

Report the exact metric set and tolerances beside every frontier.

## Risk

- reference interval reduction;
- exact-cell recovery;
- reconstruction MAE.

Do not substitute structural coverage for reconstruction risk without showing A2 calibration.

## Utility

- per-task success;
- macro-average;
- minimum task utility;
- workload-weighted utility with visible weights.

## Availability

- p50/p95 logical delay;
- deadline success;
- transformed, delayed, and denied responses.

## Cost

- ledger entries and serialized bytes;
- policy decision time;
- provenance response overhead.

Toy microseconds are descriptive, not production latency claims.

## Uncertainty

Use paired bootstrap confidence intervals because policies share trial states and streams.

## Stability

- frontier inclusion frequency across bootstrap samples;
- inclusion frequency across workload weights;
- dominance reversal count;
- seed-subset consistency.

## Invariants

- identical trial opportunities across policies;
- oriented metrics remain documented;
- missing values never imply zero cost;
- deny-all cannot win when utility is included;
- release-all cannot win when risk is included;
- every dominated configuration has at least one recorded dominator;
- changing visualization scale cannot change computed dominance.
