# C1 Metrics

## Security and conservation

### Union exposure

```text
UE = |union of released disclosure keys| / |disclosure universe|
```

### Budget overrun

```text
BO = max(0, UE - nominal_budget)
```

Report overrun probability, magnitude, first-overrun request and whether the mechanism detected it before or after release.

### Conservation error

```text
CE = max(0, total_authority_issued - nominal_budget_units)
```

For reservation and escrow mechanisms, authority includes all spendable local rights, including temporarily disconnected replicas.

### Budget multiplication factor

```text
BMF = maximum simultaneously spendable authority / nominal_budget_units
```

### Delayed-detection exposure

New disclosure released beyond the cap before eventual reconciliation detects the inconsistency.

## Accounting correctness

### False-charge rate

Already-covered disclosure keys charged as new because accounting states disagree.

### Missed-charge rate

New disclosure keys released without reducing the relevant available authority.

### Duplicate suppression

Fraction of repeated disclosure keys recognized without another budget charge.

### Replica divergence

Maximum pairwise difference between replica views of consumed structural units, reported before and after reconciliation.

## Utility

- legitimate task completion;
- false-denial rate;
- duplicate-request success;
- new-disclosure success;
- stranded-budget fraction;
- reservation utilization;
- denial reason by synchronization condition.

C1 reports these measures only to expose accounting trade-offs. Exhaustion policy, availability optimization and fair allocation remain C2, C3 and C5.

## Coordination and visibility

- synchronous lookups per request;
- coordination messages and bytes;
- state reads and writes;
- reconciliation operations;
- budget-domain keys visible per operator;
- disclosure keys crossing an organization boundary;
- central dependency indicator.

## Invariant tests

1. Oracle and central exact accounting never exceed the structural cap while available.
2. Independent disjoint replicas can multiply the effective budget.
3. Eventual reconciliation cannot reduce evaluator exposure already released.
4. Escrow and reservation mechanisms never issue more authority than the nominal budget.
5. Duplicate-only requests do not consume new structural budget under exact accounting.
6. Denied requests never change evaluator exposure.
7. Every reported row contains exactly 96 attempted requests.

## Reporting rule

No mechanism is described as better from overrun alone. Every comparison jointly reports conservation, false charge, legitimate utility, stranded authority, coordination cost and visibility.
