# B4 Architecture

## Components

1. **Logical clock** — session start/end і gaps.
2. **Hidden-state fixture** — статичний набір фактів у primary run.
3. **Durable principal** — незмінний evaluator-only actor.
4. **Session manager** — створює session IDs без зміни principal.
5. **Query scheduler** — розподіляє matched workload між sessions.
6. **Historical exposure store** — append-only disclosure provenance.
7. **Ledger view** — обчислює policy-visible exposure після reset/TTL/decay.
8. **Disclosure policy** — allow, coarsen або deny.
9. **Persistent observer memory** — union усіх фактично отриманих відповідей.
10. **Evaluator** — порівнює accounted exposure з retained observer knowledge.

## Memory policies

| Policy | Current ledger view | Main risk |
|---|---|---|
| Session reset | current session only | full budget refresh |
| Persistent principal | all historical exposure | indefinite tracking and utility denial |
| Fixed TTL | entries newer than TTL | cliff-edge recovery after expiry |
| Rolling window | events inside time window | boundary gaming |
| Exponential decay | weighted historical exposure | old facts remain known despite lower weight |
| Oracle relevance | only information still useful to observer | evaluator-only bound |

## Critical distinction

```text
accounted_exposure(t) != observer_known_exposure(t)
```

Decay changes the server's accounting weight. It does not erase facts from the observer's memory.

## Trust boundaries

- Principal ground truth is unavailable to session-only policies.
- Observer memory receives only disclosed responses and never decays automatically.
- Policy sees only declared ledger view at logical time t.
- Future sessions and gaps are hidden from the policy.
- Evaluator records both raw historical exposure and current weighted exposure.
- Clock manipulation is disabled in v0.1 and reserved for a follow-up attack.

## Required provenance

Every decision links to:

- principal and session ground truth for evaluator;
- session-visible identity for policy;
- disclosure unit;
- original timestamp;
- current ledger weight;
- retention/decay rule version.
