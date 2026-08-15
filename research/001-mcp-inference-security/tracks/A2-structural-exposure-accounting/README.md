# A2 — Structural Exposure Accounting

**Program:** Research 001 — MCP Inference Security  
**Track:** A2  
**Status:** Designed  
**Depends on:** A1 request-frequency vs cumulative exposure  
**Claim maturity:** Unvalidated proxy design

## Простими словами

A1 показав, що кількість запитів і кількість відкритих частин стану — не те саме. A2 перевіряє, чи можемо ми дешево рахувати саме **нове структурне охоплення**: наприклад, які комбінації `location × resource × epoch` система вже показала клієнту.

## Research question

> Can a schema-derived structural coverage ledger track cumulative exposure closely enough to guide policy without understanding the full semantics of every tool response?

## Narrow hypothesis

For synthetic tools whose outputs map to declared state dimensions, normalized unique coverage and precision-weighted coverage will correlate with reduction of the observer's candidate state better than raw request counts, while requiring much less machinery than general semantic inference.

## Null hypothesis

Structural coverage scores do not correlate with actual reduction of observer uncertainty more reliably than request counts, or the correlation depends so strongly on hand-written tool mappings that the abstraction provides no reusable value.

## What A2 counts

A disclosure unit is a normalized tuple:

```text
principal × epoch × object dimensions × projection × precision
```

Example:

```text
observer-0 × epoch-1 × north × fuel × capacity-band × 0.33
```

A2 compares several ledgers:

1. raw request count;
2. unique parameter tuples;
3. unique hidden-cell coverage;
4. dimension-marginal coverage;
5. precision-weighted coverage;
6. an experiment-only interval-reduction reference.

The interval-reduction reference evaluates the proxies. It is not proposed as the production ledger.

## Explicit exclusions

A2 does not solve:

- identity rotation or durable principal attribution;
- semantic equivalence across arbitrary natural-language outputs;
- collusion or distributed accounting;
- dynamic hidden state;
- approximate distributed counters;
- policy fairness or budget recovery;
- differential-privacy guarantees.

## Decision rule

Structural accounting remains a viable research direction only if at least one schema-derived proxy:

- predicts observer uncertainty reduction materially better than request count;
- remains monotonic and bounded;
- behaves consistently across tool mixtures and duplicate-heavy streams;
- does not require access to the hidden ground truth during enforcement;
- preserves a stable meaning when one tool exposes several cells.

## Expected output

- a normalized disclosure-event schema;
- exact reference ledger;
- four structural proxy implementations;
- comparison against an interval-reduction oracle;
- correlation and calibration results;
- counterexamples where structural accounting fails.
