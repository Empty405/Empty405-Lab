# C3 Falsification Plan

## Claims under test

1. Hard deny and fail-closed behavior preserve exposure but can collapse useful availability.
2. Replay, safe snapshot and accounted graceful degradation recover some availability without new exposure.
3. Queue/retry improves short-disruption completion but can worsen tail latency and recovery storms.
4. Fail-open improves apparent completion by accepting measurable exposure violations.
5. No tested deployable policy dominates security, useful availability, latency tails and operational cost in every disruption.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- hard deny matches safe fallback policies on useful completion under replayable workloads;
- safe snapshots or accounted degradation produce unavoidable new exposure;
- queue/retry never improves short-outage completion or never worsens recovery backlog;
- fail-open produces no additional exposure over safe policies;
- tail latency and timeout remain unchanged across disruptions;
- one deployable policy dominates all others on security, completion, tails and cost with uncertainty included;
- differences arise from unequal task schedules rather than policy behavior.

## Critical counterexamples

- a timed-out task executes after recovery and produces an unwanted side effect;
- retry creates duplicate logical tasks or duplicate external actions;
- queue capacity is exceeded silently;
- a stale snapshot is mislabeled current and causes task failure;
- fail-open disclosure disappears from the audit after reconciliation;
- a contaminated fallback is treated as safe because it is low quality;
- recovery silently restores exposure budget;
- critical tasks bypass the cap solely because of a label;
- fast denial is reported as successful low latency.

## Confounders

- different arrivals, deadlines or dependency schedules between policies;
- mixing C1 accounting inconsistency into C3;
- mixing C6 budget recovery into dependency recovery;
- removing timeouts from latency distributions;
- counting retries as tasks;
- treating any response as useful completion;
- averaging healthy and outage periods;
- hiding exposure behind aggregate uptime.

## Interpretation boundaries

C3 evaluates synthetic service availability under exposure-control constraints. It does not define a real production SLO, legal emergency-access rule, acceptable medical/safety risk, or client priority.

Fail-open is an intentionally unsafe comparison baseline. Better uptime in this model is not evidence that fail-open should be deployed.
