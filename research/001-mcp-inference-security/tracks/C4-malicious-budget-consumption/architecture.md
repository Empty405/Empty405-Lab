# C4 Architecture

## Components

### Episode generator

Creates a 120-tick paired schedule of legitimate tasks, principal identities, structural requirements, deadlines and attacker opportunities. Every policy receives the same seeded episode.

### Fixed shared-budget state

Provides one exact C1 ledger, one disclosure universe and a fixed remaining cap. C4 never resets, decays or replenishes budget.

### Principal registry

Maps requests to durable synthetic principals established by the B-track assumptions. The evaluator marks principals as legitimate or adversarial, but deployable policies receive only stable IDs and request history.

### Attacker strategy

One of:

- frequency flood — many low-cost requests;
- novelty maximizer — requests with high marginal exposure;
- front-loaded burn — consumes budget before legitimate arrivals;
- adaptive burn — selects the highest admissible marginal cost from observable outcomes;
- camouflage — matches benign timing while targeting novel units;
- benign-load control — identical volume without strategic novelty selection.

### Admission policy

One of:

- global FIFO;
- global rate limit;
- per-principal reservation;
- per-principal marginal-cost cap;
- weighted fair share;
- bounded hybrid;
- evaluator-only oracle.

### Shared ledger

Atomically charges the union of newly released structural units. Duplicate or replayed units cost zero additional budget. Denied requests release no units.

### Task and exposure evaluator

Measures legitimate task sufficiency, attacker capture and released exposure. Future legitimate value and attacker role remain evaluator-only.

## Request path

```text
request → principal history → marginal-cost estimate → admission policy
                                                     ↓
                                            atomic ledger charge
                                                     ↓
                                      response / replay / denial
                                                     ↓
                                      utility and harm evaluator
```

## Trust boundaries

1. Client boundary — clients choose timing and allowed request content but cannot forge evaluator labels.
2. Identity boundary — principal IDs are fixed inputs from B-track assumptions; C4 does not solve Sybil resistance.
3. Observer boundary — v0.1 uses exact structural marginal cost; semantic estimation error belongs to D.
4. Ledger boundary — check-and-charge is atomic and globally consistent.
5. Policy boundary — deployable policies cannot see attacker role, future demand or oracle task value.
6. Evaluator boundary — counterfactual legitimate utility and optimal allocation never enter policy evidence.

## Policy semantics

### Global FIFO

Admits requests in arrival order while remaining cap covers exact marginal exposure.

### Global rate limit

Limits request count per principal per window without considering marginal exposure cost.

### Per-principal reservation

Reserves a fixed minimum budget share for each active principal; unused reserved capacity is not borrowed during the primary episode.

### Per-principal marginal-cost cap

Bounds how much new exposure one principal may consume while allowing zero-cost replay.

### Weighted fair share

Allocates equal synthetic weights across active principals and admits within each share.

### Bounded hybrid

Combines a request-rate ceiling, per-principal exposure ceiling and a small shared overflow pool.

### Oracle

Evaluator-only control that maximizes legitimate completed task value under the same global exposure cap and schedule.

## Invariants

1. Total charged exposure never exceeds the fixed cap.
2. Duplicate or replay requests never consume budget twice.
3. Denied requests release no response exposure.
4. One request has exactly one terminal outcome.
5. Policy decisions cannot use attacker labels or future arrivals.
6. Identity rotation and Sybil creation are disabled in the primary matrix.
7. Reservation and fair-share accounting conserve the global cap.
8. Attacker traffic and benign-load controls match declared volume and timing.
9. No policy silently replenishes budget.
10. Oracle knowledge never enters deployable policy inputs.
