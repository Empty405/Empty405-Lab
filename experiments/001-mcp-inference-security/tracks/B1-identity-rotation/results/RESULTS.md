# B1 v0.1 Results — Identity Rotation

## Outcome

The narrow hypothesis is supported inside the declared synthetic model: accounting keyed only to a visible identity or session resets after rotation and allows one durable principal to exceed its configured exposure budget. Attribution-aware strategies reduce this bypass, but their protection degrades as allowed linkage signals become noisy or missing.

This is a simulation result about declared assumptions, not evidence that a production system can or should identify real people.

## Run

- root seed: `40511`;
- 324 configurations;
- 1,000 trials per configuration;
- 324,000 compressed raw trial rows;
- fixed total of 100 attacker requests per trial;
- six unit tests passed.

## Representative result

At budget `0.25` and 16 rotations:

| Strategy | Clean exposure | Noisy exposure | Missing exposure | Missing false-split rate | Missing legitimate utility |
|---|---:|---:|---:|---:|---:|
| per identity | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| durable credential | 0.255 | 0.391 | 0.716 | 0.496 | 0.969 |
| deterministic linkage | 0.296 | 0.519 | 0.817 | 0.606 | 0.906 |
| probabilistic linkage | 0.270 | 0.401 | 0.587 | 0.358 | 0.925 |
| oracle | 0.250 | 0.250 | 0.250 | 0.000 | 1.000 |

Per-identity exposure reaches 100% because 17 visible identities each receive a fresh 25-unit ledger while the total request count remains fixed. The oracle remains at the 25% budget and is an experimental upper bound, not a deployable defense.

## What survived falsification

- Rotation increases exposure under per-identity and per-session ledgers without increasing total requests.
- Exposure amplification grows with rotations until the hidden-state ceiling is reached.
- Attribution-aware accounting reduces excess exposure when signals link rotated identities reliably.
- Missing signals produce false splits and recover much of the attacker's exposure advantage.

## Cost of attribution

The synthetic shared-environment scenario produces false merges for non-oracle linkage. At the representative missing-signal point, legitimate utility falls to 0.906 for deterministic linkage and 0.925 for probabilistic linkage. Therefore stronger accounting cannot be evaluated by reconstruction alone.

## Limitations

- v0.1 implements fixed-cadence rotation only, not reactive rotation-on-denial.
- Link and false-merge probabilities are declared synthetic inputs, not empirical estimates.
- Reconstruction equals unique structural exposure; semantic inference is excluded.
- The legitimate-user model is intentionally small and does not justify a production attribution policy.

## Next research question

B2 should test concurrent Sybil identities, where the attacker can distribute requests in parallel instead of rotating one visible identity sequentially.
