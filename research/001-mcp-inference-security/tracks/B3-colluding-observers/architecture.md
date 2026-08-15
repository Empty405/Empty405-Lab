# B3 Architecture

## Components

1. **Hidden-state fixture** — спільний секретний стан.
2. **Observer population** — незалежні principals з окремими sessions і задачами.
3. **Query behavior generator** — створює independent, overlapping або partitioned workloads.
4. **MCP gateway** — автентифікація, policy та exposure ledgers.
5. **Server-side detector** — бачить лише дозволені traffic features.
6. **Exchange network** — передає дозволені відповіді за collusion graph поза gateway.
7. **Individual observers** — реконструюють зі своїх відповідей.
8. **Coalition observer** — реконструює з реально обміняного union.
9. **Evaluator** — має ground-truth coalition labels і hidden state.

## Visibility boundary

Server can observe:

- identity, session and organization claims;
- query/response provenance;
- timing and structural query similarity;
- its own disclosure decisions.

Server cannot observe by default:

- private messages between observers;
- copied responses after delivery;
- true social relationships;
- coalition membership;
- external reconstruction code.

## Coalition topologies

- clique;
- star;
- chain;
- sparse random graph;
- disconnected subgroups.

Primary v0.1 uses a clique with post-hoc exchange. Other topologies are follow-up sensitivity tests.

## Policy families

| Policy | Accounting scope | Main failure |
|---|---|---|
| Per client | identity | coalition union unbounded |
| Organization | declared organization | false claims and cross-org collusion |
| Behavioral cohort | inferred similar traffic | false suspicion of legitimate common tasks |
| Diversity-aware | penalize complementary coverage | harms parallel legitimate research |
| Global | server-wide budget | availability collapse |
| Oracle coalition | true coalition | evaluator-only upper bound |

## Trust boundaries

- Policy/detector cannot read coalition ground truth.
- Exchange happens only after server decisions.
- Coalition observer receives only explicitly shared responses.
- Legitimate control groups may run similar queries but never share outputs.
- Paired policies receive identical workloads and seeds.
