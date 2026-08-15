#!/usr/bin/env python3
"""Build a compact, validated index of completed experiment artifacts."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, TextIO

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validation.integrity_checker import validate_results_dir
from validation.schema_enforcer import load_metadata

FIELDS = (
    "program",
    "module",
    "result_path",
    "declared_rows",
    "raw_rows",
    "raw_files",
    "configuration_count",
)


def configuration_count(metadata: dict[str, Any]) -> int | str:
    for key in ("configuration_count", "configurations", "scenario_count"):
        value = metadata.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, (list, dict)):
            return len(value)
    return ""


def collect(root: Path) -> list[dict[str, Any]]:
    rows = []
    experiments = root / "experiments"
    if not experiments.exists():
        return rows
    for metadata_path in sorted(experiments.rglob("results/benchmark.json")):
        results = metadata_path.parent
        module = results.parent
        relative = module.relative_to(experiments)
        metadata = load_metadata(metadata_path)
        report = validate_results_dir(results)
        rows.append(
            {
                "program": relative.parts[0] if relative.parts else "",
                "module": module.name,
                "result_path": results.relative_to(root).as_posix(),
                "declared_rows": report["declared_rows"],
                "raw_rows": report["raw_rows"],
                "raw_files": len(report["raw_files"]),
                "configuration_count": configuration_count(metadata),
            }
        )
    return rows


def write_csv(rows: list[dict[str, Any]], handle: TextIO) -> None:
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", default="-", help="CSV path or - for stdout")
    args = parser.parse_args()
    rows = collect(args.root.resolve())
    if args.output == "-":
        write_csv(rows, sys.stdout)
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as handle:
            write_csv(rows, handle)
        print(f"wrote {len(rows)} experiment rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
