# C4 Falsification Plan

## Claims under test

1. Strategic request selection can cause more legitimate harm than volume/timing-matched benign load.
2. Global FIFO permits disproportionate budget capture under at least one strategic pattern.
3. Principal-aware bounded policies reduce denial-of-information without increasing exposure.
4. Request-rate limits alone can miss low-frequency, high-marginal-cost burning.
5. No deployable policy dominates attack suppression, benign utility, utilization, fairness and cost across every workload.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- matched strategic and benign loads produce indistinguishable victim harm;
- global FIFO remains close to oracle across every attack pattern and intensity;
- principal-aware policies do not reduce legitimate completion loss;
- simple request-rate limiting matches exposure-aware policies at lower cost;
- apparent protection comes only from leaving most budget unused;
- one deployable policy dominates all others with uncertainty included;
- effects disappear when attacker and benign traffic are exactly paired.

## Critical counterexamples

- duplicate-only requests consume new budget;
- a denied attacker request changes the released union;
- reservations sum above the global cap;
- a legitimate burst is mislabeled malicious by evaluator leakage;
- adaptive attacker code reads hidden future tasks;
- global accounting races overshoot the cap;
- attacker capture appears high only because legitimate tasks need the same units;
- defense protects average utility while starving one legitimate principal;
- unused reservations are reported as security gain without utilization cost.

## Confounders

- unequal request count or timing between strategic and benign controls;
- identity rotation or Sybil creation from the B-track;
- semantic marginal-cost estimation errors from the D-track;
- budget decay or replenishment from C6;
- different legitimate schedules between policies;
- treating request count as exposure cost;
- using attacker role inside deployable policies;
- mixing task value with structural exposure without reporting both;
- averaging away late-critical failures.

## Interpretation boundaries

C4 is a synthetic contention study under exact identity and exact structural accounting. It does not prove resistance to real Sybil attacks, define production client quotas, determine legal priority, or justify discrimination against high-volume users.

The oracle is evaluator-only. A policy that approaches it in the benchmark may still be impractical if it depends on inaccurate task-value or marginal-cost estimates.
