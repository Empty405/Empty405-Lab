# C5 Falsification Plan

## Claims under test

1. FIFO can create arrival-order-dependent starvation under shared exposure scarcity.
2. Equal reservation reduces starvation but may strand capacity under asymmetric demand.
3. Weighted and bounded-borrowing policies can improve the utility–fairness trade-off.
4. Misspecified weights can reverse expected benefits and harm low-demand clients.
5. No deployable policy dominates utility, starvation, utilization and cost across every demand profile.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- FIFO matches allocation-aware policies on starvation and minimum utility;
- equal reservation does not strand capacity under sparse demand;
- bounded borrowing provides no utilization gain over fixed reservation;
- weight misspecification has negligible effect;
- policy rankings are invariant to arrival order and scarcity;
- one deployable policy dominates all others with uncertainty included;
- apparent fairness gains disappear after inactive principals are excluded.

## Critical counterexamples

- an inactive principal is labeled starved;
- reservation shares exceed the cap;
- borrowing produces unaccounted exposure;
- a denied request changes the released union;
- duplicate units are charged more than once;
- a late client loses its guarantee because early borrowing has no debt bound;
- evaluator task value leaks into a deployable policy;
- Jain index improves while one active client receives zero useful utility;
- unused capacity is omitted from a fairness claim.

## Confounders

- unequal request sets or arrivals between policies;
- malicious behavior from C4;
- identity rotation or Sybils from B;
- budget decay from C6;
- semantic marginal-cost error from D;
- different caps between policies;
- treating accepted requests as completed utility;
- including zero-demand clients in starvation;
- hiding weight misspecification behind aggregate averages.

## Interpretation boundaries

C5 evaluates synthetic allocation rules under exact identities, exact accounting and declared weights. It does not define moral, legal or economic fairness, production priority classes, emergency access, or acceptable discrimination.

Synthetic task value exists for controlled comparison only. Oracle performance is an upper bound, not a deployable policy recommendation.
