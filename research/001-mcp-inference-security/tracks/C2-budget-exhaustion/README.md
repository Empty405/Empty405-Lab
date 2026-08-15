# C2 — Budget exhaustion

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C2  
**Status:** Experiment design v0.1

## Простими словами

Коли exposure-бюджет уже використано, система має відповісти на наступний запит: відмовити, повторити вже відому інформацію, дати грубіший результат або дозволити контрольований виняток. C2 перевіряє, які варіанти справді не відкривають новий прихований стан і наскільки вони залишаються корисними для легітимної задачі.

## Дослідницьке питання

> Яка post-exhaustion policy найкраще зберігає нульовий або явно обмежений приріст exposure після досягнення cap, водночас дозволяючи повторне використання вже розкритої інформації та завершення задач, які не потребують нового розкриття?

## Гіпотеза

Безумовний hard deny найпростіше зберігає cap, але помилково блокує запити, що можна виконати з уже розкритого стану. Replay-only і safe-snapshot policies можуть відновити частину корисності без нового structural exposure. Coarse fallback без окремого semantic accounting інколи створює приховане нове розкриття, а bounded override робить ризик явним і вимірюваним, але не нульовим.

## Нульова гіпотеза

Після вирівнювання pre-exhaustion state, workload і task requirements жодна post-exhaustion policy не підвищує legitimate task completion порівняно з hard deny без статистично або практично значущого приросту exposure чи прихованого виняткового каналу.

## Одиниця аналізу

Один **exhaustion episode**: budget domain із точно вичерпаним structural budget, фіксованим pre-exhaustion exposure union і наступною послідовністю запитів. C1 ledger є точним первинним control; C2 не виправляє distributed accounting.

## Межі

C2 досліджує:

- рішення одразу після досягнення cap;
- повторні, нові, змішані та multi-step post-exhaustion workloads;
- hard deny, replay, downgrade, safe snapshot і bounded override;
- explicit exposure gain, false denial, task completion та policy ambiguity;
- перехід через boundary без прихованого reset.

C2 не оптимізує service availability у часі (C3), не моделює цільове спалювання бюджету (C4), не розподіляє бюджет між клієнтами (C5) і не повертає бюджет через decay або recovery (C6). Semantic equivalence та encoding bypasses належать D2–D4.

## Артефакти v0.1

- `architecture.md` — exhaustion gate, response classes і trust boundaries;
- `experiment-design.md` — paired matrix, controls і stop conditions;
- `metrics.md` — post-cap exposure, false denial, utility та override risk;
- `falsification.md` — докази проти гіпотези й критичні контрприклади;
- `related-work.md` — майбутній source-backed огляд.

## Наступний крок

Реалізувати детермінований benchmark із 54,000 paired trials, invariant tests і security–post-exhaustion-utility frontier.
