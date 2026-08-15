# C1 — Shared exposure accounting

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C1  
**Status:** Experiment design v0.1

## Простими словами

Один агент може отримувати інформацію через кілька клієнтів, інструментів або MCP-серверів. Якщо кожен вузол веде власний лічильник, один номінальний бюджет непомітно перетворюється на кілька. C1 перевіряє, як різні системи спільного обліку зберігають один бюджет і що вони помилково списують з нього.

## Дослідницьке питання

> Який механізм спільного exposure-обліку найкраще зберігає conservation одного логічного бюджету між кількома виконавцями за конкуренції, затримки та розділення мережі, не створюючи надмірних помилкових списань і централізованої видимості?

## Гіпотеза

Незалежні локальні лічильники множать доступний бюджет, а eventual merge виявляє перевищення лише після розкриття. Точний централізований ledger зберігає conservation, але створює availability і metadata bottleneck. Escrow/reservation механізми можуть утримати hard cap без синхронного глобального lookup на кожен запит, проте залишають невикористані фрагменти бюджету та потребують явного повернення прав.

## Нульова гіпотеза

Після вирівнювання workload, budget і failure assumptions механізми спільного обліку не зменшують надлишкове розкриття порівняно з незалежними лічильниками або роблять це лише через неприйнятне падіння legitimate utility чи збільшення coordination cost.

## Одиниця аналізу

Одна **budget domain**: політично визначена група клієнтів і сервісів, які мають спільно витрачати один exposure-бюджет. Ground-truth exposure union існує лише в evaluator; механізми бачать дозволені structural disclosure keys та свої локальні ledger states.

## Межі

C1 досліджує:

- conservation і подвійне витрачання одного budget domain;
- concurrent decisions, delayed synchronization і network partition;
- false charge через повторні або overlap disclosures;
- centralized, eventual, hierarchical й escrow-based accounting;
- мінімальні security, utility, visibility та operational trade-offs.

C1 не визначає поведінку після повного виснаження бюджету (C2), не оптимізує availability (C3), не моделює цільове budget burning (C4), не обирає справедливий allocation rule (C5) і не відновлює бюджет у часі (C6). Principal membership надходить із B6 як фіксований evaluator input.

## Артефакти v0.1

- `architecture.md` — компоненти, state ownership і trust boundaries;
- `experiment-design.md` — paired matrix, controls і stop conditions;
- `metrics.md` — conservation, overrun, false charge, utility і cost;
- `falsification.md` — докази проти гіпотези та критичні контрприклади;
- `related-work.md` — майбутній source-backed огляд.

## Наступний крок

Реалізувати детермінований benchmark із 54,000 paired trials, invariant tests і окремим звітом про security–coordination frontier.
