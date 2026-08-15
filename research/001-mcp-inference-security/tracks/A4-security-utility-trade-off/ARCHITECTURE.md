# A4 Architecture

```text
Scenario + Workload Manifest
            │
            ▼
      Unified Policy API
   ┌────────┼─────────┐
   ▼        ▼         ▼
 rate    coverage   adaptive ... 
   └────────┼─────────┘
            ▼
     Canonical Event Log
            │
            ▼
      Metric Evaluator
            │
            ▼
   Pareto / Sensitivity Engine
            │
       ┌────┴────┐
       ▼         ▼
   frontier   dominance evidence
```

## Workload manifest

Every comparison records the same:

- hidden-state generator and seed;
- query and legitimate task streams;
- principal model;
- deadlines;
- tool projections;
- metric definitions;
- policy parameter grid.

## Unified policy API

```text
decide(request, proposed_response, exposure_snapshot, logical_time)
→ release | transform | delay | deny
```

Every decision emits normalized reason, precision, delay, coverage keys, and provenance.

## Canonical result record

```json
{
  "scenario": "mixed-static",
  "policy": "coverage",
  "configuration": {"cap": 0.5},
  "seed": 40504,
  "risk": {"interval_reduction": 0.48, "exact_recovery": 0.0},
  "utility": {"macro": 0.71, "minimum_task": 0.42},
  "availability": {"p95_delay": 0, "deadline_success": 0.88},
  "cost": {"ledger_entries": 144, "evaluation_us": 12}
}
```

## Pareto engine

Dominance is computed on raw oriented metrics. Floating-point tolerances are declared in configuration. Missing metrics cannot be treated as zero cost.

## Sensitivity engine

Recomputes conclusions across:

- task-weight profiles;
- observer deadlines;
- risk metrics;
- policy grids;
- dominance tolerances;
- seed subsets.

## Output

- non-dominated configurations;
- dominated configurations and their dominators;
- task-weight sensitivity;
- deadline-specific frontiers;
- uncertainty intervals;
- configuration and code hashes.

## Boundary

A4 ranks tested configurations, not policy families in general. An untested configuration cannot be declared dominated.
