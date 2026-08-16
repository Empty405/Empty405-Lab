# C6 Experiment Design

## Independent variables

- policy: no recovery, fixed-window reset, linear decay, exponential decay, version invalidation, evidence-based recovery, oracle;
- state regime: static, slow drift, abrupt replacement, cyclic return, deceptive version bump;
- request cadence: sparse, steady, burst, adaptive revisit;
- horizon: short, medium, long;
- 200 paired seeds per configuration.

## Minimum matrix

`7 policies × 5 state regimes × 4 request cadences × 3 horizons × 200 trials = 84,000 trials`.

## Procedure

1. Generate identical versioned hidden-state and request schedules.
2. Initialize current and lifetime ledgers.
3. Apply requests in timestamp order.
4. Estimate current marginal exposure.
5. Update recovery state using only policy-permitted evidence.
6. Admit or deny and atomically record the response.
7. Preserve every response in the lifetime evaluator.
8. Measure current utility, stale knowledge and historical reconstruction.
9. Continue through every epoch without deleting evaluator history.
10. Compare with no-recovery and oracle controls.

## Controls

- static state across all epochs;
- version bump without content change;
- complete state replacement;
- one changed unit only;
- cyclic return to an earlier state;
- duplicate-only requests;
- reset boundary immediately before a burst;
- lifetime observer with perfect memory;
- oracle under the same requests and state schedule.

## Required outputs

Request, epoch, version, structural units, change evidence, policy charge before/after, recovered capacity, current completion, stale-unit validity, lifetime union, reconstruction score, denied exposure, ledger operations and metadata cost.

## Stop conditions

Stop if reset deletes lifetime history, identical version bumps recover evidence-based capacity, cyclic state return is treated as unseen, policies receive unequal clocks or schedules, denied requests release data, or utility is reported without lifetime reconstruction.
