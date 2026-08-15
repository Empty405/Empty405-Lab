# B3 v0.1 Results — Colluding Observers

## Outcome

The narrow hypothesis is supported inside the declared synthetic model. Independent observers can remain individually below their disclosure budgets and still reconstruct substantially more after full post-hoc exchange. The effect survives fixed total traffic and is strongest when observers collect complementary, low-overlap information.

Server-visible traffic similarity is insufficient to infer private collusion reliably. Policies that constrain cross-client structural coverage reduce coalition reconstruction but impose material utility or false-suspicion cost on legitimate groups.

## Run

- root seed: `40513`;
- 1,296 configurations;
- 500 trials per configuration;
- 648,000 compressed raw trial rows;
- exactly 96 coalition requests per trial;
- full post-hoc exchange;
- seven unit tests passed.

## Representative result

Coalition size 16, low overlap, partitioned queries, budget `0.25`:

| Policy | Coalition reconstruction | Maximum individual | Coalition gain | Legitimate group utility | Denied requests |
|---|---:|---:|---:|---:|---:|
| per client | 0.960 | 0.060 | 0.900 | 1.000 | 0.0 |
| organization | 0.960 | 0.060 | 0.900 | 0.899 | 0.0 |
| behavioral cohort | 0.947 | 0.060 | 0.887 | 0.964 | 1.3 |
| diversity-aware | 0.380 | 0.030 | 0.350 | 0.754 | 58.0 |
| global | 0.250 | 0.020 | 0.230 | 0.000 | 71.0 |
| oracle coalition | 0.250 | 0.020 | 0.230 | 1.000 | 71.0 |

## What survived falsification

- Coalition gain remains large with fixed aggregate traffic; it is not merely extra request volume.
- Partitioned queries produce a larger unique union than independent or overlapping behavior.
- Per-client accounting cannot constrain off-server union.
- Organization accounting fails when the coalition spans accounting groups or each group stays below its cap.
- Behavioral cohort detection performs poorly on complementary queries because query similarity is weak.
- Diversity-aware limits reduce reconstruction but also deny legitimate complementary work.

## Central limitation exposed by B3

The gateway cannot see private post-hoc copying by default. Once an individually permitted response has left the server, coalition membership and exchange may be observationally indistinguishable from independent legitimate use. The oracle result is therefore an experimental bound, not a deployable policy.

## Limitations

- Full post-hoc exchange only; partial and online exchange are deferred.
- Detector and false-suspicion rates are synthetic assumptions.
- The primary topology is a clique.
- Structural set union is not semantic reconstruction.
- Results do not establish that any real user group is colluding.

## Next question

B4 should test accumulation across sessions and long time horizons, where observers can spread the same composition process over historical windows.
