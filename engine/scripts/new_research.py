#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "research"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--root", default="research")
    parser.add_argument("--raw-idea", default="")
    args = parser.parse_args()

    research_id = str(args.id).zfill(3)
    slug = args.slug or slugify(args.title)
    target = Path(args.root) / f"{research_id}-{slug}"

    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing research: {target}")

    (target / "experiment").mkdir(parents=True)
    (target / "results").mkdir()
    (target / "sources").mkdir()

    record = {
        "engine_version": "0.1",
        "research": {
            "id": research_id,
            "title": args.title,
            "slug": slug,
            "status": "idea"
        },
        "raw_idea": args.raw_idea,
        "question": "",
        "initial_claim": "",
        "narrowed_claim": "",
        "hypothesis": "",
        "prior_art": [],
        "strongest_objections": [],
        "falsification": {"criteria": []},
        "success_criteria": [],
        "experiment": {
            "plan": "",
            "metrics": [],
            "results_path": f"{target}/results/RESULTS.md"
        },
        "reproducibility": {
            "command": "",
            "seed": None,
            "environment": ""
        },
        "review": {
            "outcome": "pending",
            "limitations": [],
            "claim_audit": []
        },
        "next_questions": []
    }

    (target / "research.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )

    research_md = f"""# Research {research_id} — {args.title}

**Status:** Idea  
**Engine:** Empty405 Research Engine v0.1

## Raw Idea

{args.raw_idea or "TBD"}

## Research Question

TBD

## Prior Art

TBD

## Narrowed Claim

TBD

## Hypothesis

TBD

## Falsification Criteria

TBD

## Experiment

See `experiment/EXPERIMENT.md`.

## Results

See `results/RESULTS.md`.

## Review

TBD

## Limitations

TBD

## Next Questions

TBD
"""
    (target / "README.md").write_text(research_md, encoding="utf-8")
    (target / "experiment" / "EXPERIMENT.md").write_text(
        "# Experiment\n\nTBD\n", encoding="utf-8"
    )
    (target / "results" / "RESULTS.md").write_text(
        "# Results\n\nTBD\n", encoding="utf-8"
    )
    (target / "sources" / "README.md").write_text(
        "# Sources\n\nPrimary and supporting sources for this research.\n",
        encoding="utf-8"
    )

    print(f"Created: {target}")
    print(f"Record:  {target / 'research.json'}")


if __name__ == "__main__":
    main()
