# B6 Architecture

## Components

1. **Principal simulator** — ground-truth actor, devices, accounts and credential lifecycle.
2. **Credential issuer** — issues, rotates, revokes and reissues credentials under a declared policy.
3. **Client wallet** — stores pseudonyms, spend tokens or proofs and may copy or lose them.
4. **MCP gateway** — authenticates a presented context and requests an attribution decision.
5. **Attribution service** — maps observations to a policy-scoped principal key.
6. **Exposure ledger** — charges disclosures to that key and enforces the remaining budget.
7. **Recovery and revocation service** — handles loss, compromise, transfer and re-enrollment.
8. **Observer/adversary** — attempts budget reset, credential sharing or cross-context linkage.
9. **Evaluator** — holds ground truth and measures security, privacy, utility and cost.

## Attribution models

| Model | Continuity | Cross-context visibility | Primary risk |
|---|---|---|---|
| Session identifier | one session | low | reset after rotation |
| Account subject | credential/account lifecycle | issuer and service | new-account bypass |
| Global stable identifier | broad/global | every receiving operator | surveillance and catastrophic false merge |
| Pairwise pseudonym + broker | per service with controlled joining | broker sees joins | broker trust and outage |
| Anonymous budget credential | transferable remaining budget, not identity | issuer sees issuance/redemption policy | replay, fork and recovery |
| Oracle principal | exact ground truth | evaluator only | non-deployable upper bound |

## Core flow

1. A client presents a credential, pseudonym or anonymous budget proof.
2. The gateway sends only declared evidence to the attribution service.
3. The service returns a policy-scoped principal key or an explicit unknown result.
4. The exposure ledger checks and charges the budget before disclosure.
5. Rotation, recovery, transfer or outage changes the available evidence.
6. The evaluator compares the decision with ground truth without revealing it to deployable components.

## Trust boundaries

- Ground-truth principal ID never enters a deployable mechanism.
- Pairwise identifiers for different services are not directly equal.
- The gateway cannot inspect wallet secrets not presented by the protocol.
- Anonymous budget credentials must not silently become stable tracking identifiers.
- Recovery cannot mint a fresh full budget without accounting for the previous credential.
- A shared device or network address is not sufficient proof of a shared principal.
- Every party able to join contexts is recorded in the linkability surface.
- Unknown identity must produce an explicit policy decision, not an implicit unlimited budget.

## Minimal data objects

```text
AttributionEvidence {
  policy_scope,
  credential_class,
  scoped_subject_or_commitment,
  lifecycle_epoch,
  issuer,
  revocation_or_spend_proof,
  nonce,
  signature
}

AttributionDecision {
  policy_scoped_principal_key,
  confidence_or_exactness,
  decision_basis,
  expiry,
  recovery_state,
  audit_reference
}
```

## Failure modes

- false split after rotation, loss or reissue;
- false merge of household, shared device or recycled account;
- copied or transferred credential;
- forked anonymous spend state;
- issuer or broker collusion;
- coordinator outage and fail-open reset;
- revocation delay;
- recovery abuse;
- correlation through supposedly non-identifying metadata;
- exclusion of clients unable to maintain durable credentials.
