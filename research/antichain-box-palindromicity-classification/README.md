# Palindromicity of antichain polynomials of three-dimensional boxes

## Manuscript

- [Read or download the PDF](antichain-box-palindromicity-classification.pdf)
- [LaTeX source](antichain-box-palindromicity-classification.tex)
- [BibTeX citation](CITATION.bib)
- DOI: pending Zenodo publication
- [Exact finite verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (29 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

For positive integers $a,b,c$, let

$$
N_{a,b,c}(x)=\sum_A x^{|A|}
$$

be the antichain generating polynomial of the product poset
$[a]\times[b]\times[c]$. After sorting $a\leq b\leq c$, the manuscript proves
the complete classification

$$
N_{a,b,c}(x)\text{ is palindromic}
\quad\Longleftrightarrow\quad
(a,b,c)=(1,r,r)\text{ or }(2,r,r+1).
$$

In particular, no three-dimensional box with $a,b,c\geq3$ has a palindromic
antichain polynomial. Combined with the known one- and two-layer cases, this
settles the rectangular minuscule branch of Ding and Dong's Conjecture B: every
palindromic case in this branch is strictly gamma-positive.

## Proof structure

Antichains are represented by nonnegative matrices with bounded last-passage
value. The proof first identifies the monic parameter range
$c=a+b-1-2d$. It then classifies every binary support one below maximum by
path-complementation and minimum-separator arguments, and counts all legal
single-cell weight increments. For $d\geq1$ this gives an exact
next-to-leading coefficient strictly below $abc$, while the remaining
$d=0$ coefficient is strictly above $abc$. The first and next-to-leading
coefficients therefore exclude palindromicity in every genuine higher-layer
case.

## Verification

Three standard-library Python programs check independent finite evidence:

- the Ding--Dong transfer recurrence, published examples, small-parameter
  palindromicity map, and coefficient formula;
- a direct complement enumerator with the mandatory counterexample to the
  retracted preliminary formula;
- an independent frontier dynamic program for the first $d=3$ cases.

These checks calibrate formulas and boundary cases. The all-parameter result
rests on the proof in the manuscript.

## Scope and prior-work boundary

Ding and Dong established the last-passage representation and formulated the
minuscule gamma-positivity conjecture. Amanov and Yeliussizov supplied the
plane-partition formulation used here. The previously released two-layer
paper classifies $[2]\times[m]\times[n]$ and proves strict gamma-positivity in
the adjacent cases. The new contribution is the general exclusion of all
$a,b,c\geq3$ and hence the complete palindromicity classification above.

A targeted literature review found no direct prior proof of this retained
higher-layer classification. This records the search boundary and is not an
exhaustive worldwide-priority guarantee.

## Reproduction

Using Python 3.11 or newer, run from this entry directory:

```powershell
python -X utf8 .\verification\scan_rectangular_boxes.py
python -X utf8 .\verification\verify_next_to_leading.py
python -X utf8 .\verification\verify_lpp_frontier.py
```

Each command must finish with a `PASS` line.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing,
symbolic and finite verification, adversarial auditing, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Antichain generating polynomial; palindromicity; gamma-positivity; minuscule
poset; product of chains; plane partition; last-passage percolation; lattice
path; vertex separator; combinatorics; AI-assisted mathematics.
