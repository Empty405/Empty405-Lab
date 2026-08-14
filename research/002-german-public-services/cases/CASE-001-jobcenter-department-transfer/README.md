# CASE-001 — Jobcenter Department Transfer and Historical Communication Visibility

## Status

OBSERVATION

## Date first observed

2026-08-14

## Research area

- Jobcenter
- jobcenter.digital
- departmental responsibility
- administrative records
- communication history
- data availability
- traceability
- access control

## Observation

During an appointment following a change of administrative responsibility,
a Jobcenter employee stated that previous communications/materials were not
visible to her.

The observation occurred in the context of a transfer between administrative
areas / responsibilities.

## What is established

At least one employee in the new administrative context did not have visible
access to at least part of the previous communication or submitted material.

## What is NOT established

This observation does not currently prove that:

- the previous records were deleted;
- the records were lost;
- the records were absent from the eAkte;
- another department could not access them;
- Jobcenter systems failed to transfer the records;
- all Jobcenter transfers behave in the same way;
- a security vulnerability exists.

## Initial hypotheses

### H1 — Access-control boundary

The historical records still exist but are not accessible to the employee
because of departmental access permissions.

### H2 — Separate administrative context

A change of responsibility creates or exposes a different record context,
while older records remain stored elsewhere.

### H3 — Routing / synchronization issue

Historical communications exist but were not correctly associated with the
new administrative context.

### H4 — Interface limitation

The backend contains the records, but the employee-facing interface does not
display them in the current workflow.

### H5 — Record-transfer failure

Some historical information was not successfully transferred.

This hypothesis requires substantially stronger evidence.

## Security properties potentially affected

- Availability
- Integrity
- Traceability
- Accountability
- Administrative consistency

## Potential risk

If relevant historical communication is unavailable to an authorized employee,
administrative decisions could potentially be made without complete case
context.

This is currently a research hypothesis, not a confirmed systemic risk.

## Evidence required

- official documentation about Jobcenter record transfer;
- documentation concerning eAkte and jobcenter.digital message routing;
- retention rules;
- access-control rules between organisational units;
- information about Zuständigkeitswechsel;
- information about U25 / Ü25 transitions where applicable;
- first-party access request / Akteneinsicht where appropriate;
- written clarification from relevant institutions;
- comparison with additional cases.

## Next steps

1. Map the documented data flow.
2. Identify applicable legislation and administrative rules.
3. Collect official technical/privacy documentation.
4. Formulate neutral clarification requests.
5. Compare institutional responses.
6. Test alternative explanations.
7. Reassess the finding status.

## Current confidence

Low.

There is a concrete observation, but insufficient evidence to determine its
technical or organisational cause.
