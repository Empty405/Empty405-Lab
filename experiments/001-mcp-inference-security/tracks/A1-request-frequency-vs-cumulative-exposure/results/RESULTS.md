# A1 v0.1 Results

**Runs:** 1000 per configuration  
**Root seed:** `40501`  
**Configurations:** 2 query scenarios × 2 observer conditions × 5 policies  
**Total trial rows:** 20,000

## Answer first

Within this synthetic static benchmark, a patient observer reached the same final observable state under a resettable window rate limit as under the unrestricted baseline: **100%**. The rate limiter changed collection time from 0 to 540 logical seconds in the unique-query scenario and to 1680 seconds in the duplicate-heavy scenario.

An exact non-resetting coverage budget capped final observable state at **50%**. A hybrid policy preserved the same cap while also slowing collection. This supports the narrow A1 distinction between controlling collection speed and controlling final unique exposure.

The result does not show that rate limiting is useless. Under a 180-second deadline it reduced final exposure to 41.67% for unique queries and 14.58% for duplicate-heavy queries, demonstrating real value for time-sensitive state.

## Patient observer

| Scenario | Policy | Observable state | Reconstruction | Logical time | Legitimate utility |
|---|---|---:|---:|---:|---:|
| Unique | Baseline | 100.00% | 91.58% | 0 | 100.00% |
| Unique | Rate limit | 100.00% | 91.58% | 540 | 83.33% |
| Unique | Lifetime quota | 50.00% | 83.17% | 0 | 100.00% |
| Unique | Coverage budget | 50.00% | 83.17% | 0 | 100.00% |
| Unique | Hybrid | 50.00% | 83.17% | 240 | 83.33% |
| Duplicate-heavy | Baseline | 100.00% | 91.58% | 0 | 100.00% |
| Duplicate-heavy | Rate limit | 100.00% | 91.58% | 1680 | 83.33% |
| Duplicate-heavy | Lifetime quota | 16.67% | 77.60% | 0 | 100.00% |
| Duplicate-heavy | Coverage budget | 50.00% | 83.17% | 0 | 100.00% |
| Duplicate-heavy | Hybrid | 50.00% | 83.17% | 840 | 83.33% |

## Deadline boundary

With a 180-second observer deadline:

- rate limiting capped unique-query exposure at 41.67%;
- rate limiting capped duplicate-heavy exposure at 14.58%;
- the hybrid matched the rate limiter before the deadline and retained a permanent 50% cap afterward;
- baseline still exposed 100% because the toy server has no service-time model.

## Quota versus structural coverage

In the unique-query scenario, a 48-request lifetime quota and a 48-cell coverage budget both exposed 50% of the state. In the duplicate-heavy scenario, the lifetime quota spent requests on repeated cells and exposed only 16.67%, while coverage accounting allowed repeated already-disclosed answers and exposed its configured 50%.

This is not automatically an advantage for coverage accounting. It shows that request quotas and structural budgets allocate scarcity differently: a quota counts traffic; a coverage budget counts new structural disclosure.

## Utility result

Legitimate utility is evaluated using a separate 12-query workload with a 30-second task deadline. The baseline, lifetime quota, and coverage budget answered all 12 requests. The rate and hybrid policies answered 10 before the deadline, producing 83.33% utility.

The utility workload is intentionally small and synthetic. It does not establish production usability.

## Hypothesis decisions

| Hypothesis | Result |
|---|---|
| H1: patient rate limiting converges to baseline exposure | Supported in both scenarios |
| H2: rate limiting increases time-to-exposure | Supported |
| H3: non-resetting coverage creates final-state separation | Supported by construction and observed |
| H4: deadlines create a boundary where rate limiting protects state | Supported |
| H5: request quotas differ from coverage budgets under duplicates | Supported |

## Limitations

- static synthetic state;
- one stable principal;
- exact structural keys;
- deterministic three-band observer;
- no semantic equivalence;
- no identity rotation or collusion;
- no network or server processing latency;
- utility workload is not based on production MCP traces.

## Reproduction

```bash
python benchmark.py --runs 1000 --seed 40501
python plot_results.py
python -m unittest -v test_benchmark.py
```

Raw per-trial data is stored in `trials.csv.gz`; aggregated configuration and results are stored in `benchmark.json`.
