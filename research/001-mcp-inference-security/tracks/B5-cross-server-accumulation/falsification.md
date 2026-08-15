# B5 Falsification Plan

## Claims under test

1. Independent local budgets multiply across servers.
2. Complementary server outputs increase aggregate reconstruction more than overlapping outputs.
3. Eventual consistency creates exploitable exposure overshoot.
4. Stronger shared accounting exchanges security for metadata privacy, availability and governance cost.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- server count does not change client union at fixed total requests;
- disjoint and high-overlap outputs perform equivalently;
- delayed/partitioned sync matches healthy sync;
- local accounting performs like exact federation;
- approximate sketches match exact accounting without collision or utility cost;
- metadata-minimal coordination achieves exact results under all failures.

## Confounders

- granting more total requests as servers increase;
- hidden state changing by server;
- duplicate disclosures counted as unique;
- client observer receiving denied responses;
- central ledger using oracle principal identity;
- partitioned nodes silently fail-open;
- metadata cost measured without identifier/linkability fields.

## Interpretation boundaries

Cross-server coordination may require operators to share identifiers, query structure or exposure history that they otherwise would not possess. Preventing reconstruction must not be presented as a free privacy improvement if it creates a new cross-organization tracking system.

B5 evaluates mechanisms under declared trust and failure assumptions. Legal basis, governance and production deployment require F3, B6 and J1–J3.
