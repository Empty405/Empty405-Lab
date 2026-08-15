# A2 Architecture

## Objective

Separate tool-specific extraction from generic cumulative accounting.

```text
MCP response
    │
    ▼
Disclosure Adapter ──▶ normalized DisclosureEvent
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
            Tuple Ledger  Marginal Ledger  Weighted Ledger
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                       Exposure Snapshot
                              │
                              ▼
                     Metrics / future policy
```

## 1. Disclosure Adapter

Each experimental tool declares how its response maps to structural dimensions. The adapter must not read the hidden state.

Input:

```json
{
  "principal": "observer-0",
  "tool": "capacity_band",
  "arguments": {"location": "north", "resource": "fuel"},
  "response": {"band": "high"},
  "epoch": "epoch-1"
}
```

Output:

```json
{
  "principal": "observer-0",
  "epoch": "epoch-1",
  "dimensions": {"location": "north", "resource": "fuel"},
  "projection": "capacity_band",
  "precision": 0.33,
  "coverage_keys": ["epoch-1:north:fuel"]
}
```

## 2. Event contract

Required fields:

- stable principal supplied by the experiment;
- logical epoch;
- tool and projection identifiers;
- canonical dimension names and values;
- exact coverage keys;
- declared precision weight;
- source query and response identifiers.

The event describes what the server released, not what the observer actually understood.

## 3. Ledgers

### Request ledger

Counts released responses. Baseline comparator only.

### Tuple ledger

Stores unique canonical dimension tuples.

### Marginal ledger

Separately records coverage of each dimension and pairwise combinations. It can detect broad enumeration even when full tuples remain sparse.

### Precision-weighted ledger

Accumulates the maximum declared precision for each coverage key rather than summing repeated disclosures:

```text
exposure(key) = max(previous_precision, released_precision)
```

This prevents identical repeats from consuming exposure repeatedly while allowing a later more precise response to increase exposure.

### Reference interval ledger

Used only in the experiment. It applies tool responses to candidate intervals and measures actual width reduction. A real gateway would not know the observer's complete prior or reasoning state.

## 4. Exposure snapshot

A snapshot contains raw counts and normalized values in `[0, 1]`:

```json
{
  "request_count": 42,
  "tuple_coverage": 0.31,
  "marginal_coverage": 0.67,
  "weighted_coverage": 0.22
}
```

No single scalar is declared authoritative before the experiment.

## 5. Trust boundaries

- tool adapters are trusted policy configuration;
- client-provided coverage metadata is never trusted;
- ledgers cannot read observer memory;
- the reference interval ledger cannot influence enforcement;
- metrics consume immutable disclosure events;
- results retain adapter and configuration hashes.

## 6. Failure behavior

Unknown tools or missing mappings must be explicit:

- `unmapped-deny`;
- `unmapped-conservative`;
- `unmapped-observe-only`.

Silently treating an unmapped response as zero exposure is forbidden.

## Extension points

D2/D4 may replace declared mappings with semantic equivalence models. J2/J3 may replace exact sets with sketches and distributed state. Neither extension is part of A2.
