# C4 Experiment Design

## Primary experiment

Hold legitimate arrivals, structural requirements, deadlines, principal set, shared ledger, disclosure cap and attacker opportunity schedule constant. Vary only admission policy, attacker strategy, attack intensity and legitimate workload shape.

## Independent variables

- policy: global FIFO, global rate limit, per-principal reservation, per-principal marginal-cost cap, weighted fair share, bounded hybrid, oracle;
- attacker strategy: benign-load control, frequency flood, novelty maximizer, front-loaded burn, adaptive burn, camouflage;
- attack intensity: low, medium, high;
- legitimate workload: steady, burst, late-critical;
- paired trial seed: 200 trials per configuration.

## Minimum v0.1 matrix

`7 policies × 6 attacker strategies × 3 intensities × 3 legitimate workloads × 200 paired trials = 75,600 trials`.

Each episode fixes 120 ticks, four legitimate principals, one adversarial principal, one exact ledger, one global cap and atomic check-and-charge. Principal count and identity mapping remain fixed.

## Paired trial procedure

1. Generate legitimate tasks, deadlines, task values and attacker opportunities.
2. Assign the same structural units and timing to every paired policy.
3. Initialize the exact released union and remaining shared cap.
4. Generate attacker requests according to the selected strategy.
5. Estimate exact marginal structural exposure for each request.
6. Let the selected policy admit, replay or deny without role labels or future knowledge.
7. Atomically charge newly released units before returning a response.
8. Record terminal request outcome and legitimate task sufficiency.
9. Continue until tick 119 without budget reset or borrowing outside policy rules.
10. Compare deployable policies with benign-load and oracle controls.

## Controls

- no attacker;
- benign traffic with attacker-matched request count and timing;
- duplicate-only attacker requests with zero marginal exposure;
- one high-cost legitimate burst;
- attacker arriving entirely after legitimate demand;
- cap sufficient for every request;
- cap sufficient only for legitimate oracle allocation;
- global FIFO baseline;
- oracle with identical schedule and cap.

## Required raw outputs

- episode, tick, request ID and principal ID;
- evaluator role label stored only in results;
- strategy, policy and workload;
- requested structural units and marginal exposure cost;
- admission, replay, denial and completion outcome;
- ledger before/after and remaining cap;
- legitimate task value, deadline and sufficiency;
- per-principal requests, exposure charged and useful completions;
- policy reads, ledger operations, audit writes and metadata bytes.

## Statistical plan

- paired differences against benign-load control;
- confidence intervals for victim completion loss and attacker capture;
- per-principal allocation and Jain-style fairness reported with utility caveats;
- security–availability–fairness Pareto frontier;
- separate front-loaded, adaptive and camouflage effects;
- utilization and unused reservation cost;
- intensity response curves;
- oracle regret under identical cap.

## Stop conditions

Stop and repair the experiment if:

- policies receive different legitimate schedules or attacker opportunities;
- attacker and benign-load controls differ in declared volume or timing;
- a denied request releases units;
- duplicate units consume budget twice;
- total charge exceeds the cap;
- deployable policy reads evaluator role or future value;
- identity rotation or extra Sybils enter the primary matrix;
- reservation accounting creates or loses budget silently;
- request count is confused with exposure cost;
- legitimate denial is called security success without utility reporting.
