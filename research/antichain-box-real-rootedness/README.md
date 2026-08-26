# Real-rootedness, palindromicity, and gamma-positivity of antichain polynomials for [2] x [m] x [n]

## Manuscript

- [Read or download the PDF](antichain-box-real-rootedness.pdf)
- [LaTeX source](antichain-box-real-rootedness.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22115309](https://doi.org/10.5281/zenodo.22115309)
- Concept DOI: [10.5281/zenodo.22112708](https://doi.org/10.5281/zenodo.22112708)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.2-beta (27 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main results

For all positive integers $m,n$, let

$$
N_{[2]\times[m]\times[n]}(x)=\sum_A x^{|A|}
$$

be the antichain generating polynomial of the product poset. The manuscript
proves:

1. every zero of this polynomial is real and negative, proving Ding and
   Dong's Conjecture 4.3;
2. the polynomial is palindromic if and only if $|m-n|=1$; and
3. in precisely these adjacent-parameter cases, all gamma coefficients are
   strictly positive.

The latter two conclusions prove Ding and Dong's Conjecture 4.5 and verify
their general gamma-positivity conjecture for the complete subfamily
$k=2$, $P=[m]\times[n]$.

The manuscript also proves the previously unproved $2\times2$ determinantal
formula found experimentally by He, Langner, and Witek for the associated
Zhang--Zhang polynomial, after making the required unit variable shift
explicit.

## Proof structure

Antichains are encoded by pairs of balanced two-rowed arrays. A canonical
two-gap tail switch gives a weight-preserving bijection between crossing pairs
and the two off-diagonal determinant classes, proving the determinant formula
for all positive $m,n$, including boundary cases.

After the Möbius substitution $t=(1+x)/(1-x)$, the determinant factors into
two linear combinations of adjacent Jacobi polynomials. Strict interlacing and
explicit endpoint signs place all finite zeros in $(-1,1)$; transforming back
places every zero of the antichain polynomial in $(-\infty,0)$.

For palindromicity, the proof first derives the necessary degree condition and
then uses the adjacent Jacobi symmetry to establish sufficiency. Negative real
roots occur in reciprocal pairs, while an explicit nonzero value at $x=-1$
rules out a central factor; this makes every gamma coefficient strictly
positive.

## Verification

The supplied programs independently check two evidence layers:

- `verification/verify.py` checks exact enumeration, the tail-switching
  bijection and inverse, Jacobi identities, transformed factorizations,
  negative-real-root calibration, and two destructive controls;
- `verification/verify_palindromicity.py` checks the Jacobi symmetry identities,
  the palindromicity classification on 144 parameter pairs, strict gamma
  coefficients in 20 adjacent cases, the exact signed value at $x=-1$, and
  square/gap-two destructive controls.

These finite checks guard the implementation and boundary cases; the general
claims rest on the proofs in the manuscript.

## Scope and prior-work boundary

The theorem gives a complete result for the two-layer product
$[2]\times[m]\times[n]$. It does not claim a corresponding classification for
$[k]\times[m]\times[n]$ with $k>2$.

Ding and Dong's necessary condition already implies that palindromicity in the
two-layer rectangular family can occur only when $|m-n|=1$. The new contribution
is the converse, the exact if-and-only-if classification, and strict gamma
positivity in every adjacent case, combined with the real-rootedness and
determinantal results already released in v0.1.

A targeted search found no direct prior proof of the retained new claims. This
records the search boundary; it is not a claim of exhaustive worldwide
priority.

## Reproduction

With Python 3.11 or newer and SymPy 1.14.0 installed, run from this entry
directory:

```powershell
python -m pip install -r verification\requirements.txt
python -X utf8 verification\verify.py
python -X utf8 verification\verify_palindromicity.py
```

Both programs must complete successfully and report `PASS`. Their finite
calibration does not replace the general proof.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature triage, proof development and stress testing, exact finite
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the full disclosure and responsibility statement.

## Keywords

Antichain generating polynomial; real-rooted polynomial; palindromicity;
gamma-positivity; product poset; Jacobi polynomial; lattice path;
tail-switching bijection; Zhang--Zhang polynomial; extended strict order
polynomial; combinatorics; AI-assisted mathematics.
