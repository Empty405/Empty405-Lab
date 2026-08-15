# B4 Experiment Design

## Primary comparison: fixed total requests

The principal sends the same total number of queries in every condition. Only their distribution across sessions and gaps changes. This isolates reset and memory-policy effects from extra traffic.

## Secondary comparison: fixed requests per session

Measures operational long-horizon accumulation where more sessions naturally create more total traffic. Results must report request volume explicitly.

## Independent variables

- session count: `1, 2, 4, 8, 16, 32`;
- memory policy: session reset, persistent principal, fixed TTL, rolling window, exponential decay;
- session gap: immediate, short, medium, long;
- budget: `0.25, 0.50, 0.75`;
- workload: duplicate-heavy, random, partitioned;
- TTL/window: declared in logical-time units;
- decay half-life: declared in logical-time units.

## Minimum v0.1 matrix

`6 session counts × 5 memory policies × 4 gaps × 3 budgets × 3 workloads × 500 paired trials = 540,000 trials`.

Primary hidden state is static. A small sensitivity run may invalidate selected units over time, but dynamic-state claims belong to E2.

## Legitimate controls

- user resuming an unfinished task;
- periodic monitoring with repeated queries;
- long-running research project;
- account recovery after inactivity;
- legally required data deletion followed by a new interaction.

## Outputs

- observer-known exposure after every session;
- policy-accounted exposure;
- forgotten-but-known exposure;
- time/session count to threshold reconstruction;
- legitimate continuation success;
- denied requests and delay;
- retained ledger entries, bytes and evaluation cost.

## Statistical plan

- paired seeds and identical query multiset;
- dose-response by session count and gap;
- mean, median, p95 and uncertainty intervals;
- compare hard TTL discontinuities with smooth decay;
- report security and continuity utility jointly;
- preserve null results for duplicate-heavy workloads.

## Stop conditions

Stop if:

- total requests differ in primary comparisons;
- observer memory decays merely because ledger weights decay;
- hidden state resets between sessions;
- principal identity leaks into a session-only policy;
- expired entries disappear from audit provenance;
- dynamic-state invalidation is counted as privacy recovery without checking observer inference.
