# C5 Metrics

## Utility

### Total legitimate utility

```text
TLU = sum(completed_task_value)
```

### Utility completion ratio

Completed synthetic value divided by feasible requested value, reported globally and per active principal.

### Oracle regret

Difference between evaluator-only maximum feasible task value and policy-completed value under the same cap.

## Starvation

An active principal is starved when it has feasible positive demand but receives zero useful completion while another principal consumes positive new exposure.

Report:

- starved principal count;
- starvation episode rate;
- minimum active-principal utility;
- longest denial streak;
- time to first useful completion.

Inactive principals are excluded from starvation denominators.

## Fairness

### Jain utility index

Computed across active principals from completed utility, with zero-demand principals excluded and zero-allocation episodes reported separately.

### Allocation share error

Absolute difference between actual exposure share and declared target share.

### Envy count

Number of ordered principal pairs where one principal would obtain higher completed utility under the other's allocation, using evaluator-only counterfactual replay.

Additional measures:

- max/min utility ratio;
- generalized-entropy inequality;
- protected minimum guarantee;
- share-violation count;
- ordering sensitivity.

## Utilization

- total charged units / cap;
- remaining cap;
- unused reserved units;
- borrowed and lent units;
- stranded capacity;
- replay utilization;
- useful utility per charged exposure unit.

## Conservation and safety

- cap overshoot;
- duplicate-charge count;
- denied-response exposure;
- per-principal/global reconciliation error;
- silent budget reset;
- unaccounted borrowing;
- request terminal-outcome count.

## Weight robustness

- utility loss under misspecified weights;
- starvation change under misspecification;
- allocation-share error;
- ranking reversal between declared-weight and equal-weight outcomes.

## Operational cost

- allocation state reads/writes;
- marginal-cost computations;
- queue/defer operations;
- ledger operations;
- audit writes;
- metadata bytes;
- decisions per useful completion.

## Invariant tests

1. Global charge never exceeds cap.
2. Per-principal charges sum to global charge.
3. Duplicate-only workload consumes zero new exposure.
4. Denied requests expose zero units.
5. All paired policies receive identical request sets.
6. Reservations sum to at most the cap.
7. Borrowing is explicit and bounded.
8. Inactive principals are excluded from starvation.
9. Oracle uses the same cap and requests.
10. Non-oracle policies cannot read evaluator task value.
11. Every request has one terminal outcome.
12. Raw events recompute utility, allocation and conservation aggregates.

## Reporting rule

No policy is called fair from one scalar index. Every result jointly reports total utility, minimum active-client utility, starvation, inequality, envy, utilization, exposure conservation, oracle regret and operational cost.
