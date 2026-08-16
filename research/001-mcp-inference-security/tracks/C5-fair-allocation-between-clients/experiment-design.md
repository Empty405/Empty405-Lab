# C5 Experiment Design

## Primary experiment

Hold principals, requests, structural units, task values, arrivals, deadlines, shared ledger and cap constant. Vary only allocation policy, demand profile, weight profile and scarcity level.

## Independent variables

- policy: global FIFO, equal reservation, weighted reservation, progressive max-min, proportional share, bounded borrowing, oracle;
- demand profile: balanced steady, balanced burst, asymmetric heavy client, sparse clients, late high-value demand;
- weight profile: equal, demand-proportional, value-proportional, misspecified;
- scarcity: mild, moderate, severe;
- paired trial seed: 200 trials per configuration.

## Minimum v0.1 matrix

`7 policies × 5 demand profiles × 4 weight profiles × 3 scarcity levels × 200 paired trials = 84,000 trials`.

Each episode fixes 120 ticks, five legitimate principals, one atomic shared ledger, an exact initial exposure union and one cap derived from scarcity.

## Paired trial procedure

1. Generate one set of legitimate client requests and task values.
2. Assign identical structural units, arrivals and deadlines to every policy.
3. Initialize exact ledger state and scarcity-specific cap.
4. Reveal only policy-permitted metadata and declared weights.
5. Estimate exact marginal exposure cost.
6. Admit, replay, defer or deny according to the allocation rule.
7. Atomically charge newly released units.
8. Record request outcome, client utility and allocation state.
9. Close the episode without cap reset or decay.
10. Compare policies against FIFO and utility-oracle controls.

## Controls

- equal demand and equal value;
- identical requests reordered across principals;
- all requests duplicate-only;
- cap sufficient for all demand;
- one inactive principal;
- one late burst after early borrowing;
- weights matching demand;
- weights matching task value;
- deliberately misspecified weights;
- oracle under identical cap and request set.

## Required raw outputs

- episode, tick, request ID and principal ID;
- demand and weight profile;
- task value and deadline;
- requested units and marginal exposure cost;
- admission, replay, deferral or denial;
- ledger before/after and remaining cap;
- reserved, used, borrowed and lent units;
- per-principal completion and utility;
- policy reads, allocator operations, ledger writes and metadata bytes.

## Statistical plan

- paired utility and starvation differences;
- confidence intervals for per-principal minimum utility;
- Jain index and generalized-entropy inequality with zero-demand handling;
- envy and share-violation counts;
- utilization and unused reservation cost;
- oracle regret;
- sensitivity to arrival order and weight misspecification;
- utility–fairness–utilization Pareto frontier.

## Stop conditions

Stop and repair the experiment if:

- policies receive different requests, values or arrivals;
- denied requests release exposure;
- duplicate units consume budget twice;
- per-principal charges do not conserve the global charge;
- reservation or borrowing creates capacity;
- inactive clients are counted as starved;
- raw request acceptance is treated as utility;
- evaluator task value leaks into non-oracle policies;
- fairness improves only because the policy leaves capacity unused and this is not reported;
- averaging hides a completely starved active principal.
