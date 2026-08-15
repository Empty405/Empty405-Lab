# B2 Experiment Design

## Two primary comparisons

### Fixed request volume

Hold total attacker requests constant. This isolates budget multiplication and coordination from simply sending more traffic.

### Fixed deadline

Give every policy the same logical deadline and per-identity concurrency. This measures parallel speed advantage but reports total executed requests as a separate mediator.

## Independent variables

- Sybil pool size: `1, 2, 4, 8, 16, 32, 64`;
- ledger scope: identity, session, attributed cluster, global, proof-cost, oracle;
- coordination: duplicate, random, partition, adaptive coverage;
- exposure budget: `0.25, 0.50, 0.75`;
- signal quality: clean, noisy, missing;
- concurrency limit: `1, 4, 16, unlimited`;
- identity creation cost: zero, low, medium, high.

## Controlled variables

- hidden state and query universe;
- total requests in fixed-volume runs;
- deadline in fixed-deadline runs;
- observer algorithm;
- policy configuration;
- seeds and workload;
- response encoding.

## Legitimate controls

Run the same policy against:

1. independent users with independent networks;
2. a household or organization sharing infrastructure;
3. bursty legitimate automation;
4. accessibility-sensitive clients with low tolerance for proof cost.

## Minimum v0.1 matrix

Use fixed request volume and one declared concurrency schedule:

`7 pool sizes × 6 ledger scopes × 4 coordination modes × 3 budgets × 3 signal qualities × 500 paired trials = 756,000 trials`.

A separate smaller deadline experiment measures concurrency advantage without mixing it into the primary reconstruction result.

## Statistical plan

- paired seeds across policy and pool size;
- mean, median, p95 and confidence intervals;
- marginal reconstruction gain per added identity;
- dose-response and saturation point;
- security metrics paired with legitimate utility and worst-group fairness;
- retain null results for duplicate coordination.

## Stop conditions

Stop and repair if:

- total request counts differ in fixed-volume comparisons;
- aggregate observer sees denied responses;
- identity count changes the hidden state or query universe;
- oracle labels enter a deployable policy;
- global policy silently uses a larger budget;
- legitimate clients are accidentally treated as collaborating attackers.
