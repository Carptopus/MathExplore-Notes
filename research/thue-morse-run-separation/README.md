# Exact first separation in the Thue--Morse run-length sequence

## Manuscript

- [Read or download the PDF](exact-first-separation-thue-morse.pdf)
- [LaTeX source](exact-first-separation-thue-morse.tex)
- [BibTeX citation](CITATION.bib)
- [Verification programs](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Candidate version: v0.1-beta (2 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

Status: internally verified v0.1-beta release candidate; manuscript audit, complete verification
rerun, and seven-page PDF artifact audit PASS. External publication is not authorized.

## Main result

Let `d` be the adjacent-run-length sequence of the Thue--Morse word. For every `q >= 2`, the
manuscript determines the exact first position at which `d(2^(q+2)n)` and `d(2^q n)` differ:

```text
N_q = floor(2^E_q / 9),
E_q = 2^(q+1)-2 for even q, and 2^(q+1)+1 for odd q.
```

It also treats arbitrary distances in the same ratio-four scale chain and gives an exact infinite
family for multipliers characterized by a multiplicative-order condition.

## Reproduction

The verification package uses Python integers only and has no third-party Python dependency. It
cross-checks the morphic and canonical-Jacobsthal encodings, reproduces the first two exact
minimum cases, checks the explicit witnesses and false-exponent negative controls, and performs
destructive finite tests of both directions of the scale lemma and the binary minimizers.

```powershell
cd verification
.\run_all.ps1
```

## Scope

The result solves an infinite ratio-four subfamily of Shallit's general first-separation question.
It does not determine the exact answer for two arbitrary multipliers or the nondivisibility cases
outside the stated multiplicative-order family. External priority confirmation and formal peer
review remain pending.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
