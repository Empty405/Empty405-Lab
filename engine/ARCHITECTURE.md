# Architecture

Empty405 Research Engine separates **research state** from **agents**.

```text
                     ┌──────────────┐
raw idea ───────────▶│ research.json│◀──────────────┐
                     └──────┬───────┘               │
                            │                       │
        ┌───────────────────┼───────────────────┐   │
        ▼                   ▼                   ▼   │
      Scout               Critic          Experimenter
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                         Executor
                            │
                            ▼
                          Results
                            │
                            ▼
                         Reviewer
                            │
                            ▼
                        Publisher
                            │
                            └───────────────────────▶ research.json
```

## Why state is separate

The engine should not depend on one model.

Future adapters may use:

- local Ollama models;
- hosted models;
- deterministic Python tools;
- MCP tools;
- n8n workflows;
- human review.

Every actor reads and writes the same explicit research contract.

## Safety against research drift

The state stores separately:

- raw idea;
- initial claim;
- narrowed claim;
- prior art;
- falsification criteria;
- success criteria;
- raw results;
- interpretation;
- limitations;
- outcome.

This makes it harder for a later agent to silently rewrite the original hypothesis after seeing the results.

## v0.2 direction

The next engine version can add:

- immutable stage snapshots;
- provenance hashes;
- source verification;
- experiment manifests;
- model/tool adapters;
- GitHub Actions;
- automatic figure generation;
- claim-to-source mapping;
- automatic adversarial review.
