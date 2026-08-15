#!/usr/bin/env python3
"""Checkpointed validator/runner for completed Empty405-Lab experiments."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from validation.integrity_checker import validate_results_dir


@dataclass(frozen=True)
class Module:
    key: str
    path: Path


def discover(root: Path) -> list[Module]:
    experiments = root / "experiments"
    modules = []
    if not experiments.exists():
        return modules
    for benchmark in experiments.rglob("benchmark.py"):
        directory = benchmark.parent
        if (directory / "test_benchmark.py").exists() and (directory / "results" / "benchmark.json").exists():
            modules.append(Module(directory.name, directory))
    return sorted(modules, key=lambda item: item.path.as_posix())


def fingerprint(module: Module) -> str:
    digest = hashlib.sha256()
    paths = [module.path / "benchmark.py", module.path / "test_benchmark.py", module.path / "results" / "benchmark.json"]
    paths += sorted((module.path / "results").glob("*.csv.gz"))
    for path in paths:
        digest.update(path.relative_to(module.path).as_posix().encode())
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
    return digest.hexdigest()


def validate_results(module: Module) -> dict:
    return validate_results_dir(module.path / "results")


def run_command(command: list[str], cwd: Path) -> None:
    print("$", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "modules": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--state", type=Path, default=Path(".cache/research-runner/state.json"))
    parser.add_argument("--resume", action="store_true", help="skip unchanged modules that previously passed")
    parser.add_argument("--dry-run", action="store_true", help="show the queue without executing")
    parser.add_argument("--run-benchmarks", action="store_true", help="regenerate full benchmark artifacts before validation")
    parser.add_argument("--max-modules", type=int, default=0, help="0 means process every discovered module")
    parser.add_argument("--ci", action="store_true", help="disable persistent resume state")
    args = parser.parse_args()

    root = args.root.resolve()
    state_path = args.state if args.state.is_absolute() else root / args.state
    state = {"version": 1, "modules": {}} if args.ci else load_state(state_path)
    queue = discover(root)
    if args.max_modules > 0:
        queue = queue[: args.max_modules]
    print(f"discovered {len(queue)} ready experiment modules")
    if not queue:
        return 0

    processed = skipped = 0
    for index, module in enumerate(queue, 1):
        mark = fingerprint(module)
        previous = state["modules"].get(module.path.relative_to(root).as_posix(), {})
        if args.resume and previous.get("status") == "passed" and previous.get("fingerprint") == mark:
            print(f"[{index}/{len(queue)}] SKIP {module.key} (unchanged)")
            skipped += 1
            continue
        print(f"[{index}/{len(queue)}] {'PLAN' if args.dry_run else 'RUN '} {module.key}")
        if args.dry_run:
            continue
        key = module.path.relative_to(root).as_posix()
        try:
            run_command([sys.executable, "-m", "unittest", "-v", "test_benchmark.py"], module.path)
            if args.run_benchmarks:
                run_command([sys.executable, "benchmark.py"], module.path)
            report = validate_results(module)
            state["modules"][key] = {
                "status": "passed",
                "fingerprint": fingerprint(module),
                "checked_at": int(time.time()),
                **report,
            }
            if not args.ci:
                save_state(state_path, state)
            print(f"PASS {module.key}: {report['raw_rows']:,} raw rows")
            processed += 1
        except Exception as error:
            state["modules"][key] = {
                "status": "failed",
                "fingerprint": mark,
                "checked_at": int(time.time()),
                "error": str(error),
            }
            if not args.ci:
                save_state(state_path, state)
            print(f"FAIL {module.key}: {error}", file=sys.stderr)
            return 1
    print(f"complete: processed={processed}, skipped={skipped}, total={len(queue)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
