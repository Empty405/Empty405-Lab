# C6 Metrics

## Utility and recovery

- current task-completion rate;
- useful response rate;
- recovered capacity;
- time from exhaustion to next useful completion;
- unused recovered capacity;
- recovery precision: recovered units truly obsolete / recovered units;
- recovery recall: obsolete charged units recovered / obsolete charged units.

## Historical risk

### Lifetime exposure

Union of all versioned structural facts ever released to the observer.

### Repeat-release amplification

Facts released again after policy recovery divided by distinct lifetime facts.

### Historical reconstruction score

Fraction of versioned hidden state reconstructable from the complete response history.

### False forgetting

Capacity restored for facts that remain valid, recur later, or still improve reconstruction.

## Freshness

- current-valid released units;
- obsolete released units;
- stale response rate;
- version-lag distribution;
- change-detector false positive and false negative rates.

## Conservation

- current charge;
- lifetime charge;
- recovered units;
- reset events;
- charge/recovery reconciliation error;
- cap overshoot;
- denied-response exposure;
- silent lifetime-history deletion.

## Operational cost

Clock reads, version reads, detector calls, ledger writes, historical index bytes and audit writes.

## Invariant tests

1. Lifetime history is append-only.
2. Static state never justifies evidence-based recovery.
3. Version-only bump restores no verified capacity.
4. Fixed reset does not erase lifetime exposure.
5. Cyclic return remains recognized in lifetime history.
6. Denied requests expose zero units.
7. Duplicate current-version requests cost zero.
8. Recovery never creates capacity beyond policy bounds.
9. Current charges reconcile with release and recovery.
10. Oracle uses identical schedules.
11. Every request has one terminal outcome.
12. Raw events recompute recovery and reconstruction aggregates.

## Reporting rule

No recovery policy is called safe from current utility alone. Every comparison reports current utility, recovered capacity, false forgetting, repeat-release amplification, lifetime reconstruction, freshness and operational cost.
