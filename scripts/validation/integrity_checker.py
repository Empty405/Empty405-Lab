#!/usr/bin/env python3
"""Validate compressed experiment datasets and emit artifact hashes."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validation.schema_enforcer import declared_rows, load_metadata


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def count_gzip_rows(path: Path) -> int:
    try:
        with gzip.open(path, "rt", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if not header or any(not column.strip() for column in header):
                raise RuntimeError(f"{path.name}: missing or invalid CSV header")
            return sum(1 for _ in reader)
    except (OSError, EOFError, UnicodeError, csv.Error) as error:
        raise RuntimeError(f"{path.name}: unreadable compressed CSV: {error}") from error


def validate_results_dir(results: Path) -> dict[str, Any]:
    metadata_path = results / "benchmark.json"
    metadata = load_metadata(metadata_path)
    raw_files = sorted(results.glob("*.csv.gz"))
    if not raw_files:
        raise RuntimeError("no compressed raw CSV artifacts")

    counts = {path.name: count_gzip_rows(path) for path in raw_files}
    total = sum(counts.values())
    if total <= 0:
        raise RuntimeError("raw artifacts contain no data rows")

    expected = declared_rows(metadata)
    if total != expected:
        raise RuntimeError(f"raw row mismatch: metadata={expected:,}, files={total:,}")

    hashes = {metadata_path.name: sha256_file(metadata_path)}
    hashes.update({path.name: sha256_file(path) for path in raw_files})
    return {
        "raw_files": counts,
        "raw_rows": total,
        "declared_rows": expected,
        "sha256": hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="+", type=Path, help="experiment results directories")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()
    reports = {}
    for results in args.results:
        reports[str(results)] = validate_results_dir(results)
        if not args.json:
            print(f"PASS {results}: {reports[str(results)]['raw_rows']:,} raw rows")
    if args.json:
        print(json.dumps(reports, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
