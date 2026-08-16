# C5 — Fair allocation between clients

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C5  
**Status:** Experiment design v0.1

## Простими словами

Навіть без зловмисника один shared disclosure budget створює конфлікт: активний або “дорогий” клієнт може отримати більшість нової інформації, а інший — майже нічого. C5 перевіряє, яке правило розподілу зберігає корисність, не допускає starvation і не створює прихований додатковий exposure.

## Дослідницьке питання

> Як allocation policies змінюють legitimate utility, starvation, utilization і exposure conservation, коли клієнти мають різний попит, marginal exposure cost, task value та burst timing, але всі вважаються легітимними?

## Гіпотеза

Global FIFO максимізує простоту й часто utilization, але чутливий до arrival order і може створювати starvation. Equal reservation захищає мінімальну частку, але втрачає capacity при нерівному попиті. Weighted fair allocation і bounded borrowing повинні краще балансувати minimum guarantees та utilization, однак їхній результат залежить від правильності weights і точності marginal-cost accounting.

## Нульова гіпотеза

Після вирівнювання request set, cap, task value та arrival schedule allocation rule не створює практично значущої різниці в legitimate utility або starvation, або будь-яке покращення fairness повністю пояснюється більшим невикористаним бюджетом чи додатковим exposure.

## Одиниця аналізу

Один **multi-client allocation episode**: 120 ticks, фіксований набір легітимних principals, один exact shared ledger/cap, heterogeneous requests, allocation policy та terminal outcomes. Evaluator знає task value і counterfactual feasible allocation; deployable policies бачать лише дозволені metadata.

## Межі

C5 досліджує:

- усіх клієнтів як легітимних;
- steady, bursty, asymmetric і sparse demand;
- equal, weighted, max-min, proportional, bounded-borrowing та FIFO allocation;
- utility, starvation, envy, utilization і cap conservation;
- sensitivity до помилково заданих weights.

C5 не моделює malicious burning (C4), identity/Sybil failure (B), budget decay (C6), semantic observer error (D) або юридичні правила пріоритету. Synthetic task value не є реальною соціальною цінністю.

## Артефакти v0.1

- `architecture.md` — principals, allocator, ledger і trust boundaries;
- `experiment-design.md` — paired matrix, demand profiles, controls і stop conditions;
- `metrics.md` — utility, starvation, fairness, envy, utilization і cost;
- `falsification.md` — докази проти гіпотези та критичні контрприклади;
- `related-work.md` — план source-backed порівняння fairness mechanisms.

## Наступний крок

Реалізувати детермінований benchmark із raw request events, counterfactual controls, invariant tests і utility–fairness–utilization frontier.
