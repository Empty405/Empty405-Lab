# Gap Analysis

> Distinguishing established security concepts from potentially MCP-specific engineering gaps.

**Status:** Working Analysis  
**Version:** 0.1  
**Project:** Empty405 Lab

---

## Purpose

This document evaluates the main claims from the MCP Inference Security hypothesis against the related work already identified.

The objective is to avoid presenting established privacy or security concepts as new discoveries.

Each claim is classified according to:

- existing solution;
- current coverage;
- remaining gap;
- confidence;
- next validation step.

---

# Claim 1 — Legitimate Queries Can Create Cumulative Disclosure

## Claim

A sequence of individually legitimate MCP requests may collectively reveal information that no single request exposes.

## Existing Solutions

Relevant established fields include:

- statistical database inference control;
- query auditing;
- differential privacy;
- privacy accounting;
- access-pattern analysis.

## Coverage

**High**

The general security principle is well established.

The project should not claim that cumulative disclosure itself is a new discovery.

## Remaining Gap

The open question is whether heterogeneous MCP tool calls create implementation problems that existing query-auditing systems do not conveniently address.

Examples:

- different tools expose different schemas;
- one agent may query several independent servers;
- tool semantics may change dynamically;
- observations may be retained in agent memory.

## Confidence

**High** that the general problem exists.

**Low/Medium** that MCP requires a new primitive.

## Next Test

Model cumulative information collection across several simulated MCP tools and determine whether traditional per-endpoint controls meaningfully limit the resulting coverage.

---

# Claim 2 — Rate Limiting Is Not Equivalent to Inference Control

## Claim

Requests-per-second limits may prevent abuse without preventing slow longitudinal collection.

## Existing Solutions

Relevant mechanisms include:

- rate limiting;
- query quotas;
- anti-enumeration controls;
- query auditing;
- privacy budgets;
- anomaly detection.

## Coverage

**Medium/High**

The limitation of simple rate limiting is not new.

A sufficiently patient observer can remain below ordinary traffic thresholds.

## Remaining Gap

MCP gateways may benefit from semantic accounting based on what is being queried rather than only how frequently requests occur.

Possible example:

```text
requests per minute
```

versus:

```text
percentage of location × resource × time space observed
```

## Confidence

**High** that ordinary rate limits do not measure information exposure.

**Medium** that parameter-space coverage is a useful practical replacement.

## Next Test

Compare:

1. standard request-rate limits;
2. fixed daily quotas;
3. parameter-space coverage limits.

Measure how much operational state an observer reconstructs under each model.

---

# Claim 3 — An Inference Budget Could Be Useful

## Claim

A system may benefit from tracking approximate cumulative exposure rather than only request counts.

## Existing Solutions

Strong conceptual overlap exists with:

- privacy budgets;
- differential privacy composition;
- query auditing;
- disclosure-control systems.

## Coverage

**Medium**

The mathematical concept of cumulative privacy accounting already exists.

The difficult part is applying it to heterogeneous, non-statistical MCP tool outputs.

## Remaining Gap

A practical MCP-oriented abstraction may need to account for:

- tool identity;
- resource identity;
- parameter combinations;
- time windows;
- geographic coverage;
- precision of returned data.

It is not yet clear whether these dimensions can be reduced to a useful generic score.

## Confidence

**Medium**

The idea appears technically plausible, but the metric remains undefined.

## Next Test

Avoid semantic "knowledge measurement" initially.

Use structural coverage as a proxy:

```text
coverage =
observed_parameter_combinations /
possible_parameter_combinations
```

Then test whether this correlates with actual reconstruction capability.

---

# Claim 4 — Progressive Disclosure May Be More Useful Than Binary Denial

## Claim

Instead of only:

```text
ALLOW / DENY
```

a server or gateway could support:

```text
EXACT
BUCKETED
AGGREGATED
DELAYED
DENY
```

## Existing Solutions

Similar concepts already exist in:

- data minimization;
- aggregation;
- precision reduction;
- statistical disclosure control;
- differential privacy;
- access-tier systems.

## Coverage

**High** at the general privacy level.

The concept itself is not new.

## Remaining Gap

Potential value may exist in standardizing how an MCP server or gateway represents disclosure levels.

Possible dimensions:

- precision;
- freshness;
- spatial resolution;
- historical depth.

## Confidence

**Medium**

Useful as an engineering pattern.

Unclear whether it belongs in MCP itself.

## Next Test

Implement the same MCP tool under several disclosure modes and measure:

- usefulness to legitimate clients;
- information available to observers;
- caching behavior;
- implementation complexity.

---

# Claim 5 — MCP Gateways May Be a Practical Enforcement Layer

## Claim

Inference-aware policies may be easier to implement in an MCP gateway than independently inside every MCP server.

## Existing Solutions

Gateways already commonly provide:

- authentication;
- authorization;
- logging;
- rate limiting;
- request transformation;
- policy enforcement.

## Coverage

**Medium**

Gateway enforcement is an established architecture.

The MCP-specific question concerns which semantic information the gateway needs.

## Remaining Gap

A useful gateway may need visibility into:

- tool names;
- resource types;
- parameters;
- disclosure classes;
- caller identity;
- accumulated coverage.

This may require metadata or conventions beyond ordinary network-level rate limiting.

## Confidence

**Medium/High**

This currently appears to be one of the strongest practical directions for experimentation.

## Next Test

Build a minimal gateway in front of a toy MCP server.

Do not begin with AI or synthetic deception.

Implement only:

1. request classification;
2. coverage counter;
3. disclosure policy;
4. response degradation.

---

# Claim 6 — Cross-Tool Correlation May Create an Agent-Specific Problem

## Claim

AI agents can combine outputs from heterogeneous tools more easily than traditional single-API clients.

Example:

```text
inventory tool
+
transport tool
+
weather tool
+
energy tool
+
memory
=
new inference
```

## Existing Solutions

Adjacent research exists in:

- data fusion;
- information-flow control;
- inference attacks;
- privacy composition;
- database joins;
- multi-source OSINT.

## Coverage

**Medium**

Cross-source inference is not new.

However, MCP provides a common machine interface that may reduce the cost of performing this composition automatically.

## Remaining Gap

Potential MCP-specific questions include:

- how to label disclosure properties across tools;
- whether hosts should understand combinations of sensitive dimensions;
- whether independent MCP servers can coordinate exposure policies;
- whether agent memory changes practical risk.

## Confidence

**Medium**

This appears interesting but currently lacks experimental evidence.

## Next Test

Create several independently harmless toy tools.

Measure whether an agent can reconstruct a hidden state more accurately when the tools are combined.

Compare:

```text
single tool
vs
multiple tools
```

---

# Claim 7 — Provenance Is Important, But Not Novel

## Claim

Agents need to distinguish exact, delayed, aggregated, transformed, and synthetic information.

## Existing Solutions

Prior work exists in:

- data provenance;
- scientific workflows;
- database provenance;
- MCP trust and annotation proposals.

## Coverage

**High**

The general provenance problem is established.

## Remaining Gap

Potential MCP-specific value may exist in standardized metadata describing disclosure transformations.

For example:

```json
{
  "precision": "bucketed",
  "freshness": "1h",
  "synthetic": false
}
```

## Confidence

**High** that provenance matters.

**Low** that provenance itself is a novel contribution.

## Next Test

Study existing MCP annotation proposals before defining any new metadata format.

---

# Claim 8 — Controlled Deception Should Not Be the Core Proposal

## Claim

Synthetic or intentionally misleading responses could theoretically interfere with hostile collection.

## Existing Solutions

Related fields include:

- honeypots;
- deception systems;
- synthetic environments;
- moving-target defense.

## Coverage

**Medium**

Defensive deception is already a substantial security field.

## Risks

Synthetic data may:

- contaminate caches;
- poison RAG systems;
- propagate into legitimate analytics;
- create safety failures;
- be defeated through repeated sampling;
- create trust problems.

## Remaining Gap

Controlled deception may be worth testing only in isolated environments where synthetic and trusted data planes cannot mix.

## Confidence

**Low** as a default MCP mechanism.

**Medium** as an optional specialized defense.

## Next Test

Do not include deception in the first prototype.

Treat it as a separate future research branch.

---

# Gap Matrix

| Area | Existing Research Coverage | Possible MCP-Specific Gap | Confidence |
|---|---|---|---|
| Cumulative inference | High | Heterogeneous tool integration | Medium |
| Rate limiting | High | Semantic exposure accounting | Medium |
| Privacy budgeting | High | Non-statistical MCP outputs | Medium |
| Precision degradation | High | Interoperable disclosure levels | Medium |
| Gateway enforcement | High | MCP-aware semantic policy | Medium-High |
| Cross-tool correlation | Medium-High | Agent/tool composition | Medium |
| Provenance | High | Disclosure transformation metadata | Low-Medium |
| Controlled deception | High | MCP-specific isolated data plane | Low |

---

# Strongest Remaining Research Question

After the first related-work and gap-analysis passes, the broad idea can be reduced to a narrower question:

> Can lightweight structural exposure accounting and adaptive disclosure provide useful protection against cumulative cross-tool inference in heterogeneous MCP environments without requiring expensive semantic knowledge tracking?

This is significantly narrower than the original proposal.

That is desirable.

---

# Current Candidate Contribution

The strongest potential contribution is currently NOT:

> discovering cumulative inference attacks.

That field already exists.

It is also NOT:

> inventing privacy budgets, provenance, or precision reduction.

Those concepts already exist.

The potentially useful contribution may instead be:

> designing and experimentally evaluating a lightweight MCP-aware gateway that applies established inference-control ideas to heterogeneous agent tool traffic.

A possible first prototype could contain only:

```text
MCP Client
    ↓
Security Gateway
    ↓
MCP Server
```

with:

```text
request classification
+
parameter-space coverage
+
simple policy presets
+
precision degradation
+
basic provenance
```

No LLM-based security decision is required for the first prototype.

---

# Decision Gate

Before producing a full protocol proposal, the project should answer three questions experimentally.

## Test A — Does the attack matter?

Can an observer reconstruct useful hidden system state from individually permitted MCP queries?

## Test B — Does structural exposure accounting help?

Does parameter-space coverage or a similar cheap proxy detect the collection pattern better than ordinary rate limiting?

## Test C — Does adaptive disclosure preserve utility?

Can precision degradation meaningfully reduce reconstruction accuracy without making the tool useless to legitimate clients?

If the answer to these questions is mostly **no**, the project should not proceed toward a protocol proposal.

If the answers are meaningfully **yes**, a prototype and technical proposal become justified.

---

# Current Status

**General security principle:** Established  
**MCP-specific gap:** Plausible, not demonstrated  
**Novel mechanism:** Not established  
**Prototype justified:** Yes, as an experiment  
**Protocol change justified:** Not yet  
**Publication as research hypothesis:** Yes

---

# Next Phase

**Phase 4 — Minimal Experimental Design**

Design a toy environment containing:

1. one hidden operational state;
2. several MCP-accessible views of that state;
3. a passive observer;
4. standard rate limiting;
5. structural exposure accounting;
6. adaptive precision degradation.

The first experiment should answer whether the proposed gap exists in practice before additional architecture is designed.

---

*The purpose of gap analysis is not to make the idea bigger. It is to discover how small the real problem actually is.*
