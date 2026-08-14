# MCP Inference Security — Experiment 002 / v0.2 Stress Test

> Harder synthetic test of cumulative exposure accounting under larger state, dynamic time, heterogeneous tools, stronger reconstruction, and identity rotation.

**Research:** Empty405 Lab Research 001  
**Experiment:** 002  
**Version:** v0.2  
**Status:** Completed synthetic stress test  
**Runs:** 1000  
**Seed:** `40502`

---

## Why This Experiment Exists

v0.1 demonstrated a difference between:

```text
request frequency
```

and:

```text
cumulative structural exposure
```

under a very small 9-cell synthetic environment.

v0.2 deliberately attacks the assumptions of v0.1.

It asks whether the effect survives:

- 288 hidden cells;
- a new randomized state every run;
- three time steps;
- four overlapping tool projections;
- a stronger constraint-composition observer;
- one identity versus four rotating identities;
- a separate legitimate-task utility metric.

---

## Run

From the repository root:

```bash
python experiments/002-mcp-inference-security-stress-test/src/benchmark.py
```

Canonical result is written to:

```text
experiments/002-mcp-inference-security-stress-test/results/benchmark-v0.2.json
```

Plotting is optional and requires Matplotlib:

```bash
python experiments/002-mcp-inference-security-stress-test/src/plot_results.py
```

---

## Canonical v0.2 Result

The exact canonical values are stored in `results/benchmark-v0.2.json`.

The principal findings are:

### One identity

- Baseline information exposure: ~91.43%
- Hard per-identity coverage: ~27.30%
- Hard shared-principal coverage: ~27.30%
- Adaptive shared-principal exposure: ~72.33%
- Adaptive shared-principal utility: ~81.93%

### Four rotating identities

- Baseline information exposure: ~91.43%
- Hard per-identity coverage: ~91.43%
- Hard shared-principal coverage: ~27.30%
- Adaptive shared-principal exposure: ~72.33%
- Adaptive shared-principal utility: ~81.93%

The per-identity hard budget therefore collapses to baseline exposure under four-identity rotation in this synthetic attack strategy.

Shared-principal accounting does not.

---

## Main Interpretation

The most important v0.2 observation is not that hard blocking is strongest.

That is expected.

The important observation is that:

> exposure state scoped only to the presented identity can be reset by identity rotation, while exposure state shared across the logical principal remains stable.

Adaptive shared-principal disclosure preserves substantially more legitimate task utility than hard shared blocking, while exposing less structural information than baseline.

This remains a synthetic result.

---

## Files

```text
src/model.py
src/policies.py
src/observer.py
src/benchmark.py
src/plot_results.py
results/benchmark-v0.2.json
results/RESULTS.md
```

---

## Requirements

Benchmark:

```text
Python standard library only
```

Plots:

```text
matplotlib
```

---

## Boundary

This experiment does not solve principal identity.

It assumes that a gateway can associate multiple rotating client identities with one shared logical principal for the shared-principal modes.

That assumption is intentionally visible because it becomes a central production problem exposed by v0.2.
