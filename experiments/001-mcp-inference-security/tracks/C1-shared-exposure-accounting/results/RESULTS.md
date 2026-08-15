# C1 Results — Shared Exposure Accounting

## Run identity

- Schema: `c1.v0.1`
- Root seed: `40521`
- Raw rows: **54,000**
- Configurations: **270**
- Trials per configuration: **200**
- Decision replicas: **4**
- Requests per trial: **96**
- Structural disclosure universe: **100 units**

## Main result

The simulation supports the directional hypothesis that shared-budget conservation is not obtained by merging independent counters after disclosure. Independent ledgers and eventual reconciliation preserved high request utility but allowed irreversible budget overruns. Central exact accounting prevented overruns at the cost of a synchronous dependency, the broadest modeled operator visibility, and complete denial during partition. Hierarchical reservations and escrow rights preserved the hard cap during partition without per-request central lookup, but produced stranded authority and false charges when replicas observed overlapping disclosures independently.

## Mechanism-level averages

| Mechanism | Exposure | Mean overrun | Overrun rate | False charges | Duplicate suppression | Utility | Coordination messages | Visible operators |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Independent | 0.5300 | 0.1765 | 0.5693 | 13.60 | 0.7228 | 1.0000 | 0.00 | 1.00 |
| Central exact | 0.2356 | 0.0000 | 0.0000 | 0.00 | 1.0000 | 0.5358 | 128.00 | 5.00 |
| Eventual merge | 0.4531 | 0.0995 | 0.3830 | 6.05 | 0.8779 | 0.9118 | 41.33 | 4.00 |
| Hierarchical reservation | 0.3439 | 0.0000 | 0.0000 | 5.62 | 0.9035 | 0.7144 | 8.00 | 2.00 |
| Escrow rights | 0.3473 | 0.0000 | 0.0000 | 3.74 | 0.9356 | 0.7439 | 40.00 | 2.00 |
| Oracle | 0.3535 | 0.0000 | 0.0000 | 0.00 | 1.0000 | 0.8037 | 0.00 | 0.00 |

These are averages across intentionally different workloads, budgets, and synchronization conditions. They characterize this simulator rather than real MCP deployments.

## Diagnostic slices

### Partitioned disjoint workload

At budget `0.25`, independent and eventual ledgers released `0.96` of the universe, an overrun of `0.71`, because four replicas each retained local spending authority. Hierarchical reservation, escrow, and oracle accounting stopped at `0.25`. Central exact accounting failed closed and released `0.00`.

### Duplicate-heavy healthy workload

At budget `0.25`, every mechanism released the same eight unique structural units (`0.08` exposure). Exact shared views reported duplicate suppression `1.0` with zero false charges. The regression test now explicitly protects this metric semantics.

### Conservation versus availability

The hard-cap mechanisms did not obtain security for free. Central fail-closed behavior reduced mean utility to `0.5358`. Reservation and escrow raised utility relative to central accounting but could strand authority at replicas that did not receive useful new disclosures.

## Falsification status

The null hypothesis is weakened inside this model: shared exact and bounded-authority mechanisms materially reduce overrun relative to independent accounting. The stronger claim remains unproven because topology, reservation skew, semantic equivalence, adversarial consumption, and real coordination latency are synthetic or deferred.

No deployable mechanism dominates every dimension. This supports proceeding to C2–C6, but it does not establish that the chosen budget value or domain membership is correct.

## Limitations

- Structural disclosure keys are synthetic and do not capture semantic equivalence.
- The topology is fixed to four replicas with equal initial authority splitting.
- Budget-domain membership is evaluator-provided from the B6 scope.
- Coordination messages and operator visibility are abstract cost indicators.
- Central partition uses a fixed fail-closed policy.
- Fairness, malicious budget burning, exhaustion behavior, and decay remain C2–C6.
- Confidence intervals describe simulator variation, not real deployment uncertainty.

## Next experiments

1. Vary replica count and reservation skew.
2. Add explicit right-transfer and replay faults.
3. Test scalar counters against representation-equivalent disclosure keys.
4. Connect exhaustion behavior to C2 and availability costs to C3.
5. Use C4 workloads to measure deliberate authority stranding and budget burning.
