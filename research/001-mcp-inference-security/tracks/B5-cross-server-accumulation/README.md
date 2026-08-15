# B5 — Cross-server Accumulation

**Program:** Research 001 — MCP Inference Security  
**Track:** B — Identity / Principal Problem  
**Status:** Designed  
**Depends on:** A2, B1, B4  
**Feeds into:** B6, C1, F2, F4, F6, J2, J3

## Простими словами

Один MCP-сервер може чесно зупинити клієнта на 25% exposure. Але якщо клієнт звернеться до чотирьох незалежних серверів, кожен із них може окремо видати дозволені 25%, а клієнт локально складе 100%.

B5 перевіряє, що відбувається, коли exposure accounting розділений між серверами, які мають різних операторів, політики, затримки синхронізації та правила приватності.

## Research question

> How does fragmented exposure accounting across independently operated MCP servers affect aggregate reconstruction, and what security–privacy–availability trade-offs arise from coordinating their ledgers?

## Narrow hypothesis

За суто локальних per-server budgets aggregate exposure зростатиме з кількістю серверів до насичення hidden state. Централізований або федеративний shared budget зменшить accumulation, але створить metadata disclosure, synchronization, availability, trust і governance costs. Eventual consistency залишить exploitable race windows.

## Null hypothesis

Після фіксації загальної кількості запитів server count і synchronization model не змінюють aggregate reconstruction; природне перекриття відповідей або локальні budgets достатньо обмежують union.

## Unit of analysis

- **principal:** один ground-truth client, відомий evaluator;
- **server:** окремий MCP policy/accounting domain;
- **local ledger:** exposure state, який бачить один server;
- **federated view:** узгоджена або приблизна cross-server exposure state;
- **sync event:** передача budget metadata між domains;
- **client observer:** локально об'єднує факти з усіх servers.

## Scope

Included:

- 1–32 MCP servers;
- fixed total request volume;
- complementary, random та overlapping server outputs;
- local, centralized, eventual, signed-token, sketch і oracle accounting;
- sync lag, partition/failure, metadata disclosure, utility та overhead.

Excluded:

- кілька organizations як правова модель — F3;
- кілька незалежних clients — F1;
- семантична cross-tool composition — D4;
- production deployment — J1–J3;
- остаточний durable principal mechanism — B6.

## Decision rule

B5 підтримує гіпотезу, якщо local ledgers допускають cross-server union вище nominal principal budget за matched requests, а inconsistent federated views створюють вимірюваний race-window gain.

Захист вважається кращим лише разом зі звітом про shared metadata, false linkage, availability, latency та behavior under partial failure.
