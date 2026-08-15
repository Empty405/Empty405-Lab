# C2 Architecture

## Components

### Pre-exhaustion fixture

Creates a budget domain whose exact structural exposure union equals the nominal cap. The fixture also stores previously released responses, pre-approved safe snapshots, and evaluator-only task requirements.

### Exhaustion gate

Receives the exact C1 ledger state and labels the domain `exhausted` before any post-cap request is evaluated. It must not create a new ledger, session, account, or local fallback budget.

### Response classifier

Classifies a candidate response as:

- exact replay of already exposed units;
- new structural disclosure;
- mixed old and new disclosure;
- coarse fallback;
- pre-approved safe snapshot;
- bounded override disclosure.

The classifier uses structural keys in v0.1. Semantic equivalence is not assumed solved.

### Post-exhaustion policy engine

One of:

- hard deny;
- replay-only;
- coarse fallback;
- safe snapshot;
- bounded override token;
- evaluator-only cap-aware oracle.

### Task evaluator

Knows which already exposed or new units are minimally required to complete the synthetic task. This ground truth is never passed to deployable policies except the evaluator-only oracle control.

### Audit sink

Records the boundary transition, response class, policy decision, denial reason, released units, override use, task progress, and terminal outcome.

## State model

```text
exhaustion episode
├── nominal cap
├── pre-exhaustion union == cap
├── cached exact responses
├── pre-approved safe snapshots
├── post-cap request sequence
├── explicit override allowance
└── evaluator-only task requirements
```

## Trust boundaries

1. Client boundary — the client can replay, reorder, or adapt requests but cannot relabel a response as previously exposed.
2. Ledger boundary — the exhaustion gate receives exact C1 state and cannot silently create a fresh budget.
3. Classifier boundary — representation labels are policy inputs, not evaluator truth about semantic equivalence.
4. Override boundary — exceptional authority is explicit, bounded, auditable, and included in exposure metrics.
5. Evaluator boundary — task sufficiency and the global exposure union are unavailable to deployable policies.

## Policy semantics

### Hard deny

Rejects every post-exhaustion request, including exact replay.

### Replay-only

Allows a response only when every structural unit is already in the pre-exhaustion union.

### Coarse fallback

Returns a lower-resolution representation. Any coarse key not already covered by the accounting schema counts as new exposure; the word “coarse” does not make it free.

### Safe snapshot

Returns one of a fixed set of artifacts approved and charged before exhaustion. No dynamic fields may be inserted after the boundary.

### Bounded override

Allows a small, explicit number of new structural units. Override exposure is a policy violation budget, not ordinary recovery or a silent reset.

### Oracle

Evaluator-only control that reuses the minimum already exposed information sufficient for the task and denies tasks requiring new exposure beyond the cap.

## Invariants

1. Exhaustion never creates a new ordinary budget.
2. Denied requests add no exposure.
3. Exact replay consumes no new structural budget.
4. Every newly released unit after cap appears in `post_cap_exposure_gain`.
5. Safe snapshots contain only pre-charged units.
6. Override authority is finite and cannot be replayed or forked.
7. Time alone does not restore budget in C2.
8. Oracle task requirements never enter deployable policy evidence.

## Boundary to later modules

C2 produces denial, downgrade and terminal-task outcomes. C3 will model their availability cost over time; C4 will add malicious exhaustion/override use; C5 will compare client allocation; C6 will introduce explicit recovery and decay.
