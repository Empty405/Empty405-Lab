# B6 Results — Durable Principal Attribution

## Run identity

- Schema: `b6.v0.1`
- Root seed: `40516`
- Raw rows: **108,000**
- Configurations: **360**
- Trials per configuration: **300**
- Fixed workload: **80 requests per trial**
- Unknown-attribution policy: restricted bootstrap

## Main result

The simulation supports the directional hypothesis that no deployable attribution unit dominates security, privacy, and availability simultaneously. Stable global attribution eliminated duplicated-budget bypass in this model, but it exposed the largest linkability surface. Session-scoped accounting minimized modeled linkability while allowing lifecycle changes to create fresh ledgers.

Across the complete matrix, the session mechanism produced a mean budget-bypass rate of **0.4988** and a false-split rate of **0.8000**. Global-ID and oracle attribution produced **0.0000** modeled bypass and **0.0000** false split; however, global ID linked **4.0 contexts**, the largest deployable value, while the oracle is evaluator-only.

## Mechanism-level averages

| Mechanism | Mean exposure | Bypass rate | False split | False merge | Linked contexts | Utility |
|---|---:|---:|---:|---:|---:|---:|
| Session | 0.5031 | 0.4988 | 0.8000 | 0.0000 | 1.00 | 0.9411 |
| Account | 0.4655 | 0.2465 | 0.4000 | 0.2500 | 2.00 | 0.8725 |
| Global ID | 0.3461 | 0.0000 | 0.0000 | 0.2500 | 4.00 | 0.6481 |
| Pairwise pseudonym | 0.3651 | 0.1251 | 0.3000 | 0.0000 | 2.25 | 0.6824 |
| Anonymous credential | 0.3602 | 0.0938 | 0.2000 | 0.2500 | 1.00 | 0.6743 |
| Oracle | 0.4285 | 0.0000 | 0.0000 | 0.0000 | 0.00 | 0.8030 |

These are averages over deliberately different lifecycle and failure conditions. They describe the benchmark, not real-world population rates.

## Diagnostic slices

Under honest account rotation with budget `0.25`, session and account attribution reached about `0.496` exposure and always duplicated the budget. Global ID, pairwise pseudonyms, anonymous credentials, and the oracle remained at `0.25` exposure with no bypass in that slice.

During attribution-service outage with budget `0.50`, the restricted-bootstrap policy held global-ID, pairwise, and anonymous-credential exposure to `0.10`, but legitimate utility fell to about `0.18`. This is an availability cost, not a free security improvement.

Credential transfer creates false merges for account, global-ID, and anonymous-credential models because possession of deployable evidence is not equivalent to transfer of the evaluator's ground-truth principal.

## Falsification status

The null hypothesis is weakened inside this synthetic model: several durable mechanisms materially reduce duplicated-budget exposure relative to session accounting. The broader hypothesis is not proven. A mechanism could change position after realistic issuer failures, population structure, recovery protocols, semantic reconstruction, or measured operational costs are introduced.

## Limitations

- Attribution, lifecycle events, outages, and costs are synthetic abstractions.
- Structural exposure is not semantic reconstruction or information-theoretic privacy loss.
- Linkability is an ordinal context count, not a legal or empirical privacy measurement.
- The fixed population mixture does not establish worst-group fairness.
- Confidence intervals reflect simulator variation, not uncertainty about real deployments.
- The oracle is a control and must never be interpreted as a deployable identity system.

## Next experiments

1. Add shared-device and legitimate multi-device population sensitivity.
2. Compare fail-closed, restricted-bootstrap, and local-fallback unknown policies.
3. Model revocation delay and credential replay explicitly.
4. Replace ordinal linkability with actor-scoped observable events.
5. Connect B6 outputs to C1 shared accounting and F6 federated accounting.
