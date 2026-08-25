# Verification

This directory contains the exact finite-graph verification package for the
first two Abelian-border threshold layers.

## Environment

- Python 3.11 or newer;
- NetworkX 3.6.1;
- optional C++17 compiler for the independent graph implementations;
- no random seed, floating-point decision or external dataset.

The pinned Python dependency is recorded in `requirements.txt`.

## Python checks

From the project entry directory, run:

```powershell
python -X utf8 verification\verify.py
python -X utf8 verification\verify_period_bounds.py
```

The first command checks the Abelian-border definition on all 131,070
nonempty binary words of length at most 16, independent small graphs, the two
full overlap graphs, the four closed-phase certificates and the frozen source
hashes. The second command reconstructs every nonbranching cycle and verifies
the sharp ordinary and Abelian period bounds.

Both commands must print `"status": "VERIFIED"` and exit with code 0. Their
fixed summaries are in `results/threshold-certificates.txt` and
`results/period-bound-certificates.txt`.

## Independent C++ graph implementations

With `g++` available:

```powershell
g++ -std=c++17 -O2 -Wall -Wextra -pedantic verification\verify_threshold14.cpp -o verify_threshold14.exe
g++ -std=c++17 -O2 -Wall -Wextra -pedantic verification\verify_threshold15.cpp -o verify_threshold15.exe
.\verify_threshold14.exe
.\verify_threshold15.exe
```

Their graph counts and closed-phase data must agree with the fixed result
files. The executables are generated artifacts and are not distributed.

## Evidence boundary

The programs exhaust finite overlap graphs. The manuscript separately proves
that every infinite word satisfying the threshold hypothesis yields an
infinite graph path and that the certified recurrent components force the
claimed eventual periodicity. Passing the programs does not replace that
mathematical reduction or external peer review.

The code is licensed under MIT; fixed result files are dedicated under CC0
1.0.
