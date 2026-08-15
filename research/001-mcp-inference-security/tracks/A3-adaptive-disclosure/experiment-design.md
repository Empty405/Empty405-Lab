# A3 Experiment Design

## Hidden state

```text
12 locations × 8 resources × 3 epochs = 288 integer cells
```

## Compared modes

1. unrestricted exact responses;
2. hard block at matched exposure thresholds;
3. adaptive precision ladder;
4. adaptive ladder without hysteresis;
5. naive randomized ranges as a negative control.

The randomized control is included to demonstrate repeated-sampling risk, not proposed as a defense.

## Observer

A deterministic interval-composition observer maintains candidate intervals per cell. Every released response intersects the candidate interval.

## Legitimate task families

- threshold task: determine whether value exceeds 50;
- category task: determine low/medium/high;
- planning task: obtain a range no wider than 20;
- exact task: obtain the exact value;
- aggregate task: determine regional mean band.

A response is useful only if its declared precision satisfies the task.

## Attack streams

- full enumeration;
- repeated same-cell sampling;
- precision-boundary probing;
- alternating tools exposing the same cell;
- duplicate-heavy collection;
- mixed task-looking enumeration.

## Trials

- 1000 randomized states;
- root seed `40503`;
- identical streams across modes;
- checkpoints throughout the query stream;
- threshold sweep over at least five ladder configurations.

## Primary tests

### T1 — Utility at matched exposure

Compare adaptive disclosure with hard blocking at comparable final reconstruction score.

### T2 — Repeated-sampling resistance

Repeated queries at a fixed level must not narrow the observer interval below that level's declared width.

### T3 — Monotonic degradation

Within one epoch, exposure growth cannot produce a more precise level.

### T4 — Boundary stability

Small changes around thresholds cannot create oscillating precision when hysteresis is enabled.

### T5 — Cross-tool composition

Nested transformations for tool aliases cannot combine into a more precise result than policy intends.

### T6 — Provenance completeness

Every transformed response includes level, freshness, reason, transformation flag, and policy version.

## Falsification criteria

A3 is weakened or rejected if:

- adaptive utility does not exceed matched hard blocking;
- repeated outputs reconstruct exact values;
- small threshold perturbations cause unstable level switching;
- task-aware exceptions become an unbounded bypass;
- provenance is insufficient for downstream interpretation;
- utility gains exist only because adaptive mode leaks more information than the matched hard policy.

## Required negative result

The experiment must include a non-nested or randomized transformation that fails under repeated sampling, demonstrating why deterministic nested outputs are mandatory.
