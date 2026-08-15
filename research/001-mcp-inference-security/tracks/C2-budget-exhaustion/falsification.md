# C2 Falsification Plan

## Claims under test

1. Hard deny preserves the cap but blocks some tasks satisfiable from already exposed information.
2. Replay-only and pre-charged safe snapshots recover utility without new structural exposure.
3. Coarse fallback is not automatically safe; unaccounted coarse representations can reveal new structure.
4. Bounded override converts an implicit bypass into explicit, measurable exceptional exposure but cannot provide zero-loss security.
5. No tested deployable policy dominates post-cap security, utility and operational simplicity in every workload.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- hard deny creates no additional false denials relative to safe reuse policies;
- replay-only or safe snapshots add structural exposure despite correct precharging;
- coarse fallback never creates novel structural keys under any tested workload;
- bounded override releases more than its allowance or can be replayed;
- safe reuse provides no task-completion gain over hard deny;
- one deployable policy dominates every other policy on exposure, completion, false denial and cost with uncertainty included;
- task construction, rather than exhaustion policy, explains all differences.

## Critical counterexamples

- changing session or account silently restores a full ordinary budget;
- an exact replay is denied and the client cannot finish a task requiring no new information;
- a “coarse” range narrows the hidden state beyond all previous disclosures;
- a safe snapshot receives one fresh dynamic field after exhaustion;
- one override token is copied and spent multiple times;
- override use is omitted from the exposure report;
- a criticality label automatically bypasses the cap without bounded authority;
- denial responses themselves reveal which hidden-state condition caused exhaustion.

## Confounders

- different pre-exhaustion unions or tasks between policies;
- distributed accounting error inherited from C1;
- counting denied responses as released exposure;
- assuming representation coarseness equals semantic safety;
- treating cached text as safe without checking its structural units;
- hiding exception exposure in a separate metric;
- introducing temporal budget recovery from C6;
- averaging duplicate-only and new-only workloads together.

## Interpretation boundaries

C2 tests immediate behavior after a policy-defined structural budget reaches its cap. It does not establish that the cap is calibrated correctly, that semantic equivalence is solved, or that denying a task is legally or ethically acceptable.

Criticality is a synthetic sensitivity label, not authorization. Real emergency access, human review, liability and appeal procedures require separate governance and production research.
