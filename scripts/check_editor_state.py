#!/usr/bin/env python3
"""Run quick workspace checks: ruff, mypy, black --check.

This script follows the editor-friendly typing patterns from python/SKILL.md.
"""
from __future__ import annotations

import sys
import subprocess
from typing import List


def run_cmd(args: List[str]) -> int:
    print("Running:", " ".join(args))
    rc = subprocess.run(args).returncode
    if rc != 0:
        print(f"Command {' '.join(args)} failed with exit code {rc}")
    return rc


def main() -> int:
    checks = [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "mypy", "."],
        [sys.executable, "-m", "black", "--check", "."],
    ]
    exit_codes: List[int] = []
    for cmd in checks:
        rc = run_cmd(cmd)
        exit_codes.append(rc)
    # return 0 only if all checks passed
    return 0 if all(rc == 0 for rc in exit_codes) else 1


if __name__ == "__main__":
    sys.exit(main())
