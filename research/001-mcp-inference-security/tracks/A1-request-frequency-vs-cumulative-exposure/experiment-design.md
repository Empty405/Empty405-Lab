# A1 Experiment Design

## Experimental matrix

Run the same scenario and query stream under:

1. baseline;
2. rate limits of 5, 10, and 20 requests per window;
3. window durations of 10, 60, and 300 logical seconds;
4. lifetime quotas matching 25%, 50%, and 75% of the query space;
5. coverage budgets matching 25%, 50%, and 75% of unique cells;
6. hybrid policies combining each rate limit with the corresponding coverage budget.

## Observer conditions

### Patient observer

Waits until `retry_at` and continues until every permitted query has been answered or permanently denied.

### Deadline observer

Stops at fixed logical deadlines. Deadlines reveal when rate limiting has real security value because information becomes stale or the attack has a time constraint.

### Query-budget observer

Stops after a fixed number of attempts. This separates time cost from request cost.

## Trials

Minimum initial benchmark:

- 1000 randomized states;
- fixed root seed `40501`;
- randomized query order derived from the trial seed;
- identical trial inputs across policy modes;
- static state;
- one stable principal;
- one observer algorithm.

## Primary hypotheses

### H1 — Asymptotic convergence

With no deadline, final observable state under a resettable rate limiter approaches baseline.

### H2 — Time displacement

Rate limiting increases time-to-threshold for 25%, 50%, 75%, and 90% exposure.

### H3 — Final-state separation

A non-resetting coverage budget caps final observable state below baseline at the configured budget fraction.

### H4 — Deadline boundary

With sufficiently short deadlines, rate limiting reduces exposure before the deadline and therefore can be an effective control for time-sensitive secrets.

### H5 — Request quota distinction

A lifetime request quota may reduce final exposure without understanding structure, but wastes budget on duplicate queries and does not allocate disclosure according to new information.

## Falsification criteria

The core A1 claim is weakened or falsified if any of the following survives debugging and replication:

- a patient observer cannot converge toward baseline under resettable rate limits;
- convergence differences remain after every delayed query is eventually released;
- a coverage budget fails to cap the exact coverage unit it tracks;
- the reported advantage comes only from unequal released-query opportunities;
- conclusions reverse under modest changes in state size, query order, or seed;
- ordinary non-resetting quotas provide equivalent exposure and utility behavior, making structural accounting unnecessary for the tested scenario.

## Required plots

1. exposure vs logical time;
2. exposure vs released queries;
3. exposure vs attempted queries;
4. reconstruction vs logical time;
5. legitimate utility vs exposure cap;
6. final exposure by policy with confidence intervals;
7. convergence gap between baseline and rate limit as deadline increases.

## Statistical reporting

Report mean, median, standard deviation, 95% bootstrap confidence intervals, and the full per-trial output. Do not report only the seed-405 example.

## Controls

- replay identical query streams;
- use exact accounting before approximate accounting;
- preserve raw ledger events;
- test duplicate-heavy and unique-heavy query streams separately;
- validate metric bounds and monotonicity;
- distinguish delayed from permanently denied responses.

## Interpretation rules

A delay is not counted as a prevented disclosure if the response is eventually released.

A denial is not automatically a privacy success; utility cost must be reported.

Structural coverage is a proxy for disclosure, not a proof of mutual information or differential privacy.

A result supports only the tested static, single-principal scenario.
