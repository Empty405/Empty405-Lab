# A3 Architecture

## Components

```text
request + proposed response
          │
          ▼
  Sensitivity Adapter
          │ disclosure event
          ▼
    Exposure Ledger
          │ exposure snapshot
          ▼
 Precision Controller ──▶ Disclosure Transformer
          │                         │
          ▼                         ▼
 decision metadata           transformed response
          └──────────────┬──────────┘
                         ▼
                 Provenance Envelope
```

## Sensitivity adapter

Maps a tool projection to:

- affected coverage keys;
- sensitivity class;
- supported precision levels;
- task requirements;
- transformation functions.

Unknown mappings cannot default to full precision.

## Exposure ledger

Consumes normalized events from A2. A3 initially uses exact precision-weighted coverage and a stable single principal.

## Precision controller

A state machine selects the maximum allowed precision.

Example thresholds:

| Exposure | Maximum level |
|---:|---|
| 0–0.20 | L0 exact |
| >0.20–0.40 | L1 narrow range |
| >0.40–0.60 | L2 broad range |
| >0.60–0.75 | L3 category |
| >0.75–0.90 | L4 aggregate |
| >0.90 | L5 unavailable |

Thresholds are experimental parameters, not recommendations.

## Hysteresis

A small hysteresis margin prevents the response level from oscillating when exposure lies near a boundary. Within a static epoch, precision can only stay equal or degrade. Recovery belongs to C6/E3.

## Disclosure transformer

Transformations must be deterministic and nested:

```text
exact value ⊆ narrow range ⊆ broad range ⊆ category
```

Two responses at the same or lower precision must not intersect into a narrower set than the declared level.

## Provenance envelope

```json
{
  "value": "high",
  "disclosure": {
    "level": "L3",
    "precision": "category",
    "freshness_epoch": "epoch-1",
    "transformed": true,
    "synthetic": false,
    "reason": "cumulative-exposure",
    "policy_version": "A3-v0.1"
  }
}
```

## Failures

- unsupported transformation → deny with reason;
- missing exposure state → conservative configured level;
- stale ledger → no precision upgrade;
- malformed provenance → response is not released;
- unknown projection → explicit unmapped policy.

## Trust boundaries

The client cannot select its precision level or edit provenance. The transformer may read the proposed response but not observer memory. The reference observer exists only in experiments and cannot influence enforcement.
