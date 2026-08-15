# B2 Falsification Plan

## Claims under test

1. Per-identity budgets multiply under a coordinated Sybil pool.
2. Disjoint query partitioning increases reconstruction more efficiently than duplication.
3. Parallel identities reduce time-to-reconstruction under finite deadlines.
4. Shared accounting reduces attack gain but can harm legitimate multi-tenant users.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- reconstruction remains invariant with pool size at matched request volume;
- duplicate, random and partitioned coordination perform equivalently;
- finite-deadline speed does not improve with concurrency;
- per-identity accounting matches attributed or oracle accounting;
- shared policies reduce neither exposure nor time-to-reconstruction;
- apparent amplification disappears after controlling for actual request count.

## Confounders

- silently granting each identity a full extra request workload;
- duplicate queries counted as new structural exposure;
- scheduler giving Sybils lower latency than legitimate clients;
- global budget using a different nominal cap;
- controller ground truth leaking into clustering;
- false merges omitted from the utility calculation.

## Interpretation boundaries

A Sybil simulation demonstrates a vulnerability under declared identity and budget assumptions. It does not show that real identities can be linked accurately or that identity proofing is proportionate.

Proof-of-personhood, device fingerprinting, payment requirements and government identity checks introduce independent privacy, exclusion and governance risks. B2 reports these as costs; it does not select a production identity regime.
