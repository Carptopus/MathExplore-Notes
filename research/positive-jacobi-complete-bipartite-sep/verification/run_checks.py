"""Run the four fixed checks serially, with a 300-second limit per child.

No network, installation, user parameter grid, automatic retry, or batch search.
Use `python -O run_checks.py` to run all children with optimization enabled.
"""
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
CHECKS = ('check_k4n_jacobi.py', 'check_k5n_jacobi.py',
          'verify_second_tail_positive_kernel.py', 'check_original_ehrhart.py')
TIMEOUT_SECONDS = 300


def main():
    if len(sys.argv) != 1:
        raise SystemExit('This runner accepts no parameter or workload arguments')
    for name in CHECKS:
        start = time.monotonic()
        command = [sys.executable, '-X', 'utf8']
        if sys.flags.optimize:
            command.append('-O')
        command.append(str(HERE / name))
        print('RUN ' + name, flush=True)
        try:
            completed = subprocess.run(command, cwd=HERE, timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            raise SystemExit(f'TIMEOUT {name}; no mathematical conclusion; no retry')
        if completed.returncode:
            raise SystemExit(f'FAILED {name}: exit {completed.returncode}; remaining checks not run')
        print(f'OK {name}: {time.monotonic()-start:.2f}s', flush=True)
    print('PASS: all four fixed entries; general claims have the scope stated in the manuscript', flush=True)


if __name__ == '__main__':
    main()
