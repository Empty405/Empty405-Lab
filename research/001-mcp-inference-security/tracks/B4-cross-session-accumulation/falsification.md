# B4 Falsification Plan

## Claims under test

1. Session reset can refresh exposure budget without erasing observer knowledge.
2. TTL and decay create a gap between accounted and known exposure.
3. Longer gaps increase bypass under expiring memory policies.
4. Persistent accounting improves security but harms legitimate continuity and increases retention cost.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- session count has no effect at fixed total requests;
- observer-known exposure remains within the nominal budget under session reset;
- TTL/decay never create forgotten-but-known exposure;
- session gap does not change outcomes near retention boundaries;
- duplicate-heavy workloads explain all apparent accumulation;
- persistent accounting provides no security advantage.

## Confounders

- more sessions silently receiving more total requests;
- session IDs mistaken for durable principal IDs;
- query content changing with session count;
- ledger decay incorrectly erasing observer memory;
- static hidden facts being invalidated without declaration;
- expired audit evidence being deleted before evaluation.

## Interpretation boundaries

Persistent exposure memory can reduce reconstruction while creating durable profiling, deletion, proportionality and governance risks. B4 measures that trade-off; it does not declare indefinite retention acceptable.

Conversely, TTL or decay is not automatically privacy-preserving. If the observer retains old facts, accounting decay may restore utility while reopening the same disclosure budget.
