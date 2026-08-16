# C5 Related Work Plan

**Status:** Source collection pending.

C5 requires a source-backed review before production claims. The review will distinguish allocation fairness, scheduling fairness and privacy/disclosure-budget allocation.

## Source families to collect

- max-min fairness and progressive filling;
- weighted fair queuing and generalized processor sharing;
- proportional fairness;
- dominant-resource fairness and multi-resource allocation;
- quota reservation, borrowing and hierarchical token buckets;
- fairness metrics including Jain index and generalized entropy;
- envy-freeness and fair division;
- privacy-budget allocation and composition;
- multi-tenant admission control and service-level objectives.

## Evidence rules

1. Prefer primary papers, standards and authoritative system documentation.
2. Record the allocated resource, client model, objective and assumptions.
3. Do not transfer fairness guarantees from divisible compute resources to disclosure exposure without stating the analogy boundary.
4. Separate declared weights from evaluator task value.
5. Tie MCP-specific conclusions to C5 evidence rather than analogy alone.

## Open comparison questions

- Which fairness objective remains meaningful when requests have unequal marginal exposure cost?
- When should unused reservations be borrowed, and how is late demand protected?
- How sensitive are weighted policies to strategic or accidental weight misspecification?
- Can utility fairness coexist with exposure-share fairness?
- Which metrics remain interpretable when client demand is zero or highly bursty?
