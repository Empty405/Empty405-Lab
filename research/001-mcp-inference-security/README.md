# MCP Inference Security

> Controlling longitudinal and cross-tool information leakage in agentic systems.

**Status:** Early Research / Open for Criticism  
**Project:** Empty405 Lab  
**Version:** 0.1

---

## Problem

Access control answers an important question:

> Is this user or agent allowed to access this resource?

However, an agentic system can potentially collect many individually permitted pieces of information across repeated queries, tools, data sources, and time.

The security problem may therefore extend beyond individual authorization decisions.

A second question appears:

> What can an agent infer from the cumulative information that the system has released?

This research explores whether modern MCP-based systems need additional mechanisms for reasoning about cumulative information exposure.

---

## Why It Matters

A single response may reveal very little.

A sequence of legitimate responses may reveal substantially more.

For example, an agent could repeatedly query information about:

- locations;
- inventory;
- availability;
- timestamps;
- resource states;
- operational changes.

Each response may be individually harmless and properly authorized.

But correlations across these responses could potentially reveal patterns that were never explicitly exposed by any single tool call.

This becomes more important when AI agents can automatically collect, store, correlate, and analyze information at a scale that would be inconvenient for a human operator.

---

## Core Hypothesis

MCP security currently focuses heavily on protecting individual resources, tools, credentials, and authorization boundaries.

This research investigates an additional layer:

**inference-aware information control.**

The working hypothesis is:

> Agentic systems may require security controls that reason not only about what a principal can access, but also about what that principal can infer from cumulative information released across resources, tools, time, and potentially multiple MCP servers.

For this research, this potential class of exposure is referred to as:

**Agentic Mosaic Inference.**

This is currently a working term, not a proposed official MCP security category.

---

## Example

Consider a hypothetical MCP-enabled retail or logistics network.

An external agent cannot directly request:

> "Show me the operational state of the entire network."

However, it may be permitted to ask legitimate questions such as:

- Is product X available at location A?
- Is product X available at location B?
- When was availability updated?
- Which nearby locations currently provide the same resource?

One answer may reveal almost nothing.

Thousands of observations collected over time could potentially reconstruct:

- supply patterns;
- regional demand anomalies;
- resource shortages;
- operational rhythms;
- relationships between locations.

The security concern is therefore not necessarily unauthorized access.

The concern is **authorized observations producing unintended aggregate knowledge**.

---

## Existing Controls

Several existing security and privacy mechanisms are relevant to this problem, including:

- authentication;
- authorization;
- rate limiting;
- access scopes;
- data minimization;
- aggregation;
- caching policies;
- anomaly detection;
- privacy-preserving data release;
- differential privacy.

This project does **not** assume that MCP currently has no security mechanisms.

The research question is narrower:

> Are existing controls sufficient when autonomous agents can perform longitudinal and cross-tool information aggregation?

---

## What May Be Missing

A possible missing abstraction is a mechanism for tracking or limiting cumulative information exposure.

Instead of considering only:

`request → authorization → response`

a system could potentially consider:

`request + previous disclosures + context → disclosure decision`

Possible dimensions include:

- query coverage;
- temporal precision;
- spatial precision;
- resource coverage;
- repeated observations;
- cross-tool correlation.

The goal would not necessarily be to block access.

The system could instead progressively reduce the precision of information being disclosed.

---

## Possible Directions

Several mechanisms are worth investigating.

### 1. Inference-Aware Query Budgets

Track approximate coverage of sensitive parameter spaces rather than only requests per second.

For example:

`location × resource × time window`

A client approaching excessive coverage could receive increasingly aggregated information.

### 2. Progressive Precision Degradation

Responses could move through levels such as:

`exact → bucketed → aggregated → delayed → unavailable`

depending on trust level and cumulative exposure.

### 3. Deterministic Epoch Bucketing

Anonymous or low-trust clients could receive stable aggregated snapshots within defined time epochs.

This may reduce longitudinal precision while preserving cacheability.

### 4. Lightweight Exposure Accounting

Full historical query graphs may be too expensive.

Approximate structures such as counters, sketches, or probabilistic data structures could potentially provide cheaper exposure accounting.

### 5. Policy Presets

Security mechanisms should not require every MCP developer to become a privacy researcher.

Possible profiles could include:

- `standard`
- `privacy-first`
- `sensitive-infrastructure`

### 6. Provenance for Modified Responses

If information is aggregated, delayed, degraded, or synthetic, downstream systems need a way to distinguish it from authoritative ground-truth data.

This is particularly important for agents, caches, analytics systems, and RAG pipelines.

---

## Controlled Deception

Synthetic responses and defensive data manipulation are an interesting but significantly more controversial direction.

Naive random falsehoods could:

- poison legitimate analytics;
- contaminate caches;
- corrupt RAG systems;
- create safety problems;
- reduce trust in the underlying service.

Therefore, this project does **not** currently propose indiscriminate false-data injection as a default mechanism.

If synthetic defensive responses are investigated, they should require strict provenance, isolation, policy controls, and clearly defined threat models.

Aggregation and precision reduction should generally be investigated before deception.

---

## Open Questions

This research currently leaves several important questions unresolved:

1. How should cumulative information gain be measured?

2. Can useful exposure accounting be implemented without storing complete query histories?

3. How should identity rotation and Sybil behavior affect inference budgets?

4. How should exposure be coordinated across independent MCP servers?

5. What latency and storage overhead would these controls introduce?

6. How can adaptive disclosure remain compatible with CDN and edge caching?

7. Which protections belong in MCP standards or SDKs, and which should remain application-specific?

8. How should modified or synthetic responses propagate provenance to downstream agents?

9. Where is the boundary between legitimate privacy protection and harmful data deception?

10. Which parts of this problem are already adequately addressed by existing privacy and API-security research?

---

## Research Direction

The next stage is not implementation.

The next stage is validation.

This project should first compare the hypothesis against:

- current MCP security architecture;
- existing API security practices;
- differential privacy research;
- inference-control research;
- traffic-analysis defenses;
- anti-enumeration techniques;
- privacy budgeting;
- related work in distributed systems.

Only after that comparison should the project determine whether a genuinely MCP-specific security primitive is justified.

---

## Contributions

Criticism is explicitly welcome.

Especially useful contributions include:

- prior research solving the same problem;
- examples showing that existing MCP mechanisms already address it;
- counterexamples to the threat model;
- better terminology;
- practical implementation constraints;
- alternative architectures;
- small experiments measuring cumulative information leakage.

The objective is not to prove this proposal correct.

The objective is to determine which parts survive scrutiny.

---

## Current Status

**Stage:** Hypothesis formation  
**Implementation:** None  
**Specification:** None  
**Security guarantee:** None  
**Open for review:** Yes

---

*Start empty. Ask strange questions. Build what survives.*
