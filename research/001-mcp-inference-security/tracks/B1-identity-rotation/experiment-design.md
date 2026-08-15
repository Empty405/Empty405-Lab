# B1 Experiment Design

## Primary experiment

Запустити одного durable attacker проти того самого hidden state. Атакувальник робить фіксовану кількість структурно унікальних запитів і ротують visible identity за заданим розкладом. Порівняти attribution/accounting strategies на парних seeds.

## Independent variables

- rotation count: `0, 1, 2, 4, 8, 16`;
- rotation cadence: fixed interval, on-denial, on-budget-threshold;
- attribution strategy: identity, session, durable credential, deterministic, probabilistic, oracle;
- exposure budget: `0.25, 0.50, 0.75`;
- signal quality: clean, noisy, partially missing;
- legitimate population: isolated clients, shared network, shared device pool.

## Controlled variables

- hidden state;
- query sequence and semantic coverage;
- total attacker request count;
- observer algorithm;
- trial seed;
- disclosure budget and response encoding;
- deadline.

## Scenarios

1. **Stable baseline:** attacker never rotates.
2. **Fixed rotation:** identity changes every N requests.
3. **Reactive rotation:** identity changes immediately after denial.
4. **Signal loss:** stable attribution signals disappear during rotation.
5. **Shared environment:** unrelated legitimate users share weak signals.
6. **Credential reissue:** durable credential changes but principal remains the same.

## Outputs per trial

- raw request and decision log;
- identity-to-attribution mapping;
- cumulative exposure trajectory;
- reconstructed hidden units;
- legitimate task outcomes;
- false merge/split events;
- policy evaluation and storage cost.

## Statistical plan

- paired comparisons by seed and workload;
- report mean, median, p95 and uncertainty intervals;
- estimate dose-response between rotation count and excess exposure;
- report security and utility jointly, not as one hidden weighted score;
- retain all negative and null results.

## Minimum viable run

`6 rotation counts × 6 strategies × 3 budgets × 3 signal qualities × 1000 paired trials`.

Shared-environment utility scenarios are a separate crossed run so security findings are not silently averaged with attribution harm.

## Stop conditions

Stop and repair the harness if:

- policy code can access ground-truth principal IDs;
- request counts differ across paired policies;
- rotation alters query content;
- reconstruction exceeds the known hidden-state bound;
- an attribution decision lacks provenance.
