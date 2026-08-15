# Research Track Index

## A — Cumulative Information Exposure

Як окремі дозволені відповіді накопичуються і разом відкривають більше, ніж кожна відповідь окремо.

- [A1 — Request-frequency vs cumulative exposure](A1-request-frequency-vs-cumulative-exposure/README.md)
- [A2 — Structural exposure accounting](A2-structural-exposure-accounting/README.md)
- [A3 — Adaptive disclosure](A3-adaptive-disclosure/README.md)
- [A4 — Security–utility trade-off](A4-security-utility-trade-off/README.md)

## B — Identity / Principal Problem

Визначає, кому саме приписувати накопичену інформацію, коли токени, сесії та ідентичності змінюються.

- [B1 — Identity rotation](B1-identity-rotation/README.md)
- [B2 — Sybil / multiple identities](B2-sybil-multiple-identities/README.md)
- [B3 — Colluding observers](B3-colluding-observers/README.md)
- [B4 — Cross-session accumulation](B4-cross-session-accumulation/README.md)
- [B5 — Cross-server accumulation](B5-cross-server-accumulation/README.md)
- [B6 — Durable principal attribution](B6-durable-principal-attribution/README.md)

## C — Shared-Budget Problem

Досліджує спільний бюджет розкриття: хто його витрачає, як ділити його чесно і що робити після вичерпання.

- [C1 — Shared exposure accounting](C1-shared-exposure-accounting/README.md)
- [C2 — Budget exhaustion](C2-budget-exhaustion/README.md)
- [C3 — Availability degradation](C3-availability-degradation/README.md)
- [C4 — Malicious budget consumption](C4-malicious-budget-consumption/README.md)
- [C5 — Fair allocation between clients](C5-fair-allocation-between-clients/README.md)
- [C6 — Budget recovery / decay](C6-budget-recovery-decay/README.md)

## D — Observer Problem

Визначає, що саме здатен помітити захисний спостерігач і де він помиляється через різні формулювання та представлення.

- [D1 — Structural observer](D1-structural-observer/README.md)
- [D2 — Semantic equivalence](D2-semantic-equivalence/README.md)
- [D3 — Encoding / representation differences](D3-encoding-representation-differences/README.md)
- [D4 — Cross-tool semantic composition](D4-cross-tool-semantic-composition/README.md)
- [D5 — Partial-information inference](D5-partial-information-inference/README.md)
- [D6 — Observer false negatives](D6-observer-false-negatives/README.md)
- [D7 — Observer false positives](D7-observer-false-positives/README.md)

## E — Temporal Exposure

Додає час: прихований стан змінюється, старі дані можуть втрачати цінність, а повторні спостереження відкривають динаміку.

- [E1 — Static hidden state](E1-static-hidden-state/README.md)
- [E2 — Dynamic hidden state](E2-dynamic-hidden-state/README.md)
- [E3 — Exposure decay](E3-exposure-decay/README.md)
- [E4 — Historical information](E4-historical-information/README.md)
- [E5 — Repeated observations](E5-repeated-observations/README.md)
- [E6 — Change inference](E6-change-inference/README.md)

## F — Distributed Exposure

Розглядає витік, розподілений між клієнтами, серверами й організаціями, які не мають спільного журналу.

- [F1 — Multiple clients](F1-multiple-clients/README.md)
- [F2 — Multiple MCP servers](F2-multiple-mcp-servers/README.md)
- [F3 — Multiple organizations](F3-multiple-organizations/README.md)
- [F4 — Distributed observations](F4-distributed-observations/README.md)
- [F5 — External reconstruction](F5-external-reconstruction/README.md)
- [F6 — Federated exposure accounting](F6-federated-exposure-accounting/README.md)

## G — Attacker / Reconstruction Model

Поступово посилює модель атакувальника — від простих правил до статистики, ML, LLM та адаптивної стратегії.

- [G1 — Deterministic observer](G1-deterministic-observer/README.md)
- [G2 — Constraint-composition observer](G2-constraint-composition-observer/README.md)
- [G3 — Statistical inference](G3-statistical-inference/README.md)
- [G4 — Bayesian reconstruction](G4-bayesian-reconstruction/README.md)
- [G5 — ML reconstruction](G5-ml-reconstruction/README.md)
- [G6 — LLM-agent reconstruction](G6-llm-agent-reconstruction/README.md)
- [G7 — Adaptive attacker](G7-adaptive-attacker/README.md)

## H — Defense Mechanisms

Порівнює конкретні захисти: від rate limiting і квот до шуму, аудиту та гібридних політик.

- [H1 — Rate limiting](H1-rate-limiting/README.md)
- [H2 — Hard coverage](H2-hard-coverage/README.md)
- [H3 — Adaptive disclosure](H3-adaptive-disclosure/README.md)
- [H4 — Noise](H4-noise/README.md)
- [H5 — Query auditing](H5-query-auditing/README.md)
- [H6 — Differential privacy comparison](H6-differential-privacy-comparison/README.md)
- [H7 — Information-flow mechanisms](H7-information-flow-mechanisms/README.md)
- [H8 — Hybrid policies](H8-hybrid-policies/README.md)

## I — Metrics

Визначає, як чесно виміряти реконструкцію, витік, корисність, доступність і технічну ціну захисту.

- [I1 — Reconstruction score](I1-reconstruction-score/README.md)
- [I2 — Observable state](I2-observable-state/README.md)
- [I3 — Legitimate utility](I3-legitimate-utility/README.md)
- [I4 — Information gain](I4-information-gain/README.md)
- [I5 — Entropy reduction](I5-entropy-reduction/README.md)
- [I6 — Privacy loss](I6-privacy-loss/README.md)
- [I7 — Availability cost](I7-availability-cost/README.md)
- [I8 — Computational overhead](I8-computational-overhead/README.md)

## J — Production Engineering

Переносить ідеї з toy-експерименту в реальну інженерію gateway, лічильників, синхронізації та відмовостійкості.

- [J1 — Gateway architecture](J1-gateway-architecture/README.md)
- [J2 — Distributed counters](J2-distributed-counters/README.md)
- [J3 — State synchronization](J3-state-synchronization/README.md)
- [J4 — Latency](J4-latency/README.md)
- [J5 — Memory / storage cost](J5-memory-storage-cost/README.md)
- [J6 — Failure recovery](J6-failure-recovery/README.md)
- [J7 — Real MCP implementation](J7-real-mcp-implementation/README.md)

