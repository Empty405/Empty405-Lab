# MCP Inference Security — Experiment 001

> Reproducible toy experiment for cumulative cross-tool information reconstruction and exposure-aware disclosure controls.

**Project:** Empty405 Lab  
**Experiment Version:** v0.1  
**Status:** Completed Toy Proof-of-Concept  
**Random Seed:** `405`

---

## Research Question

This experiment asks:

> Can lightweight cumulative exposure accounting and adaptive disclosure reduce reconstruction of hidden state more effectively than conventional time-based rate limiting?

The experiment does not attempt to prove a general MCP vulnerability.

It tests a narrower synthetic hypothesis under controlled conditions.

---

## Experiment Overview

A hidden operational state contains nine values:

```text
3 locations × 3 resource types = 9 hidden cells
```

The observer is not given direct access to the complete hidden state.

Instead, simplified MCP-style tools expose partial information derived from the same state.

The observer combines these permitted responses and attempts to reconstruct the underlying values.

---

## Architecture

```text
                 Hidden State
                      │
                      ▼
               Synthetic Server
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
 Availability Tool         Capacity Band Tool
          │                       │
          └───────────┬───────────┘
                      ▼
                   Observer
                      │
                      ▼
               Reconstruction
```

For adaptive disclosure:

```text
Observer
   │
   ▼
Adaptive Gateway
   │
   ▼
Hidden State / Tools
```

The observer sees only the response released by the gateway.

---

## Hidden State

The current synthetic dataset is stored in:

```text
hidden_state.json
```

Example:

```json
{
  "locations": {
    "north": {
      "fuel": 82,
      "medical": 31,
      "food": 64
    }
  }
}
```

The full dataset contains:

- `north`
- `central`
- `south`

and:

- `fuel`
- `medical`
- `food`

---

## Partial Information Tools

### Availability Tool

Returns only whether a resource is above a threshold.

Example:

```json
{
  "location": "north",
  "resource": "fuel",
  "available": true
}
```

### Capacity Band Tool

Returns only a coarse category:

```text
low
medium
high
```

Neither tool exposes the exact hidden value directly.

The observer combines both responses to estimate the value.

---

## Baseline Reconstruction

The baseline observer combines:

```text
availability
+
capacity band
```

to estimate hidden values.

For example:

```text
Hidden value: 82

Availability:
true

Capacity:
high

Observer estimate:
84
```

In the initial dataset, the baseline reconstruction produced:

```text
Mean Absolute Error: 6.22
Simple Reconstruction Score: 93.78
```

The later unified benchmark reports a reconstruction score of:

```text
93.83%
```

---

## Experimental Modes

Four modes are compared.

### 1. Baseline

All permitted responses are returned normally.

```text
Observable state: 100%
```

### 2. Rate Limit + Waiting

The observer is temporarily rate-limited.

However, it waits for the rate-limit window to reset and continues querying.

This tests whether time-based rate limiting changes the final information available to a patient observer.

### 3. Hard Coverage Policy

The policy tracks unique:

```text
location × resource
```

combinations.

After five unique combinations have been exposed, new combinations are blocked.

Unlike a time-based rate limit, waiting does not reset this structural exposure state.

### 4. Adaptive Disclosure

Response precision decreases as cumulative structural coverage increases.

Current policy:

```text
Coverage 1–3
→ exact

Coverage 4–5
→ numeric range

Coverage 6–7
→ low / medium / high

Coverage 8+
→ limited
```

This tests whether useful access can be preserved while reducing cumulative reconstruction.

---

## Reproducible Benchmark

The main benchmark runs:

```text
1000 randomized trials
```

with fixed:

```text
random_seed = 405
```

The fixed seed makes the benchmark reproducible.

Run:

```bash
python experiments/001-mcp-inference-security/results/randomized_benchmark.py
```

Expected canonical result:

```text
Baseline
Reconstruction: 93.83%
Observable: 100.00%

Rate Limit + Waiting
Reconstruction: 93.83%
Observable: 100.00%

Hard Coverage Policy
Reconstruction: 52.13%
Observable: 55.56%

Adaptive Disclosure
Reconstruction: 75.71%
Observable: 77.78%
```

The raw canonical result is stored in:

```text
results/benchmark-v0.1.json
```

---

## Results

| Mode | Reconstruction Score | Observable State |
|---|---:|---:|
| Baseline | 93.83% | 100.00% |
| Rate Limit + Waiting | 93.83% | 100.00% |
| Hard Coverage Policy | 52.13% | 55.56% |
| Adaptive Disclosure | 75.71% | 77.78% |

Full interpretation:

[`results/RESULTS.md`](results/RESULTS.md)

---

## Preliminary Interpretation

In this synthetic environment:

### Time-based rate limiting

changed:

```text
collection time
```

but did not change:

```text
final observable state
```

once the observer was allowed to wait and continue.

### Structural exposure accounting

changed the final amount of state that could be observed.

### Adaptive disclosure

produced an intermediate security–utility trade-off:

```text
more utility than hard blocking
+
less reconstruction than baseline
```

---

## Metric

The current benchmark uses a project-specific normalized reconstruction metric.

For an estimable cell:

```text
score = 1 - (absolute_error / 100)
```

For an unknown or unavailable cell:

```text
score = 0
```

The final reconstruction score is the mean across all hidden cells.

This metric exists only to compare the experimental modes consistently.

It is not a standardized privacy or information-theoretic metric.

---

## Repository Structure

```text
001-mcp-inference-security/
├── README.md
├── hidden_state.json
├── server/
│   ├── tool_availability.py
│   ├── tool_capacity_band.py
│   └── adaptive_gateway.py
├── observer/
│   ├── reconstruct.py
│   ├── evaluate.py
│   ├── rate_limit_test.py
│   ├── rate_limit_wait_test.py
│   ├── coverage_test.py
│   └── adaptive_test.py
├── policies/
│   ├── rate_limit.py
│   ├── coverage_policy.py
│   └── adaptive_disclosure.py
└── results/
    ├── randomized_benchmark.py
    ├── benchmark-v0.1.json
    └── RESULTS.md
```

---

## Requirements

The current experiment uses only the Python standard library.

No third-party Python packages are required.

A recent Python 3 installation should be sufficient.

Check:

```bash
python --version
```

---

## Quick Reproduction

From the root of `Empty405-Lab`:

```bash
python experiments/001-mcp-inference-security/results/randomized_benchmark.py
```

For individual tests:

```bash
python experiments/001-mcp-inference-security/observer/reconstruct.py
```

```bash
python experiments/001-mcp-inference-security/observer/evaluate.py
```

```bash
python experiments/001-mcp-inference-security/observer/rate_limit_test.py
```

```bash
python experiments/001-mcp-inference-security/observer/rate_limit_wait_test.py
```

```bash
python experiments/001-mcp-inference-security/observer/coverage_test.py
```

```bash
python experiments/001-mcp-inference-security/observer/adaptive_test.py
```

---

## Limitations

This is intentionally a small synthetic experiment.

Current limitations include:

- only nine hidden cells;
- static hidden state;
- synthetic MCP-style tools rather than production MCP servers;
- deterministic observer logic;
- no LLM attacker;
- no multiple identities;
- no Sybil behavior;
- no cross-server coordination;
- no realistic distributed gateway;
- no production latency benchmark;
- no established privacy metric;
- simplified disclosure policies.

The results should not be generalized beyond this experimental environment.

---

## What This Experiment Does Not Claim

This experiment does not claim:

- that MCP is fundamentally insecure;
- that a new vulnerability class has been proven;
- that rate limiting is generally useless;
- that adaptive disclosure is a complete defense;
- that coverage accounting should become part of the MCP standard;
- that the current metric is scientifically sufficient.

The result supports only a narrow experimental observation:

> Under this synthetic model, cumulative structural exposure controls changed the final reconstruction outcome while conventional time-based rate limiting primarily changed collection time.

---

## Research Context

The experiment belongs to:

[`../../research/001-mcp-inference-security/`](../../research/001-mcp-inference-security/)

Research documents include:

- initial hypothesis;
- related work;
- gap analysis;
- experimental design.

---

## Next Version

Potential v0.2 work includes:

- larger randomized hidden states;
- dynamic state over time;
- additional tool schemas;
- stronger statistical observers;
- multiple identities;
- cross-server correlation;
- performance measurements;
- comparison with established privacy mechanisms.

v0.1 is intentionally kept small and reproducible.

---

*Build the smallest experiment capable of proving the idea wrong.*
