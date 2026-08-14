# WAVE-001 — Berlin Jobcenter Comparative Pilot

## Status

READY FOR MANUAL SEND

## Date prepared

2026-08-14

## Request template

REQ-003 — Standardisierte Vergleichsanfrage

## Institutions

1. Jobcenter Berlin Friedrichshain-Kreuzberg
2. Jobcenter Berlin Mitte
3. Jobcenter Berlin Treptow-Köpenick

## Primary channel

jobcenter.digital / Postfachservice

Using the same channel is preferred so that response-time comparisons remain
methodologically meaningful.

## Experimental rule

The eight core questions in REQ-003 must remain identical for all three
institutions.

Only institution-specific addressing may differ.

## Measurement

Immediately after each successful send:

    ./scripts/request-tracker.py sent CMP-XXX jobcenter.digital

Record automatic acknowledgements separately:

    ./scripts/request-tracker.py ack CMP-XXX

## Evidence preservation

For every sent request preserve privately:

- exact submitted text
- submission confirmation
- timestamp
- screenshots or exported confirmation where available
- eventual responses

Do not commit personal account identifiers, BG numbers, Kundennummer or
unredacted personal correspondence to the public repository.

## Pilot purpose

This wave tests:

- routing behavior
- response speed
- response completeness
- legal grounding
- source transparency
- consistency between Jobcenter offices
- treatment of questions concerning historical communication and language access

No inference of corruption or discrimination will be made from one response
or from response time alone.
