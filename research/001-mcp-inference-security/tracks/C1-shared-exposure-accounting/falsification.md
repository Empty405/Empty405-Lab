# C1 Falsification Plan

## Claims under test

1. Independent replica ledgers multiply a nominal shared exposure budget when outputs are complementary.
2. Eventual reconciliation detects some violations only after irreversible disclosure.
3. Exact central accounting preserves conservation but introduces a synchronous dependency and broader metadata visibility.
4. Reservation or escrow mechanisms can preserve a hard cap during partition without a lookup per request, at the cost of stranded or misallocated authority.
5. No tested deployable mechanism dominates security, utility, visibility and coordination cost in every condition.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- independent replicas do not increase union exposure under disjoint workloads;
- eventual accounting prevents rather than merely detects all partition overruns;
- central exact accounting adds no measurable dependency, messages or visibility;
- escrow/reservation mechanisms exceed their issued authority;
- bounded local authority causes no measurable stranded budget or denial cost;
- one deployable mechanism dominates all others on every reported dimension with uncertainty included;
- overlap pattern, rather than shared accounting, explains all measured differences.

## Critical counterexamples

- four replicas each authorize a full nominal budget during partition;
- reconciliation reports a clean ledger after excess disclosure already occurred;
- the same disclosure is charged four times because replica representations differ;
- escrow rights are copied, replayed or recreated after reconnect;
- a central outage silently switches to unlimited local accounting;
- reservations preserve the cap only by denying all legitimate requests;
- budget-domain metadata reveals more cross-service activity than the protected disclosure itself;
- one replica hoards unused authority while all useful requests reach another replica.

## Confounders

- unequal workloads, budgets or request order between mechanisms;
- changing principal attribution while testing shared accounting;
- counting attempted or denied outputs as exposure;
- treating post-hoc detection as prevention;
- comparing scalar counters with structural-union mechanisms without stating the mismatch;
- hiding reserved rights from total spendable authority;
- averaging healthy and partitioned phases;
- excluding coordination metadata and operator visibility.

## Interpretation boundaries

C1 tests conservation of a policy-defined shared structural-exposure budget. It does not establish that the budget value is safe, that membership is correctly attributed, or that all semantically equivalent disclosures share one key.

A hard cap can still be operationally harmful or unfair. C1 therefore provides accounting primitives for C2–C6 rather than deciding exhaustion, availability, adversarial consumption, allocation or recovery policy.
