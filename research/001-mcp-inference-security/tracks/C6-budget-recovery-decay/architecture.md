# C6 Architecture

## Components

- **Epoch generator** — creates requests and hidden-state versions across a fixed multi-epoch horizon.
- **Current-state ledger** — records structural units exposed for the active version.
- **Lifetime ledger** — immutable evaluator-only union of every released versioned fact.
- **Change detector** — emits none, weak, strong or verified evidence of state change.
- **Recovery policy** — no recovery, fixed-window reset, linear decay, exponential decay, version invalidation, evidence-based recovery or oracle.
- **Reconstruction evaluator** — measures current and historical reconstruction without exposing lifetime ground truth to deployable policies.

## Policy semantics

1. **No recovery** — charged exposure never returns.
2. **Fixed-window reset** — restores capacity at deterministic boundaries.
3. **Linear decay** — gradually returns charged capacity by age.
4. **Exponential decay** — discounts old charges with a fixed half-life.
5. **Version invalidation** — retires charges only for units proven obsolete in a new version.
6. **Evidence-based recovery** — restores bounded capacity proportional to verified semantic change evidence.
7. **Oracle** — evaluator-only policy restoring only capacity whose old facts no longer improve current reconstruction.

## Trust boundaries

1. External observers retain every response.
2. Clock progression cannot erase lifetime exposure.
3. Administrative reset changes policy state, not observer memory.
4. Version identifiers do not prove content invalidation.
5. Change evidence is distinct from evaluator ground truth.
6. Oracle future knowledge never enters deployable policies.

## Invariants

- lifetime released history is append-only;
- reset never deletes evaluator observations;
- identical-state version bumps restore no evidence-based capacity;
- obsolete and still-valid units are separated;
- current cap and recovered capacity reconcile exactly;
- denied requests release no units;
- duplicate current-version units cost zero;
- every request has one terminal outcome;
- policy clocks are paired across trials;
- recovery never exceeds explicitly permitted bounds.
