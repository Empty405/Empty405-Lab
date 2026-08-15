# B5 v0.1 Results — Cross-server Accumulation

## Outcome

The narrow hypothesis is supported inside the declared synthetic federation model. Independent local ledgers multiply exposure across servers even when total request volume is fixed. Exact healthy shared accounting holds the client union near the principal budget, while delayed or partitioned views reopen substantial exposure windows.

## Run

- root seed: `40515`;
- 1,296 configurations;
- 450 trials per configuration;
- 583,200 compressed raw rows;
- exactly 96 requests per trial;
- seven unit tests passed.

## Arithmetic correction

The design originally stated that 300 trials per configuration yielded 583,200 rows. The correct product is 388,800. v0.1 uses 450 trials per configuration to produce the declared 583,200-row total, and the design is corrected in this PR.

## Representative result

16 servers, disjoint outputs, budget `0.25`:

| Sync | Model | Exposure | Workload utility | Metadata bytes | Accounting groups |
|---|---|---:|---:|---:|---:|
| healthy | local | 0.960 | 1.000 | 0 | 16 |
| healthy | central | 0.250 | 0.260 | 6,144 | 1 |
| healthy | eventual | 0.250 | 0.260 | 3,072 | 1 |
| healthy | signed token | 0.250 | 0.260 | 1,536 | 1 |
| healthy | sketch | 0.251 | 0.261 | 768 | 1 |
| delayed | eventual | 0.960 | 1.000 | 384 | 4 |
| delayed | signed token | 0.500 | 0.521 | 192 | 2 |
| delayed | sketch | 0.960 | 1.000 | 96 | 8 |
| partitioned | central | 0.000 | 0.000 | 0 | 1 |
| partitioned | eventual | 0.960 | 1.000 | 0 | 16 |

## What survived falsification

- Local budgets multiply across complementary servers at fixed traffic.
- High output overlap reduces the unique union; server count alone is insufficient.
- Healthy exact coordination enforces the shared budget.
- Delayed replicas and forked tokens produce exposure proportional to independent accounting groups.
- Partitioned eventual systems fail open in this model; partitioned central accounting fails closed.
- Lower-metadata coordination is not automatically safer when stale views dominate.

## Central trade-off

Healthy central coordination holds exposure at `0.250` but shares 6,144 bytes of modeled metadata and reduces workload completion to `0.260`. During a partition it discloses nothing and provides zero utility. Local accounting preserves availability and metadata isolation but reaches `0.960` exposure.

## Limitations

- synthetic synchronization groups and sketch error;
- complementary round-robin routing only;
- central partition is explicitly fail-closed;
- metadata bytes are an abstract payload estimate;
- structural union is not semantic reconstruction.

## Next question

B6 should ask which durable principal attribution, if any, can support shared accounting without turning federation into disproportionate cross-operator tracking.
