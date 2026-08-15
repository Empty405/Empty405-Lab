# A3 Metrics

## Reconstruction

- observable cell fraction;
- reference interval reduction;
- reconstruction mean absolute error;
- exact-cell recovery rate.

## Legitimate utility

For task `t`:

```text
utility(t) = successful task answers / attempted task answers
```

Report per-task utility and macro-average. Do not hide exact-task failure behind easier category tasks.

## Matched-risk comparison

Compare adaptive and hard-block modes at equal or nearest achievable:

- reference interval reduction;
- reconstruction error;
- exact recovery rate.

Utility comparisons without matched risk are invalid.

## Stability

- precision-level reversals per run;
- boundary oscillations;
- repeated-sampling excess precision;
- cross-tool composition violations.

## Provenance

- envelope completeness;
- invalid or missing reason codes;
- mismatch between declared and actual interval width;
- stale epoch usage.

## Operational metrics

- transformation time;
- controller decision time;
- exposure-ledger entries;
- response-size overhead;
- provenance bytes.

## Invariants

- level never improves within a static epoch;
- output sets are nested across levels;
- identical policy state produces identical transformed output;
- repeated same-level answers do not narrow below declared precision;
- all transformations carry provenance;
- `synthetic=false` for every A3 response;
- unknown mappings never receive L0 by default.

## Success condition

A3 receives preliminary support if an adaptive configuration lies above hard blocking on legitimate utility at matched reconstruction risk and passes every composition and provenance invariant.
