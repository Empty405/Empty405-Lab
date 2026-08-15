# A2 Experiment Design

## Goal

Test whether cheap schema-derived exposure proxies track observer uncertainty reduction better than raw request counts.

## Hidden state

```text
12 locations × 8 resources × 3 epochs = 288 cells
```

Each cell is an integer from 0 to 100. A2 keeps the state static within an epoch and evaluates epochs independently.

## Tool projections

1. availability threshold — one cell, low precision;
2. capacity band — one cell, medium precision;
3. numeric range — one cell, high precision;
4. regional scarcity summary — multiple cells, coarse precision;
5. duplicate alias — same structural cell through another tool name.

The alias is declared in the adapter. Arbitrary semantic alias discovery remains outside A2.

## Query streams

- unique enumeration;
- duplicate-heavy;
- precision escalation: availability → band → range;
- broad marginal scan across every location but few resources;
- multi-cell summary heavy;
- mixed randomized tool stream.

## Compared predictors

- released request count;
- unique argument tuple coverage;
- exact cell coverage;
- dimension-marginal coverage;
- precision-weighted cell coverage.

## Reference outcomes

### Interval reduction

The experimental observer begins with candidate interval `[0, 100]` for every cell. Released constraints shrink intervals.

```text
reference exposure = mean(1 - remaining_width / 100)
```

### Reconstruction error

Midpoint estimates are compared with hidden values.

The reference observer is deterministic and declared in advance.

## Trials

- 1000 randomized states per stream;
- root seed `40502`;
- identical states and query streams for every ledger;
- checkpoints after 5%, 10%, 25%, 50%, 75%, and 100% of the stream.

## Primary tests

### T1 — Correlation

Compare each proxy with interval reduction across every checkpoint and trial using Pearson and Spearman correlations.

### T2 — Calibration

Group proxy values into deciles and compare predicted exposure with mean reference exposure.

### T3 — Duplicate invariance

Identical repeated disclosure must not increase tuple, cell, or weighted exposure after the first release.

### T4 — Precision escalation

A more precise later projection must increase weighted exposure even when exact cell coverage remains unchanged.

### T5 — Multi-cell response

A regional summary must account for every declared affected cell without being counted as only one request.

### T6 — Tool alias

Two declared tool aliases exposing the same cell must share coverage keys.

## Falsification criteria

A2 is weakened if:

- request count predicts reference exposure as well as every structural proxy;
- proxy rankings reverse across modest changes in tool mix;
- weighted coverage is non-monotonic or exceeds one;
- declared mappings require hidden-state access;
- multi-cell outputs cannot be represented without arbitrary manual scoring;
- small mapping errors cause large undetectable accounting errors.

## Counterexample requirement

The final report must include at least one constructed case where structural coverage overestimates knowledge and one where it underestimates knowledge.
