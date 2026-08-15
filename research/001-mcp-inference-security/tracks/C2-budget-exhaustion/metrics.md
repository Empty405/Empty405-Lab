# C2 Metrics

## Security after exhaustion

### Post-cap exposure gain

```text
PCEG = |released_union_after_episode - pre_exhaustion_union| / |disclosure_universe|
```

### Cap violation event

`1` when any non-precharged structural unit is released after exhaustion, including coarse output and override units.

### First violating request

Index of the first post-cap request that releases a new unit; `-1` if no violation occurs.

### Silent reset indicator

`1` if an ordinary new budget or ledger is created after exhaustion without an explicit C6 recovery event. It must remain zero in C2.

### Override exposure

New units released under explicit override authority, reported separately and included in total post-cap gain.

## Classification correctness

- exact-replay acceptance;
- new-disclosure rejection;
- mixed-response rejection or sanitization;
- contaminated-snapshot acceptance;
- coarse-key novelty;
- override replay/fork acceptance;
- response-class ambiguity rate.

## Utility

### Post-exhaustion task completion

Fraction of synthetic task requirements satisfied by allowed responses.

### False-denial rate

Requests or tasks denied even though they were satisfiable entirely from the pre-exhaustion union.

### Safe reuse rate

Previously exposed units successfully reused without new exposure.

### Downgrade adequacy

Fraction of tasks completed by coarse fallback or safe snapshot without new exposure.

Additional measures:

- terminal success/failure;
- requests to terminal response;
- denial burst length;
- replay, snapshot, downgrade and override counts;
- result specificity retained.

## Override risk

- allowance issued and consumed;
- unused allowance;
- exposure per override;
- token replay attempts accepted;
- distinct clients or contexts able to invoke override;
- audit completeness.

## Operational cost

- policy-state reads;
- classifier operations;
- audit writes;
- response metadata bytes;
- terminal-decision latency proxy;
- human/manual review dependency indicator.

## Invariant tests

1. Hard deny produces zero post-cap exposure gain.
2. Replay-only accepts exact replays without new exposure.
3. New-disjoint requests are denied by hard-cap policies.
4. Denied requests never change exposure or task state.
5. Safe snapshots use only pre-charged units.
6. A contaminated snapshot is rejected or counted as a violation.
7. Bounded override never releases more than its explicit allowance.
8. Override replay cannot create additional authority.
9. Every trial begins exactly at cap and contains 48 post-cap requests.

## Reporting rule

No policy is described as safe from task completion alone or useful from low exposure alone. Every result jointly reports post-cap gain, false denial, task completion, response class, override use and operational dependency.
