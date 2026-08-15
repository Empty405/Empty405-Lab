# C2 Experiment Design

## Primary experiment

Start every paired trial with the same exact C1 ledger at the nominal cap, identical cached responses, safe snapshots, task requirements and post-cap requests. Vary only the post-exhaustion policy, workload, budget and task criticality.

## Independent variables

- policy: hard deny, replay-only, coarse fallback, safe snapshot, bounded override, oracle;
- post-exhaustion workload: duplicate-only, new-disjoint, mixed, hotspot, staged multi-step;
- nominal budget: `0.25, 0.50, 0.75`;
- task criticality: optional, routine, critical;
- paired trial seed: 200 trials per configuration.

## Minimum v0.1 matrix

`6 policies × 5 workloads × 3 budgets × 3 task-criticality classes × 200 paired trials = 54,000 trials`.

The primary matrix fixes a 100-unit disclosure universe, an exactly exhausted ledger, 48 post-cap requests, one bounded-override allowance, and deterministic structural response classification. Distributed ledger inconsistency is excluded so C1 failures do not masquerade as C2 policy effects.

## Paired trial procedure

1. Generate a hidden-state fixture and exact pre-exhaustion union equal to the cap.
2. Generate cached exact responses and pre-approved safe snapshots from that union.
3. Generate one task requirement set and 48 post-cap requests.
4. Mark the budget domain exhausted before the first evaluated request.
5. Apply the selected policy to every candidate response.
6. Add only released new units to post-cap exposure gain.
7. Track task progress using evaluator-only requirements.
8. Record denial, downgrade, replay, snapshot and override outcomes separately.
9. Compare each policy with hard-deny and cap-aware-oracle controls under the same seed.

## Controls

- ledger exactly one unit below cap, to test boundary transition;
- ledger exactly at cap;
- duplicate-only workload requiring no new exposure;
- new-only workload requiring new disclosure;
- safe snapshot containing only pre-charged units;
- deliberately contaminated snapshot containing one new unit;
- override allowance of zero;
- repeated use of one override token;
- oracle with identical task requirements and request order.

## Required outputs

- pre-exhaustion union and nominal cap;
- post-cap released old and new units;
- post-cap exposure gain and first violating request;
- exact replay, downgrade, snapshot, override and denial counts;
- false-denial events for tasks satisfiable from prior exposure;
- task completion and minimum-required-new-units;
- override allowance issued, used, replayed and denied;
- terminal response class and requests to termination;
- response metadata, policy-state reads and audit writes.

## Statistical plan

- paired policy differences under identical seeds;
- confidence intervals for post-cap gain and task completion;
- security–post-exhaustion-utility frontier;
- duplicate-only and new-only workloads reported separately;
- worst task-criticality class, without assigning legal priority;
- boundary tests separated from steady exhausted-state requests;
- contaminated snapshot and override replay reported as invariant failures.

## Stop conditions

Stop and repair the experiment if:

- any paired policy receives a different pre-exhaustion union or task;
- the ledger is not exactly at the stated cap;
- denied responses enter the exposure union;
- “coarse” outputs are assumed free without structural accounting;
- safe snapshots contain dynamically inserted post-cap fields;
- override disclosure is omitted from exposure gain;
- an override token can be replayed or forked;
- time or a new session silently resets the budget;
- evaluator task requirements enter deployable policy decisions;
- criticality labels are interpreted as legal or moral entitlement.
