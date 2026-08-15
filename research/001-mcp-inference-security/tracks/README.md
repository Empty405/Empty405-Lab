# MCP Inference Security — Research Tracks

This directory decomposes Research 001 into independently falsifiable tracks.

Each track must have its own question, scope boundary, architecture, experiment, metrics, falsification criteria, Git branch, and review history. A result in one track must not be treated as evidence for another track without an explicit dependency.

## Program map

| Group | Scope | Tracks |
|---|---|---|
| A | Cumulative information exposure | A1–A4 |
| B | Identity and accounting principal | B1–B6 |
| C | Shared-budget behavior | C1–C6 |
| D | Observer capability and error | D1–D7 |
| E | Temporal exposure | E1–E6 |
| F | Distributed exposure | F1–F6 |
| G | Attacker and reconstruction models | G1–G7 |
| H | Defense mechanisms | H1–H8 |
| I | Metrics | I1–I8 |
| J | Production engineering | J1–J7 |

Research 002 covers the Research Engine tracks K1–K14.

## Track lifecycle

`proposed → designed → implemented → running → reviewed → published | falsified | archived`

## Git convention

- Branch: `research/<track-id>-<slug>`
- Directory: `research/001-mcp-inference-security/tracks/<track-id>-<slug>/`
- Experiment: `experiments/001-mcp-inference-security/tracks/<track-id>-<slug>/`
- One track per pull request unless an explicit dependency makes separation impossible.

## Active track

- [A1 — Request-frequency vs cumulative exposure](A1-request-frequency-vs-cumulative-exposure/README.md) — designed; implementation pending.
