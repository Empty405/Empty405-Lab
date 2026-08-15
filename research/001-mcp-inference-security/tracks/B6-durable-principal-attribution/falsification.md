# B6 Falsification Plan

## Claims under test

1. Session- or account-scoped identities allow exposure-budget resets across lifecycle boundaries.
2. More durable/global attribution reduces budget bypass but expands linkability and the damage of false merges.
3. Pairwise pseudonyms and anonymous budget credentials can move the security–privacy frontier but require explicit trust, recovery and availability assumptions.
4. No deployable mechanism matches oracle continuity, privacy and utility under every tested condition.

## Evidence against the hypothesis

The claims are weakened or rejected if:

- lifecycle rotation does not increase exposure under session/account baselines;
- global identifiers add no measurable continuity over scoped alternatives;
- pairwise or anonymous mechanisms match oracle security across transfer, recovery and outage while exposing no additional linkage;
- stronger durability does not increase false-merge harm or linkability;
- unknown-identity handling, rather than attribution, explains all security differences;
- a single deployable mechanism dominates every other mechanism on security, privacy, utility and cost with uncertainty included.

## Critical counterexamples

- two people sharing a device are merged and one loses access;
- one person using multiple legitimate devices is split into fresh budgets;
- stolen credentials transfer historical budget attribution to the victim indefinitely;
- recovery restores service only by silently resetting exposure;
- pairwise identifiers become globally joinable through metadata;
- anonymous credentials can be forked without detection;
- an attribution outage causes unlimited fail-open disclosure;
- fail-closed protection excludes an entire low-resource client group.

## Confounders

- varying request count or hidden state between mechanisms;
- treating accounts, devices or network addresses as ground-truth people;
- counting denied disclosures as observed;
- ignoring issuer and broker observations;
- averaging false merge and false split into one number;
- omitting credential lifecycle and recovery;
- giving the oracle deployable status;
- excluding clients who cannot maintain durable hardware or accounts.

## Interpretation boundaries

B6 evaluates policy-scoped attribution for exposure accounting, not proof of legal or biological identity. A lower reconstruction score does not justify biometric identification, covert fingerprinting or unrestricted cross-service tracking.

A globally stable key may be technically effective and still be unacceptable because it creates a new surveillance and exclusion surface. Conclusions must state who can link which contexts, for how long, and what happens when attribution is wrong.
