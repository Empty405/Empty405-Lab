# Related Work

> Prior art and adjacent research relevant to MCP Inference Security.

**Status:** Active Research  
**Version:** 0.1  
**Last reviewed:** 2026-08-13

---

## Purpose

This document tracks existing work related to the hypothesis described in
`README.md`.

The objective is not to prove that MCP requires a new security mechanism.

The objective is to determine:

1. which parts of the problem are already understood;
2. which existing mechanisms can be reused;
3. which parts may be specific to agentic and MCP environments;
4. whether any genuinely useful gap remains.

---

# 1. MCP Authorization

## Existing Work

The current MCP authorization specification provides transport-level
authorization for HTTP-based MCP servers.

It is based primarily on OAuth 2.1 and related standards.

Current security considerations include areas such as:

- token audience validation;
- token theft;
- authorization-code protection;
- confused-deputy attacks;
- redirect security;
- privilege restriction.

## What It Solves

This provides an answer to questions such as:

> Is this principal authorized to access this protected MCP server or resource?

It establishes important identity and authorization boundaries.

## Relation to Our Hypothesis

Authorization and cumulative inference are not necessarily the same problem.

A principal may be correctly authenticated and correctly authorized for every
individual request while still potentially learning unintended information by
combining many permitted responses.

Therefore:

**Authorization is a prerequisite, but may not by itself constitute inference control.**

## Current Assessment

**Known / Existing**

MCP already has substantial authorization architecture.

The research should not present inference-aware disclosure as a replacement for
OAuth, scopes, or access control.

---

# 2. MCP Trust Model

Official MCP security documentation defines explicit trust assumptions between
clients, servers, execution environments, developers, operators, and users.

Server developers are responsible for implementing appropriate access controls.

Client developers are responsible for consent, visibility, and appropriate
handling of server capabilities.

## Relation to Our Hypothesis

This suggests an important architectural question:

> Is cumulative disclosure an MCP protocol concern, a server implementation
> concern, a gateway concern, or an application policy concern?

This question is currently unresolved.

A mechanism should not be proposed at protocol level unless there is evidence
that application-level controls are insufficient or unnecessarily fragmented.

---

# 3. Stateless MCP and Gateway Enforcement

MCP 2026-07-28 introduced a stateless protocol core.

Requests carry information that allows infrastructure such as gateways, rate
limiters, and WAFs to meter and route MCP traffic without requiring the previous
session architecture.

## Relation to Our Hypothesis

This is highly relevant.

Inference-aware accounting does not necessarily need to live inside every MCP
server.

A gateway could potentially maintain external disclosure state while MCP itself
remains stateless.

Conceptually:

client
  ↓
MCP request
  ↓
inference-aware gateway
  ↓
MCP server

The gateway could potentially evaluate:

- caller identity;
- requested tool;
- requested resource;
- parameter-space coverage;
- previous disclosure counters;
- policy.

## Current Assessment

**Potential implementation location**

The new stateless MCP architecture may actually make gateway-based experimentation
easier.

---

# 4. MCP Trust and Provenance Metadata

Previous MCP community proposals have explored trust and sensitivity annotations
for data moving through MCP systems.

These proposals include concepts such as:

- sensitivity metadata;
- provenance;
- trust propagation;
- policy enforcement.

## Relation to Our Hypothesis

This overlaps with our proposed provenance requirement.

Therefore, provenance metadata should NOT currently be presented as a novel idea
of this project.

A more specific research question is:

> Could existing or future MCP metadata also communicate disclosure properties
> such as aggregation, precision reduction, freshness, or synthetic origin?

## Current Assessment

**Partially overlapping prior work exists.**

Further investigation is required before proposing new metadata.

---

# 5. Statistical Database Inference Control

The general inference problem substantially predates MCP and modern AI agents.

Statistical database research has long studied situations where individually
acceptable aggregate queries can be combined to infer protected information.

This field includes mechanisms known broadly as:

**inference control**

and

**query auditing**.

Some approaches evaluate previous query responses before deciding whether a new
query can safely be answered.

## Relation to Our Hypothesis

This is extremely important.

The core concept:

> many individually acceptable responses can collectively disclose protected
> information

is NOT new.

Therefore, "Agentic Mosaic Inference" should currently be treated as a working
description of an agentic manifestation of an established inference-control
problem, not as the discovery of an entirely new security principle.

## Current Assessment

**Strong prior art exists.**

Our research must build on this literature rather than reinvent it.

---

# 6. Query Auditing

Historical statistical-database research includes systems that audit sequences
of queries to determine whether additional responses could create unacceptable
information disclosure.

Some research also demonstrates a subtle problem:

> refusing a query can itself reveal information.

This is directly relevant to our earlier discussion about hard blocking.

However, this does NOT automatically justify returning false information.

It demonstrates only that disclosure decisions themselves can sometimes become
observable signals.

## Relation to Our Hypothesis

Our proposed "inference-aware query budget" appears conceptually related to
historical query auditing.

The potentially new engineering question is whether simplified forms of this
idea are useful for modern agent/tool environments.

---

# 7. Differential Privacy

Differential privacy provides formal mechanisms for limiting information leakage
from statistical outputs.

A central concept is the privacy-loss budget.

Repeated queries consume privacy budget, and composition matters.

## Relation to Our Hypothesis

This strongly overlaps with the intuitive idea behind an "inference budget."

Therefore we should NOT invent a new mathematical framework before determining
whether differential privacy or related privacy-accounting methods already solve
the required problem.

However, MCP tool calls may include:

- non-statistical data;
- structured resources;
- operational state;
- heterogeneous tools;
- exact business data.

Differential privacy may therefore be highly relevant without being a complete
drop-in solution.

## Current Assessment

**Existing formal foundation worth studying.**

---

# 8. Precision Reduction

Existing privacy and statistical-security research includes mechanisms that
reduce the precision of released information.

Examples include:

- aggregation;
- rounding;
- bucketing;
- noise;
- range responses.

## Relation to Our Hypothesis

Our proposed:

exact → bucketed → aggregated → delayed

model is therefore best viewed as an engineering composition of established
privacy ideas rather than a fundamentally new primitive.

The MCP-specific question is whether a standardized way to express such
disclosure levels would improve interoperability.

---

# 9. Preliminary Gap

After the first related-work pass, the broad inference problem is clearly not new.

Several components already have substantial prior art:

KNOWN:
- authentication;
- authorization;
- rate limiting;
- query auditing;
- inference control;
- differential privacy;
- privacy budgets;
- aggregation;
- precision reduction;
- provenance concepts.

The potentially interesting area is narrower.

## Possible MCP / Agentic Gap

Modern AI agents can automatically:

- enumerate tools;
- perform repeated queries;
- correlate heterogeneous responses;
- retain observations;
- combine information across tools;
- potentially combine information across independent MCP servers.

The preliminary research question therefore becomes:

> Do agentic MCP environments need a lightweight, interoperable mechanism for
> cumulative disclosure accounting across heterogeneous tool and resource calls?

Possible sub-problems include:

1. cross-tool disclosure accounting;
2. heterogeneous parameter-space coverage;
3. disclosure metadata;
4. gateway-level enforcement;
5. cross-server coordination;
6. interaction with stateless MCP infrastructure.

This is currently a **research question**, not a claimed protocol vulnerability.

---

# 10. What We Have Learned So Far

The original idea has already changed.

Initial intuition:

> Prevent hostile agents from reconstructing operational information by
> manipulating responses.

Current research direction:

> Investigate whether established inference-control and privacy-accounting
> techniques require new integration primitives for agentic MCP environments.

This is a narrower and more defensible question.

---

# Next Research Pass

Investigate:

- modern inference-control literature;
- differential privacy composition;
- API enumeration defenses;
- privacy-preserving telemetry;
- agent memory and cross-tool correlation;
- MCP gateway architectures;
- existing MCP security extensions;
- information-flow control;
- provenance standards.

Then classify every proposed mechanism as:

**Existing → Adaptable → Potential Gap → Unsupported**

---

*Research should become smaller as uncertainty disappears.*

---

# References

## MCP Specification and Security

1. **Model Context Protocol Specification — 2026-07-28**  
   Model Context Protocol.  
   Official specification defining the current MCP protocol architecture.  
   https://modelcontextprotocol.io/specification/2026-07-28

2. **MCP Authorization — 2026-07-28**  
   Model Context Protocol.  
   Defines authorization for protected MCP servers using OAuth 2.1 resource-server and client roles.  
   https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

3. **MCP Authorization Security Considerations — 2026-07-28**  
   Model Context Protocol.  
   Covers token validation, audience restrictions, and related authorization security requirements.  
   https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations

4. **MCP Security Best Practices**  
   Model Context Protocol.  
   Security guidance covering implementation risks, authorization flows, token handling, traffic controls, and related MCP-specific attack surfaces.  
   https://modelcontextprotocol.io/specification/draft/basic/security_best_practices

5. **MCP Tools — Security Considerations**  
   Model Context Protocol.  
   Specifies that servers should validate tool inputs, implement access controls, rate-limit tool invocations, and sanitize outputs.  
   https://modelcontextprotocol.io/specification/2026-07-28/server/tools

6. **The 2026-07-28 MCP Specification**  
   Model Context Protocol Blog, 28 July 2026.  
   Describes the move toward a stateless, cacheable, routable MCP core suitable for ordinary web infrastructure.  
   https://blog.modelcontextprotocol.io/posts/2026-07-28/

7. **MCP 2026-07-28 Changelog**  
   Model Context Protocol.  
   Documents the stateless protocol redesign and request-level metadata changes.  
   https://modelcontextprotocol.io/specification/2026-07-28/changelog

---

## MCP Trust, Sensitivity, and Policy Work

8. **Annotations for MCP Requests and Responses**  
   Model Context Protocol GitHub Issue #711.  
   Proposal for trust, sensitivity, attribution, and provenance metadata in MCP data flows.  
   https://github.com/modelcontextprotocol/modelcontextprotocol/issues/711

9. **SEP-1487: Addition of `trustedHint` Tool Annotation**  
   Model Context Protocol GitHub.  
   Proposal for explicit trust metadata associated with MCP tools.  
   https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1487

10. **SEP-1763: Interceptors for Model Context Protocol**  
    Model Context Protocol GitHub.  
    Proposal for intercepting, validating, and transforming MCP messages across protocol lifecycle events.  
    https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1763

11. **Portable Execution Records for Multi-Step MCP Workflows**  
    Model Context Protocol Discussion #2493.  
    Discussion touching on auditability, trust annotations, sensitivity, attribution, and multi-step agent execution history.  
    https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2493

---

## Differential Privacy

12. **NIST SP 800-226 — Guidelines for Evaluating Differential Privacy Guarantees**  
    National Institute of Standards and Technology, 2025.  
    Formal guidance on evaluating differential privacy guarantees, including privacy-loss composition across multiple releases.  
    https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf

13. **Differential Privacy for Privacy-Preserving Data Analysis**  
    National Institute of Standards and Technology, 2020.  
    Introductory explanation of differential privacy, including composition across multiple analyses.  
    https://www.nist.gov/blogs/cybersecurity-insights/differential-privacy-privacy-preserving-data-analysis-introduction-our

14. **Automatic Proofs of Differential Privacy**  
    National Institute of Standards and Technology, 2021.  
    Discusses sequential composition, adaptive settings, privacy filters, and privacy odometers.  
    https://www.nist.gov/blogs/cybersecurity-insights/automatic-proofs-differential-privacy

15. **The Composition Theorem for Differential Privacy**  
    Peter Kairouz, Sewoong Oh, Pramod Viswanath.  
    arXiv:1311.0776, 2013.  
    Studies how sequential querying degrades overall privacy guarantees under differential privacy.  
    https://arxiv.org/abs/1311.0776

---

## Query Auditing and Inference Control

16. **Towards Robustness in Query Auditing**  
    Shubha U. Nabar et al.  
    VLDB, 2006.  
    Studies online query auditing for statistical databases and the problem of preventing disclosure from streams of aggregate queries.  
    https://www.vldb.org/conf/2006/p151-nabar.pdf

17. **A Survey of Query Auditing Techniques for Data Privacy**  
    Shubha U. Nabar et al.  
    Survey of techniques for detecting and preventing information disclosure through sequences of database queries.  
    https://theory.stanford.edu/~nmishra/Papers/surveyQueryAuditingTechniquesDataPrivacy.pdf

18. **An Efficient Online Auditing Approach to Limit Private Data Disclosure**  
    H. Lu et al., 2009.  
    Describes online auditing where disclosure can occur when users combine answers from past queries.  
    https://openproceedings.org/2009/conf/edbt/LuLAV09.pdf

19. **Statistical Database Auditing Without Query Denial Threat**  
    H. Lu, 2014.  
    Studies the fact that query denial itself may leak information and proposes accounting for information leaked by both answered and denied queries.  
    https://ink.library.smu.edu.sg/sis_research/2550/

20. **Efficient Inference Control for Range Sum Queries**  
    F. Y. Chin, 1984.  
    Early work on auditing answered queries to determine whether a new query could compromise protected information, while noting substantial time and storage overhead.  
    https://www.sciencedirect.com/science/article/pii/0304397584900252

---

## Additional Relevant Research

21. **Query Monitoring and Analysis for Database Privacy**  
    A. Kumar et al., 2015.  
    Proposes a security-automata architecture that monitors input queries and outputs to enforce privacy and usage policies.  
    https://pmc.ncbi.nlm.nih.gov/articles/PMC4795904/

22. **Database Queries that Explain their Work**  
    James Cheney, Amal Ahmed, Umut A. Acar, 2014.  
    Research on provenance and traceability for database queries and scientific workflows.  
    https://arxiv.org/abs/1408.1675

---

# Current Interpretation of Prior Art

The current evidence suggests:

**Established concepts**
- inference control;
- query auditing;
- cumulative disclosure;
- privacy-budget composition;
- precision reduction;
- provenance;
- trust annotations;
- rate limiting;
- authorization.

**Potentially adaptable concepts**
- privacy accounting;
- online query auditing;
- progressive disclosure reduction;
- provenance metadata;
- gateway enforcement.

**Potentially MCP-specific research area**
- cumulative disclosure across heterogeneous MCP tools;
- cross-tool and cross-server information composition;
- lightweight exposure accounting for agentic workflows;
- interoperable disclosure metadata;
- policy enforcement at MCP gateway or host level.

At this stage, the project should not claim discovery of a new fundamental security principle.

The potentially novel contribution, if any, is likely to be found in the **integration, abstraction, and engineering of existing inference-control ideas for heterogeneous agentic MCP environments**.
