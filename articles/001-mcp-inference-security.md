# MCP Inference Security: Beyond Per-Request Authorization

> A toy investigation into cumulative cross-tool information exposure in agentic systems.

**Project:** Empty405 Lab  
**Research:** 001  
**Status:** Research Article / Experimental v0.1  
**Experiment:** 1000 randomized trials  
**Random seed:** `405`

---

## Abstract

Current MCP security guidance addresses authorization and a range of protocol and implementation security concerns.

However, an additional question appears when autonomous agents can repeatedly query multiple tools, retain observations, and correlate responses over time:

> What can an authorized client infer from the cumulative information released across many individually permitted requests?

This article investigates that question through a small synthetic experiment.

The work does not claim discovery of a new fundamental security principle. Cumulative disclosure, query auditing, inference control, privacy accounting, and related privacy mechanisms already have substantial prior art [1–3].

Instead, the experiment asks whether a lightweight structural exposure model may be useful in heterogeneous MCP-style tool environments.

Four modes are compared:

1. unrestricted baseline;
2. conventional rate limiting with waiting;
3. hard structural coverage limits;
4. adaptive disclosure based on cumulative structural coverage.

Across 1000 randomized trials with fixed seed `405`, the toy model produced:

| Mode | Reconstruction Score | Observable State |
|---|---:|---:|
| Baseline | 93.83% | 100.00% |
| Rate Limit + Waiting | 93.83% | 100.00% |
| Hard Coverage Policy | 52.13% | 55.56% |
| Adaptive Disclosure | 75.71% | 77.78% |

In this synthetic environment, time-based rate limiting primarily increased collection time, while structural exposure-aware controls changed the final reconstruction outcome.

The result is not evidence for an MCP vulnerability or protocol change.

It is evidence that the narrower engineering question is worth testing under harder conditions.

---

## 1. The Problem

Traditional access control asks:

> Is this client allowed to access this resource?

That question is essential.

But an agentic environment creates a second question:

> What can the client infer after combining many permitted responses?

A single response may reveal very little.

A sequence of responses may reveal considerably more.

Consider a system exposing several independent tools:

```text
Inventory Tool
Transport Tool
Availability Tool
Regional Summary Tool
Agent Memory
```

Each tool may correctly enforce authorization.

Each individual response may be considered safe.

But an automated agent can:

```text
query
→ store
→ correlate
→ query again
→ retain history
→ reconstruct patterns
```

The security concern is therefore not necessarily unauthorized access.

It may instead be:

**authorized observations producing unintended aggregate knowledge.**

---

## 2. This Is Not a New Fundamental Security Principle

The broad problem substantially predates MCP [1–3].

Relevant established research includes:

- statistical database inference control;
- query auditing;
- statistical disclosure control;
- differential privacy;
- privacy-loss accounting and composition.

Historical work on statistical database inference demonstrated that combinations and sequences of permitted queries can reveal protected information [1,2].

Differential privacy later provided formal mechanisms for reasoning about privacy loss and composition across repeated releases [3].

Therefore, this project does not claim:

> “Cumulative inference is a newly discovered MCP vulnerability.”

That claim would be incorrect.

The narrower question is:

> Do heterogeneous MCP-style tool environments create a useful engineering niche for lightweight cumulative exposure accounting and adaptive disclosure?

---

## 3. Why Agentic Tool Systems Are Interesting

Modern agents reduce the cost of information composition.

A human operator may find it inconvenient to continuously query several APIs, preserve all observations, normalize schemas, and correlate changes over time.

An agent can automate that process.

Conceptually:

```text
Tool A ─┐
Tool B ─┤
Tool C ─┼──→ Agent Memory ─→ Correlation ─→ New Inference
Tool D ─┤
Tool E ─┘
```

MCP provides a common protocol through which heterogeneous tools and resources can be exposed to agentic clients.

That does not automatically create a vulnerability.

But it may make old inference problems easier to operationalize.

---

## 4. Authorization and Inference Are Different Questions

Authorization can correctly decide:

```text
ALLOW
```

for every individual request.

The cumulative result can still be undesirable.

For example:

```text
Request 1 → allowed
Request 2 → allowed
Request 3 → allowed
...
Request 500 → allowed
```

A rate limiter may control:

> How quickly are these requests made?

But that is not the same as:

> How much distinct state has already been exposed?

This distinction became the central focus of the experiment.

---

## 5. Working Hypothesis

The research hypothesis was reduced to:

> Can lightweight structural exposure accounting and adaptive disclosure provide useful protection against cumulative cross-tool reconstruction without requiring expensive semantic knowledge tracking?

The phrase **structural exposure** is important.

The experiment does not attempt to measure how much “knowledge” an agent possesses.

That would require a much stronger semantic model.

Instead, it tracks simple structural coverage such as:

```text
location × resource
```

or, in a larger system:

```text
location × resource × time_window
```

This is deliberately crude.

The purpose is to test whether a cheap proxy is useful before designing a more complicated mechanism.

---

## 6. Toy Experimental Environment

The synthetic hidden state contains:

```text
3 locations × 3 resources = 9 hidden cells
```

Example:

```json
{
  "north": {
    "fuel": 82,
    "medical": 31,
    "food": 64
  }
}
```

The full hidden matrix contains:

```text
north
central
south
```

and:

```text
fuel
medical
food
```

The observer is not given the complete state directly.

---

## 7. Partial Information Tools

Two simplified MCP-style tools expose partial information.

### Availability Tool

Instead of returning an exact value, it returns:

```json
{
  "location": "north",
  "resource": "fuel",
  "available": true
}
```

### Capacity Band Tool

A second tool returns:

```text
low
medium
high
```

Neither tool directly returns:

```text
82
```

However, combining:

```text
available = true
+
capacity = high
```

allows an observer to estimate the hidden value.

In one example:

```text
True value:       82
Observer estimate: 84
```

This demonstrates the basic cumulative reconstruction mechanism used in the experiment.

---

## 8. Baseline Reconstruction

The baseline observer combines the two permitted outputs for all nine hidden cells.

Initial evaluation produced:

```text
Mean Absolute Error: 6.22
```

The later unified normalized benchmark produced:

```text
Reconstruction Score: 93.83%
Observable State:     100.00%
```

This establishes the unrestricted reference point.

---

## 9. Rate Limiting

A conventional time-based limiter was introduced.

The observer initially attempted 18 tool calls.

With a short-window limit:

```text
Allowed: 5
Blocked: 13
```

At first glance, this appears effective.

However, the observer was then modified to behave patiently:

```text
query
→ hit rate limit
→ wait
→ continue
```

Result:

```text
Successful queries:          18
Complete dataset collected: true
```

The limiter added approximately ten seconds in the toy configuration.

It did not change the eventual information available to the observer.

In the final randomized benchmark:

```text
Baseline reconstruction:    93.83%
Rate limit reconstruction:  93.83%

Baseline observable state:  100%
Rate limit observable state:100%
```

This does not mean rate limiting is generally ineffective.

Rate limiting protects infrastructure, controls bursts, slows abuse, and serves many other purposes.

The experiment demonstrates only that:

> Under a patient-observer model, time-based request limits do not necessarily bound cumulative information exposure.

---

## 10. Structural Coverage Accounting

The next mechanism tracks distinct:

```text
location × resource
```

combinations.

The policy allows the observer to access five unique combinations.

Repeated access to an already observed combination does not increase coverage.

Once five unique combinations have been exposed, new combinations are denied.

Conceptually:

```text
north × fuel
north × medical
north × food
central × fuel
central × medical

coverage = 5
```

A later request for:

```text
south × food
```

does not become available simply because the observer waits.

This is the fundamental difference from the time-based limiter.

---

## 11. Hard Coverage Results

The hard coverage policy produced:

```text
Mean Reconstruction Score: 52.13%
Observable State:          55.56%
```

Across randomized trials:

```text
Minimum score: 50.78%
Maximum score: 53.39%
```

The mechanism substantially reduced reconstruction.

But it did so by substantially reducing access.

That creates an obvious problem:

> A security mechanism that prevents legitimate clients from using the service is not necessarily useful.

This motivated adaptive disclosure.

---

## 12. Adaptive Disclosure

Instead of moving directly from:

```text
ALLOW
```

to:

```text
DENY
```

the adaptive policy progressively reduces precision.

The toy policy uses:

```text
Coverage 1–3
→ exact

Coverage 4–5
→ numeric range

Coverage 6–7
→ category

Coverage 8+
→ limited
```

Example:

```text
82
↓
80–90
↓
high
↓
limited
```

The objective is to preserve some client utility while making complete reconstruction more difficult.

---

## 13. Adaptive Disclosure Results

Across 1000 randomized trials:

```text
Mean Reconstruction Score: 75.71%
Observable State:          77.78%
```

Range:

```text
Minimum score: 73.83%
Maximum score: 77.44%
```

This placed adaptive disclosure between unrestricted access and hard blocking.

It preserved more information than the hard coverage policy while reducing reconstruction relative to baseline.

---

## 14. Main Experimental Result

The final canonical benchmark is:

| Mode | Reconstruction Score | Observable State |
|---|---:|---:|
| Baseline | 93.83% | 100.00% |
| Rate Limit + Waiting | 93.83% | 100.00% |
| Hard Coverage Policy | 52.13% | 55.56% |
| Adaptive Disclosure | 75.71% | 77.78% |

The experiment therefore exposes a simple distinction.

### Request-frequency control

asks:

> How quickly can the client ask?

### Exposure-aware control

asks:

> How much distinct state has the client already observed?

In this synthetic model, those two controls produced different final information outcomes.

---

## 15. Reconstruction Score

The current metric is intentionally simple.

For an estimable hidden cell:

```text
score = 1 - (absolute_error / 100)
```

For a cell that the observer cannot estimate:

```text
score = 0
```

The final reconstruction score is the mean across all cells.

This metric exists only to compare the experimental modes consistently.

It is not:

- a formal privacy metric;
- an entropy measure;
- mutual information;
- a differential privacy guarantee;
- a standardized information-theoretic measure.

A stronger future experiment should replace or complement this metric.

---

## 16. Security–Utility Trade-off

The experiment reveals a predictable but important trade-off.

Hard Coverage:

```text
Reconstruction: 52.13%
Observable:     55.56%
```

Adaptive Disclosure:

```text
Reconstruction: 75.71%
Observable:     77.78%
```

Hard blocking provides stronger reduction in reconstruction but removes more useful access.

Adaptive disclosure preserves more utility but exposes more information.

Therefore, a practical system should not optimize only:

```text
minimum disclosure
```

It must optimize something closer to:

```text
privacy / security
+
legitimate utility
+
latency
+
state cost
+
developer complexity
```

---

## 17. Figures

### Reconstruction Score by Defense Mode

![Reconstruction Score by Defense Mode](../experiments/001-mcp-inference-security/results/figure-1-reconstruction-score.png)

### Security–Utility Trade-off

![Security–Utility Trade-off](../experiments/001-mcp-inference-security/results/figure-2-security-utility-tradeoff.png)

The second figure illustrates the central trade-off.

Baseline and Rate Limit + Waiting overlap because their final informational outcomes are identical under the current assumptions.

Hard Coverage moves toward lower reconstruction and lower observability.

Adaptive Disclosure occupies an intermediate position.

---

## 18. Why a Gateway Is an Interesting Implementation Point

The experiment suggests that exposure accounting does not necessarily need to be implemented independently inside every tool.

A possible architecture is:

```text
MCP Client
    ↓
Exposure-Aware Gateway
    ↓
MCP Server / Tools
```

The gateway could maintain:

- caller identity;
- structural coverage;
- tool/resource classifications;
- disclosure policy;
- response precision state.

This remains only a candidate architecture.

The experiment does not establish that gateway enforcement is the best production design.

---

## 19. Why Controlled Deception Was Removed from the Core

An early version of the idea considered returning synthetic or misleading information to suspicious clients.

That direction was deliberately removed from the core experiment.

False data can create serious secondary problems:

- cache contamination;
- RAG contamination;
- analytics corruption;
- propagation into legitimate systems;
- inconsistent downstream decisions;
- trust failures.

The first experiment therefore uses:

```text
precision reduction
```

rather than:

```text
false information
```

Controlled deception may remain a separate research topic, but it should not be treated as a default mechanism.

---

## 20. Limitations

The experiment is intentionally small.

Major limitations include:

- only nine hidden cells;
- static hidden state;
- synthetic tools;
- simplified MCP-style interfaces;
- deterministic reconstruction;
- no LLM attacker;
- no statistical learning attacker;
- no Sybil identities;
- no identity rotation;
- no colluding clients;
- no distributed servers;
- no cross-server accounting;
- no realistic caching model;
- no production latency benchmark;
- no throughput measurement;
- no established privacy metric.

These limitations are substantial.

The results must therefore remain narrow.

---

## 21. What This Work Does Not Prove

This work does not prove:

- that MCP is insecure;
- that MCP contains a new vulnerability;
- that cumulative inference is a new discovery;
- that coverage accounting should become part of the MCP specification;
- that adaptive disclosure is superior to differential privacy;
- that this policy generalizes to real infrastructure;
- that the current reconstruction score is scientifically sufficient.

The strongest defensible claim is:

> In this synthetic experiment, structural cumulative-exposure controls changed the final state-reconstruction outcome, while conventional time-based rate limiting primarily changed collection time.

---

## 22. What May Actually Be Interesting

After related-work review and experimentation, the potentially useful contribution has become much narrower than the original idea.

It is not:

> discovering cumulative inference.

It may instead be:

> experimentally adapting established inference-control concepts to heterogeneous agent tool traffic using lightweight structural exposure accounting.

Possible research questions include:

- Can structural coverage approximate information gain cheaply?
- Can policies operate across heterogeneous tool schemas?
- How should identities share or isolate budgets?
- Can multiple servers coordinate exposure state?
- How should transformed responses communicate provenance?
- Can adaptive disclosure preserve enough legitimate utility?
- What is the latency and memory cost at scale?

These are engineering questions rather than claims of a new security principle.

---

## 23. Reproducibility

The canonical benchmark uses:

```text
1000 randomized runs
random seed = 405
```

Run from the repository root:

```bash
python experiments/001-mcp-inference-security/results/randomized_benchmark.py
```

Expected canonical values:

```text
Baseline              93.83%
Rate Limit + Waiting  93.83%
Hard Coverage         52.13%
Adaptive Disclosure   75.71%
```

Raw output:

```text
experiments/001-mcp-inference-security/results/benchmark-v0.1.json
```

Experiment documentation:

```text
experiments/001-mcp-inference-security/README.md
```

Full result interpretation:

```text
experiments/001-mcp-inference-security/results/RESULTS.md
```

---

## 24. Next Experimental Stage

The next version should make the experiment harder rather than make the claim larger.

Potential v0.2 work includes:

1. randomized hidden states;
2. hundreds or thousands of state dimensions;
3. changing values over time;
4. heterogeneous tool schemas;
5. stronger reconstruction algorithms;
6. statistical attackers;
7. LLM-based observers;
8. multiple identities;
9. Sybil behavior;
10. cross-server correlation;
11. gateway latency measurement;
12. memory and storage overhead;
13. comparison with differential privacy;
14. formal utility metrics;
15. stronger information-theoretic evaluation.

The central question becomes:

> Does the observed effect survive when the toy assumptions are removed?

---

## References

1. Dorothy E. Denning and Jan Schlörer.  
   **“Inference Controls for Statistical Databases.”**  
   *IEEE Computer*, 16(7), pp. 69–82, 1983.  
   DOI: `10.1109/MC.1983.1654444`

2. Dorothy E. Denning, Peter J. Denning, and Mayer D. Schwartz.  
   **“The Tracker: A Threat to Statistical Database Security.”**  
   *ACM Transactions on Database Systems*, 4(1), pp. 76–96, 1979.  
   DOI: `10.1145/320064.320069`

3. Cynthia Dwork and Aaron Roth.  
   **The Algorithmic Foundations of Differential Privacy.**  
   *Foundations and Trends in Theoretical Computer Science*, 9(3–4), pp. 211–407, 2014.  
   DOI: `10.1561/0400000042`

4. Model Context Protocol.  
   **Model Context Protocol Specification, Revision 2026-07-28.**  
   Official MCP specification, 2026.  
   See: Model Context Protocol specification and authorization documentation.

5. David Soria Parra and Den Delimarsky.  
   **“The 2026-07-28 Specification.”**  
   Model Context Protocol Blog, July 28, 2026.

---

### Relationship to Prior Work

The first three references establish that inference from combinations of permitted statistical releases, query-sequence attacks, disclosure control, and cumulative privacy composition substantially predate MCP.

The MCP references establish the protocol and security context in which this experiment is positioned.

Accordingly, this work does not claim cumulative inference as a new security principle. Its narrower experimental question is whether lightweight structural exposure accounting can provide a useful engineering abstraction for heterogeneous MCP-style tool interactions.

---

## Conclusion

The initial idea began broadly.

Related-work analysis reduced it.

Gap analysis reduced it again.

The experiment reduced it further.

That is the intended process.

The current result does not justify a new protocol standard.

It does justify a harder experiment.

The most interesting observation from v0.1 is not that rate limiting is “bad” or that adaptive disclosure is “the solution.”

It is the narrower distinction between:

```text
request frequency
```

and:

```text
cumulative structural exposure
```

In this toy environment, those quantities were not equivalent.

Whether that distinction remains useful in realistic MCP systems is the next question.

---

**Empty405 Lab**

*Start empty. Ask strange questions. Build what survives.* 
