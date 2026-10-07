# Bounded verification package

This package checks fixed finite controls for the manuscript. General theorems are proved in the manuscript, not inferred from these runs. It needs Windows and Python 3.10 or newer, using only the standard library. It does not install packages, contact a service, run randomized discovery, or enumerate an unrestricted base-intersection graph.

From this directory:

```powershell
<path-to-python.exe> -B -X utf8 run_all.py
```

In the MathExplore working checkout the interpreter is `.venv\Scripts\python.exe`, invoked from the repository root with the full script path. Use normal Python, not `-O` or `-OO`; optimized-mode execution is explicitly rejected by the entry point and the assertion-based binary checker.

## Scope

- `check_connection_law.py`: fixed small base families, exact enumeration of all additions, uniform incidence budgets, and the nonmatroid P6 negative control; at most 12 base vertices.
- `check_cover_frontier.py`: fixed rank-two and rank-three matroids, direct selected-family enumeration against the coverage and domination frontiers; at most 7 elements and 12 bases. Both normalization branches are required.
- `laminar_solver.py` and `check_deepening.py`: capacity-tree DP, output construction, independent small subset/rank and family-enumeration reference, paving controls, nested-constraint and crossing-input rejection, and a forced incidence-cycle positive control. The solver accepts at most 64 explicit elements and 192 tree nodes; small-reference enumeration is capped at 8 elements, 12 graph vertices, 96 fixtures and 250,000 selected families. Loops are deliberately rejected by this implementation; the theorem permits deleting them first.
- `simple_rank4_q5.json`: a 32-element optimal-output control. Feasibility, coverage, distinctness and connectivity are checked; global optimality follows from the manuscript's sharp example, not an exhaustive graph search.
- `verify_fixed_witnesses.py` and `results/fixed_simple_binary.json`: independent row elimination for the d=5 and d=8 binary witnesses, all nonzero-functional supports and cocircuit detection, base legality, coverage/shared elements and four corruptions. This does not enumerate all base families. It imports only `resource_guard.py`, not the discovery probe or the witness-construction implementation.

The runner executes commands serially, with an outer 55-second timeout per command and no retry. Internal checks use a 45-second time gate and a 256 MiB current process working-set/private-memory gate; size limits are checked before large loops. The limits are implementation safety contracts, not mathematical bounds. The runner prints JSON to stdout and leaves the published fixed inputs unchanged.

## Provenance

The laminar solver, its fixed functional checker and its 32-element input are copied from the frozen internal verification files. The two small connection/frontier checkers have additional resource calls but unchanged mathematical logic. The binary checker retains its independent elimination logic and fixed input while its resource import is decoupled from discovery. All public-package copies receive a fresh serial guard run; historical runs are not substituted for it.

Python code: [MIT license](LICENSE-CODE-MIT.txt). Fixed witness data: CC BY 4.0. Hashes are listed in the package manifest when the delivery bundle is frozen.
