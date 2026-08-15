# B1 Architecture

## Components

1. **Hidden-state fixture** — незмінний набір атомарних фактів, які можна поступово відкрити.
2. **Principal generator** — створює ground-truth durable principals: атакувальний і легітимні.
3. **Identity issuer** — видає visible identities та виконує rotation schedule.
4. **Query scheduler** — подає однаковий query workload усім політикам.
5. **Attribution layer** — оцінює, які identities належать одному principal, не бачачи ground truth.
6. **Exposure ledger** — накопичує structural exposure за attribution key.
7. **Disclosure policy** — allow, coarsen або deny на основі ledger і бюджету.
8. **Observer** — реконструює hidden state з усіх дозволених відповідей атакувального principal.
9. **Evaluator** — порівнює спостереження з ground truth і рахує security та utility.

## Data model

```text
RequestEvent {
  event_id,
  logical_time,
  ground_truth_principal_id,  # evaluator only
  visible_identity_id,
  session_id,
  attribution_signals,
  query_id,
  legitimate_task_id
}

AttributionDecision {
  event_id,
  attribution_key,
  confidence,
  evidence_classes,
  policy_version
}

ExposureEntry {
  attribution_key,
  disclosed_units,
  cumulative_exposure,
  decision,
  provenance
}
```

## Trust boundaries

- Ground-truth principal IDs доступні лише generator/evaluator.
- Attribution layer не може читати ground truth.
- Observer бачить тільки відповіді, які отримав атакувальний principal.
- Policy читає attribution key, ledger і поточний запит, але не майбутній rotation schedule.
- Random seeds, policy configuration і raw decisions зберігаються для відтворення.

## Attribution strategies

| Strategy | Ledger key | Expected weakness |
|---|---|---|
| Per identity | `visible_identity_id` | Повне скидання після rotation |
| Per session | `session_id` | Ще легше скидання між сесіями |
| Durable credential | стабільний credential subject | Не працює після перевидачі або крадіжки |
| Deterministic linkage | hash стабільних дозволених сигналів | False merges за NAT/shared device |
| Probabilistic linkage | cluster above threshold | False splits/merges залежать від threshold |
| Oracle | ground-truth principal | Верхня межа, не production defense |

Oracle використовується тільки як експериментальна межа якості.

## Required invariants

- Однакові запити й seeds для парних порівнянь.
- Rotation змінює visible identity, але не hidden state чи attacker objective.
- Policy не отримує evaluator-only поля.
- Exposure ledger append-only у межах trial.
- Кожне disclosure рішення має provenance до query, attribution decision і budget state.
