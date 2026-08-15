# B6 Experiment Design

## Primary experiment

Hold the query multiset, hidden state and nominal principal budget constant. Vary only the attribution mechanism and lifecycle/adversarial condition, then measure whether disclosures remain charged to the correct ground-truth principal.

## Independent variables

- attribution mechanism: session ID, account subject, global stable ID, pairwise pseudonym with broker, anonymous budget credential, oracle;
- lifecycle condition: stable use, token rotation, account rotation, multi-device use, credential loss and reissue;
- adversarial/failure condition: honest, credential transfer, issuer/broker collusion, partial attribution-service outage;
- principal budget: `0.25, 0.50, 0.75`;
- population structure: independent users, household/shared device, legitimate multi-device user;
- policy for unknown attribution: fail closed, restricted bootstrap budget, local-only fallback.

## Minimum v0.1 matrix

`6 mechanisms × 5 lifecycle conditions × 4 adversarial/failure conditions × 3 budgets × 300 paired trials = 108,000 trials`.

The primary matrix uses one fixed population mixture and restricted-bootstrap handling for unknown attribution. Population structure and unknown-policy sensitivity are follow-up analyses rather than hidden multipliers in the stated row count.

## Paired trial procedure

1. Generate ground-truth principals, devices, accounts and a fixed query sequence.
2. Assign the same hidden-state fixture and budget to every mechanism.
3. Apply the selected lifecycle event at a fixed point.
4. Apply the adversarial or outage condition.
5. Let the mechanism produce only its permitted attribution evidence.
6. Enforce disclosure against the attributed ledger key.
7. Record decisions, disclosures, linkage observations, denials and operational messages.
8. Compare with the oracle using the same seed and workload.

## Controls

- unchanged credential and one device;
- session-scoped accounting baseline;
- exact oracle attribution;
- no lifecycle event;
- two legitimate people sharing one device;
- one legitimate principal using two devices;
- fully unavailable attribution service;
- credential theft without ground-truth principal transfer.

## Required outputs

- true principal and attributed policy key, separated in storage;
- disclosure union per true principal;
- false-merge and false-split events;
- budget reset or duplicated-budget events;
- linkage observations by actor and context;
- legitimate task success and denial reason;
- recovery/revocation outcome and latency;
- protocol bytes, lookups and state writes.

## Statistical plan

- paired mechanism differences under identical seeds;
- confidence intervals for false merge/split and bypass exposure;
- security–privacy Pareto frontier;
- worst-group results for shared-device and multi-device populations;
- sensitivity to unknown-identity policy;
- report lifecycle phases separately instead of averaging away recovery failures.

## Stop conditions

Stop and fix the experiment if:

- ground-truth IDs enter deployable attribution evidence;
- changing mechanisms changes the query workload;
- denied responses enter the client exposure union;
- copied credentials are treated as ground-truth person transfer;
- false merge and false split are collapsed into one accuracy score;
- linkability is measured without actor and context scope;
- recovery silently receives a new full budget;
- oracle behavior depends on deployable identifiers.
