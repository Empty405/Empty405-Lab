#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path


BASE_REQUIRED = [
    ("question",),
    ("hypothesis",),
    ("falsification", "criteria"),
    ("experiment", "plan"),
    ("experiment", "metrics"),
    ("reproducibility", "command"),
]

PUBLISH_REQUIRED = BASE_REQUIRED + [
    ("prior_art",),
    ("strongest_objections",),
    ("success_criteria",),
    ("review", "limitations"),
    ("review", "claim_audit"),
    ("next_questions",),
]


def get_path(data, path):
    value = data
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def missing(value):
    return value is None or value == "" or value == [] or value == {}


def validate(data, stage="design"):
    errors = []

    if data.get("engine_version") != "0.1":
        errors.append("engine_version must be 0.1")

    research = data.get("research", {})
    if not research.get("id"):
        errors.append("research.id is required")
    if not research.get("title"):
        errors.append("research.title is required")

    required = PUBLISH_REQUIRED if stage == "publish" else BASE_REQUIRED

    for path in required:
        value = get_path(data, path)
        if missing(value):
            errors.append("missing: " + ".".join(path))

    if stage == "publish":
        outcome = get_path(data, ("review", "outcome"))
        if outcome in (None, "", "pending"):
            errors.append("review.outcome must be resolved before publication")

        status = research.get("status")
        if status != "publish-ready":
            errors.append("research.status must be publish-ready")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("record")
    parser.add_argument("--stage", choices=["design", "publish"], default="design")
    args = parser.parse_args()

    path = Path(args.record)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data, args.stage)

    if errors:
        print(f"INVALID ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"VALID: {path} [{args.stage}]")


if __name__ == "__main__":
    main()
