# A4 v0.1 Results — Descriptive Pareto Frontier

**Trials:** 1000 paired trials per context/configuration  
**Configurations:** 15  
**Workload profiles:** 6  
**Deadlines:** 4  
**Raw trial rows:** 360,000  
**Root seed:** `40504`

Raw paired trials are partitioned into one compressed CSV per workload profile.

## Answer first

No single tested configuration dominated every security, utility, delay, and accounting objective. Frontier membership changed with observer deadline, supporting the A1 conclusion that delay matters when information is time-sensitive.

The three adaptive configurations remained non-dominated in all 24 workload/deadline contexts despite losing equal-weight matched-risk macro utility in A3. They stayed on the multidimensional frontier because they redistributed task utility and occupied different risk/cost points. Non-dominated does not mean recommended or best.

Coverage caps and the tested hybrid were dominated in every v0.1 context. This happened because the unified stream queried each cell once: request quotas produced identical release decisions with lower modeled ledger cost. A2 demonstrated that this equivalence does not hold under duplicates and precision escalation, so the result applies only to this harness.

## Frontier inclusion

| Configuration | Frontier contexts / 24 |
|---|---:|
| Release all | 24 |
| Deny all | 24 |
| Quota 0.25 / 0.50 / 0.75 | 24 each |
| Adaptive conservative / balanced / permissive | 24 each |
| Rate 5 | 18 |
| Rate 10 | 12 |
| Rate 20 | 12 |
| Coverage 0.25 / 0.50 / 0.75 | 0 |
| Hybrid rate 10 + coverage 0.50 | 0 |

Release-all and deny-all remain on a raw Pareto frontier because each is an extreme: one maximizes utility and the other minimizes risk and cost. Their presence is a useful sanity check and shows why a frontier is not a recommendation list.

## Deadline effect

| Deadline | Rate configurations appearing on at least one frontier |
|---|---|
| Patient | none |
| Long (600) | rate 5 |
| Medium (180) | rate 5, rate 10, rate 20 |
| Short (60) | rate 5, rate 10, rate 20 |

Under a patient observer, rate limiting added delay without changing final risk and was dominated. With finite deadlines it created distinct risk/availability trade-offs and entered the frontier.

## Stable descriptive findings

- no tested policy was universally best;
- rate limiting's frontier position depended on deadline;
- equal-decision request quotas dominated exact coverage caps when the stream contained no duplicates or precision escalation;
- adaptive configurations were non-dominated but not universally superior;
- extremes remain Pareto-optimal unless minimum acceptability constraints are added.

## Important missing validation

The current result uses aggregate means and has **not yet run paired bootstrap frontier stability**. Therefore the repository labels these as descriptive frontier results, not robust dominance findings. Confidence intervals and inclusion frequency across bootstrap samples remain required before stronger claims.

## Limitations

- unique-cell query stream only;
- synthetic task profiles;
- modeled operation counts and ledger bytes, not production measurements;
- no bootstrap uncertainty in v0.1;
- no dynamic state, identity rotation, or distributed accounting;
- only tested configurations can be classified.

## Reproduction

```bash
python benchmark.py --runs 1000 --seed 40504
python plot_results.py
python -m unittest -v test_benchmark.py
```
