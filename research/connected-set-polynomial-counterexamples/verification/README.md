# Verification

The verification program checks four logically distinct claims:

1. the closed coefficient formula for all four graph families through `d=64`;
2. agreement with direct graph computation for the finite calibration range;
3. absence of eligible counterexamples through order seven using the NetworkX graph atlas;
4. the complete order-eight classification using Brendan McKay's official connected-graph catalogue.

## Requirements

- Python 3.13 or compatible;
- NetworkX 3.6.1;
- PowerShell 7 for the wrapper command.

The project environment already provides these requirements. No external solver is used.

## Order-eight catalogue

Download `graph8c.g6` from:

<https://users.cecs.anu.edu.au/~bdm/data/graph8c.g6>

Expected SHA-256:

```text
0002354F1AB3344A2706626A037AD15367BF23A2163AA68F552C3A169CA9A036
```

The verifier rejects a catalogue with any other digest.

## Complete run

From the repository root:

```powershell
pwsh -NoProfile -File .\research\Connected-Set-Polynomial-Counterexamples\verification\run_all.ps1 `
  -Graph8Catalog <path-to-graph8c.g6>
```

The expected catalogue totals are 11,117 connected graphs, 11,094 satisfying the edge condition,
and exactly four nonunimodal classes. The program also checks that those four classes are the first
members of the four stated infinite families.

## Evidence boundary

The catalogue scan proves the finite minimum-order classification only after accepting the frozen
catalogue source and the verifier implementation. The infinite families and their nonunimodality
are established by the manuscript's symbolic rooted-block decomposition; the finite scan is not a
substitute for that proof.

