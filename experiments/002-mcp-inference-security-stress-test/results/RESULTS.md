# Experimental Results — MCP Inference Security v0.2

**Research:** 001  
**Experiment:** 002  
**Runs:** 1000  
**Random seed:** `40502`  
**Cells per run:** 288  
**Status:** Synthetic Stress Test

---

## Research Question

> Does an exposure-aware security–utility advantage survive larger randomized state spaces, dynamic state, heterogeneous tool projections, stronger reconstruction, and identity rotation?

---

## Environment

Each run contains:

```text
12 locations
× 8 resources
× 3 time steps
= 288 hidden cells
```

The state is regenerated on every randomized run.

Four overlapping tool projections are available:

- availability;
- four-level capacity band;
- 10-point numeric range;
- temporal trend.

The observer intersects all released numeric constraints and reconstructs the remaining feasible interval.

---

## Results — One Identity

| Mode | Information Exposure | MAE | Within ±5 | Task Utility | Observable |
|---|---:|---:|---:|---:|---:|
| Baseline | 91.43% | 2.21 | 100.00% | 100.00% | 100.00% |
| Rate Limit + Waiting | 91.43% | 2.21 | 100.00% | 100.00% | 100.00% |
| Hard Coverage / Identity | 27.30% | 18.75 | 37.53% | 29.86% | 29.86% |
| Hard Coverage / Shared | 27.30% | 18.75 | 37.53% | 29.86% | 29.86% |
| Adaptive / Shared | 72.33% | 7.50 | 52.12% | 81.93% | 100.00% |

With one identity, per-identity and shared-principal hard coverage are equivalent.

---

## Results — Four Rotating Identities

| Mode | Information Exposure | MAE | Within ±5 | Task Utility | Observable |
|---|---:|---:|---:|---:|---:|
| Baseline | 91.43% | 2.21 | 100.00% | 100.00% | 100.00% |
| Rate Limit + Waiting | 91.43% | 2.21 | 100.00% | 100.00% | 100.00% |
| Hard Coverage / Identity | 91.43% | 2.21 | 100.00% | 100.00% | 100.00% |
| Hard Coverage / Shared | 27.30% | 18.75 | 37.53% | 29.86% | 29.86% |
| Adaptive / Shared | 72.33% | 7.50 | 52.12% | 81.93% | 100.00% |

---

## Main Finding 1 — Identity-Local Budgets Are Resettable

The hard per-identity policy moves from:

```text
27.30% information exposure
```

with one identity to:

```text
91.43% information exposure
```

with four rotating identities.

Under this attack strategy, it effectively returns to baseline exposure.

This does not prove that production identity systems are bypassable.

It shows that **where the cumulative budget is scoped** is a first-order design question.

---

## Main Finding 2 — Shared Exposure State Survives Rotation

Hard shared-principal coverage remains at approximately:

```text
27.30% information exposure
```

under four identities.

Adaptive shared-principal disclosure remains at approximately:

```text
72.33% information exposure
```

with:

```text
81.93% legitimate task utility
```

The synthetic result therefore supports investigating exposure state above the raw session/client-identity layer.

---

## Main Finding 3 — Utility and Exposure Are Not the Same Metric

Adaptive shared-principal disclosure exposes approximately:

```text
72.33%
```

while preserving approximately:

```text
81.93%
```

task utility.

This happens because low-resolution responses can remain sufficient for some legitimate operational tasks while carrying less reconstructive precision than high-resolution responses.

The utility metric is still project-specific.

The result should therefore be interpreted as a stress-test signal, not a production guarantee.

---

## Metric Limitations

`information_exposure_percent` is based on interval narrowing.

It is not:

- entropy;
- mutual information;
- differential privacy epsilon;
- a formal privacy-loss bound.

`legitimate_task_utility_percent` is a weighted synthetic task proxy.

It is not a measured user or production workload.

These choices are intentionally explicit.

---

## What v0.2 Supports

The experiment supports further investigation of:

- shared-principal exposure accounting;
- cross-identity budget coordination;
- semantic-key normalization across tools;
- adaptive precision reduction;
- security–utility optimization.

---

## What v0.2 Does Not Prove

v0.2 does not prove:

- that MCP itself is insecure;
- that Sybil resistance is solved;
- that shared principals are easy to identify;
- that interval narrowing is the correct production privacy metric;
- that adaptive disclosure beats established privacy mechanisms;
- that the synthetic utility weights generalize.

---

## Conclusion

v0.2 survives several stressors that were absent from v0.1:

- larger randomized state;
- temporal change;
- overlapping tool projections;
- stronger constraint composition;
- identity rotation.

It also exposes a major architectural dependency:

> an exposure budget scoped only to the presented identity can be reset by identity rotation.

In this synthetic benchmark, shared-principal accounting survives that rotation.

Adaptive shared-principal disclosure preserves more task utility than hard shared blocking while remaining below baseline information exposure.

The next question is no longer whether identity matters.

It is whether a real system can establish and coordinate a meaningful principal boundary cheaply and safely.
