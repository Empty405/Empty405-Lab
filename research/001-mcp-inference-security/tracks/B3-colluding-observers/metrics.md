# B3 Metrics

## Coalition security

### Coalition reconstruction gain

```text
CRG = coalition_reconstruction - max(individual_reconstruction)
```

### Coalition amplification

```text
CA = coalition_exposure / max(max_individual_exposure, epsilon)
```

### Exchange gain

```text
EG = reconstruction_after_exchange - reconstruction_before_exchange
```

### Complementarity efficiency

```text
CE = unique_union_units / sum(individual_disclosed_units)
```

High CE means little overlap; low CE means many duplicated observations.

### Threshold coalition size

Smallest coalition that reaches a declared reconstruction threshold.

## Detection

- collusion detection precision/recall;
- false suspicion rate on legitimate similar-workload groups;
- detection delay;
- calibration by signal quality;
- undetectable post-hoc exchange rate.

## Utility and fairness

- individual legitimate task success;
- group task completion;
- denied requests;
- p95 latency;
- worst-group utility;
- fairness between solo and team users.

## Operational metrics

- detector evaluation time;
- ledger bytes per observer;
- cohort count;
- provenance completeness;
- communication-edge storage if explicitly enabled.

## Reporting rule

Every result must state request regime, coalition size, exchange fraction, topology, overlap, coordination, policy visibility and whether the policy used only server-observable information.
