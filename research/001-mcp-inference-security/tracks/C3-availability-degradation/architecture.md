# C3 Architecture

## Components

### Episode generator

Creates a 120-tick schedule containing task arrivals, structural requirements, deadlines, dependency latency, outage intervals, partition intervals and recovery load. Every policy receives the same seeded episode.

### Fixed security state

Provides one exact C1 shared ledger and a fixed C2 exhaustion state. C3 does not create new budget, change principal membership, or reinterpret previously exposed structural units.

### Dependency emulator

Models the availability of the accounting service, policy classifier, snapshot store and audit sink. It emits healthy, slowdown, outage, partition and recovery-storm conditions.

### Availability policy

One of:

- hard deny;
- replay-only;
- safe snapshot;
- graceful degradation;
- bounded queue and retry;
- fail-open baseline;
- evaluator-only availability oracle.

### Queue and retry manager

Tracks admission time, retry count, next retry tick, deadline, terminal timeout and recovery replay. Queue capacity and retry backoff are fixed across policies that use the component.

### Task evaluator

Knows which prior, coarse or new units are sufficient for each synthetic task. It records completion and quality without supplying ground truth to deployable policies.

### Exposure evaluator

Maintains the released structural union. Any fail-open or fallback response containing a new unit remains exposure even if the dependency later recovers.

## Time model

```text
tick 0 ─────────────── tick 119
  arrivals → admission → decision/queue → response/timeout
                           ↓
                 dependency condition
                           ↓
                recovery and queue drain
```

One tick is an abstract ordering/latency unit, not a millisecond claim.

## Trust boundaries

1. Client boundary — clients submit tasks and retries but cannot change deadlines or response classification after admission.
2. Dependency boundary — availability failures affect permitted evidence, not evaluator ground truth.
3. Queue boundary — queued tasks retain original budget domain, deadline and policy; dequeue cannot silently reset state.
4. Fallback boundary — cached/snapshot/coarse responses expose only explicitly modeled fields.
5. Evaluator boundary — task sufficiency and global exposure remain unavailable to deployable policies.

## Policy semantics

### Hard deny

Terminates protected requests immediately when the normal decision path cannot authorize them.

### Replay-only

Serves responses composed entirely of already exposed units; otherwise terminates with denial.

### Safe snapshot

Serves a pre-charged static artifact. Staleness is reported independently from exposure.

### Graceful degradation

Returns a reduced-quality response from an explicitly accounted fallback catalog. Unknown or novel fallback fields are denied.

### Bounded queue and retry

Queues unresolved tasks up to fixed capacity and deadline, with deterministic backoff. Expired work is not executed after recovery.

### Fail-open baseline

Continues normal responses without an available authorization decision. This is an intentionally unsafe availability baseline, not a recommendation.

### Oracle

Evaluator-only control that selects the highest-quality response available without new exposure and knows whether waiting will finish before the deadline.

## Invariants

1. Denied and timed-out tasks release no response exposure.
2. Fail-open exposure is never relabeled as safe after recovery.
3. Queue dequeue preserves the original cap state and deadline.
4. Expired tasks never execute.
5. Safe snapshots remain pre-charged and immutable.
6. Staleness and exposure are separate metrics.
7. Retry attempts are not counted as new tasks.
8. Oracle future knowledge never enters deployable policy evidence.

## Recovery semantics

Recovery restores dependency availability only. It does not replenish exposure budget, forgive earlier violations, or extend task deadlines. C6 owns budget recovery and decay.
