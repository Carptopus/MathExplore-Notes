"""Run and freeze all finite calibration checks for the public entry."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def run(script: str, *arguments: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    two_adic = run(
        "verify_two_adic_obstruction.py",
        "--output",
        str(RESULTS / "two-adic-obstruction.json"),
    )
    split_lines = run("verify_split_eigenlines.py")
    (RESULTS / "split-eigenlines.json").write_text(
        json.dumps(split_lines, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    split_obstruction = run("verify_split_antipodal_obstruction.py")

    expected = {
        "two_adic": "PASS_FINITE_VALUATION_CALIBRATION",
        "split_eigenlines": "PASS_SPLIT_EIGENLINE_BOUNDARY",
        "split_obstruction": "PASS",
    }
    actual = {
        "two_adic": two_adic["status"],
        "split_eigenlines": split_lines["status"],
        "split_obstruction": split_obstruction["status"],
    }
    if actual != expected:
        raise AssertionError({"expected": expected, "actual": actual})

    print(json.dumps({"status": "PASS", "checks": actual}, indent=2))


if __name__ == "__main__":
    main()
