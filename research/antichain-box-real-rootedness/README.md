# Real-rootedness of antichain polynomials for [2] x [m] x [n]

## Manuscript

- [Read or download the PDF](antichain-box-real-rootedness.pdf)
- [LaTeX source](antichain-box-real-rootedness.tex)
- [BibTeX citation](CITATION.bib)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (26 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main results

For all positive integers $m,n$, let

$$
N_{[2]\times[m]\times[n]}(x)=\sum_A x^{|A|}
$$

be the antichain generating polynomial of the product poset. The manuscript
proves that every zero of this polynomial is real and negative. This proves
Conjecture 4.3 of Ding and Dong (arXiv:1905.06692).

It also proves the previously unproved $2\times2$ determinantal formula found
experimentally by He, Langner, and Witek for the associated Zhang--Zhang
polynomial, after making the required unit variable shift explicit.

## Proof structure

Antichains are encoded by pairs of balanced two-rowed arrays. A canonical
two-gap tail switch gives a weight-preserving bijection between crossing pairs
and the two off-diagonal determinant classes, proving the determinant formula
for all positive $m,n$, including boundary cases.

After the Möbius substitution $t=(1+x)/(1-x)$, the determinant factors into
two linear combinations of adjacent Jacobi polynomials. Strict interlacing and
explicit endpoint signs place all finite zeros in $(-1,1)$; transforming back
places every zero of the antichain polynomial in $(-\infty,0)$.

## Verification

The supplied Python program independently checks:

- exact antichain enumeration against the determinant for 16 parameter pairs;
- the tail-switch bijection and canonical inverse on 5,226 negative objects;
- a deliberately incorrect off-diagonal index and a noncanonical inverse cut;
- Jacobi connection identities for 36 parameter pairs;
- exact transformed factorizations for 20 parameter pairs; and
- numerical negative-real-root calibration for 49 parameter pairs.

These finite checks guard the implementation and boundary cases; the general
claim rests on the proof in the manuscript.

## Scope and prior-work boundary

The theorem covers the two-layer product $[2]\times[m]\times[n]$. It does not
claim a corresponding theorem for $[k]\times[m]\times[n]$ with $k>2$, nor
does it address the separate gamma-positivity conjecture for a related family.

A targeted search of the original conjecture, the determinantal paper, the
$O(2,m,n)$ literature, and extended strict order-polynomial work found no
direct prior proof of either main theorem. This records the search boundary;
it is not a claim of exhaustive worldwide priority.

## Reproduction

With Python 3.11 or newer and SymPy 1.14.0 installed, run from this entry
directory:

```powershell
python -X utf8 verification\verify.py
```

All seven positive checks must print `PASS`; the final `BOUNDARY` line states
that finite calibration does not replace the general proof.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature triage, proof development and stress testing, exact finite
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the full disclosure and responsibility statement.

## Keywords

Antichain generating polynomial; real-rooted polynomial; product poset;
Jacobi polynomial; lattice path; tail-switching bijection; Zhang--Zhang
polynomial; extended strict order polynomial; combinatorics; AI-assisted
mathematics.
