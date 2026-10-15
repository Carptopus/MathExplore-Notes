"""Run the frozen public regression controls sequentially."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    scripts = sorted(ROOT.glob("check_*.py"))
    if not scripts:
        raise RuntimeError("no verification scripts found")
    for script in scripts:
        print(f"==> {script.name}", flush=True)
        subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT)
    print(f"PASS: {len(scripts)} verification scripts", flush=True)


if __name__ == "__main__":
    main()
