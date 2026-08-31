# Weighted recursive constructions for shattering triples with six permutations

## Manuscript

- [Read or download the PDF](six-permutation-weighted-shattering.pdf)
- [LaTeX source](six-permutation-weighted-shattering.tex)
- [BibTeX citation](CITATION.bib)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (31 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data license: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let \(\Pi=(\pi_1,\ldots,\pi_6)\) be a six-permutation template on \([N]\),
and let \(G(\Pi)\) be its set of shattered triples. For a probability vector
\(w=(w_1,\ldots,w_N)\) with at least two positive entries, define

$$
A=6\sum_{\{i,j,k\}\in G(\Pi)}w_iw_jw_k,
\qquad
B=\sum_{i=1}^Nw_i^3.
$$

The manuscript proves that six permutations of every \(n\)-element set,
\(n\ge3\), can shatter at least

$$
\frac{A}{1-B}\binom n3
$$

triples. Uniform weights recover the standard finite-template recursion.

Applying the weighted theorem to the published 26-point template of Černá,
Kielak and Volec gives the exact lower bound

$$
c_3\ge\frac{1288385}{2599242}
=0.495677201276\ldots,
$$

strictly improving the \(482/975\) bound obtained by uniform recursion on the
same template.

## Proof and computational boundary

The general theorem follows from a probabilistic lexicographic recursion on
independent infinite words. The included Python program reconstructs the
published 26-point template, confirms that it shatters 1446 of 2600 triples,
and verifies the weighted constant and strict improvement using exact rational
arithmetic. The finite computation checks the application, not the general
proof.

## Scope and prior-work boundary

The result does not prove \(c_3=1/2\), classify optimal templates, or improve
the known upper bound. The comparison is limited to accessible published
sources; it does not assert that unpublished or unindexed parallel work does
not exist.

## Reproduction

Requirements: PowerShell 7 and Python 3.10 or newer. No third-party Python
package is required. From the repository root run:

~~~powershell
pwsh -NoProfile -File .\research\six-permutation-weighted-shattering\verification\run_all.ps1
~~~

The command must finish with:

~~~text
PASS: weighted six-permutation shattering certificate verified
~~~

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing, exact
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the complete disclosure and responsibility statement.

## Keywords

Permutation shattering; extremal combinatorics; weighted blow-ups;
lexicographic recursion; probabilistic method; exact certificates;
AI-assisted mathematics.

