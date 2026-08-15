# B1 Falsification Plan

## Claims under test

1. Per-identity accounting is resettable through identity rotation.
2. Rotation count creates a measurable exposure-amplification curve.
3. Stronger attribution reduces bypass but introduces utility and attribution errors.

## Evidence against the hypothesis

The hypothesis is weakened or rejected if, under matched requests and workloads:

- rotation does not materially increase excess exposure or reconstruction;
- amplification disappears across all tested budgets and cadences;
- per-identity accounting performs comparably to oracle principal accounting;
- attribution-aware defenses reduce neither excess exposure nor reconstruction;
- observed differences are caused by unequal query counts, deadlines or hidden-state changes.

## Confounders to audit

- more identities accidentally receiving more total requests;
- query scheduler changing after a denial;
- observer using identity labels as extra information;
- hidden state resetting during identity rotation;
- oracle principal IDs leaking into policy decisions;
- shared-network scenarios being mistaken for attacker linkage.

## Interpretation boundaries

A successful simulation does not prove that production systems can reliably identify people. It demonstrates the consequences of specified attribution assumptions.

B1 must not recommend invasive fingerprinting from security metrics alone. Any production proposal requires an explicit privacy, proportionality and false-attribution review in B6/J1.
