# B2 Architecture

## Components

1. **Hidden-state fixture** — атомарні факти та структурні зв'язки.
2. **Sybil controller** — ground-truth actor і єдина attacker objective.
3. **Identity pool** — одночасно активні visible identities.
4. **Coordinator** — розподіляє query plan між identities.
5. **Concurrent scheduler** — моделює logical time, parallel slots і deadlines.
6. **Attribution layer** — будує allowed linkage між identities.
7. **Budget manager** — застосовує ledger scope.
8. **Disclosure policy** — allow, coarsen або deny.
9. **Aggregate observer** — об'єднує відповіді всього Sybil pool.
10. **Evaluator** — рахує reconstruction, attribution harm, fairness і cost.

## Trust boundaries

- Controller ground truth недоступний policy та attribution layer.
- Кожна visible identity бачить лише власні відповіді; aggregate observer отримує їх після disclosure.
- Policy не бачить майбутній query plan або pool size, якщо це прямо не дозволено сценарієм.
- Scheduler не збільшує загальну кількість запитів у fixed-request comparison.
- Legitimate clients ніколи не передають результати aggregate observer.

## Ledger scopes

| Scope | Budget key | Main risk |
|---|---|---|
| Per identity | visible identity | budget multiplication |
| Per session | session | cheap reset and multiplication |
| Attributed cluster | inferred controller cluster | false split / false merge |
| Global server | one shared ledger | availability collapse |
| Proof-cost identity | identity with creation cost | unequal access and incomplete resistance |
| Oracle controller | ground-truth controller | experimental bound only |

## Coordinator strategies

- **duplicate:** identities repeat the same query plan;
- **partition:** identities receive disjoint structural regions;
- **adaptive coverage:** controller sends the next query to the identity with available budget;
- **random:** queries are assigned without coordination.

Partition and adaptive coverage are expected to expose the strongest reconstruction advantage.

## Event model

```text
SybilRequest {
  logical_time,
  controller_id,       # evaluator only
  identity_id,
  query_id,
  coordination_mode,
  attribution_signals,
  deadline
}

PolicyDecision {
  attribution_key,
  ledger_scope,
  pre_exposure,
  disclosed_units,
  action,
  provenance
}
```

## Invariants

- Fixed-request comparisons use identical total query counts.
- Fixed-deadline comparisons report achieved request volume separately.
- Hidden state never resets between identities.
- Observer combines only actually disclosed units.
- Oracle controller linkage cannot leak into deployable policies.
