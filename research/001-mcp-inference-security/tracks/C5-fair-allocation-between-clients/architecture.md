# C5 Architecture

## Components

### Episode generator

Creates one paired 120-tick schedule containing durable principals, requests, structural units, task values, deadlines and declared client weights. Every policy receives the same episode.

### Client profiles

All principals are legitimate. Profiles vary independently in request frequency, burst timing, marginal exposure cost, task value and overlap with previously released units.

### Shared ledger

Maintains one exact structural exposure union and one fixed global cap. Atomic check-and-charge prevents overshoot and duplicate charging.

### Allocation policy

One of:

- global FIFO;
- equal reservation;
- weighted reservation;
- progressive max-min;
- proportional share;
- bounded borrowing;
- evaluator-only utility oracle.

### Allocation state

Tracks per-principal charges, guarantees, borrowed capacity, active demand and terminal outcomes. Zero-cost replay remains admissible without consuming a share.

### Utility evaluator

Measures request sufficiency and synthetic task value. Evaluator-only value and counterfactual feasibility never enter policies that do not explicitly receive declared weights.

## Request path

```text
request → principal state → marginal exposure cost → allocation rule
                                                  ↓
                                         atomic ledger charge
                                                  ↓
                                      response / replay / denial
                                                  ↓
                                  utility and fairness evaluator
```

## Trust boundaries

1. Identity boundary — durable principal mapping is fixed from B-track assumptions.
2. Client boundary — every client may choose legitimate timing and request content.
3. Observer boundary — marginal structural cost is exact in v0.1.
4. Weight boundary — declared weights are policy inputs, not evaluator task values.
5. Ledger boundary — global and per-principal charges conserve one cap.
6. Evaluator boundary — future demand, role-independent task value and oracle allocation remain hidden.

## Policy semantics

### Global FIFO

Admits in arrival order while the global remaining cap covers marginal cost.

### Equal reservation

Partitions the cap equally across principals. Unused reservations are not borrowed.

### Weighted reservation

Partitions the cap according to fixed declared weights. Unused shares remain isolated.

### Progressive max-min

Raises every active principal's charged allocation toward a common exposure level, admitting the least-allocated feasible principal first.

### Proportional share

Allocates according to declared weights while permitting continuous competition within the remaining global cap.

### Bounded borrowing

Guarantees a minimum equal share, then allows limited borrowing from currently inactive shares with explicit debt accounting.

### Utility oracle

Evaluator-only control maximizing completed synthetic task value under the same cap and request set.

## Invariants

1. Released exposure never exceeds the global cap.
2. Per-principal charges sum to global new exposure.
3. Duplicate/replay units cost zero.
4. Denied requests release no units.
5. Every request has exactly one terminal outcome.
6. All policies receive identical requests and arrivals.
7. Reservations and borrowing never create capacity.
8. Borrowed capacity is explicitly attributable.
9. Deployable policies cannot read oracle value or future demand.
10. Weight changes do not change the underlying request set.
