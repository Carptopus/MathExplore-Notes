# Realizability and minimum dimension of Fano half-rank profiles over F2

## Manuscript

- [Read or download the PDF](fano-half-rank-profiles.pdf)
- [LaTeX source](fano-half-rank-profiles.tex)
- [BibTeX citation](CITATION.bib)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (30 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data license: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let $V$ be a finite-dimensional vector space over $\mathbb F_2$ and let
$B:\mathbb F_2^3\to\mathrm{Alt}(V)$ be a linear family of alternating
bilinear forms. Its half-rank profile is

$$
h(a)=\frac12\mathrm{rank}(B_a),
\qquad a\in\mathbb F_2^3\setminus\{0\}.
$$

The manuscript classifies these labelled seven-point Fano profiles completely.
The triangle inequalities are sufficient for realizability except for seven
primitive line jumps and seven infinite parity cosets supported on singleton
faces. For every realizable profile, it also determines the minimum possible
dimension $\mu(h)$. If $t=\max h$, then $\mu(h)$ is either $2t$ or $2t+1$;
the profiles requiring the extra dimension are described by a finite list of
low-height orbits and one explicit infinite family.

## Proof and computational boundary

The infinite obstructions and the dimension lower bounds are proved using
Pfaffian parity, commuting self-adjoint idempotents, and a rank-two Pfaffian
update identity. Computation enters only through finite exact interfaces: a
Hilbert-basis certificate for the Fano triangle cone and a conductor reduction
to 812 frozen sharp bases. Fixed-seed searches locate witnesses, but every
retained witness is checked by exact binary rank and `NO_HIT` is never used as
a nonexistence proof.

## Scope and prior-work boundary

The result classifies labelled rank profiles over $\mathbb F_2$ in arbitrary
ambient dimension. It does not classify alternating-matrix spaces up to
isomorphism, treat arbitrary finite fields, or count spaces with a prescribed
profile. The closest checked literature concerns rank triples, small matrix
sizes, rank-set bounds, or orbit enumeration and does not directly provide the
seven-point realizability semigroup or its minimum-dimension function.

A targeted literature review found no direct prior statement covering the two
retained classifications. This records the checked boundary and is not a
worldwide-priority guarantee.

## Reproduction

Requirements: PowerShell 7, Python 3.11 or newer with SymPy 1.14 or a compatible
later version, and `g++` with C++17 support. From the repository root run:

```powershell
pwsh -NoProfile -File .\research\fano-half-rank-profiles\verification\run_all.ps1
```

The command must finish with
`PASS: all core Fano half-rank profile checks completed`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing,
symbolic and finite verification, adversarial auditing, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Alternating bilinear forms; alternating matrix spaces; Fano plane; rank
profiles; finite fields; Hilbert bases; minimum dimension; Pfaffians;
Reed--Muller codes; computer-assisted proof; AI-assisted mathematics.
