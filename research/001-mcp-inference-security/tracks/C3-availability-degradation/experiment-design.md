# C3 Experiment Design

## Primary experiment

Hold task arrivals, task requirements, deadlines, ledger state, exposure cap and dependency schedule constant. Vary only the availability policy, disruption condition, workload intensity and synthetic task criticality.

## Independent variables

- policy: hard deny, replay-only, safe snapshot, graceful degradation, bounded queue/retry, fail-open, oracle;
- disruption: healthy, slowdown, outage, partition, recovery storm;
- workload intensity: low, burst, sustained;
- task criticality: optional, routine, critical;
- paired trial seed: 200 trials per configuration.

## Minimum v0.1 matrix

`7 policies × 5 disruptions × 3 workload intensities × 3 task-criticality classes × 200 paired trials = 63,000 trials`.

The primary matrix fixes 120 ticks, one budget domain, one exact cap state, deterministic queue capacity, retry schedule, task deadlines and pre-charged fallback catalog. Replica count, multi-tenant fairness and budget recovery are excluded.

## Paired trial procedure

1. Generate one 120-tick task-arrival and dependency schedule.
2. Assign identical structural requirements, quality target and deadline to each paired policy.
3. Initialize the exact ledger/cap and pre-charged fallback catalog.
4. At each tick, admit arrivals and apply the current dependency condition.
5. Let the selected policy deny, respond, degrade, queue or fail open.
6. Process retries without creating duplicate logical tasks.
7. Expire overdue tasks before any recovery execution.
8. Drain eligible queued work during recovery within fixed capacity.
9. Record task outcome, latency, response quality, staleness, queue state and exposure.
10. Compare with fail-open and oracle controls under the same seed.

## Controls

- healthy dependency with no exhaustion pressure;
- exact cap with duplicate-only tasks;
- complete outage lasting beyond every deadline;
- one-tick slowdown shorter than retry backoff;
- queue capacity zero;
- queue capacity sufficient for all arrivals;
- immutable pre-charged snapshot;
- fallback contaminated with one new structural field;
- fail-open baseline;
- oracle with identical future schedule.

## Required outputs

- logical task ID, arrival, deadline and terminal tick;
- success, denial, timeout, degraded and stale outcomes;
- response quality and task completion;
- first-response and completion latency;
- queue length, peak queue, retries and dropped tasks;
- recovery drain rate and recovery completion time;
- released new units and exposure-violation events;
- safe replay/snapshot/fallback counts;
- dependency calls, policy reads, audit writes and metadata bytes.

## Statistical plan

- paired policy differences under identical episodes;
- confidence intervals for completion, timeout and exposure violation;
- p50/p95/p99 latency from raw task events;
- security–availability Pareto frontier;
- disruption phases reported separately;
- queue stability under sustained versus burst load;
- recovery-storm backlog and deadline survival;
- criticality sensitivity without policy priority semantics.

## Stop conditions

Stop and repair the experiment if:

- paired policies receive different arrivals, deadlines or disruptions;
- retries are counted as new logical tasks;
- denied or timed-out tasks release response exposure;
- expired queued work executes after recovery;
- fail-open disclosure is erased after reconciliation;
- snapshot staleness is counted as new exposure or vice versa;
- recovery replenishes budget or extends deadlines;
- oracle future knowledge enters deployable policies;
- averages hide tail latency or recovery-storm failure;
- criticality labels automatically authorize bypass.
