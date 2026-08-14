# MCP Inference Security v0.2: Identity Rotation and Shared Exposure Budgets

> A synthetic stress test of cumulative exposure accounting under larger state, dynamic time, heterogeneous tool projections, and rotating identities.

**Project:** Empty405 Lab  
**Research:** 001  
**Version:** v0.2  
**Experiment:** 002  
**Runs:** 1000 randomized trials  
**Random seed:** `40502`

---

## Abstract

v0.1 of MCP Inference Security tested whether cumulative structural exposure controls could change hidden-state reconstruction in a small synthetic MCP-style environment.

v0.2 deliberately attacks the assumptions of that first experiment.

The state space increases from 9 to 288 cells per run, the hidden state is regenerated every trial, values change across three time steps, four overlapping tool projections are exposed, the observer composes constraints across tools, and the benchmark introduces identity rotation.

Five modes are compared:

1. baseline;
2. rate limiting with waiting;
3. hard coverage scoped per identity;
4. hard coverage shared across a logical principal;
5. adaptive disclosure shared across a logical principal.

Across 1000 fixed-seed randomized trials, the central result is that a hard structural budget scoped only to the presented identity collapses under four-identity rotation:

```text
one identity:  27.30% information exposure
four identities: 91.43% information exposure
```

The four-identity result is effectively baseline:

```text
baseline: 91.43%
```

In contrast, hard and adaptive policies sharing one cumulative principal state remain stable under rotation.

Adaptive shared-principal disclosure preserves approximately:

```text
81.93% task utility
```

at approximately:

```text
72.33% information exposure
```

This remains a synthetic result.

It does not solve principal identity, establish a production privacy guarantee, or demonstrate a vulnerability in MCP.

It narrows the next engineering problem:

> cumulative exposure accounting is only as durable as the identity or principal boundary to which the budget is attached.

---

## 1. Why v0.2 Exists

The purpose of v0.1 was to determine whether a simple distinction was experimentally visible:

```text
request frequency
vs
cumulative structural exposure
```

It was.

But v0.1 left several obvious weaknesses:

- nine static cells;
- one identity;
- two main partial-information projections;
- a simple reconstruction heuristic;
- utility approximated by observability.

v0.2 addresses those weaknesses without changing the underlying research question into a larger claim.

---

## 2. Harder Environment

Every run contains:

```text
12 locations
× 8 resources
× 3 time steps
= 288 hidden cells
```

A new state is generated on every run.

The first time step is random.

Subsequent states drift stochastically and remain bounded to the `0–100` domain.

This removes the fixed 3×3 hidden matrix used in v0.1.

---

## 3. Heterogeneous Tool Projections

Four synthetic tools expose overlapping projections of each semantic cell.

### Availability

```text
value >= 50
```

### Capacity band

```text
q1 = 0–24
q2 = 25–49
q3 = 50–74
q4 = 75–100
```

### Numeric range

```text
10-point bucket
```

### Trend

```text
up
stable
down
```

No single abstraction is treated as the hidden state itself.

The observer composes the projections.

---

## 4. Stronger Observer

The observer begins with:

```text
0–100
```

as the feasible domain for every hidden cell.

Released numeric constraints are intersected.

For example:

```text
availability = true
band = q3
range = 60–69
```

reduces the feasible state to:

```text
60–69
```

The midpoint becomes the reconstruction estimate.

The benchmark records:

- remaining interval width;
- information exposure;
- mean absolute error;
- reconstruction within ±5 units.

This is stronger than the v0.1 two-signal midpoint heuristic, but it remains a deterministic synthetic observer.

---

## 5. Identity Rotation

The experiment executes every mode twice:

```text
1 identity
```

and:

```text
4 rotating identities
```

For an identity-local policy, cells are distributed across identities so each identity consumes a separate budget.

For shared-principal policies, all four identities consume one cumulative structural state.

This is not a claim about real-world Sybil resolution.

It is a stress test of budget scope.

---

## 6. Policies

### Baseline

All tool projections are available.

### Rate Limit + Waiting

As in v0.1, the patient observer is allowed to wait and continue.

The eventual informational outcome is therefore modeled as baseline.

### Hard Coverage — Per Identity

Each identity can expose 30% of semantic cells.

A new identity receives a fresh budget.

### Hard Coverage — Shared Principal

All identities jointly receive one 30% semantic budget.

### Adaptive Disclosure — Shared Principal

Coverage is shared across identities.

Precision changes as cumulative unique semantic coverage grows:

```text
first 30% → full
next 40%  → coarse
last 30%  → minimal
```

No false information is introduced.

---

## 7. Separate Security and Utility Metrics

v0.2 removes the v0.1 assumption that observable percentage is a sufficient utility proxy.

### Information Exposure

A project-specific interval-narrowing metric measures how much the feasible `0–100` domain has been reduced.

### Legitimate Task Utility

A separate weighted task proxy is used:

```text
availability = 50%
band         = 30%
trend        = 20%
```

This allows coarse answers to remain useful even when they are less reconstructive.

Neither metric is standardized.

---

## 8. Canonical Results

### One Identity

| Mode | Exposure | Task Utility | Within ±5 |
|---|---:|---:|---:|
| Baseline | 91.43% | 100.00% | 100.00% |
| Rate Limit + Waiting | 91.43% | 100.00% | 100.00% |
| Hard / Identity | 27.30% | 29.86% | 37.53% |
| Hard / Shared | 27.30% | 29.86% | 37.53% |
| Adaptive / Shared | 72.33% | 81.93% | 52.12% |

### Four Rotating Identities

| Mode | Exposure | Task Utility | Within ±5 |
|---|---:|---:|---:|
| Baseline | 91.43% | 100.00% | 100.00% |
| Rate Limit + Waiting | 91.43% | 100.00% | 100.00% |
| Hard / Identity | 91.43% | 100.00% | 100.00% |
| Hard / Shared | 27.30% | 29.86% | 37.53% |
| Adaptive / Shared | 72.33% | 81.93% | 52.12% |

---

## 9. Identity-Local Budget Failure

The strongest new result is the identity-rotation test.

Hard per-identity coverage changes from:

```text
27.30%
```

to:

```text
91.43%
```

when the attacker rotates across four identities.

That matches baseline exposure in this benchmark.

The security mechanism has not been mathematically defeated.

Its **scope has been reset**.

This is a different problem.

---

## 10. Shared Principal as an Architectural Dependency

Hard shared coverage remains near:

```text
27.30%
```

under the same rotation.

Adaptive shared disclosure remains near:

```text
72.33%
```

This makes a hidden assumption explicit:

> cumulative exposure control requires a durable principal boundary that survives session and client identity changes.

v0.2 does not solve that boundary.

It identifies it as a dependency.

---

## 11. Security–Utility Result

Hard shared coverage yields lower exposure:

```text
27.30%
```

but also only:

```text
29.86%
```

task utility.

Adaptive shared disclosure yields:

```text
72.33% exposure
81.93% task utility
```

The result is not a universal optimum.

It demonstrates why utility should be measured separately from disclosure.

---

## 12. Limitations

v0.2 remains synthetic.

Important limitations include:

- no production MCP server;
- no networked gateway;
- no real authentication system;
- no real principal-resolution mechanism;
- deterministic constraint observer;
- interval-based exposure metric;
- synthetic task utility weights;
- only four tool schemas;
- only four rotating identities;
- no colluding organizations;
- no differential privacy comparison;
- no learned attacker;
- no measured gateway latency.

The result therefore remains an engineering stress-test signal.

---

## 13. Reproducibility

Run:

```bash
python experiments/002-mcp-inference-security-stress-test/src/benchmark.py
```

Canonical configuration:

```text
runs = 1000
seed = 40502
cells per run = 288
```

Raw canonical output:

```text
experiments/002-mcp-inference-security-stress-test/results/benchmark-v0.2.json
```

Full results:

```text
experiments/002-mcp-inference-security-stress-test/results/RESULTS.md
```

---

## Conclusion

v0.1 showed that request frequency and cumulative structural exposure were not equivalent in a small synthetic environment.

v0.2 makes that observation harder to preserve.

The effect survives a larger randomized state, temporal change, overlapping tools, and a stronger reconstruction process when the exposure budget is shared across a durable logical principal.

It does not survive identity rotation when the budget is scoped independently to each presented identity.

That shifts the research problem.

The next architectural question is not merely:

> How should cumulative exposure be counted?

It is:

> What stable principal should cumulative exposure belong to, and how can that principal be established without creating an invasive or brittle identity system?

That question remains open.

---

**Empty405 Lab**

*Make the experiment harder before making the claim larger.*
