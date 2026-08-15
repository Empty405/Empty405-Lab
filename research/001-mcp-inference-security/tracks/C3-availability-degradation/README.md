# C3 — Availability degradation

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C3  
**Status:** Experiment design v0.1

## Простими словами

Захист може не допустити витік, але зробити сервіс практично непридатним: відповіді зникають, черга росте, retry закінчуються timeout, а після відновлення приходить лавина старих задач. C3 вимірює цю ціну в часі й окремо перевіряє небезпечну спокусу “тимчасово відкрити все”, щоб покращити uptime.

## Дослідницьке питання

> Як post-exhaustion та dependency-failure policies змінюють task availability, tail latency, queue stability і exposure під slowdown, outage, partition та recovery storm, якщо shared ledger і cap зафіксовані з C1–C2?

## Гіпотеза

Hard deny і fail-closed зберігають cap, але створюють найгіршу availability для задач, які могли б використати вже відомі дані. Replay, safe snapshot і graceful degradation відновлюють частину task success без нового exposure. Queue-and-retry допомагає лише при коротких збоях і може погіршити tail latency та recovery storm. Fail-open покращує apparent uptime ціною прямого security violation.

## Нульова гіпотеза

Після вирівнювання workload, disruption schedule, timeout і task requirements захисні policies не створюють практично значущої різниці в availability або будь-яке її покращення повністю пояснюється додатковим exposure.

## Одиниця аналізу

Один **availability episode**: 120 дискретних ticks, фіксований потік легітимних задач, точний ledger/cap state, dependency schedule, policy decisions і recovery phase. Ground-truth task sufficiency та released exposure union існують лише в evaluator.

## Межі

C3 досліджує:

- success, timeout, queueing і latency протягом disruption;
- healthy, slowdown, outage, partition і recovery-storm schedules;
- hard deny, replay, snapshot, graceful degradation, queue/retry, fail-open та oracle;
- stale-but-safe responses і explicit exposure violations;
- service-level trade-off між security та availability.

C3 не моделює навмисне budget burning (C4), fairness між клієнтами (C5) або budget recovery/decay (C6). Criticality є лише synthetic sensitivity label, а не право на bypass. Реальні SLO, emergency access і governance належать production research J1–J6.

## Артефакти v0.1

- `architecture.md` — time model, queues, dependencies і trust boundaries;
- `experiment-design.md` — paired matrix, controls і stop conditions;
- `metrics.md` — availability, latency, queue, exposure та recovery metrics;
- `falsification.md` — докази проти гіпотези й критичні контрприклади;
- `related-work.md` — майбутній source-backed огляд.

## Наступний крок

Реалізувати детермінований benchmark із 63,000 paired trials, invariant tests і security–availability frontier.
