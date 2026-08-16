# C4 Metrics

## Budget capture

### Attacker budget capture ratio

```text
ABCR = attacker_new_exposure_units / total_new_exposure_units
```

Report alongside absolute units and remaining cap. High capture is not harmful when the same units are needed by legitimate tasks, so overlap is reported separately.

### Early capture

Fraction of the initial cap consumed by the adversarial principal before the first legitimate burst or by a fixed episode checkpoint.

### Wasted exposure ratio

```text
WER = attacker_charged_units_not_used_by_any_legitimate_task / attacker_charged_units
```

This separates competitive use from destructive burning.

## Victim harm

### Legitimate completion loss

Paired difference in useful legitimate task completion between the selected attacker strategy and volume/timing-matched benign control.

### Denial-of-information rate

Legitimate tasks that would complete under the oracle or benign control but fail because required budget was consumed earlier.

Additional measures:

- victim denial and timeout rates;
- lost synthetic task value;
- late-critical completion;
- minimum per-principal completion;
- time to first budget-caused denial.

## Allocation and fairness

- per-principal exposure allocation;
- per-principal useful completion;
- maximum-to-minimum allocation ratio;
- Jain index over legitimate utility;
- protected minimum share;
- unused reserved budget;
- cross-principal utility variance.

Fairness is never reported from raw request acceptance alone because principals may generate different useful demand.

## Security and conservation

- total released union;
- cap overshoot;
- duplicate-charge count;
- denied-response exposure;
- silent reset indicator;
- attacker novel-unit coverage;
- attacker/legitimate structural overlap;
- exposure per legitimate completed task.

## Policy quality

### Oracle regret

Difference between evaluator-only maximum legitimate task value and the deployable policy under the same cap and schedule.

### Benign efficiency loss

Legitimate utility lost under a defense when the matched client is benign rather than strategic.

### Attack suppression gain

Reduction in victim harm relative to global FIFO, jointly reported with benign efficiency loss and unused cap.

## Operational cost

- admission decisions;
- marginal-cost computations;
- principal-state reads and writes;
- ledger operations;
- audit writes;
- metadata bytes;
- denied requests per useful completion.

## Invariant tests

1. Global released union never exceeds the cap.
2. Duplicate-only attacks consume zero new budget.
3. Denied requests expose zero units.
4. Benign and strategic matched controls have equal volume and timing.
5. Per-principal charges sum to the global charge.
6. Reservation shares never create capacity.
7. No budget reset occurs across ticks.
8. Oracle uses the same requests and cap.
9. Deployable policies never read evaluator role.
10. Every request has one terminal outcome.
11. Every episode has exactly 120 ticks.
12. Raw events recompute all capture and harm aggregates.

## Reporting rule

A defense is not called successful from lower attacker acceptance alone. Every result jointly reports victim harm, legitimate utility, exposure conservation, attacker capture, unused capacity, fairness and operational cost.
