# Compatible orderings of binary vector spaces

## Manuscript

- [Read or download the PDF](binary-compatible-orderings.pdf)
- [LaTeX source](binary-compatible-orderings.tex)
- [BibTeX citation](CITATION.bib)
- [Exact four-dimensional verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (31 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data license: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

A total order on a finite vector space is *compatible* when the unique
order-preserving bijection between any two subspaces of the same dimension is
linear. For every `n >= 4`, the manuscript proves that compatible total orders
on the binary vector space `F_2^n` form exactly eight orbits under `GL(n,2)`.
Consequently, their labelled number is

$$
8|\mathrm{GL}(n,2)|
=8\prod_{i=0}^{n-1}(2^n-2^i).
$$

Four orbits have zero as their least element. They are represented by two
explicit flag-order families and the reversals of their nonzero parts; full
order reversal gives the other four. The counts in dimensions one, two and
three are respectively `2`, `12` and `10080`.

## Proof and computational boundary

The only computer-assisted proof obligation is an exhaustive, symmetry-broken
classification in dimension four. Two implementations use different complete
invariants for ordered Fano planes and return the same four normalized
representatives. They share the necessary linear normalization and prefix-search
architecture, so the second is an invariant-level cross-check rather than a
fully independent search design.

The general theorem is mathematical: a local line condition forces an initial
complete flag, and a unique-lift lemma propagates each of the two relevant
three-dimensional types through all higher dimensions.

## Scope

The result answers the compatible-order counting problem over the binary field.
It does not classify compatible orders over fields with more than two elements.
The literature comparison covers Cameron's original notes and the BCC30 problem
statement; it does not claim that unpublished or unindexed parallel work cannot
exist.

## Reproduction

Requirements: PowerShell 7 and Python 3.10 or newer. No third-party Python
package is required. From the repository root run:

~~~powershell
pwsh -NoProfile -File .\research\binary-compatible-orderings\verification\run_all.ps1
~~~

The command must finish with:

~~~text
PASS: binary compatible-order certificates verified
~~~

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing, exact
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the complete disclosure and responsibility statement.

## Keywords

Compatible orderings; binary vector spaces; finite geometry; Fano planes;
general linear groups; exhaustive classification; computer-assisted mathematics;
AI-assisted mathematics.
