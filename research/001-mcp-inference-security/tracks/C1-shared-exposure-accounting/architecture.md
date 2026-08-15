# C1 Architecture

## Components

### Workload generator

Creates one fixed sequence of structural disclosure keys, duplicates, overlaps, clients, services and concurrent request batches. Every accounting mechanism receives the same seeded workload.

### Policy mapper

Maps an already-attributed principal and resource scope to a `budget_domain_id`. C1 treats this mapping as fixed input so attribution errors from B6 do not contaminate accounting results.

### Decision points

Gateway or server replicas decide whether a disclosure key may be released. A decision point can use only state permitted by its tested mechanism and current network condition.

### Shared-accounting mechanism

One of:

- independent local ledgers;
- synchronous central exact ledger;
- eventual merge ledger;
- hierarchical parent/child reservations;
- escrow rights with bounded local spend;
- evaluator-only oracle.

### Exposure evaluator

Maintains the true union of disclosures released to the budget domain. It detects double spend, delayed overrun, false charge and disagreement but never supplies ground truth to deployable mechanisms.

### Audit sink

Records decisions, local and merged state, synchronization messages, reservations, rights transfers, denials and evaluator outcomes.

## State model

```text
budget domain
├── nominal budget
├── structural disclosure universe
├── released union (evaluator only)
├── replica-local observed sets
├── reserved or escrow rights
└── synchronization/audit events
```

A shared ledger must distinguish a new disclosure from an already charged duplicate. Scalar request counters are an intentionally weak baseline because they cannot represent overlap.

## Trust boundaries

1. Client boundary — clients may replay or concurrently submit the same workload but cannot write ledger state.
2. Decision boundary — replicas can release data only after a mechanism-specific authorization decision.
3. Coordination boundary — central services, brokers or peer replicas observe only the metadata explicitly exchanged by the mechanism.
4. Evaluator boundary — ground-truth union and global chronology are unavailable to deployable components.
5. Organization boundary — cross-organization messages expose a separately measured visibility surface.

## Accounting invariants

### Conservation

For hard-cap mechanisms, the union of newly released disclosure keys must not exceed the nominal budget.

### No double charge

Releasing an already-accounted disclosure key must not consume additional budget solely because it was served by another replica.

### Bounded local authority

During partition, a replica cannot authorize more new disclosure than its current reservation or escrow rights.

### No post-hoc repair claim

An eventual merge can detect an overrun but cannot retroactively retract disclosure; detected-late exposure remains a security failure.

### Evaluator isolation

Mechanism decisions must remain unchanged if evaluator-only identifiers and global chronology are removed.

## Failure semantics

- Central exact accounting fails closed when its ledger is unavailable in v0.1.
- Eventual accounting continues locally and reconciles after delay or partition.
- Hierarchical reservation and escrow continue only within preallocated authority.
- Lost or stranded reservations are not silently recreated.
- Rejoin merges accounting state but never removes previously released exposure.

## Privacy boundary

C1 measures which operators can observe a budget-domain key and which disclosure keys cross coordination boundaries. It does not claim anonymity: privacy-preserving domain membership and federated governance remain B6 and F6 concerns.
