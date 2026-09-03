# Triangle sums, peripheral cycles, and contractions for orderable cographic matroids

This directory contains a structural continuation of the projective-plane
cographic-orderability result.

- [Read or download the PDF](cographic-surface-operations.pdf)
- [LaTeX source](cographic-surface-operations.tex)
- [BibTeX citation](CITATION.bib)
- [Verification package](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (4 September 2026)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/cographic-surface-operations)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

## Main results

For a closed simplicial surface triangulation `T`, let `U(T)` mean that the
face-adjacency ordering cyclically orders every bond of its one-skeleton. The
manuscript proves:

1. a general triangle-rooted gluing theorem for compatible cographic
   orderings;
2. an exact triangle-sum criterion: `U(T1 #_triangle T2)` holds if and only if
   both `U(T1)` and `U(T2)` hold;
3. infinite families of 3-connected regular non-graphic orderable cographic
   matroids on every nonorientable genus;
4. a peripheral-cycle obstruction and an explicit Klein-bottle example showing
   that `U` is not preserved by vertex splitting;
5. descent of `U` under legal edge contraction, reducing existence on each
   fixed closed surface to finitely many irreducible triangulations.

Status: internally verified public Beta v0.1. The proof, manuscript, PDF, and
bounded verification package passed zero-trust audits. External mathematical
review remains pending.

## Reproduction

The finite checks use only Python 3's standard library. From PowerShell:

```powershell
cd verification
.\run_all.ps1 -Python python
```

The runner verifies projective-plane positive controls, examples through
nonorientable genus five, all 90 labelled single vertex splits of the frozen
Klein-bottle example, and a bounded two-step diagnostic. The last check is
reported only as a finite `NO_HIT`; it is not evidence for a general theorem.

## Scope

The manuscript gives closure, obstruction, construction, and reduction results
for the prescribed face-adjacency ordering. It does not classify all orderable
cographic matroids, prove a converse to the general rooted gluing theorem, or
claim exhaustive worldwide priority.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing, exact
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the complete disclosure.
