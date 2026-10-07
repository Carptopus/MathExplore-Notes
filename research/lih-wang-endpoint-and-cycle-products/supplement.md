# Exact finite certificates for the Lih--Wang endpoint and cycle-family results

Carptopus

Status: internal supplement; not peer reviewed

This supplement states exactly what each finite computation proves. It is part
of the proof package for the accompanying manuscript. No computation below is a
sample of matrices or parameter values standing in for an unproved continuous
claim.

## 1. Endpoint gate in orders 2 through 31

For each \(2\le n\le31\) and \(1\le j\le n\), the endpoint checker
constructs the two rational Bernstein quantities \(s_{n,j}\) and
\(d_{n,j}\) in (2.10)--(2.11) of the manuscript and proves them strictly
positive. The zeroth Bernstein layer is an identity. Thus all 495 nontrivial
layers of the universal one-collision envelope are closed exactly.

Run from the repository root:

    .\.venv\Scripts\python.exe -X utf8 loops\LIH-WANG-DIRECT-SUM-GATE-0001\verification\endpoint_threshold_guard.py

Frozen script SHA-256:

    92134EF380BB170B429C1DA581B8B120525A94004D8818636831183CDA5030B5

Expected certificate digest:

    9b857ec7f67ca6319d3cabc31c2b3f8fd88690766b51898ffbb577c155a9107e

## 2. All-transposition shared-center stars

For \(3\le n\le6\), and every permitted star degree \(2\le k<n\), the
certificate consists of exact Bernstein coefficients on the complete interval
\(0\le a\le1/k\). The verifier reconstructs the matrix from its row
description, recomputes the rook coefficients, checks the certificate, and then
changes the claimed certificate to confirm that the destructive control is
rejected. It does not import the discovery formula.

    .\.venv\Scripts\python.exe -X utf8 loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\verify_star_certificate.py --certificate loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\results\star_low_degree_certificates.json --output tmp\lih-wang-star-verification.json

Frozen SHA-256 values:

- verifier:
  6B62DABBC0E1DC8C88AF635199DC52D72A14A0CF69C981F2D281FBD227710164;
- certificate:
  1DA27D8D7B4BA33CC2F73B5FBC876958FF806509AD2357CD967394D79D12FFA5;
- independent reconstruction receipt:
  754D34F07532FD1F97FB00EB5A971762B85B04060626F4F5B7F2FFE758DEB4D5.

Order \(n=7\) is not included in these continuous certificates. It is closed
by the analytic permanent-threshold gate used in the manuscript; the same
verifier checks that threshold arithmetic only.

## 3. Shared-center orders 8 through 31

Two exact scalar certificates close the continuous parameter ranges left after
the analytic endpoint and collision reductions.

For \(8\le n\le15\), the coupled small-mean checker verifies 92 Bernstein
layers together with the four coupling gates and a control obtained by dropping
the deterministic unit term:

    .\.venv\Scripts\python.exe -X utf8 loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\coupled_small_mean_guard.py

Script SHA-256:
9F9C15EC33AC51AE7A725240E5C2D030EFFF8C75FE497F4992B1E0CC3E600DA4.
Expected digest:
fcec1ecd6696659d57cce642eaa5ca73b2736fd92c0bb8dbb0bcb60920c49a1e.

For \(16\le n\le31\), the Poisson/Bernoulli boundary checker verifies 376
Bernstein layers after proving the scalar split and monotonicity conditions:

    .\.venv\Scripts\python.exe -X utf8 loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\poisson_boundary_window_guard.py

Script SHA-256:
FA9B0396FE24441D9AA4A7C5A7871E31999AA79BB615DB1FFB2D323CCE8A1EBA.
Expected digest:
7a8f89627a7afb141eefc19f9d1d60ba4eb49bbafcdcda757ebbb1bd109c82a3.

## 4. Non-star shared-center structures in orders 3 through 7

After short-branch symmetrization, the complete non-star range has 32 support
structures. The discovery packet subdivides their full stick-breaking
parameter domains into 318 exact rational Bernstein boxes. The independent
checker reconstructs each original matrix and every required coefficient without
calling the discovery generator.

    .\.venv\Scripts\python.exe -X utf8 loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\run_small_shape_independent_window.py --packet loops\LIH-WANG-NONCUBICAL-FACES-0001\verification\results\small_shape_window_s32_v1.json --output tmp\lih-wang-small-shape-independent.json

Frozen SHA-256 values:

- discovery packet:
  E50A431535547C10B6A08FECA98F4287A7A03731150E0E3F938B8563E574EE61;
- independent checker:
  8D9F3C147BDB354EE103A9BEA04BD824F902BA39224CBE6C167C6097B5C4F84B;
- window runner:
  36E693C2AC1BE509363EE9942287576BE6ADBC33F677626C3645F5B440BBBF77;
- frozen independent receipt:
  FEEA45B5E2275A75664D51E210BC8360C00C3252203241B2423477276F4231F6.

The word “complete” here refers only to the enumerated shared-center support
structures in orders \(3\) through \(7\), after the stated symmetrization.

## 5. Scope and trust boundary

The scripts prove the finite rational statements listed above. They do not
prove:

- the universal one-collision envelope;
- the midpoint-equivalence theorem for \(n\ge32\);
- the entropy lower bound or one-hot decorrelation lemma;
- the independent-cycle product theorem;
- the analytic estimates for \(n\ge32\);
- any novelty or priority claim.

Those obligations are paid in the manuscript. The full frozen dependency list
and source hashes are recorded in
loops/LIH-WANG-PUBLICATION-PREP-0001/A1-写作前审计包.md.
