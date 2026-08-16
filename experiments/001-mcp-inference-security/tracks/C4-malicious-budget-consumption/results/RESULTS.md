# C4 Malicious Budget Consumption — Results

## Run identity

- Schema: `c4.v0.1`
- Root seed: `40524`
- Raw trial rows: **75,600**
- Raw request events: **5,443,200**
- Configurations: **378**
- Trials per configuration: **200**
- Episode length: **120 ticks**
- Shared exposure cap: **48 units**

All 12 invariant tests passed. Declared and compressed row counts match, gzip integrity passed, and every JSON numeric value is finite.

## Main result

Under high-intensity traffic and global FIFO, volume/timing-matched benign load retains mean legitimate completion of `0.7747`. Strategic selection causes substantially greater harm:

| Strategy | Legitimate completion | Attacker capture | Wasted attacker exposure |
|---|---:|---:|---:|
| Benign control | 0.7747 | 0.4486 | 0.0000 |
| Novelty maximizer | 0.3945 | 0.8934 | 0.4530 |
| Front-loaded burn | 0.3558 | 0.9990 | 0.4400 |
| Adaptive burn | 0.3978 | 0.8942 | 0.4559 |
| Camouflage | 0.5396 | 0.4846 | 0.4581 |

This supports the narrow claim that strategic marginal-exposure selection can cause more denial-of-information than equivalent request volume alone.

## Policy comparison

For high-intensity adaptive burn:

| Policy | Legitimate completion | Attacker capture | Unused capacity |
|---|---:|---:|---:|
| Global FIFO | 0.3978 | 0.8942 | 0.0000 |
| Rate limit | 0.3984 | 0.8933 | 0.0000 |
| Reservation | 0.7150 | 0.1664 | 0.0073 |
| Marginal cap | 0.7332 | 0.0972 | 0.0000 |
| Fair share | 0.6550 | 0.1997 | 0.0670 |
| Bounded hybrid | 0.7414 | 0.0714 | 0.0041 |
| Oracle | 0.7758 | 0.0000 | 0.0001 |

Request-count rate limiting is almost indistinguishable from FIFO because low-frequency requests can still carry high marginal exposure. Exposure-aware bounded policies suppress attacker capture while retaining most legitimate completion. Fair share protects principals but leaves more capacity unused in this fixed reservation model.

## Interpretation

The benchmark supports four directional findings:

1. strategic budget burning is not equivalent to benign volume;
2. front-loading can nearly monopolize FIFO allocation before late legitimate demand arrives;
3. request-count controls miss high-cost novelty attacks;
4. bounded hybrid and marginal-cost caps approach the evaluator oracle without cap violation, but depend on exact identity and exact marginal exposure.

No result establishes production safety. The model excludes Sybils, semantic observer error, distributed ledger races, budget decay, and governance of legitimate priority.

## Falsification status

The primary null hypothesis is weakened because matched strategic and benign loads produce large paired utility differences. The claim that simple rate limiting is sufficient is also weakened. The broader hypothesis remains conditional on the exact-identity and exact-accounting assumptions; relaxing them belongs to B, D, C5–C6, and J tracks.
