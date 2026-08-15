# B2 v0.1 Results — Coordinated Sybil Identities

## Outcome

The narrow hypothesis is supported inside the declared synthetic model. With total attacker request volume fixed at 100, per-identity and per-session budgets can still multiply across a Sybil pool. Query coordination determines whether that additional budget becomes new structural exposure or is wasted on duplicates.

Attribution-aware and shared scopes reduce the attack, but their security result must be paired with false merges, availability loss and identity-proof burden.

## Run

- root seed: `40512`;
- 1,512 configurations;
- 500 trials per configuration;
- 756,000 compressed raw trial rows;
- exactly 100 attacker requests per trial;
- seven unit tests passed.

## Representative result

Budget `0.25`, pool size 16, missing attribution signals:

| Coordination | Ledger scope | Exposure | False-split rate | Legitimate utility | Denied requests |
|---|---|---:|---:|---:|---:|
| duplicate | per identity | 0.070 | 1.000 | 1.000 | 0.0 |
| random | per identity | 0.634 | 1.000 | 1.000 | 0.0 |
| partition | per identity | 1.000 | 1.000 | 1.000 | 0.0 |
| partition | attributed cluster | 0.709 | 0.493 | 0.890 | 29.1 |
| partition | global | 0.250 | 0.000 | 0.000 | 75.0 |
| partition | proof cost | 0.280 | 1.000 | 0.250 | 72.0 |
| partition | oracle | 0.250 | 0.000 | 1.000 | 75.0 |

## What survived falsification

- Per-identity budget multiplication survives when total requests are held constant.
- Partitioned queries are substantially more effective than duplicate or random allocation.
- The attack saturates at full structural exposure, so marginal identity gain eventually falls to zero.
- Missing attribution signals create false splits and allow attributed-cluster exposure to rise toward the per-identity result.
- A global budget stops multiplication but collapses the modeled legitimate utility when unrelated users share the exhausted ledger.

## Important negative result

Identity count alone is not sufficient. At 16 identities, duplicate coordination exposes only 0.070 under per-identity accounting because clients repeat the same local query positions. The security problem is the combination of multiple budgets and coordinated non-overlapping queries.

## Interpretation boundaries

- v0.1 is the fixed-request experiment; finite-deadline concurrency remains untested.
- Linkage and false-merge probabilities are synthetic declared assumptions.
- Proof cost is an admission-cap abstraction, not a real identity technology.
- Structural exposure is not semantic reconstruction.
- The results do not justify fingerprinting, proof-of-personhood or compulsory identity checks.

## Next question

B3 should distinguish one centrally controlled Sybil pool from genuinely independent observers that later collude and combine their outputs.
