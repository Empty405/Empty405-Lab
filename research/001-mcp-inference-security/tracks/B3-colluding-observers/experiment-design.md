# B3 Experiment Design

## Primary experiment: post-hoc coalition

Observers complete their queries independently or under a declared coordination mode. After all server decisions, coalition members share a configured fraction of disclosed observations. The gateway cannot react retroactively.

## Independent variables

- coalition size: `1, 2, 4, 8, 16, 32`;
- response overlap: disjoint, low, medium, high;
- query behavior: independent, overlapping, partitioned;
- exchange fraction: `0, 0.25, 0.50, 1.0`;
- policy: per-client, organization, behavioral cohort, diversity-aware, global, oracle;
- per-client budget: `0.25, 0.50, 0.75`;
- detector signal quality: clean, noisy, missing.

## Controlled comparisons

### Fixed total requests

The whole coalition receives a constant request volume. Isolates information composition from extra traffic.

### Fixed per-observer requests

Each observer receives the same workload. Measures production scaling but explicitly reports aggregate traffic.

Primary v0.1 uses fixed total requests and full post-hoc exchange.

## Minimum v0.1 matrix

`6 coalition sizes × 4 overlap levels × 3 query behaviors × 6 policies × 3 budgets × 500 paired trials = 648,000 trials`.

Partial exchange and online coordination are follow-up sensitivity experiments.

## Legitimate controls

- independent analysts investigating the same incident;
- students following the same tutorial;
- organization members with shared infrastructure;
- redundant monitoring agents;
- parallel research team that does not exchange protected outputs.

## Outputs

- individual exposure and reconstruction;
- exchanged observation edges;
- coalition union and exact recovery;
- maximum-individual reconstruction;
- detector suspicion and ground-truth label;
- denied legitimate utility and worst-group utility;
- ledger and detector cost.

## Stop conditions

Stop if:

- coalition ground truth reaches a deployable policy;
- coalition size changes total requests in fixed-volume runs;
- unshared observations enter coalition reconstruction;
- overlap is counted as new information;
- legitimate controls are labeled colluders merely from evaluator metadata;
- post-hoc policy reacts to future exchange.
