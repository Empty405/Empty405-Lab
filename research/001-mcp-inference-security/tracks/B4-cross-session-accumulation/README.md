# B4 — Cross-session Accumulation

**Program:** Research 001 — MCP Inference Security  
**Track:** B — Identity / Principal Problem  
**Status:** Designed  
**Depends on:** A1, A2, B1, E1  
**Feeds into:** B5, B6, C6, E3, E4, E5

## Простими словами

Навіть без зміни identity клієнт може завершити одну сесію, повернутися завтра й отримати новий «чистий» бюджет. Сервер пам'ятає лише поточну сесію, а observer пам'ятає всі старі відповіді та поступово складає їх разом.

B4 досліджує не підміну identity, як B1, а межі пам'яті exposure ledger: скільки історії зберігати, коли її послаблювати та якою є ціна довгої пам'яті для легітимних повторних задач.

## Research question

> How do session resets, retention windows, and exposure decay affect long-horizon reconstruction when the same durable principal accumulates disclosures across multiple sessions?

## Narrow hypothesis

Session-scoped accounting дозволить cumulative reconstruction рости після кожного reset до насичення hidden state. Persistent principal accounting стримає це, а TTL/decay створять проміжний режим: безпека залежатиме від session gap, decay rate та того, чи справді старі відомості втратили цінність.

## Null hypothesis

Після фіксації загальної кількості запитів розподіл між сесіями не змінює reconstruction; session reset, TTL, decay та persistent accounting дають еквівалентний результат або стара інформація природно стає некорисною.

## Unit of analysis

- **durable principal:** той самий ground-truth actor у різних sessions;
- **session:** обмежений часовий інтервал взаємодії;
- **ledger memory:** історична exposure state, яку policy враховує зараз;
- **observer memory:** усі факти, які principal реально отримав раніше;
- **session gap:** логічний час між завершенням і наступним входом.

Policy не може змусити observer «забути» вже отриману відповідь.

## Scope

Included:

- один стабільний principal;
- 1–32 sessions;
- статичний hidden state як primary fixture;
- session reset, persistent, TTL, rolling-window і exponential-decay accounting;
- fixed-total-request та fixed-per-session comparisons;
- reconstruction, forgotten exposure, legitimate continuity, storage та latency.

Excluded:

- identity rotation — B1;
- multiple identities — B2;
- collusion — B3;
- multiple servers — B5;
- повністю dynamic hidden state — E2;
- нормативний вибір retention period — B6/J1.

## Decision rule

B4 підтримує гіпотезу, якщо за matched total requests session-scoped або decayed ledger дозволяє observer memory перевищити поточний accounted exposure і principal budget, а ефект має dose-response із session count і gap.

Будь-яка рекомендація retention повинна одночасно показувати security, legitimate continuity, storage cost і ризик надмірного довготривалого профілювання.
