# B3 — Colluding Observers

**Program:** Research 001 — MCP Inference Security  
**Track:** B — Identity / Principal Problem  
**Status:** Designed  
**Depends on:** A1, A2, B1, B2  
**Feeds into:** B5, B6, D4, F1, F4, F5

## Простими словами

Кілька реальних незалежних клієнтів можуть отримати різні дозволені фрагменти, а потім обмінятися ними поза MCP-сервером. Для кожного окремо бюджет не порушений, але коаліція бачить значно більше, ніж будь-хто з учасників.

B3 не припускає одного прихованого controller, як B2. Учасники мають окремі цілі й трафік, а змова визначається тим, що вони діляться спостереженнями та будують спільну реконструкцію.

## Research question

> How much additional hidden state can a coalition reconstruct by combining individually permitted observations, and which defenses remain effective when evidence of off-server sharing is unavailable?

## Narrow hypothesis

Per-client budgets обмежують окремого observer, але не обмежують union інформації коаліції. Якщо учасники координують неперекривні запити, coalition reconstruction зростатиме швидше, ніж за випадкового незалежного використання. Політики, що стримують coalition exposure без знання coalition ground truth, матимуть помітну ціну для легітимних груп.

## Null hypothesis

За однакової загальної кількості запитів обмін відповідями не дає суттєвого reconstruction gain; індивідуальні бюджети або природне перекриття відповідей достатньо обмежують coalition union.

## Unit of analysis

- **observer:** окремий легітимно автентифікований клієнт;
- **coalition:** набір observers, які обмінюються частиною спостережень;
- **collusion graph:** хто з ким може ділитися відповідями;
- **exchange timing:** post-hoc або online;
- **coalition observer:** evaluator-side reconstruction із фактично переданих відповідей.

Coalition membership є ground truth лише для симулятора й evaluator.

## Scope

Included:

- 1–32 окремих observers;
- post-hoc sharing як primary experiment;
- random, overlapping і partitioned query behavior;
- partial/full exchange;
- per-client, organizational, cohort, diversity, global і oracle-coalition policies;
- coalition reconstruction, detectability, legitimate group utility та cost.

Excluded:

- один controller з багатьма identities — B2;
- різні MCP servers — B5/F2;
- semantic equivalence — D2;
- cross-tool composition — D4;
- зовнішні публічні джерела — F5.

## Decision rule

B3 підтримує гіпотезу, якщо coalition union або exact recovery суттєво перевищують maximum individual reconstruction при matched total requests, а ефект залежить від coordination, overlap та exchange fraction.

Захист оцінюється чесно лише тоді, коли він не використовує приховане coalition membership і звітує false suspicion та legitimate group utility.
