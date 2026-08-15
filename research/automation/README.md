# Research Automation

The automation layer performs mechanical checks for completed experiment modules. It does **not** invent research designs, approve its own scientific claims, push commits, open pull requests, or merge branches.

## Research runner

The checkpointed runner discovers experiment directories, runs their unit tests, optionally regenerates benchmarks, validates result metadata, counts compressed CSV rows, computes integrity hashes, and saves resumable state.

From the repository root:

```bash
python scripts/research_runner.py --dry-run
python scripts/research_runner.py --resume
python scripts/research_runner.py --resume --max-modules 1
python scripts/research_runner.py --resume --run-benchmarks
```

State is stored atomically in `.cache/research-runner/state.json`. The cache directory is ignored by Git. An unchanged module that previously passed is skipped with `--resume`.

## Validation tools

### Schema enforcer

Checks that `benchmark.json` is valid, finite JSON and declares one consistent positive raw-row count.

```bash
python scripts/validation/schema_enforcer.py path/to/results/benchmark.json
```

### Integrity checker

Checks the compressed CSV header and row count against metadata, then reports SHA-256 hashes.

```bash
python scripts/validation/integrity_checker.py path/to/results
```

## Processing

The metric aggregator scans completed experiments, validates their artifacts and writes a compact CSV index.

```bash
python scripts/processing/metric_aggregator.py --output /tmp/experiment-index.csv
```

## Environment doctor

Checks Python, Git, repository structure, write access and free disk space before a heavy run.

```bash
python scripts/maintenance/env_doctor.py --root .
```

## GitHub Actions

`Research CI` runs for changes under `experiments/**`, `scripts/**` and the workflow itself. It:

1. runs all research-tool tests;
2. diagnoses the clean runner environment;
3. validates every discovered experiment;
4. builds a validated experiment index.

The workflow can be launched manually from **Actions → Research CI → Run workflow**. Enable `regenerate_benchmarks` only for an intentional full rerun because completed matrices can contain hundreds of thousands of trials.

## Safety boundary

These tools validate reproducibility, structure and artifact consistency. Human review remains required for assumptions, interpretation, publication and merge authorization. Cache cleaning and external notifications remain deliberately separate future capabilities.
