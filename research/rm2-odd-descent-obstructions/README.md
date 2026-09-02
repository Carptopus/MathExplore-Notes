# Odd-dimensional descent obstructions in the third support spectrum of binary second-order Reed--Muller codes

This directory contains a follow-up manuscript for two results that are not contained in the
already published `RM2-Third-Support-Regions` and `Fano-Half-Rank-Profiles` papers:

- an infinite failure of odd-to-even support descent; and
- an exact exponentially widening local parity band with six stable odd-dimensional families.

- [Read or download the PDF](odd-dimensional-descent-obstructions-rm2-third-support.pdf)
- [LaTeX source](odd-dimensional-descent-obstructions-rm2-third-support.tex)
- [BibTeX citation](CITATION.bib)
- [Verification package](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Candidate version: v0.1-beta (2 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

## Main results

- For every `m>=6`, the normalized local band around `3*2^(m-1)` contains exactly the six odd
  offsets `+-1,+-3,+-5` in odd dimension and none in even dimension.
- These six offsets give an exponentially widening parity band in the third support spectrum.
- One family begins at `m=5` and proves that odd-to-even support descent fails for every `m>=5`.

The result is a local parity classification and an infinite obstruction family. It does not
determine the complete third support spectrum.

Status: internally verified public Beta v0.1. The manuscript-level zero-trust audit, targeted
novelty refresh, stable verification run, deterministic PDF build and full-page artifact audit
have passed. External review remains pending.

## Reproduction

The verification package checks the explicit odd-dimensional obstruction family, the six stable
endpoint families and the expanding local band. From PowerShell:

```powershell
cd verification
.\run_all.ps1 -Python python
```

The scripts use only the Python standard library.

## Scope

The manuscript does not determine the complete third support spectrum. Its contribution is a
closed-form local parity classification and an infinite odd-to-even descent obstruction extracted
from the previously published low-polar-rank recursion. It does not claim a new support layer
outside that recursion or global priority over unindexed work.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
