# Small exact values and a dense-anchor bound for weak cube saturation

## Manuscript

- [Read or download the PDF](small-exact-values-dense-anchor-weak-cube-saturation.pdf)
- [LaTeX source](small-exact-values-dense-anchor-weak-cube-saturation.tex)
- [BibTeX citation](CITATION.bib)
- [Verification package](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (2 September 2026)
- DOI: [10.5281/zenodo.22254558](https://doi.org/10.5281/zenodo.22254558)
- Concept DOI: [10.5281/zenodo.22254557](https://doi.org/10.5281/zenodo.22254557)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/small-exact-values-dense-anchor-weak-cube-saturation)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

Status: internally verified public Beta v0.1. The manuscript-level zero-trust audit, full
verification run, and PDF artifact audit have passed; external review remains pending.

## Main results

The manuscript determines three exact weak saturation numbers for the three-dimensional cube:

```text
wsat(K8,Q3) = 15,
wsat(K9,Q3) = 16,
wsat(K10,Q3) = 18.
```

The value at order 9 corrects a reported value of 17 and disproves the associated proposal
`wsat(K_n,Q3)=2n-1`. A separate 28-edge graph on 11 vertices with a complete seven-vertex anchor
gives the recurrence

```text
wsat(K_(N+4),Q3) <= wsat(K_N,Q3) + 7
```

and therefore

```text
wsat(K_n,Q3) <= floor((7n+2)/4)  for every n >= 9.
```

Combined with a prior lower bound, this places the asymptotic constant between `11/7` and `7/4`.

## Reproduction

The verification package contains the normalized exhaustive enumerations, independent graph
checks, upper-witness certificates, and a PowerShell entry point:

```powershell
cd verification
.\run_all.ps1 -Python python
```

The complete run enumerates 697, 12,951, and 1,391,842 normalized candidates through the last
excluded edge count for orders 8, 9, and 10. The released certificates are independently replayed
with NetworkX.

## Scope

The manuscript does not determine `wsat(K_n,Q3)` for every order and does not determine the exact
asymptotic constant. Overlapping-block gluing is present in prior weak-saturation work. The claimed
increment is the complete-anchor lemma, the certified `K11/K7` block, the resulting `7/4` upper
bound, and the corrected exact values.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
