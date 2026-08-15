# C1 Experiment Design

## Primary experiment

Hold the budget domain, request workload, disclosure universe and nominal budget constant. Vary only the shared-accounting mechanism, workload overlap and synchronization condition, then compare every release decision with the evaluator union.

## Independent variables

- mechanism: independent local, central exact, eventual merge, hierarchical reservation, escrow rights, oracle;
- workload overlap: disjoint, duplicate-heavy, partial overlap, hotspot, adversarial interleaving;
- synchronization: healthy, delayed, partitioned;
- nominal budget: `0.25, 0.50, 0.75`;
- paired trial seed: 200 trials per configuration.

## Minimum v0.1 matrix

`6 mechanisms × 5 workload-overlap patterns × 3 synchronization conditions × 3 budgets × 200 paired trials = 54,000 trials`.

The primary matrix fixes four decision replicas, 96 requests, a 100-unit disclosure universe, one budget domain and one predeclared reservation policy. Replica count, cross-organization topology and reservation rebalance are sensitivity analyses rather than hidden multipliers.

## Paired trial procedure

1. Generate one disclosure universe and fixed request sequence.
2. Assign requests to four replicas with deterministic concurrent batches.
3. Give every mechanism the same nominal budget and initial state.
4. Apply the selected synchronization schedule.
5. Let each replica decide using only permitted local or coordinated state.
6. Add only released disclosure keys to the evaluator union.
7. Reconcile mechanism state after delayed or partitioned phases.
8. Record overruns as irreversible even if later detected.
9. Compare false charges, denials, visibility and coordination cost with the oracle.

## Controls

- one replica with exact structural accounting;
- four replicas with fully disjoint outputs;
- duplicate-only workload after the first disclosure;
- healthy synchronous central ledger;
- full partition lasting the entire release phase;
- zero-overlap and maximum-overlap workloads;
- fixed reservation sum equal to the nominal budget;
- evaluator oracle with the same request order.

## Required outputs

- nominal budget and evaluator release union;
- authorized new, duplicate and denied disclosures;
- budget overrun magnitude and first-overrun request;
- overspend detected after release;
- false-charge and duplicate-charge events;
- unused/stranded reserved rights;
- legitimate task completion and denial reasons;
- replica-state divergence before and after reconciliation;
- lookups, messages, bytes, state writes and observed domain keys.

## Statistical plan

- paired mechanism differences under identical seeds;
- confidence intervals for overrun probability and magnitude;
- security–coordination Pareto frontier;
- separate healthy, delayed and partitioned results;
- separate new-disclosure and duplicate-heavy utility;
- worst overlap-pattern result rather than only global averages;
- sensitivity to replica count and reservation skew after v0.1.

## Stop conditions

Stop and repair the experiment if:

- mechanisms receive different request sequences or concurrency schedules;
- denied disclosures enter the evaluator exposure union;
- detected-late overrun is treated as prevented exposure;
- the oracle depends on deployable coordination metadata;
- scalar request count is substituted for structural disclosure union;
- reservations sum to more than the nominal budget;
- reconciliation erases previously released exposure;
- B6 attribution errors are introduced into the primary C1 matrix;
- availability or fairness claims are inferred from a single fixed workload.
