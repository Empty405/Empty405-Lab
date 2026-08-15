# B1 — Identity rotation

**Program:** Research 001 — MCP Inference Security  
**Track:** B — Identity / Principal Problem  
**Status:** Designed  
**Depends on:** A1, A2  
**Feeds into:** B2, B4, B6, C1

## Простими словами

Сервер може вести бюджет розкриття для `client_id`. Але якщо той самий атакувальник змінить API-ключ, сесію або псевдонім, система може помилково прийняти його за нового клієнта й видати приховані частини ще раз.

B1 перевіряє саме послідовну зміну видимої ідентичності одним реальним принципалом. Одночасна армія незалежних ідентичностей належить до B2.

## Research question

> Under which attribution assumptions does identity rotation let one durable principal exceed a per-identity cumulative-exposure budget?

## Narrow hypothesis

Якщо бюджет прив'язаний лише до змінного `visible_identity`, після кожної ротації атакувальник отримує майже повний новий бюджет. Прив'язка до стабільнішого principal key зменшить обхід, але може помилково об'єднувати легітимних клієнтів і погіршувати доступність.

## Null hypothesis

Після контролю workload і кількості запитів ротація ідентичності не збільшує реконструкцію порівняно зі стабільною ідентичністю або простий per-identity ledger достатньо стримує накопичення.

## Unit of analysis

- **durable principal:** реальний суб'єкт, що виконує запити;
- **visible identity:** токен, сесія або псевдонім, який бачить gateway;
- **attribution key:** ключ, за яким система об'єднує події в один exposure ledger;
- **rotation event:** заміна visible identity без зміни durable principal.

Durable principal відомий лише симулятору як ground truth. Політика бачить тільки дозволені сигнали атрибуції.

## Scope

Included:

- один атакувальний principal;
- послідовна ротація ідентичностей;
- однаковий hidden state і query workload;
- per-identity, per-session, durable-principal і probabilistic attribution;
- reconstruction, budget bypass, false merge та legitimate utility.

Excluded:

- одночасні Sybil-ідентичності — B2;
- змова різних принципалів — B3;
- довгі перерви між сесіями — B4;
- різні MCP-сервери — B5;
- production fingerprinting deployment — B6/J1.

## Decision rule

B1 підтверджує вузьку гіпотезу, якщо rotation attack суттєво підвищує excess exposure або reconstruction для per-identity accounting, а principal-aware accounting знижує цей ефект без прихованого використання ground truth.

Результат має окремо показати ціну захисту: false merges, false splits, denied legitimate utility та ledger cost.
