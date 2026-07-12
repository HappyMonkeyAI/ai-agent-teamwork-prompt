#!/usr/bin/env python3
"""Run validation lanes selected from Git-changed paths."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from fnmatch import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def load_config(path: Path) -> list[dict]:
    """Load and validate the deliberately small, shell-free config schema."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid config: {error}") from error
    if not isinstance(data, dict) or set(data) != {"version", "lanes"}:
        raise ValueError("config must contain only version and lanes")
    if data["version"] != 1 or not isinstance(data["lanes"], list):
        raise ValueError("version must be 1 and lanes must be an array")
    names: set[str] = set()
    for lane in data["lanes"]:
        if not isinstance(lane, dict):
            raise ValueError("each lane must be an object")
        if not isinstance(lane.get("command"), list):
            raise ValueError("lane command must be an argv array, not a shell string")
        if set(lane) != {"name", "paths", "command"}:
            raise ValueError("lane keys must be exactly name, paths, and command")
        if (
            not isinstance(lane["name"], str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", lane["name"])
            or len(lane["name"]) > 64
            or lane["name"] in names
        ):
            raise ValueError("lane names must be non-empty and unique")
        names.add(lane["name"])
        for key in ("paths", "command"):
            if not lane[key] or not all(isinstance(value, str) and value for value in lane[key]):
                raise ValueError(f"lane {key} must be a non-empty string array")
    return data["lanes"]


def select_lanes(lanes: list[dict], changed_paths: list[str]) -> list[dict]:
    """Return configured lanes whose path globs match at least one changed path."""
    return [
        lane
        for lane in lanes
        if any(fnmatch(path, pattern) for path in changed_paths for pattern in lane["paths"])
    ]


def git_changed_paths(repo: Path, base: str) -> list[str]:
    """Return base-relative tracked changes plus untracked files."""
    changed = subprocess.run(
        ["git", "diff", "--name-only", "-z", "--diff-filter=ACDMRTUXB", base, "--"],
        cwd=repo, capture_output=True, check=True,
    ).stdout.split(b"\0")
    untracked = subprocess.run(
        ["git", "ls-files", "-z", "--others", "--exclude-standard"],
        cwd=repo, capture_output=True, check=True,
    ).stdout.split(b"\0")
    return list(dict.fromkeys(os.fsdecode(path) for path in changed + untracked if path))


def run_lane(repo: Path, log_dir: Path, lane: dict) -> tuple[str, int, Path]:
    log_path = log_dir / f"{lane['name']}.log"
    try:
        result = subprocess.run(lane["command"], cwd=repo, text=True, capture_output=True)
        output = result.stdout + result.stderr
        return_code = result.returncode
    except OSError as error:
        output = f"unable to execute {lane['command'][0]}: {error}\n"
        return_code = 127
    log_path.write_text(output, encoding="utf-8")
    return lane["name"], return_code, log_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD", help="Git base ref (default: HEAD)")
    parser.add_argument(
        "--config", type=Path,
        default=Path(__file__).parents[1] / "templates" / "checks.json",
        help="validation lane JSON config",
    )
    args = parser.parse_args(argv)
    repo = Path.cwd()
    try:
        lanes = load_config(args.config)
        changed = git_changed_paths(repo, args.base)
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    selected = select_lanes(lanes, changed)
    if not selected:
        print(f"SKIP no lanes selected ({len(changed)} changed files)")
        return 0
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    log_dir = repo / ".tmp" / "check-runs" / run_id
    log_dir.mkdir(parents=True)
    with ThreadPoolExecutor(max_workers=len(selected)) as executor:
        results = list(executor.map(lambda lane: run_lane(repo, log_dir, lane), selected))
    for name, return_code, log_path in results:
        status = "PASS" if return_code == 0 else "FAIL"
        print(f"{status} {name} (exit {return_code}) log={log_path.relative_to(repo)}")
    failures = sum(return_code != 0 for _, return_code, _ in results)
    print(f"SUMMARY {len(results) - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
