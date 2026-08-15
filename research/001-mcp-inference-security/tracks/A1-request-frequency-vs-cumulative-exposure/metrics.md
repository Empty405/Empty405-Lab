# A1 Metrics

## Final observable state

```text
unique coverage keys released / total coverage keys
```

Range: `[0, 1]`. This is the primary A1 disclosure metric.

## Reconstruction score

Use the existing Research 001 observer scoring rule for compatibility with v0.1. Report its definition beside every result. Do not treat it as semantic information gain.

## Time to exposure threshold

For threshold `t ∈ {0.25, 0.50, 0.75, 0.90}`:

```text
minimum logical time at which observable_state >= t
```

If never reached, report right-censored rather than substituting the run duration.

## Exposure per released response

```text
new coverage keys / released responses
```

This detects duplicate-heavy workloads and distinguishes request count from new disclosure.

## Final convergence gap

```text
baseline_final_exposure - policy_final_exposure
```

Evaluate as the observer deadline increases. A resettable rate limiter should approach zero gap under the patient-observer model.

## Legitimate utility

Fraction of predefined legitimate task queries successfully answered before their task deadline.

Utility must use a workload distinct from full-space enumeration.

## Availability cost

Report:

- delayed legitimate responses;
- denied legitimate responses;
- p50/p95 logical delay;
- task-deadline misses.

## Accounting overhead

For the toy benchmark:

- number of rate-counter entries;
- number of exact coverage keys;
- policy evaluation time.

These measurements characterize the experiment only; they are not production benchmarks.

## Metric invariants

Automated tests must verify:

- observable state never decreases in a static run;
- observable state never exceeds 1;
- released-query count never exceeds attempted-query count;
- exact coverage cannot exceed its configured cap;
- delayed responses do not enter the observer before release;
- identical ledgers produce identical metrics.
