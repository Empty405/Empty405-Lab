# C5 Fair Allocation Between Clients — Results

## Run identity

- Schema: `c5.v0.1`
- Raw trial rows: **84,000**
- Raw request events: **4,939,200**
- Configurations: **420**
- Trials per configuration: **200**

All 12 invariant tests passed. Row counts, gzip integrity, Python compilation, and finite JSON validation passed.

## Main result

Under severe scarcity and asymmetric heavy demand, FIFO achieves utility completion `0.3641` but Jain utility only `0.6256`. Allocation-aware policies improve balance:

| Policy | Utility completion | Jain utility | Utilization |
|---|---:|---:|---:|
| Global FIFO | 0.3641 | 0.6256 | 1.0000 |
| Equal reservation | 0.3119 | 0.9295 | 0.8801 |
| Progressive max-min | 0.3596 | 0.8745 | 0.9999 |
| Proportional share | 0.3583 | 0.8798 | 1.0000 |
| Bounded borrowing | 0.3620 | 0.8436 | 1.0000 |

Fixed equal reservation buys fairness by stranding capacity. Progressive max-min and bounded borrowing retain nearly FIFO-level utility and utilization while substantially improving client balance.

Under sparse demand, equal reservation utilization falls to `0.5294`; progressive max-min reaches `1.0000`, confirming that inactive reservations must be handled explicitly. Under late high-value demand, the evaluator-only oracle reaches `0.5725` utility completion versus about `0.383` for deployable policies, exposing the cost of not knowing future value.

## Interpretation

C5 supports a three-way trade-off:

1. FIFO and unrestricted borrowing maximize utilization but can preserve strong allocation inequality.
2. Fixed reservations improve equal-share fairness but can strand scarce disclosure capacity.
3. Progressive allocation and bounded borrowing recover much of the utilization without returning fully to FIFO inequality.

These results do not define moral or legal fairness. They assume exact identities, exact marginal exposure accounting, synthetic task value, and one atomic ledger.
