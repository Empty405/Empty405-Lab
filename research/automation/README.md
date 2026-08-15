# Research Runner

This runner automates mechanical verification of completed experiment modules. It discovers experiment directories, runs their unit tests, optionally regenerates benchmarks, validates aggregate JSON, counts compressed raw CSV rows, and saves a resumable checkpoint.

It does **not** invent research designs, approve its own scientific claims, push commits, open pull requests, or merge branches.

## Local use

From the repository root:

```bash
python scripts/research_runner.py --dry-run
python scripts/research_runner.py --resume
```

Process only the first ready module:

```bash
python scripts/research_runner.py --resume --max-modules 1
```

Regenerate all benchmark artifacts before validating them:

```bash
python scripts/research_runner.py --resume --run-benchmarks
```

State is stored atomically in `.cache/research-runner/state.json`. An unchanged module that previously passed is skipped with `--resume`. Any failed test, malformed JSON, missing raw artifact, or declared/raw row mismatch stops the loop immediately.

## GitHub Actions

`Research CI` runs on experiment-related pull requests and pushes to `main`. It performs a clean, non-resumed validation of every discovered experiment.

The workflow can also be launched manually from **Actions → Research CI → Run workflow**. Enable `regenerate_benchmarks` only when a full rerun is intended; completed matrices can contain hundreds of thousands of trials.

## Safety boundary

The runner validates reproducibility and artifact consistency. Human review remains required for research assumptions, interpretation, GitHub publication, and merge authorization.
