# B5 Metrics

## Cross-server amplification

```text
XSA(n) = aggregate_exposure_across_n_servers / max(exposure_at_1_server, epsilon)
```

## Excess federated exposure

```text
EFE = max(0, client_union_exposure - nominal_principal_budget)
```

## Stale-view gain

```text
SVG = exposure_under_delayed_or_partitioned_sync - exposure_under_healthy_sync
```

## Marginal server gain

Additional unique reconstruction produced by adding one server at matched total requests.

## Consistency and correctness

- local/federated view divergence;
- overshoot before convergence;
- replay/fork acceptance;
- sketch false-positive and false-negative rates;
- principal false merge/split;
- convergence time.

## Privacy and governance cost

- cross-operator bytes per request;
- identifiers and structural fields shared;
- linkability duration;
- number of operators receiving principal metadata;
- central coordinator visibility;
- audit provenance completeness.

## Availability and utility

- legitimate multi-server task success;
- fail-open exposure;
- fail-closed denial rate;
- p95 synchronization and decision latency;
- coordinator outage impact;
- worst-server and worst-user utility.

## Reporting rule

No federated defense may be called successful using reconstruction alone. Every table must pair security with synchronization condition, metadata disclosure, false linkage, availability and operational cost.
