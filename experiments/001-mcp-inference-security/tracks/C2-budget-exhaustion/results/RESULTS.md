# C2 Results — Budget Exhaustion

## Run identity

- Schema: `c2.v0.1`
- Root seed: `40522`
- Raw rows: **54,000**
- Configurations: **270**
- Trials per configuration: **200**
- Post-cap requests per trial: **48**
- Structural disclosure universe: **100 units**
- Explicit override allowance: **5 units**

## Main result

The simulation supports the directional hypothesis that immediate hard denial is not the only way to preserve an exhausted structural cap. Replay-only and pre-charged snapshots reused prior exposure without post-cap gain, while completing some synthetic tasks that hard deny always failed. In contrast, the modeled coarse fallback achieved high task completion by using an intentionally uncharged representation namespace and therefore violated the cap in every tested configuration. Bounded override made exceptional exposure explicit and capped, but did not provide zero-loss security.

## Policy-level averages

| Policy | Post-cap gain | Violation rate | False denials | Safe-reuse ratio | Task progress | Completion | Override used |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hard deny | 0.0000 | 0.0000 | 22.07 | 0.0000 | 0.0000 | 0.0000 | 0.00 |
| Replay-only | 0.0000 | 0.0000 | 0.00 | 1.0000 | 0.3975 | 0.2071 | 0.00 |
| Coarse fallback | 0.0498 | 1.0000 | 0.00 | 0.0000 | 0.9049 | 0.8073 | 0.00 |
| Safe snapshot | 0.0000 | 0.0000 | 0.00 | 1.0000 | 0.1968 | 0.0040 | 0.00 |
| Bounded override | 0.0395 | 0.8000 | 0.00 | 1.0000 | 0.6176 | 0.2633 | 3.99 |
| Oracle | 0.0000 | 0.0000 | 0.00 | 1.0000 | 0.4975 | 0.2143 | 0.00 |

The safe-reuse ratio is computed from aggregate `safe_reused_requests / safe_candidate_requests`; workloads with no safe candidate do not receive a vacuous score of one. These values characterize the simulator, not real MCP task populations.

## Diagnostic slices

### Duplicate-only routine task at budget 0.25

Replay-only, bounded override, and oracle completed every task with zero post-cap exposure and safe-reuse ratio `1.0`. Hard deny rejected all 48 requests. Safe snapshot remained secure but completed almost no full tasks because its fixed eight-unit view often omitted required prior units.

### New-disjoint critical task at budget 0.25

Hard deny, replay-only, safe snapshot, and oracle preserved zero gain but could not complete tasks requiring new information. Bounded override released exactly its maximum five new units (`0.05` exposure) and reached only about `0.104` task progress. The modeled coarse fallback released six uncharged coarse keys (`0.06`) and completed the bucket-level task.

### Coarse output interpretation

The `1.0` violation rate for coarse fallback is a property of this explicit test fixture: coarse keys live in a namespace not charged before exhaustion. It demonstrates that “lower resolution” is not automatically free; it does not prove every coarse representation leaks new information.

## Metric correction found during analysis

The initial implementation assigned `safe_reuse_rate = 1.0` to trials with zero safe candidates. Analysis caught the aggregation artifact before publication. The corrected schema records `safe_candidate_requests` and `safe_reused_requests`, uses zero for a zero-denominator trial, and includes regression tests preventing hard deny from claiming reuse it never performed.

## Falsification status

The null hypothesis is weakened inside this model: replay-only materially improves completion over hard deny without additional structural exposure. The stronger hypothesis remains unproven because semantic equivalence, real task value, representation leakage, denial side channels, and governance are not modeled.

No deployable policy dominates every dimension. Bounded override and uncharged coarse fallback trade measurable exposure for utility; safe snapshot trades flexibility for stronger cap preservation.

## Limitations

- Response classes and task requirements are synthetic.
- The C1 ledger is exact and already at cap; distributed accounting failures are excluded.
- Coarse outputs deliberately use an uncharged structural namespace.
- Snapshot content is static and precharged; dynamic template risks remain follow-up work.
- Criticality is a sensitivity label, not authorization or legal priority.
- No semantic equivalence, encoding bypass, denial side channel, appeal process, or human governance is modeled.
- Confidence intervals describe simulator variation, not deployment uncertainty.

## Next experiments

1. Add semantically equivalent and encoding-varied replays through D2–D3.
2. Test dynamic snapshot contamination and denial side channels.
3. Move denial duration and retry behavior into C3 availability degradation.
4. Add malicious exhaustion and override targeting in C4.
5. Compare explicit recovery and decay only in C6.
