# A continuous family of counterexamples to the middle runner conjecture

## Manuscript

- [Read or download the PDF](middle-runner-counterexamples.pdf)
- [LaTeX source](middle-runner-counterexamples.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22120844](https://doi.org/10.5281/zenodo.22120844)
- Concept DOI: [10.5281/zenodo.22120843](https://doi.org/10.5281/zenodo.22120843)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (27 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

The 2015 AIM problem list allows runners with arbitrary initial positions and
conjectures a symmetry between complementary order statistics. For velocities
$(1,2,3)$ and initial positions $(0,0,a)$, let $M(a)$ be the average median
position over one common period. The manuscript proves

$$
M(a)=
\begin{cases}
\displaystyle \frac12-\frac49a\left(\frac12-a\right),
  &0\leq a\leq\frac12,\\[6pt]
\displaystyle \frac12+\frac49\left(a-\frac12\right)(1-a),
  &\frac12\leq a\leq1.
\end{cases}
$$

Modulo one, $M(a)=1/2$ only for $a=0$ and $a=1/2$. Every other offset is a
counterexample, giving two open arcs and hence an uncountable continuous
family. The rational example $a=1/4$ has ordered-position averages

$$
\left(\frac{161}{576},\frac{17}{36},\frac{431}{576}\right).
$$

## Proof and verification

The proof determines every wrap point and trajectory intersection, orders the
resulting events separately on the two half-intervals of the parameter, and
integrates the affine median piece by piece. Time reversal supplies the second
half of the formula and the endpoint cases are checked directly.

The standard-library Python verifier independently checks the rational
counterexample, a symmetry-preserving positive control, integer-translate
invariance of the initial phase, and the closed formula at 775 distinct
rational representatives with denominator at most 50. These finite checks are
supplementary evidence; the continuous statement rests on the proof.

## Scope and prior-work boundary

The result disproves the middle runner conjecture under the hypotheses printed
in the 2015 AIM problem list and exactly classifies one natural one-parameter
family. It does not classify arbitrary three-runner systems, does not address a
strengthened version requiring a common starting position, and does not propose
a replacement conjecture.

A targeted search through the exact problem wording, author and terminology
combinations, arXiv, OpenAlex, and Crossref found no direct prior counterexample
or correction. This records the search boundary rather than an exhaustive
worldwide priority claim; unindexed or differently named equivalent work may
exist.

## Reproduction

The verifier requires Python 3.9 or newer and no third-party packages. From
this entry directory, run:

```powershell
python -X utf8 verification\verify_middle_runner_counterexample.py
```

The program must print the exact counterexample and positive control, report
`closed-form offsets checked: 775`, and finish with `PASS`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature triage, exact computation, proof development and stress
testing, verification-code review, adversarial auditing, and manuscript
preparation. The manuscript contains the full disclosure and responsibility
statement.

## Keywords

Middle runner conjecture; dynamical algebraic combinatorics; circular runners;
order statistics; periodic trajectories; counterexample; piecewise integration;
exact rational verification; AI-assisted mathematics.
