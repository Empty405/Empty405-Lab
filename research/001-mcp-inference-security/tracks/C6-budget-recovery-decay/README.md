# C6 — Budget recovery / decay

**Program:** `001-mcp-inference-security`  
**Track:** C — Shared-budget problem  
**Module:** C6  
**Status:** Experiment design v0.1

## Простими словами

Старі дані можуть втрачати практичну цінність, hidden state може змінитися, а бізнесу потрібні нові відповіді. Але просте обнулення disclosure budget дозволяє повторно розкрити ті самі або пов’язані факти й накопичити небезпечну історію. C6 відділяє decay корисності від decay knowledge та перевіряє, коли recovery можна дозволити без прихованого lifetime exposure.

## Дослідницьке питання

> Які recovery policies відновлюють legitimate utility після виснаження budget, не дозволяючи administrative reset, time decay або state change маскувати довгострокове накопичення реконструйованої інформації?

## Гіпотеза

Fixed-window reset і простий linear decay покращують короткострокову availability, але створюють повторне exposure та historical reconstruction. Version-aware і evidence-based recovery повинні безпечніше повертати capacity після підтвердженої зміни state, однак будуть консервативнішими, дорожчими та чутливими до помилок change detector.

## Нульова гіпотеза

Після вирівнювання request history, hidden-state schedule та lifetime evaluator recovery policies не створюють практично значущої різниці, або будь-яке utility-покращення досягається лише пропорційним збільшенням lifetime reconstructability.

## Одиниця аналізу

Один **multi-epoch disclosure episode**: послідовність state versions, requests, releases, budget transitions і evaluator reconstruction over time. Deployable policy бачить лише дозволені timestamps, versions та change evidence; lifetime evaluator зберігає всю історію.

## Межі

C6 досліджує time-based, window-based, version-aware та evidence-based recovery. Він не визначає юридичне право на забуття, не стирає пам’ять зовнішнього спостерігача, не вирішує semantic observer errors (D), temporal inference повністю (E) або distributed history (F).

## Наступний крок

Реалізувати paired benchmark із raw epoch events, lifetime exposure ledger, reconstruction evaluator, invariant tests і utility–freshness–historical-risk frontier.
