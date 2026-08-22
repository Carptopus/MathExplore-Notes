# Attainable second support weights of binary second-order Reed--Muller codes

## Manuscript

- [Read or download the PDF](rm2-second-support-spectrum.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22059063](https://doi.org/10.5281/zenodo.22059063)
- [LaTeX source](rm2-second-support-spectrum.tex)
- [Verification code](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.2-beta (22 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- SHA-256 checksum-manifest license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $RM_2(2,n)$ be the binary Reed--Muller code obtained by evaluating Boolean
polynomials of degree at most two on $F_2^n$. For a two-dimensional subcode
$D=\langle f,g\rangle$, its support size is

$$
\mathrm{wt}(D)
=\frac{\mathrm{wt}(f)+\mathrm{wt}(g)+\mathrm{wt}(f+g)}2.
$$

The manuscript determines, for every $n$, the exact set

$$
\mathcal S_n
=\{\mathrm{wt}(D):D\le RM_2(2,n),\ \dim D=2\}.
$$

For even dimension $n=2m$, the answer is an explicit finite compatibility
system for the three zero-frequency Walsh coefficients and polar ranks of the
nonzero members of the quadratic pencil $\{f,g,f+g\}$. Every candidate value
allowed by that system is realized by an explicit finite-atom construction.
For odd dimensions the spectrum satisfies

$$
\mathcal S_{2m+1}=2\mathcal S_{2m}.
$$

The low-dimensional cases are

$$
\mathcal S_1=\{2\},\qquad
\mathcal S_2=\{2,3,4\},\qquad
\mathcal S_3=\{3,4,5,6,7,8\}.
$$

## Proof outline

- Fourier inversion expresses the four common fibers of $(f,g)$ through the
  three zero-frequency Walsh coefficients.
- The Walsh spectrum of affine quadratic functions and rank inequalities for
  alternating polar forms give the finite compatibility conditions.
- Warning's second theorem and the second generalized Hamming weight provide
  the required fiber and support lower bounds.
- A rank-lowering lemma, two- and four-variable quadratic atoms, an even-value
  descent, and three odd normal forms prove sufficiency.
- Adding one ignored variable proves the odd-dimensional doubling relation.

## Scope and prior-work boundary

The result determines which support values occur. It does not determine the
number of two-dimensional subcodes attaining each value, classify quadratic
pencils up to equivalence, or treat arbitrary collections of codewords.

The Walsh theory of one quadratic Boolean function, fixed-pencil common-zero
formulas, degenerate pencil members, order/type mechanisms, sharp bounds,
extremal constructions, alternating-matrix rank-triple counts, and homogeneous
Boolean quadratic rank types are prior work. The closest sources include
Leep--Schueller (1999), Fitzgerald--Yucas (2004), Pott--Schmidt--Zhou (2016),
and Hodges--Iyer (2022). The candidate new contribution is narrower: the union
of all attainable affine support values across all pairs in every binary
dimension, including zero-frequency Walsh signs and fibers, together with a
uniform sufficiency proof. Absolute priority remains qualified pending broader
public and expert review.

## Reproduction

The verification programs require Python 3.11 or newer and use only the
standard library. From this entry directory, run:

```powershell
python -X utf8 verification/verify_second_support_spectrum.py
python -X utf8 verification/verify_explicit_walsh_atoms.py
python -X utf8 verification/verify_normal_form_obligations.py
python -X utf8 verification/probe_walsh_atom_semigroup.py
```

The first three programs are bounded verification and falsification controls.
The last program is explicitly a discovery/calibration probe. No finite run is
used to infer the all-dimension theorem; generality comes from the symbolic
proof in the manuscript.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Reed--Muller code; second support weight; higher weight spectrum; quadratic
Boolean function; Walsh spectrum; quadratic pencil; common-zero count;
alternating polar form; generalized Hamming weight; computer-assisted
mathematics.
