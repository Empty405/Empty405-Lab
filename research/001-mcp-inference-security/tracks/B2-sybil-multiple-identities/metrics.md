# B2 Metrics

## Security metrics

### Sybil amplification

```text
SA(n) = exposure_with_n_identities / max(exposure_with_1_identity, epsilon)
```

### Excess principal exposure

```text
EPE = max(0, aggregate_controller_exposure - nominal_budget)
```

### Marginal identity gain

```text
MIG(n) = reconstruction(n) - reconstruction(n - 1)
```

Report the saturation point where added identities stop producing material gain.

### Time-to-reconstruction

First logical time at which the aggregate observer reaches a declared reconstruction threshold.

### Coordination advantage

Difference between partition/adaptive coordination and random allocation at matched pool size and request volume.

## Attribution metrics

- identity-cluster false split rate;
- legitimate-client false merge rate;
- controller linkage precision and recall;
- detected-pool-size error.

## Utility and fairness

- legitimate task success;
- denied legitimate requests;
- p95 latency;
- proof/identity creation burden;
- worst-group utility;
- Jain fairness index across legitimate clients.

## Operational metrics

- ledger bytes;
- attribution evaluation time;
- active identity and cluster count;
- policy decisions per logical second;
- provenance completeness.

## Required reporting

Every security table must state:

- comparison regime: fixed requests or fixed deadline;
- actual request count;
- pool size and concurrency;
- coordination mode;
- ledger scope;
- utility and false-merge cost.
