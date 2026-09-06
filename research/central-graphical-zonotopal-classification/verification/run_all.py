"""Run the fixed, bounded checks serially in normal and optimized modes."""
from pathlib import Path
import subprocess
import sys


def main():
    folder = Path(__file__).resolve().parent
    for script in ("verify_triangle_defect.py", "verify_gluing_interfaces.py"):
        for flags in ([], ["-O"]):
            command = [sys.executable, *flags, str(folder / script)]
            print(f"Running {script} ({'optimized' if flags else 'normal'})", flush=True)
            subprocess.run(command, cwd=folder, check=True, timeout=60)
    print("All fixed checks passed in both modes.")


if __name__ == "__main__":
    main()
