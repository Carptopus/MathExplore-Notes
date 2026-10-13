"""Run the frozen verification suite in a deterministic serial order."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


SCRIPTS = (
    "check_chi_field_random_walk_reduction.py",
    "check_exact_whitened_mgf.py",
    "check_explicit_characteristic_modulus.py",
    "check_explicit_log_remainder.py",
    "check_edgeworth_positive.py",
    "check_s42_effective_low_frequency.py",
    "check_s43_low_frequency_derivatives.py",
    "check_s44_effective_tail.py",
    "check_s47_complex_cauchy_ledger.py",
)


def main() -> None:
    verification_dir = Path(__file__).resolve().parent
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for script in SCRIPTS:
        print(f"RUN {script}", flush=True)
        subprocess.run(
            [sys.executable, "-B", str(verification_dir / script)],
            cwd=verification_dir,
            env=environment,
            check=True,
        )
    print("PASS: all frozen verification scripts completed", flush=True)


if __name__ == "__main__":
    main()

