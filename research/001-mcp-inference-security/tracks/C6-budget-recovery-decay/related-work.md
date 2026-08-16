# C6 Related Work Plan

**Status:** Source collection pending.

## Source families

- sliding-window and token-bucket quota recovery;
- privacy-budget composition and privacy odometers;
- temporal access control and key rotation;
- cache invalidation and versioned data;
- concept drift and change detection;
- data retention and machine unlearning;
- forward secrecy and key erasure;
- continual observation and longitudinal inference.

## Evidence rules

Prefer primary papers, standards and authoritative documentation. Separate resource replenishment from information forgetting. Do not equate key deletion, model unlearning, legal deletion and loss of observer knowledge. Record threat model, memory assumption, state dynamics and recovery evidence for every analogy.

## Open questions

- What evidence is sufficient to declare an exposed fact obsolete?
- How should cyclic state return affect recovery?
- Can recovery be bounded by measured reconstruction loss?
- What detector error rate makes evidence-based recovery worse than no recovery?
- Which lifetime-history structures remain practical in production gateways?
