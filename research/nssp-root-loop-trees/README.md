# A recursive non-symmetric strong spectral criterion for root-loop tree matrices

## Manuscript

- [Read or download the PDF](nssp-root-loop-trees.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22045532](https://doi.org/10.5281/zenodo.22045532)
- [LaTeX source](nssp-root-loop-trees.tex)
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

Let $(T,r)$ be a finite rooted tree. Consider a real matrix $A$ whose nonzero
off-diagonal positions are exactly both directed entries on every edge of
$T$, whose root diagonal entry is nonzero, and whose remaining diagonal
entries are zero. For each child $c$ of a vertex $v$, let $F_c(x)$ be the
characteristic polynomial of the complete descendant subtree rooted at $c$.

The manuscript proves

$$
A\text{ has the nSSP}
\quad\Longleftrightarrow\quad
\{F_c:c\text{ is a child of }v\}
\text{ is pairwise coprime for every }v.
$$

Equivalently, $A$ fails the non-symmetric strong spectral property exactly
when two sibling subtrees share an eigenvalue over $\mathbb C$.

## Proof outline

- A rooted-tree determinant recurrence reduces all directional edge weights
  to their two-way products.
- Recursive PBH arguments show that the root vector of every child subtree is
  cyclic when sibling spectra are disjoint.
- Exact first-order recovery of all edge products makes the reduced
  characteristic-coefficient Jacobian nonsingular.
- A deepest common spectral factor produces an explicit nonzero real
  pattern-zero centralizer, including zero, nonreal, and repeated roots.

The result permits arbitrary non-symmetric real weights, negative edge
products, repeated roots inside one subtree, nonreal shared-root witnesses,
and arbitrarily many nested branch vertices.

## Relation to the preceding results

At the fixed-matrix level, this theorem forms the progression

    single-loop double path
      -> root-loop spider
      -> arbitrary rooted tree.

It strictly contains the fixed-matrix criteria in the earlier
[looped-double-path](../nssp-looped-double-paths/README.md) and
[root-loop-spider](../nssp-root-loop-spiders/README.md) Betas. The earlier
classification of arbitrary loop assignments on double paths has different
pattern-level quantifiers and remains an independent result.

## Scope and boundary

This is a criterion for each fixed root-loop bidirected tree matrix. It is not
a classification of all tree patterns that allow or require nSSP.

The zero nonroot diagonal assumption is a genuine boundary of this criterion.
For the endpoint-rooted path on three vertices,

$$
A=\begin{pmatrix}1&1&0\\1&0&1\\0&1&1\end{pmatrix},
\qquad
X=A^2-A-I=
\begin{pmatrix}0&0&1\\0&1&0\\1&0&0\end{pmatrix},
$$

the recursive coprimality condition is vacuous, but $X=X^{\mathsf T}\ne0$,
$A\circ X=0$, and $AX^{\mathsf T}=X^{\mathsf T}A$. Thus the same sufficient
criterion does not extend to arbitrary fixed nonroot diagonal entries. This
does not assert that every additional loop destroys nSSP or that no more
elaborate multi-loop criterion exists.

The nSSP/transversality framework, the general
characteristic-Jacobian-to-nSSP bridge, Duarte and NEB recursions,
generalized-star and linear-tree inverse spectral methods, PBH cyclicity, and
the tree characteristic-polynomial recurrence are prior tools.
Global priority remains qualified pending broader public and expert review.

The bottom-up decision procedure is an exact symbolic algorithm only when the
entries belong to an effective exact field with exact zero testing, such as
$\mathbb Q$ or an explicitly represented algebraic-number field. It is not a
numerical guarantee for arbitrary floating-point real inputs.

## Reproduction

The verification programs require Python 3.11 or newer, use only the standard
library, and do not require network access or a computer algebra system.
From this entry directory, run:

    python -X utf8 verification/verify_recursive_tree_criterion.py --max-vertices 7 --samples 2
    python -X utf8 verification/verify_collision_witness.py
    python -X utf8 verification/verify_minimal_counterexample.py

The standard calibration covers 1746 rooted-tree cases through seven
vertices. All 366 recursively coprime cases have full verification rank
modulo 1000003, and none of the 1380 noncoprime cases has modular full rank.
Six targeted cases add exact rational elimination and independent
Newton--trace polynomial checks.

The collision-witness program constructs and checks exact rational
centralizers for a deepest shared zero root and a deepest shared factor
$x^2-1$. The boundary program checks the displayed three-vertex witness,
recomputes its exact rank as $2/3$, and verifies two rank-$3/3$ destructive
controls.

Modular full rank certifies full rank over the rationals and reals for the
displayed integer matrix. Modular rank loss alone does not prove rational rank
loss. These finite checks calibrate the proof and do not replace its general
argument or independent review.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Non-symmetric strong spectral property; nSSP; inverse eigenvalue problem;
rooted tree matrix; root-loop tree; bidirected tree; mixed edge products;
recursive characteristic polynomials; pairwise coprimality; spectral
collision; cyclic vector; centralizer witness; Jacobian method;
computer-assisted mathematics.
