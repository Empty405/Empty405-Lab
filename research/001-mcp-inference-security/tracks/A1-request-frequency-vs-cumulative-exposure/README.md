# A1 — Request-Frequency vs Cumulative Exposure

**Program:** Research 001 — MCP Inference Security  
**Track:** A1  
**Status:** Designed  
**Evidence inherited from:** v0.1 toy benchmark  
**Claim maturity:** Preliminary; not a production security guarantee

## Research question

> Under a patient observer, do request-frequency controls reduce final reconstructable information, or do they primarily increase the time required to collect the same permitted observations?

## Narrow claim

A resettable time-window rate limiter constrains throughput. It does not necessarily constrain the final set of distinct facts disclosed to a principal that can wait for windows to reset.

This claim is narrower than saying that rate limiting is ineffective. Rate limiting may still reduce load, automation speed, burst abuse, and the feasibility of attacks with deadlines.

## Null hypothesis

After controlling for elapsed time and query opportunity, a conventional rate limiter reduces final cumulative exposure and reconstruction to approximately the same degree as a non-resetting structural exposure budget.

## Alternative hypothesis

For an observer without a binding deadline, a resettable rate limiter changes collection time but converges toward the unrestricted observable state, while a non-resetting exposure budget changes the final observable state.

## Independent variable

Policy mode:

1. unrestricted baseline;
2. requests-per-window limiter;
3. fixed lifetime request quota;
4. unique-coverage budget;
5. hybrid rate plus coverage policy.

## Dependent variables

- final observable-state fraction;
- reconstruction score;
- information gained per released response;
- wall-clock collection time;
- queries attempted, delayed, released, and denied;
- legitimate task utility.

## Controlled variables

- hidden state;
- tool schemas;
- query sequence;
- observer algorithm;
- identity and accounting principal;
- disclosure precision;
- random seed.

Identity rotation, semantic equivalence, multiple servers, dynamic hidden state, and adaptive attackers are excluded. They belong to B, D, E, F, and G.

## Unit of disclosure

The canonical v0.1 unit is one unique `location × resource` cell observed within a static epoch. A released response can expose zero or more units. Repeating an already released fact does not increase unique structural coverage, although it can still increase statistical confidence; that limitation is reserved for later observer tracks.

## Core comparison

| Policy | Resets with time? | Counts requests? | Counts new coverage? | Expected effect |
|---|---:|---:|---:|---|
| Baseline | — | No | No | Fast convergence |
| Rate limit | Yes | Yes | No | Slower convergence |
| Lifetime quota | No | Yes | No | Lower final query count |
| Coverage budget | No | Optional | Yes | Lower final unique exposure |
| Hybrid | Partly | Yes | Yes | Controls speed and final coverage |

## Scope boundary

A1 does not establish:

- that every API or MCP tool leaks sensitive state;
- that structural coverage equals semantic information;
- that rate limiting has no security value;
- that a gateway can reliably identify a durable principal;
- that the proposed budget is fair, deployable, or resistant to Sybil attacks;
- that an MCP protocol change is required.

## Prior evidence

The v0.1 synthetic benchmark reported equal final reconstruction and observable state for baseline and rate-limit-plus-waiting modes, while hard coverage changed the final result. A1 treats that result as a motivating observation, not as independent replication.

## Decision rule

A1 is provisionally supported only if rate-limited runs converge toward baseline final exposure when deadlines are relaxed, while non-resetting coverage policies remain separated under identical released-query opportunities.

## Outputs

- reproducible benchmark configuration;
- time-to-exposure and exposure-to-query curves;
- convergence analysis across several deadlines and window sizes;
- negative and boundary results;
- explicit statement of which result is about time and which is about final knowledge.
