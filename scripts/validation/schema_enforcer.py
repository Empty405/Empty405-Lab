#!/usr/bin/env python3
"""Validate Empty405-Lab benchmark metadata without third-party dependencies."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROW_KEYS = ("trial_rows", "checkpoint_rows", "rows")


class SchemaError(ValueError):
    """Raised when benchmark metadata violates the laboratory contract."""


def _reject_non_finite(value: Any, location: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise SchemaError(f"{location}: non-finite number")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise SchemaError(f"{location}: object key is not a string")
            _reject_non_finite(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_non_finite(child, f"{location}[{index}]")


def declared_rows(metadata: dict[str, Any], required: bool = True) -> int | None:
    values: list[tuple[str, int]] = []
    for key in ROW_KEYS:
        if key not in metadata:
            continue
        value = metadata[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise SchemaError(f"{key}: expected integer")
        if value <= 0:
            raise SchemaError(f"{key}: expected positive row count")
        values.append((key, value))
    if not values:
        if required:
            raise SchemaError(f"missing declared row count; expected one of {ROW_KEYS}")
        return None
    if len({value for _, value in values}) != 1:
        raise SchemaError(f"conflicting declared row counts: {values}")
    return values[0][1]


def validate_metadata(metadata: Any, require_rows: bool = True) -> dict[str, Any]:
    if not isinstance(metadata, dict) or not metadata:
        raise SchemaError("benchmark metadata must be a non-empty JSON object")
    _reject_non_finite(metadata)
    declared_rows(metadata, required=require_rows)
    return metadata


def load_metadata(path: Path, require_rows: bool = False) -> dict[str, Any]:
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SchemaError(f"{path}: unreadable JSON: {error}") from error
    return validate_metadata(metadata, require_rows=require_rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="benchmark.json files")
    parser.add_argument("--strict", action="store_true", help="require a declared raw-row count")
    args = parser.parse_args()
    for path in args.paths:
        metadata = load_metadata(path, require_rows=args.strict)
        count = declared_rows(metadata, required=False)
        detail = f"{count:,} declared rows" if count is not None else "legacy metadata; row count verified from artifacts"
        print(f"PASS {path}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
