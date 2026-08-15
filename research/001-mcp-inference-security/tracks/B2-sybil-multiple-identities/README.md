# B2 — Sybil / Multiple Identities

**Program:** Research 001 — MCP Inference Security  
**Track:** B — Identity / Principal Problem  
**Status:** Designed  
**Depends on:** A1, A2, B1  
**Feeds into:** B3, B6, C1, C4, F1

## Простими словами

Один атакувальник створює багато псевдонезалежних клієнтів і запускає їх одночасно. Кожна identity отримує власний ліміт, але всі відповіді потрапляють одному controller, який складає їх у спільну картину.

На відміну від B1, identities не замінюють одна одну послідовно. Вони існують паралельно, координують різні запити й можуть використовувати concurrency для обходу перевірок.

## Research question

> How does coordinated parallel use of multiple visible identities change cumulative reconstruction, time-to-reconstruction, and legitimate multi-tenant utility under different budget scopes and Sybil-resistance assumptions?

## Narrow hypothesis

За незалежного per-identity accounting сукупна доступна експозиція ростиме зі Sybil pool size до насичення hidden state, а паралельність скоротить час до реконструкції. Shared-principal або global accounting стримає це зростання, але без точної атрибуції може помилково карати незалежних легітимних користувачів.

## Null hypothesis

Після фіксації загальної кількості запитів і deadline збільшення кількості identities не дає додаткової реконструкції або concurrency advantage; прості per-identity обмеження працюють не гірше за складніші механізми.

## Unit of analysis

- **Sybil controller:** один ground-truth actor, який координує identities;
- **Sybil identity:** окремий видимий клієнт, credential або session;
- **identity pool size:** кількість одночасно активних identities;
- **coordination strategy:** спосіб розподілу запитів між identities;
- **aggregate observer:** реконструктор, який об'єднує всі дозволені відповіді controller.

Controller ID доступний лише evaluator як ground truth.

## Scope

Included:

- один controller;
- 1–64 паралельні identities;
- coordinated query allocation;
- per-identity, shared-attribution, global і proof-cost policies;
- fixed-request та fixed-deadline comparisons;
- reconstruction, speed, fairness, false merges і operational cost.

Excluded:

- незалежні observers, які домовляються після запитів — B3;
- довгі історичні сесії — B4;
- різні MCP servers — B5/F2;
- production durable attribution — B6;
- malicious exhaustion of a genuinely shared budget — C4.

## Decision rule

B2 підтримує гіпотезу, якщо за однакової загальної кількості запитів або однакового deadline Sybil pool систематично підвищує reconstruction чи зменшує time-to-reconstruction для per-identity accounting, а захист демонструє вимірюваний security–utility trade-off.

Висновок має розділяти ефект додаткового бюджету, ефект паралельності та ефект кращої координації запитів.
