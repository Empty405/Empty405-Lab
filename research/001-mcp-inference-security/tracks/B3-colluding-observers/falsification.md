# B3 Falsification Plan

## Claims under test

1. Individually compliant observers can exceed intended exposure when they share outputs.
2. Complementary queries produce more coalition gain than overlapping queries.
3. Post-hoc sharing is difficult to constrain using server-visible evidence alone.
4. Coalition-oriented defenses create false positives for legitimate teams with similar workflows.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- coalition reconstruction does not exceed maximum individual reconstruction;
- exchange fraction has no dose-response effect;
- partitioned and overlapping workloads yield equivalent unique union;
- natural overlap keeps coalition exposure near the individual budget;
- server-observable policies stop post-hoc sharing without utility or false-suspicion cost;
- results disappear under fixed total requests.

## Confounders

- coalition receiving more requests in the fixed-volume regime;
- evaluator sharing denied or unexchanged outputs;
- duplicate units counted multiple times;
- coalition labels leaking into policy;
- legitimate groups given different workloads;
- online coordination accidentally included in the post-hoc experiment.

## Interpretation boundaries

B3 cannot prove that similar users are colluding. Similar timing or query structure can arise from shared documentation, common incidents, accessibility tools or standardized workflows.

The absence of server-visible evidence is itself a result: once information is legitimately disclosed, preventing off-server copying may be impossible without intrusive controls. The study must report this limitation rather than invent certainty from weak signals.
