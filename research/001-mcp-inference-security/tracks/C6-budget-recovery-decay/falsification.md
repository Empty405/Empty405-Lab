# C6 Falsification Plan

## Claims under test

1. Administrative or fixed-window reset can hide lifetime accumulation.
2. Time decay alone cannot prove that observer knowledge became harmless.
3. Verified state change enables safer bounded recovery than blind reset.
4. Cyclic state return defeats policies that remember only the current version.
5. No deployable policy dominates utility, freshness, historical risk and cost across all regimes.

## Evidence against the hypothesis

Reject or weaken claims if fixed reset adds no historical reconstruction over no recovery, time decay matches evidence-based recovery on false forgetting, version evidence is unnecessary, cyclic return creates no extra risk, or one deployable policy dominates every measured axis with uncertainty included.

## Critical counterexamples

- a version bump with unchanged content restores capacity;
- reset deletes evaluator history;
- a fact released in an earlier cycle is treated as globally unseen;
- detector false positives create unlimited recovery;
- obsolete units remain charged forever but are reported as safe recovery;
- current reconstruction is low while historical reconstruction is hidden;
- oracle future knowledge leaks into deployment evidence.

## Confounders

Unequal state schedules, mixing E-track temporal inference into C6, distributed observers from F, semantic detector error from D, deleting old raw events, treating version ID as content change, or comparing policies with different lifetime observers.

## Interpretation boundaries

C6 models synthetic information persistence. It does not claim that humans forget, that data deletion revokes external knowledge, or that a legal retention period makes earlier disclosure technically harmless.
