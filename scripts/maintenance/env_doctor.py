#!/usr/bin/env python3
"""Check whether the local environment can safely run Empty405-Lab research."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def diagnose(root: Path, min_free_mb: int = 1024) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("python", sys.version_info >= (3, 10), sys.version.split()[0])
    git = shutil.which("git")
    add("git", git is not None, git or "not found")
    add("repository", (root / ".git").exists(), str(root))
    add("experiments", (root / "experiments").is_dir(), str(root / "experiments"))
    add("scripts", (root / "scripts").is_dir(), str(root / "scripts"))
    add("writable", os.access(root, os.W_OK), "repository root")

    try:
        free_mb = shutil.disk_usage(root).free // (1024 * 1024)
        add("free_space", free_mb >= min_free_mb, f"{free_mb:,} MiB free; minimum {min_free_mb:,} MiB")
    except OSError as error:
        add("free_space", False, str(error))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--min-free-mb", type=int, default=1024)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks = diagnose(args.root.resolve(), args.min_free_mb)
    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        for check in checks:
            print(f"{'PASS' if check['ok'] else 'FAIL'} {check['name']}: {check['detail']}")
    return 0 if all(check["ok"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
