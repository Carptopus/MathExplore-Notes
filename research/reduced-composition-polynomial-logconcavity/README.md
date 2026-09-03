# Log-concavity of reduced composition polynomials via adjacent B-spline refinement columns

## Manuscript

- [Read or download the PDF](reduced-composition-polynomial-logconcavity.pdf)
- [LaTeX source](reduced-composition-polynomial-logconcavity.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: pending
- [Verification programs](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (4 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified public Beta; external mathematical review pending.

## Main result

Ardila and Doker associated a reduced composition polynomial $f_c(q)$ with every positive integer
composition $c$ and asked whether its coefficient sequence is unimodal or, more strongly,
log-concave. The manuscript proves that the coefficient sequence of $f_c(q)$ is log-concave for
every positive integer composition $c$. Consequently it is unimodal.

The result covers all composition lengths, all positive parts, and all coefficient positions. It
does not assert real-rootedness, ultra-log-concavity, or Pólya-frequency properties.

## Proof mechanism

The coefficient vector is first identified, up to a positive scalar, with one column of a discrete
B-spline knot-refinement matrix. Deleting the first or last part of the composition produces two
adjacent columns of a common lower-degree refinement matrix. Total nonnegativity makes their
adjacent $2\times2$ minors nonnegative. An exact identity converts those minors into the
log-concavity defects of the original coefficient sequence, while the previously established
unimodality closes the remaining sign case.

The novelty search was bounded by publicly accessible sources through 3 September 2026. No direct
proof of the stated theorem was found, but global priority and external review are not claimed.

## Reproduction

Requirements: PowerShell 7, Python 3.13 or compatible, NumPy 2.5.2, and SciPy 1.17.0. From the
repository root run:

```powershell
pwsh -NoProfile -File .\research\reduced-composition-polynomial-logconcavity\verification\run_all.ps1
```

The exact-arithmetic verifier exhausts all 8,178 nontrivial compositions of total size at most 13
and checks 53,157 adjacent minors and determinant identities. The independent spline-interface
verifier checks 75,535 instances, 199 distinct SciPy refinement samples, and two destructive
controls. These computations test the implementation and proof interfaces; they are not a
substitute for the general proof.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof exploration and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Composition polynomials; log-concavity; unimodality; discrete B-splines; knot refinement; total
positivity; enumerative combinatorics; exact verification; AI-assisted mathematics.
