# B5 Experiment Design

## Primary experiment: fixed total requests

Hold the principal's total query count constant while varying the number of servers. This isolates fragmented accounting and output complementarity from merely increasing traffic.

## Independent variables

- server count: `1, 2, 4, 8, 16, 32`;
- accounting: local, central, eventual, signed token, sketch, oracle;
- server-output overlap: disjoint, low, medium, high;
- synchronization condition: healthy, delayed, partitioned;
- principal budget: `0.25, 0.50, 0.75`;
- routing: round-robin, complementary, adaptive stale-server selection;
- fail mode: closed, local-only fallback, cached decision.

## Minimum v0.1 matrix

`6 server counts × 6 accounting models × 4 overlap levels × 3 sync conditions × 3 budgets × 450 paired trials = 583,200 trials`.

The initial design draft incorrectly paired 300 trials with the 583,200 total; 300 trials would produce 388,800 rows. v0.1 uses 450 trials and records the correction explicitly.

Primary routing is complementary at fixed total requests. Routing and fail-mode sensitivity follow after the minimum matrix.

## Controls

- one-server baseline;
- identical server outputs;
- exact central/oracle accounting;
- no synchronization failure;
- legitimate multi-server workflow with unrelated information domains;
- shared infrastructure with false principal linkage.

## Outputs

- per-server disclosed units;
- client aggregate union;
- current local/federated budget view;
- stale-view exposure gain;
- denied legitimate tasks;
- fail-open/fail-closed events;
- bytes and fields shared between operators;
- synchronization latency and policy evaluation cost.

## Statistical plan

- paired query multiset and seeds;
- dose-response by server count;
- saturation and marginal server gain;
- compare healthy vs delayed vs partitioned state;
- uncertainty intervals for sketch collisions and linkage errors;
- report security, metadata privacy and availability jointly.

## Stop conditions

Stop if:

- total requests change with server count in primary runs;
- a server reads undeclared remote state;
- client union contains denied responses;
- oracle identity leaks into deployable models;
- partition handling is undefined;
- sync metadata cost is omitted;
- shared budget silently differs from local nominal budget.
