# B4 v0.1 Results — Cross-session Accumulation

## Outcome

The narrow hypothesis is supported for the static hidden-state fixture. Session reset, expiring windows, and exponential decay can reopen disclosure capacity while the observer retains old facts. Persistent accounting holds observer knowledge to the principal budget but substantially reduces continuation utility.

## Run

- root seed: `40514`;
- 1,080 configurations;
- 500 trials per configuration;
- 540,000 compressed raw rows;
- exactly 96 requests per trial;
- seven unit tests passed.

## Representative result

16 sessions, budget `0.25`, partitioned workload:

| Gap | Policy | Observer known | Policy accounted | Exposure gap | Continuity utility |
|---|---|---:|---:|---:|---:|
| short | session reset | 0.960 | 0.060 | 0.900 | 1.000 |
| short | persistent | 0.250 | 0.250 | 0.000 | 0.260 |
| short | fixed TTL | 0.250 | 0.250 | 0.000 | 0.260 |
| short | rolling window | 0.810 | 0.250 | 0.560 | 0.844 |
| short | exponential decay | 0.960 | 0.204 | 0.756 | 1.000 |
| long | fixed TTL | 0.960 | 0.060 | 0.900 | 1.000 |
| long | rolling window | 0.960 | 0.060 | 0.900 | 1.000 |
| long | exponential decay | 0.960 | 0.063 | 0.897 | 1.000 |

## What survived falsification

- Session reset creates a large exposure gap without increasing total requests.
- Persistent accounting prevents cross-session budget refresh in the static fixture.
- TTL works while gaps remain inside its boundary, then reopens almost the full budget after expiry.
- Rolling windows and exponential decay trade security for continuation utility gradually or at window boundaries.
- Duplicate-heavy workloads accumulate less because old answers repeat; session count alone is not sufficient.

## Central finding

Lower accounted exposure is not equivalent to lower observer knowledge. At long gaps, exponential decay accounts for only `0.063` while the observer retains `0.960` of the hidden state.

## Limitations

- static hidden state only;
- fixed-total-request regime only;
- synthetic logical time and retention parameters;
- structural exposure rather than semantic inference;
- no normative claim that indefinite principal tracking is acceptable.

## Next question

B5 should test the same accumulation problem when exposure ledgers are split across independently operated MCP servers.
