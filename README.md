# EMPTY405 LAB

> **Start empty. Ask strange questions. Build what survives.**

**Ideas → Research → Criticism → Experiments → Projects**

---

## What is Empty405 Lab?

Empty405 Lab is a public laboratory for exploring ideas, systems, technologies, and long-term questions with the help of artificial intelligence.

This repository is not a collection of finished products and it is not a claim of expertise in every subject explored here.

It is a public record of a process:

**observe → question → research → challenge → experiment → build**

Some ideas may survive.

Some may evolve into something completely different.

Some may be wrong.

All three outcomes are useful.

---

## Philosophy

Ideas are cheap.

Testing them is interesting.

The purpose of this lab is to take observations and raw ideas, develop them far enough to become understandable and testable, and then expose them to criticism.

AI is used throughout this process as a research, reasoning, writing, coding, and exploration tool.

AI-generated material is not automatically treated as fact.

Research should be challenged.

Assumptions should be visible.

Mistakes should remain part of the record.

---

## Lab Structure

### `research/`

Ideas that have developed into structured research questions, technical proposals, threat models, architectural concepts, or other material worth investigating.

### `articles/`

Readable versions of research intended for wider discussion and publication.

### `experiments/`

Proofs of concept, tests, simulations, prototypes, and other attempts to determine whether an idea actually works.

### `projects/`

Ideas that survived enough criticism and experimentation to become active projects.

### `archive/`

Abandoned, superseded, failed, or historical work.

Failure is not deleted from the laboratory.

It becomes evidence.

---

## Research Status

Material published here may represent different stages of maturity.

A research document is **not necessarily a recommendation, specification, finished design, security guarantee, or production-ready solution**.

Where possible, work should clearly distinguish between:

- observation;
- hypothesis;
- existing evidence;
- proposed design;
- experiment;
- result;
- open question.

---

## Collaboration

Criticism is welcome.

Alternative designs are welcome.

Experiments that disprove an idea are welcome.

Independent implementations are welcome.

If a research direction develops into something worth building, contributors may organize around it and move the work toward an experiment or project.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidelines.

---

## Current Research

### 001 — MCP Inference Security

**Status:** Experimental Research  
**Research:** Complete through initial gap analysis  
**Experiment:** v0.1 completed  
**Reproducibility:** 1000 randomized runs, fixed seed `405`

Research question:

> Can lightweight cumulative exposure accounting and adaptive disclosure reduce cross-tool state reconstruction more effectively than conventional time-based rate limiting?

Current v0.1 result:

| Mode | Reconstruction Score | Observable State |
|---|---:|---:|
| Baseline | 93.83% | 100.00% |
| Rate Limit + Waiting | 93.83% | 100.00% |
| Hard Coverage Policy | 52.13% | 55.56% |
| Adaptive Disclosure | 75.71% | 77.78% |

The toy experiment suggests that conventional time-based rate limiting may delay cumulative collection without reducing the final observable state, while coverage-aware controls can change the final reconstruction outcome.

This is a synthetic proof-of-concept and does not establish an MCP vulnerability or justify a protocol change.

Research:

[`research/001-mcp-inference-security/`](research/001-mcp-inference-security/)

Experiment:

[`experiments/001-mcp-inference-security/`](experiments/001-mcp-inference-security/)

---

## About Empty405

Empty405 is an independent experimental identity focused on ideas, systems, AI-assisted research, and long-term technological exploration.

The goal is not to predict the future perfectly.

The goal is to leave behind a useful public record of attempts to understand and build parts of it.

---

**Empty405 Lab**

*Start empty. Ask strange questions. Build what survives.*
