# C4 Related Work Plan

**Status:** Source collection pending.

C4 needs a source-backed review before any production claim. The review will separate analogous mechanisms from direct evidence about MCP inference security.

## Source families to collect

- denial-of-service and resource-exhaustion attacks;
- algorithmic complexity and application-layer economic denial of sustainability;
- API quota abuse, rate limiting and admission control;
- max-min fairness, weighted fair queuing and dominant-resource allocation;
- privacy-budget allocation and composition;
- token-bucket and leaky-bucket traffic shaping;
- adversarial workload scheduling and multi-tenant isolation;
- abuse-resistant accounting and quota governance.

## Evidence rules

1. Prefer standards, peer-reviewed papers and primary system documentation.
2. Record the exact mechanism, threat model and resource being allocated.
3. Do not equate compute exhaustion, privacy loss and disclosure-budget exhaustion without an explicit analogy boundary.
4. Keep MCP-specific claims tied to this experiment's evidence.
5. Add stable URLs, publication identifiers and access dates when sources are collected.

## Open comparison questions

- When does request-rate limiting approximate exposure-cost limiting?
- Which fairness objective remains meaningful when requests have unequal marginal information cost?
- How should unused reservations be treated under bursty legitimate demand?
- Can adaptive admission avoid future knowledge while approaching oracle allocation?
- Which identity assumptions are necessary before per-principal controls are credible?
