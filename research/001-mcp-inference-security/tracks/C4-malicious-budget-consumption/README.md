# C4 — Malicious budget consumption

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C4  
**Status:** Experiment design v0.1

## Простими словами

Спільний disclosure budget можна атакувати без прямого обходу захисту: зловмисний клієнт навмисно робить дозволені, але дорогі запити, спалює загальний запас нової інформації та залишає законним клієнтам лише deny, replay або низькоякісні відповіді. C4 вимірює цю форму denial-of-information і перевіряє, які admission policies обмежують шкоду без прихованого збільшення exposure.

## Дослідницьке питання

> За яких умов стратегічний клієнт може виснажити shared exposure budget і знизити корисність для легітимних клієнтів, та які bounded admission policies мінімізують цю шкоду без нового exposure або знання майбутнього?

## Гіпотеза

За global first-come-first-served зловмисник із високою частотою або високою marginal exposure cost може непропорційно захопити бюджет і різко знизити legitimate task completion. Per-principal reservation, bounded marginal-cost admission і rate-shaped allocation зменшать denial-of-information, але створять trade-off між utilization, fairness, metadata cost і помилковим обмеженням bursty legitimate clients.

## Нульова гіпотеза

Після вирівнювання arrival schedule, legitimate demand, attacker request budget і disclosure cap стратегічна поведінка не створює практично значущої додаткової шкоди порівняно з еквівалентним benign load, або захисні policies не покращують legitimate utility без рівнозначного зростання exposure чи невикористаного бюджету.

## Одиниця аналізу

Один **budget-contention episode**: фіксований shared cap, exact C1 ledger, набір principal identities, 120 ticks legitimate arrivals, attacker strategy, admission policy та terminal outcomes. Evaluator знає client role і future task value; deployable policies цього не знають.

## Межі

C4 досліджує:

- strategic exhaustion через дозволені requests;
- request frequency, marginal exposure cost і timing attacks;
- legitimate completion, victim denial, budget capture та wasted exposure;
- global FIFO, rate limit, per-principal reservation, marginal-cost cap, fair-share і oracle controls;
- single shared ledger без reset або decay.

C4 не вирішує Sybil attribution заново (B1–B6), повну multi-client fairness (C5), budget recovery/decay (C6), semantic observer errors (D) або production identity governance (J). Attacker role існує лише в evaluator і не доступна deployable policies.

## Артефакти v0.1

- `architecture.md` — principals, ledger, admission path і trust boundaries;
- `experiment-design.md` — paired matrix, attacker strategies, controls і stop conditions;
- `metrics.md` — capture, victim harm, utility, fairness, exposure і cost;
- `falsification.md` — докази проти гіпотези та критичні контрприклади;
- `related-work.md` — джерельний план без неперевірених тверджень.

## Наступний крок

Реалізувати детермінований benchmark із paired episodes, raw request events, invariant tests і security–availability–fairness frontier.
