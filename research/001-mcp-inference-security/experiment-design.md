# Minimal Experimental Design

**Project:** MCP Inference Security  
**Phase:** 4 — Minimal Experimental Design  
**Status:** Proposed Experiment  
**Version:** 0.1

---

## Goal

The purpose of this experiment is to test whether a passive observer can reconstruct sensitive operational state by combining individually permitted responses from multiple MCP-accessible tools over time.

The experiment is intentionally small.

It does not attempt to prove a universal security problem or validate a production architecture.

It asks one narrower question:

> Can cumulative information exposure across multiple tools reveal substantially more about a hidden state than any individual response reveals alone?

A secondary goal is to compare several simple defensive approaches and determine whether structural exposure accounting provides measurable value beyond conventional rate limiting.

---

## Hidden State

The experiment will use a synthetic hidden operational state.

Example:

```json
{
  "locations": {
    "north": {
      "fuel": 82,
      "medical": 31,
      "food": 64
    },
    "central": {
      "fuel": 17,
      "medical": 76,
      "food": 43
    },
    "south": {
      "fuel": 55,
      "medical": 12,
      "food": 91
    }
  }
}

This state represents information that should not be directly exposed as a complete dataset.

Individual fragments, however, may legitimately be available through different tools.

The observer's objective is to reconstruct as much of this hidden matrix as possible.

MCP Tools

The toy environment will expose several independent MCP-style tools.

Tool A — Availability

Example request:

{
  "location": "north",
  "resource": "fuel"
}

Example response:

{
  "available": true
}
Tool B — Capacity Band

Example response:

{
  "location": "north",
  "resource": "fuel",
  "level": "high"
}
Tool C — Regional Summary

Example response:

{
  "region": "north",
  "scarce_resources": ["medical"]
}

No individual tool exposes the complete hidden state.

The experiment tests whether repeated queries across these tools allow the observer to reconstruct it.

Observer

A passive automated observer will query the available tools.

The observer does not exploit software vulnerabilities, bypass authentication, or modify the server.

It only uses responses that the system intentionally permits it to receive.

The observer will:

enumerate allowed parameter combinations;
query multiple tools;
store returned information;
correlate responses;
estimate the hidden state;
measure reconstruction accuracy after each query.

This models cumulative information gathering rather than traditional unauthorized access.

Baseline

The first experiment will run without inference-aware protection.

Normal authorization rules remain active, but all permitted queries return their normal precision.

This establishes the baseline reconstruction curve.

We measure how quickly the observer learns the hidden state as the number of permitted queries increases.

Rate Limit Test

The second experiment introduces conventional rate limiting.

Example policy:

rate_limit:
  requests: 20
  window: 60s

The observer performs the same reconstruction task.

The experiment measures whether rate limiting prevents reconstruction or merely increases the time required to obtain the same information.

Coverage Accounting Test

The third experiment introduces lightweight structural exposure accounting.

Instead of attempting to calculate semantic knowledge, the system tracks coverage of the parameter space.

Example dimensions:

location × resource × time_window

For example:

north × fuel × epoch_1
north × medical × epoch_1
south × fuel × epoch_1

Repeated queries that reveal new combinations increase the observer's exposure score.

Repeated queries over already observed combinations contribute little or no additional structural coverage.

The purpose is to test whether simple structural accounting can approximate cumulative information exposure without requiring full semantic analysis.

Adaptive Disclosure Test

The fourth experiment combines structural coverage accounting with progressive precision reduction.

Example disclosure levels:

Level 0 — exact value
Level 1 — range
Level 2 — category
Level 3 — regional aggregate
Level 4 — unavailable

Example transformation:

82
↓
80–90
↓
high
↓
regional availability: normal
↓
insufficient disclosure budget

As structural exposure increases, future responses reveal less precise information.

The degradation must remain deterministic for the same identity and epoch so that the defense does not introduce arbitrary contradictory data.

Metrics

The experiment will record:

Reconstruction Accuracy

How accurately the observer reconstructs the hidden state.

Query Count

How many permitted queries are required to reach a given reconstruction accuracy.

Structural Coverage

What percentage of the defined parameter space has been exposed.

Legitimate Utility

How much useful information remains available to a normal client.

Added Latency

Additional processing time introduced by exposure accounting and disclosure controls.

State Overhead

Amount of additional state required to track exposure.

Success Criteria

The hypothesis receives preliminary support if:

the baseline allows substantial reconstruction of hidden state;
conventional rate limiting primarily delays reconstruction rather than preventing it;
structural coverage correlates with reconstruction progress;
adaptive disclosure significantly reduces reconstruction accuracy;
legitimate client utility remains meaningfully higher than attacker reconstruction capability;
accounting overhead remains small enough for a lightweight gateway implementation.

This would not prove that the mechanism should become part of MCP.

It would justify further experimentation.

Failure Criteria

The hypothesis should be weakened or rejected if:

cross-tool responses do not materially improve reconstruction;
ordinary rate limiting provides equivalent protection;
structural coverage does not correlate with information gained;
adaptive disclosure destroys legitimate utility;
accounting requires excessive state or latency;
the observed problem exists only because of unrealistic assumptions in the toy environment.

A negative result is considered useful.

The purpose of the experiment is to test the hypothesis, not defend it.

Expected Output

The experiment should produce:

experiment/
├── hidden_state.json
├── server/
├── observer/
├── policies/
├── results/
└── README.md

Expected result data should allow comparison of:

Baseline
vs
Rate Limiting
vs
Coverage Accounting
vs
Adaptive Disclosure

The primary visualization should show:

Observer Reconstruction Accuracy
            ↑
100% ┤
     │
 75% ┤
     │
 50% ┤
     │
 25% ┤
     │
  0% ┼────────────────────────────→
       Number of Permitted Queries

Each defensive mode should produce its own reconstruction curve.

Research Question

The experiment ultimately asks:

Does lightweight cumulative exposure accounting combined with adaptive disclosure reduce cross-tool state reconstruction more effectively than conventional per-request rate limiting?

If the answer is yes, Phase 5 can investigate a minimal gateway prototype.

If the answer is no, the proposed architecture should be reconsidered before additional implementation work.
