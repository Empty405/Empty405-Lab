# B4 Metrics

## Exposure gap

```text
EG(t) = observer_known_exposure(t) - policy_accounted_exposure(t)
```

Positive EG means the server has discounted information that the observer still knows.

## Cross-session amplification

```text
CSA(s) = reconstruction_after_s_sessions / max(reconstruction_after_1_session, epsilon)
```

## Excess historical exposure

```text
EHE = max(0, observer_known_exposure - nominal_principal_budget)
```

## Time and sessions to threshold

First logical time and first session index at which observer reconstruction exceeds a declared threshold.

## Memory-policy metrics

- expired-but-known exposure;
- decayed-but-known exposure;
- reset gain per session;
- effective accounted exposure;
- ledger retention length;
- boundary sensitivity near TTL/window expiry.

## Legitimate utility

- task continuation success;
- repeated-monitoring success;
- denied legitimate requests;
- p95 delay;
- recovery after inactivity;
- worst-workload utility.

## Operational and governance cost

- retained entries and bytes;
- policy evaluation time;
- deletion events;
- provenance completeness;
- duration of principal-level tracking;
- fraction of decisions using historical data.

## Reporting rule

Never describe lower accounted exposure as real privacy recovery unless observer-known exposure or reconstruction also decreases under an explicit hidden-state relevance model.
