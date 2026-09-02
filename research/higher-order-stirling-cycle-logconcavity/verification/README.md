# Verification programs

These programs reproduce the symbolic identities, exact rational certificates, analytic
constants, and finite-prefix computation used in the manuscript.

## Environment

- Reference interpreter: CPython 3.13.11
- Reference symbolic package: SymPy 1.14.0
- PowerShell 7 for the aggregate runner

Create or select a Python environment containing SymPy 1.14.0, then run from the
repository root:

~~~powershell
pwsh -NoProfile -File .\research\higher-order-stirling-cycle-logconcavity\verification\run_all.ps1
~~~

To select an explicit interpreter:

~~~powershell
pwsh -NoProfile -File .\research\higher-order-stirling-cycle-logconcavity\verification\run_all.ps1 `
  -Python D:\path\to\python.exe
~~~

A nonzero exit code is a failure even if an earlier program printed a `PASS` line.

## Claim-to-certificate map

| Manuscript obligation | Program |
| --- | --- |
| (2.5)--(2.7), normalized rows | `verify_normalized_logconcavity.py` |
| (4.4)--(4.5), weighted cone | `verify_r4_weighted_cone.py` and `probe_stirling_logconcavity.py` |
| Lemma 7.1 and (7.7)--(7.11) | `verify_two_step_lc_preserver.py` |
| finite boundary strips in Lemma 7.3 | `verify_small_excess_strips.py` |
| Lemma 7.2 | `verify_sparse_cycle_k2.py` |
| (8.7), saddle curvature | `verify_saddle_curvature.py` |
| first-order cancellation and (8.6) | `verify_bulk_edgeworth_margin.py` |
| (8.9)--(8.10), orders two through five | `verify_bulk_second_order_margin.py` through `verify_bulk_fifth_order_margin.py` |
| (9.9)--(9.11), renewal envelope | `verify_renewal_reformulation.py` |
| (9.5)--(9.6), low-cumulant bounds | `verify_low_cumulant_envelope.py` |
| (9.12)--(9.15), characteristic-function constants | `verify_characteristic_tail_constants.py` |
| (9.15)--(9.25), effective remainder | `verify_effective_fourier_remainder.py` |
| (10.1)--(10.2), finite prefix | `verify_bulk_finite_prefix.py` |

The fifth-order Bernstein certificate is the longest symbolic step; the recorded audit
required about 27 minutes. The finite-prefix program visits 5,754,989 points. Runtime is
not part of the mathematical claim.

The programs are licensed under [MIT](LICENSE-CODE-MIT.txt).

## Recorded release run

The complete aggregate runner was executed from this copied public directory on
2 September 2026 with CPython 3.13.11 and SymPy 1.14.0. It finished with

~~~text
PASS: certified compact-bulk prefix checks=5754989
PASS: all higher-order Stirling cycle log-concavity certificates verified
~~~

The minimum finite-prefix slack was
`0.000032205417799388957039776739958609472` at `(k,d)=(1000,1868)`.
