# Empty405 Research Engine v0.1

> Turn raw ideas into falsifiable, reproducible research projects without optimizing for a predetermined conclusion.

**Status:** Working prototype  
**Scope:** Research orchestration and validation  
**Principle:** Make the experiment harder before making the claim larger.

## Pipeline

```text
RAW IDEA
  ↓
Scout
  ↓
Prior Art / Context
  ↓
Critic
  ↓
Claim Reduction
  ↓
Experimenter
  ↓
Falsification Plan
  ↓
Experiment
  ↓
Results
  ↓
Reviewer
  ↓
Claims Audit
  ↓
Publisher
  ↓
Research Artifact
  ↓
Next Question
```

The engine is intentionally conservative. A research project may finish as:

- `supported`
- `mixed`
- `falsified`
- `inconclusive`
- `blocked`

A falsified hypothesis is a valid result.

## v0.1 capabilities

- create a complete research workspace from one command;
- store machine-readable research metadata;
- require a falsifiable hypothesis;
- require explicit success and failure criteria;
- track prior art separately from original contribution;
- track experiment seeds and reproducibility commands;
- validate research-stage requirements;
- prevent publication status when critical fields are missing;
- provide role prompts for Scout, Critic, Experimenter, Reviewer, and Publisher;
- include a deterministic demo pipeline and tests.

## Create a research project

```bash
python engine/scripts/new_research.py \
  --id 002 \
  --title "Example Research Question"
```

Optional:

```bash
python engine/scripts/new_research.py \
  --id 002 \
  --title "Example Research Question" \
  --slug example-research \
  --root research
```

## Validate

```bash
python engine/scripts/validate_research.py research/002-example-research/research.json
```

Strict publication validation:

```bash
python engine/scripts/validate_research.py \
  research/002-example-research/research.json \
  --stage publish
```

## Run tests

```bash
python -m unittest discover engine/tests -v
```

## Design boundary

v0.1 does **not** autonomously browse literature, execute arbitrary generated code, publish papers, or decide scientific truth.

It defines the contract between those future capabilities.

The engine should eventually allow different model/tool backends to fill each role while preserving the same research state and validation rules.
