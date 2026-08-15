# A4 Experiment Design

## Unified state

```text
12 locations × 8 resources × 3 epochs
```

Use the same randomized states and query order for every policy.

## Policy grid

- exact baseline;
- rate limits across at least five request/window settings;
- hard request quotas across exposure targets;
- exact coverage caps across exposure targets;
- hybrid rate plus coverage;
- three A3 adaptive ladders;
- deny-all and release-all sanity controls.

## Workload profiles

1. balanced: equal task weights;
2. exact-critical;
3. category-first;
4. aggregate-planning;
5. deadline-critical;
6. adversarial enumeration plus separate legitimate workload.

## Deadlines

Evaluate patient, long, medium, and short deadline conditions.

## Trials

- 1000 randomized states;
- root seed `40504`;
- paired trials across policies;
- raw per-trial records retained;
- bootstrap 95% confidence intervals.

## Primary analyses

### Pareto frontier

Compute non-dominated configurations for risk, macro utility, minimum-task utility, delay, and ledger size.

### Robust dominance

A configuration is robustly dominated only if dominance persists across at least four workload profiles and bootstrap uncertainty does not reverse the comparison.

### Weight sensitivity

Report how often each configuration is selected across a grid of declared task weights. Do not publish a single hidden weight vector.

### Deadline sensitivity

Test the A1 boundary: rate limiting should move on or off the frontier as the observer deadline changes.

### Adaptive task redistribution

Test the A3 result: adaptive configurations may enter the frontier for category/aggregate profiles even though they lost equal-weight macro utility.

## Falsification criteria

A4 is weakened if:

- frontier membership is unstable across seeds;
- small normalization changes reverse most conclusions;
- paired trials do not reduce comparison noise;
- policies are compared using different task opportunities;
- one metric silently determines every result;
- operational cost is reported without reproducible measurement.

## Required outputs

- raw result table;
- frontier table per workload/deadline;
- dominance explanations;
- sensitivity heatmap;
- security–utility scatter with delay encoding;
- list of conclusions that remain stable across specifications.
