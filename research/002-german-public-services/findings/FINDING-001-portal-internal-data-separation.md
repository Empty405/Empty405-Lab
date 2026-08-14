# FINDING-001 — Separation Between Portal Data and Internal BA Procedures

## Status

DOCUMENTED ARCHITECTURAL OBSERVATION

## Source

BA-003 — Bundesagentur für Arbeit Datenschutzerklärung

Archived SHA256:
6cbc4ad64819759cd513b100e8cd16b650595b9d27d6fab8875617058c02c4d0

## Observation

The Bundesagentur für Arbeit explicitly distinguishes between:

1. online data associated with the user portal/account; and
2. data stored in non-online internal BA systems ("interne Fachverfahren").

The privacy documentation states that deletion of the user account results in
deletion of associated online data, including examples such as:

- Registrierungsdaten
- Profildaten
- Bescheidablage
- Antragsübersicht
- Postfachservice

Portal deletion is stated to occur within 21 days.

The same documentation separately states that data stored in non-online BA
systems ("interne Fachverfahren") remains stored according to applicable legal
retention and archival periods.

## Established

The user-facing portal data layer and internal BA administrative systems are
not identical data stores.

## Not established

This finding does not establish:

- how individual Postfach messages are transferred into internal systems;
- whether every message is copied into an administrative file;
- whether historical messages remain visible after a departmental transfer;
- whether records are lost during a Zuständigkeitswechsel;
- whether a security vulnerability exists.

## Security relevance

Potentially relevant properties:

- traceability
- record provenance
- administrative consistency
- availability of historical information
- auditability

## Research questions

1. What event transfers a Postfach message into an internal Fachverfahren?
2. Is the original message preserved, copied, referenced or transformed?
3. Is there a persistent identifier linking portal and internal records?
4. What happens after a Zuständigkeitswechsel?
5. Which organisational units can access historical records?
6. What audit trail exists for routing and access?
7. Can a user reconstruct the same record history visible internally?

## Confidence

High for the existence of separate online and internal data layers.

Unassessed for their detailed synchronization and routing behavior.
