# C3 Results — Availability Degradation

## Run identity

- Schema: `c3.v0.1`
- Root seed: `40523`
- Raw rows: **63,000**
- Configurations: **315**
- Trials per configuration: **200**
- Episode length: **120 ticks**
- Queue capacity: **24 tasks**

## Main result

The simulation supports the narrow claim that prior-exposure-aware fallbacks can preserve useful availability without adding structural exposure. Replay-only improved mean task completion over hard deny, and the modeled graceful-degradation catalog reached the evaluator-only oracle ceiling. Bounded queue/retry did not dominate: it preserved the cap but introduced timeouts, queue peaks, and longer latency tails. Fail-open exposed new units and produced violation events without outperforming the safe graceful policy in this fixture.

## Policy-level averages

| Policy | Completion | Exposure gain | Violation rate | Denied | Timed out | p95 latency | Peak queue | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hard deny | 0.4317 | 0.0000 | 0.0000 | 27.2197 | 0.0000 | 1.6000 | 0.0000 | 1.0000 |
| Replay-only | 0.5998 | 0.0000 | 0.0000 | 19.1909 | 0.0000 | 1.7999 | 0.0000 | 1.0000 |
| Safe snapshot | 0.0957 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.1564 | 0.0000 | 0.2854 |
| Graceful degradation | 0.7334 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.7999 | 0.0000 | 0.7799 |
| Bounded queue/retry | 0.4985 | 0.0000 | 0.0000 | 17.5380 | 6.4889 | 5.3263 | 7.3111 | 1.0000 |
| Fail-open | 0.7123 | 0.0485 | 0.1125 | 13.8197 | 0.0000 | 1.8000 | 0.0000 | 1.0000 |
| Oracle | 0.7334 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.7999 | 0.0000 | 0.7799 |

Completion is useful completion at the task-specific synthetic quality threshold. Low-quality snapshot or degraded replies remain terminal responses but are not mislabeled as completed tasks. Latency percentiles use useful completions only; timeouts remain separate terminal outcomes.

## Interpretation

### Safe fallback ceiling

Graceful degradation and the oracle coincide because both can select the same explicitly pre-charged fallback catalog in v0.1. This is a model ceiling, not evidence that a production policy can discover the oracle choice perfectly. A later semantic observer can test whether apparently coarse fallbacks are actually equivalent to new disclosure.

### Queue and recovery

Queue/retry protects the exposure cap, but its mean p95 completion latency rises to `5.3263` ticks and it times out `6.4889` tasks per episode on average. This supports the directional recovery-storm concern: postponing decisions can convert dependency failure into backlog and missed deadlines.

### Fail-open

Fail-open has mean exposure gain `0.0485` and a `0.1125` task-level violation rate. Reconciliation never removes those disclosures. Its mean completion (`0.7123`) remains below graceful degradation in this synthetic matrix, so apparent openness is not automatically the best availability strategy.

## Falsification status

The null hypothesis is weakened inside this model because replay-only and graceful degradation improve completion over hard deny without new structural exposure. The broad claim that no deployable policy can reach the oracle is not supported in v0.1: graceful degradation equals the simplified oracle by construction. This exposes a useful follow-up requirement rather than proving dominance in real systems.

## Limitations

- Arrivals, deadlines, response quality, and structural units are synthetic.
- One exact shared ledger is fixed at the C2 cap; distributed failures are excluded.
- The graceful fallback catalog is assumed pre-charged and semantically safe.
- One tick is an ordering and latency unit, not a millisecond claim.
- Side effects, cancellation races, external tool execution, and real SLOs are not modeled.
- Criticality changes only deadline and quality sensitivity; it never authorizes bypass.
- Confidence intervals describe simulator variation, not deployment uncertainty.

## Next experiments

1. Challenge fallback equivalence and representation safety in D2–D4.
2. Add cancellation and external side-effect races to queue/retry.
3. Test malicious queue and budget consumption in C4.
4. Introduce multi-client fairness in C5.
5. Keep dependency recovery separate from budget decay until C6.
