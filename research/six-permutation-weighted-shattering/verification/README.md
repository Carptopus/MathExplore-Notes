# Exact verification

The verification script stores the six rank maps of the published 26-point
template and the certified integer weight vector. It checks:

- that the template shatters exactly 1446 of the 2600 triples;
- that the weights sum to 250;
- the exact values of \(A\) and \(B\);
- the bound \(1288385/2599242\);
- its strict improvement over \(482/975\).

Run from the repository root:

~~~powershell
pwsh -NoProfile -File .\research\six-permutation-weighted-shattering\verification\run_all.ps1
~~~

The script uses only the Python standard library. It certifies the finite
template and exact arithmetic; the general weighted recursion theorem is proved
in the manuscript.

