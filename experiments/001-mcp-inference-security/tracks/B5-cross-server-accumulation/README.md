# B5 Cross-server Accumulation Benchmark

Standard-library simulation of one principal combining disclosures from independently budgeted MCP servers under local, central, eventual, signed-token, sketch, and oracle accounting.

```bash
python benchmark.py
python -m unittest -v test_benchmark.py
```

The default run uses 450 trials per configuration and produces 583,200 raw rows across 1,296 configurations with exactly 96 requests per trial.

Synchronization and sketch behavior are synthetic abstractions. Metadata exchange, linked operators, availability, and reconstruction are reported together.
