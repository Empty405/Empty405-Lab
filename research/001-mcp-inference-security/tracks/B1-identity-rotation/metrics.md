# B1 Metrics

## Security metrics

### Rotation amplification

```text
RA = exposure_with_rotation / max(exposure_without_rotation, epsilon)
```

Shows how much identity rotation multiplies final exposure.

### Excess exposure

```text
EE = max(0, principal_exposure - configured_budget)
```

The main budget-bypass quantity, computed across all identities of the ground-truth principal.

### Reconstruction gain

```text
RG = reconstruction_with_rotation - reconstruction_without_rotation
```

Report both structural coverage and exact recovery.

### Time to budget bypass

First logical time at which principal exposure exceeds the configured budget.

## Attribution metrics

### False split rate

Fraction of identity pairs from the same principal assigned to different attribution keys.

### False merge rate

Fraction of identity pairs from different principals assigned to the same attribution key.

### Linkage precision and recall

Measured against evaluator-only principal labels. These diagnose attribution; they are not exposed to the policy.

## Utility metrics

- legitimate task success;
- denied legitimate requests;
- p95 task delay;
- worst-group utility for users behind shared infrastructure.

## Operational metrics

- ledger bytes per request;
- attribution evaluation time;
- number of active attribution keys;
- provenance completeness.

## Reporting rule

Never report only average reconstruction. Every result table must pair security benefit with false merge, false split, legitimate utility and operational cost.
