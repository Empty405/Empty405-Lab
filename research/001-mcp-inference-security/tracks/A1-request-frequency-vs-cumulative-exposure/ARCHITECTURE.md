# A1 Architecture

## Purpose

The architecture isolates traffic-rate enforcement from cumulative disclosure accounting so that the experiment does not confuse delay with reduced knowledge.

```text
Scenario Generator
      │ hidden state + canonical query stream
      ▼
Policy Harness ───────────────┐
  ├─ Baseline                 │ policy events
  ├─ Window Rate Limiter      ▼
  ├─ Lifetime Quota      Disclosure Ledger
  ├─ Coverage Budget           │
  └─ Hybrid                    │ released responses
      │                        ▼
      └──────────────────▶ Observer
                               │
                               ▼
                         Metrics Evaluator
```

## Components

### 1. Scenario Generator

Creates a static synthetic state and a deterministic canonical query stream. The same scenario is replayed against every policy.

Contract:

```json
{
  "scenario_id": "a1-static-001",
  "seed": 40501,
  "dimensions": ["location", "resource"],
  "state_path": "fixtures/hidden_state.json",
  "query_stream_path": "fixtures/queries.jsonl"
}
```

### 2. Policy Harness

Receives a logical timestamp, principal, tool, parameters, and proposed response. It returns one of:

- `release`;
- `delay_until`;
- `deny`.

A1 forbids precision transformation because adaptive disclosure belongs to A3/H3.

### 3. Window Rate Limiter

State key: `principal × time_window`.

State:

```text
request_count
window_start
```

The counter resets. A patient observer may advance logical time and retry.

### 4. Lifetime Quota

State key: `principal`.

Counts released requests and does not reset within the run. It separates the effect of non-resetting request quotas from coverage-aware accounting.

### 5. Coverage Budget

State key: `principal × epoch`.

Tracks unique disclosed cells:

```text
(location, resource)
```

A response consumes budget only when it exposes a previously undisclosed cell. A1 uses an exact set; approximate sketches belong to production-engineering tracks.

### 6. Disclosure Ledger

The ledger is append-only and policy-neutral.

Event schema:

```json
{
  "run_id": "string",
  "logical_time": 0,
  "policy": "rate_limit",
  "principal": "observer-0",
  "query_id": "q-001",
  "coverage_keys": ["north:fuel"],
  "decision": "release",
  "retry_at": null
}
```

It records decisions and released coverage without estimating semantic knowledge.

### 7. Observer

The same deterministic observer consumes only released responses. It cannot see policy state, denials beyond their existence, or the hidden state.

### 8. Metrics Evaluator

Computes curves at three axes:

- attempted queries;
- released queries;
- logical time.

This three-axis design is mandatory. Using only attempted-query count can make a rate limiter look like an exposure control; using only released-query count can hide its time cost.

## State separation

```text
policy state ≠ disclosure ledger ≠ observer knowledge ≠ hidden state
```

No component may read another component's private state except through declared events.

## Reproducibility

Every run records:

- code commit;
- configuration hash;
- seed;
- generated-state hash;
- query-stream hash;
- policy parameters;
- raw event ledger;
- metric output.

## Extension points

Later tracks may replace one component without redefining A1:

- B: principal resolver;
- D/G: observer;
- E: state generator and epochs;
- H: policies;
- I: metrics;
- J: ledger storage and distributed enforcement.
