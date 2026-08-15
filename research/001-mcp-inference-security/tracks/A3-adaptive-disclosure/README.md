# A3 — Adaptive Disclosure

**Program:** Research 001 — MCP Inference Security  
**Track:** A3  
**Status:** Designed  
**Depends on:** A1 and A2  
**Distinct from:** H3 defense comparison

## Простими словами

Замість різкого «дозволено / заборонено» система може поступово робити відповіді менш точними. Спочатку клієнт бачить точне значення, потім діапазон, категорію, загальний підсумок і лише в кінці — відмову.

A3 перевіряє, чи така драбина справді зменшує реконструкцію та водночас залишає чесному клієнту корисну відповідь.

## Research question

> Can a deterministic, provenance-carrying precision ladder reduce cumulative reconstruction while preserving more task utility than matched hard blocking?

## Precision ladder

```text
L0 exact
→ L1 narrow range
→ L2 broad range
→ L3 category
→ L4 aggregate
→ L5 unavailable
```

Перехід визначається накопиченим exposure принципала, типом задачі та чутливістю projection.

## Narrow hypothesis

At matched final exposure targets, deterministic precision degradation will preserve more legitimate task utility than hard blocking, without allowing repeated sampling to reconstruct a more precise answer than the selected disclosure level intends.

## Null hypothesis

Adaptive disclosure provides no utility advantage over hard blocking at comparable reconstruction risk, or repeated degraded answers can be composed into effectively exact information.

## Required properties

- deterministic for the same principal, epoch, query class, and policy state;
- monotonic: increasing exposure cannot silently restore precision;
- compositional: repeated outputs cannot exceed the intended level;
- provenance-carrying: downstream agents know precision and freshness;
- policy-visible: every transformation has an explicit reason code;
- fail-closed for unknown sensitivity mappings.

## Explicit exclusions

A3 does not solve principal identity, collusion, distributed synchronization, arbitrary semantic equivalence, differential privacy, or deceptive false-data injection.

## Relationship to H3

A3 designs and falsifies one adaptive-disclosure primitive. H3 later compares variants of this defense against rate limits, hard coverage, noise, auditing, and hybrid policies.

## Decision rule

The mechanism remains viable only if it beats matched hard blocking on legitimate task utility, stays below the reconstruction boundary, and passes repeated-sampling, boundary-oscillation, and provenance tests.
