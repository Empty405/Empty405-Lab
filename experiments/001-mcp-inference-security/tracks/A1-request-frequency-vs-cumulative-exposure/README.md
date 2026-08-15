# A1 Benchmark Implementation

This experiment compares request-frequency controls with non-resetting cumulative exposure controls under identical static scenarios and query streams.

## Run

```bash
python benchmark.py --runs 1000 --seed 40501
python -m unittest -v test_benchmark.py
```

The benchmark uses only the Python standard library.

## Modes

- unrestricted baseline;
- resettable window rate limit;
- non-resetting lifetime request quota;
- exact unique-coverage budget;
- hybrid rate plus coverage policy.

## Observer conditions

- `patient`: waits for rate windows to reset;
- `deadline`: stops receiving delayed results after a fixed logical deadline.

## Scenarios

- `unique`: every query targets a new cell;
- `duplicate-heavy`: every cell is queried three times, exposing the difference between request count and new structural coverage.

## Interpretation boundary

The benchmark measures a synthetic static state with one stable principal and a deterministic band observer. Structural coverage is a proxy, not mutual information, differential privacy, or proof of a real MCP vulnerability.
