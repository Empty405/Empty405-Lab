# B5 Architecture

## Components

1. **Hidden-state fixture** — спільний або частково перекривний інформаційний простір.
2. **Principal client** — робить запити до кількох servers.
3. **Server fleet** — незалежні MCP endpoints і disclosure policies.
4. **Local ledgers** — server-scoped exposure state.
5. **Federation coordinator** — optional shared accounting plane.
6. **Sync transport** — delivers counters, tokens, sketches or events.
7. **Partition injector** — lag, dropped updates, stale replicas and offline nodes.
8. **Client observer** — union усіх фактично отриманих disclosures.
9. **Evaluator** — ground-truth principal, server provenance and hidden state.

## Accounting models

| Model | Shared state | Main risk |
|---|---|---|
| Local only | none | budget multiplication |
| Central ledger | exact events/counter | central surveillance and outage |
| Eventual counter | asynchronous totals | stale-state race windows |
| Signed budget token | client carries remaining budget | replay, fork and issuer trust |
| Privacy-preserving sketch | approximate shared coverage | collisions and false denial |
| Oracle federation | exact ground truth | evaluator-only bound |

## Trust boundaries

- A server cannot inspect another local ledger unless the protocol explicitly shares data.
- Client observer sees all its replies; servers do not see this local union.
- Ground-truth principal ID is unavailable to deployable federation models.
- Sync transport carries only declared fields.
- Network partition cannot silently fall back to an unlimited budget.
- Oracle federation is never a production proposal.

## Federation message

```text
ExposureUpdate {
  pseudonymous_principal_key,
  policy_version,
  structural_scope,
  exposure_delta_or_sketch,
  logical_timestamp,
  source_server,
  replay_nonce,
  signature
}
```

Every field shared across operators is included in metadata-cost accounting.

## Failure modes

- delayed or reordered updates;
- dropped messages;
- duplicated/replayed updates;
- client forks signed tokens;
- coordinator outage;
- server fail-open or fail-closed;
- version mismatch;
- sketch collision;
- principal false merge/split.
