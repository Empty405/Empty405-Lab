# C3 Metrics

## Availability outcomes

### Task completion rate

```text
TCR = completed_logical_tasks / admitted_logical_tasks
```

### Denial and timeout rates

Report terminal denial and deadline expiry separately. A fast denial is not a successful low-latency response.

### Useful-response rate

Responses meeting the task's minimum synthetic quality threshold, excluding empty acknowledgements and policy errors.

### Degraded and stale response rates

Report reduced-quality and outdated-but-precharged responses separately.

## Latency

- time to first useful response;
- task completion latency;
- p50, p95 and p99 latency;
- queue wait;
- retry delay;
- recovery completion time;
- deadline slack at completion.

Timeouts are represented as terminal outcomes, not silently removed from latency analysis.

## Queue stability

- mean and peak queue length;
- admitted, queued, retried, dropped and expired tasks;
- queue growth per tick during sustained load;
- recovery drain rate;
- backlog remaining at episode end;
- duplicate execution count.

## Security

### Availability-induced exposure gain

```text
AIEG = |released_union_after_episode - initial_exposure_union| / |disclosure_universe|
```

### Fail-open violation rate

Logical tasks releasing at least one unauthorized new unit while the authorization dependency is unavailable.

Additional measures:

- new units per successful task;
- contaminated-fallback acceptance;
- post-recovery unresolved violations;
- silent budget reset indicator;
- stale-safe versus novel response separation.

## Response quality

- exact, replay, snapshot, degraded and fail-open quality;
- task requirement coverage;
- specificity retained;
- safe fallback adequacy;
- stale age at response.

## Operational cost

- dependency calls;
- classifier and policy reads;
- retry operations;
- queue writes;
- audit writes;
- metadata bytes;
- fallback-store dependency indicator.

## Invariant tests

1. Healthy oracle completes every task satisfiable without new exposure.
2. Hard deny never creates exposure.
3. Fail-open exposure remains recorded after recovery.
4. Retry does not increase logical task count.
5. Expired tasks never execute.
6. Queue capacity is never exceeded.
7. Pre-charged snapshots add zero exposure.
8. Contaminated fallback is denied or counted as a violation.
9. Recovery changes dependency state, not budget or deadlines.
10. Every trial contains exactly 120 ticks.

## Reporting rule

No policy is called available from response count alone. Every comparison jointly reports useful task completion, denial, timeout, latency tails, queue stability, response quality and exposure violations.
