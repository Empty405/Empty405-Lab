# B6 Metrics

## Attribution correctness

### Principal-pair precision

Among contexts joined by the mechanism, the fraction belonging to the same ground-truth principal.

### Principal-pair recall

Among contexts belonging to the same ground-truth principal, the fraction successfully joined.

### False merge rate

Distinct ground-truth principals incorrectly charged to one ledger key.

### False split rate

One ground-truth principal incorrectly assigned multiple independent ledger keys.

Precision and recall must be reported separately: a mechanism can prevent false merges by refusing all joins while failing continuity completely.

## Security

### Budget continuity rate

```text
BCR = lifecycle_events_preserving_the_prior_budget / eligible_lifecycle_events
```

### Attribution bypass exposure

```text
ABE = max(0, true_principal_union_exposure - nominal_principal_budget)
```

### Budget multiplication factor

```text
BMF = total_budget_available_to_true_principal / nominal_principal_budget
```

Also report credential replay/fork acceptance, revocation-window exposure and recovery-reset exposure.

## Privacy and linkability

### Linkability surface

The number of distinct contexts and operators that can join activity to the same principal key, reported by actor rather than as one opaque score.

### Unintended linkage rate

Pairs of contexts joined outside the policy scope that required the defense.

Additional measures:

- identifier lifetime;
- broker/issuer visibility;
- metadata fields and bytes shared;
- cross-service correlation success;
- anonymity-set reduction;
- collusion gain over isolated observers.

## Utility and fairness

- legitimate task completion;
- false-denial rate;
- recovery success;
- time to restore access;
- multi-device continuity;
- shared-device collateral denial;
- worst-group utility;
- bootstrap-budget adequacy.

## Operational cost

- attribution decision latency, including p95;
- issuer/broker availability dependency;
- state reads and writes;
- proof verification cost;
- protocol bytes;
- revocation propagation time;
- recovery support events.

## Reporting rule

A mechanism is not “better” from attribution accuracy alone. Every result must jointly report bypass exposure, false merge, false split, linkability surface, legitimate utility, recovery behavior and operational dependency.
