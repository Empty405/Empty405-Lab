# A4 — Security–Utility Trade-off

**Program:** Research 001 — MCP Inference Security  
**Track:** A4  
**Status:** Designed  
**Synthesizes:** A1–A3

## Простими словами

Захист, який нічого не показує, майже завжди «безпечний», але ним неможливо користуватися. A4 будує чесну карту компромісів: скільки reconstruction, utility, delay і operational cost дає кожна політика на однаковому workload.

## Research question

> Which disclosure policies lie on the Pareto frontier across reconstruction risk, legitimate task utility, availability delay, and accounting cost under shared experimental conditions?

## Core principle

A policy is dominated if another policy is:

- no worse on every reported objective; and
- strictly better on at least one objective.

A4 does not collapse all objectives into one score by default. A single weighted score can hide who selected the weights.

## Narrow hypothesis

No single policy will dominate across every task mix and deadline. Hard blocking, rate limiting, structural budgets, and adaptive disclosure will occupy different parts of the frontier, while some configurations will be strictly dominated and can be discarded.

## Null hypothesis

After controlling for risk and workload, one simple policy dominates the alternatives or apparent trade-offs disappear as artifacts of incompatible metrics.

## Inputs from A1–A3

A1 contributes the delay/final-exposure distinction. A2 contributes calibrated structural exposure and its failure cases. A3 contributes task-specific utility, matched-risk comparison, and a negative adaptive result.

Published A1–A3 summary values are contextual evidence only. The A4 comparison reruns policies in one unified harness.

## Objectives

Minimize:

- reference interval reduction;
- exact recovery;
- p95 task delay;
- denied legitimate tasks;
- ledger bytes;
- policy evaluation time.

Maximize:

- macro task utility;
- per-task minimum utility;
- deadline success;
- provenance completeness.

## Decision rule

A4 succeeds if it produces a reproducible frontier, identifies robustly dominated configurations, and shows how conclusions change under declared task weights and deadlines. It fails if rankings depend primarily on arbitrary normalization or incomparable workloads.
