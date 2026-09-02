# Connected Peck posets with non-log-concave antichain polynomials

## Manuscript

- [Read or download the PDF](connected-peck-antichain-counterexamples.pdf)
- [LaTeX source](connected-peck-antichain-counterexamples.tex)
- [BibTeX citation](CITATION.bib)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Candidate version: v0.1-beta (2 September 2026)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/connected-peck-antichain-counterexamples)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

Status: internally verified public Beta v0.1. The manuscript-level zero-trust audit and the PDF
artifact audit passed; external review remains pending.

## Main result

For integers `a,c >= 1`, the manuscript constructs a finite connected height-one Peck poset
`P_{a,c}` with two equally sized ranks and antichain polynomial

```text
N_{P_{a,c}}(x) = (1+2x)^a + 2(1+x)^(a+c) - 2(1+x)^a.
```

For every `a >= 7`, the specialization `P_{a,2}` is not log-concave. This gives an infinite
counterexample family to Ding and Dong's Conjecture C. The first member on this parameter line has
18 elements and log-concavity defect `-72`.

## Reproduction

The verification program uses the Python standard library only. It reconstructs the Hasse graph,
checks connectivity and a perfect matching, compares the closed formula with exhaustive antichain
enumeration, scans all `2^18` subsets in the first case, and exercises both negative and positive
parameter controls.

```powershell
cd verification
.\run_all.ps1
```

## Scope

The manuscript does not claim that the 18-element example is globally minimal among all connected
Peck posets. Bhattacharyya and Kahn's earlier bipartite construction motivated the approach but has
unequal bipartition sizes; the balanced ranks, perfect matching and closed infinite family proved
here are the claimed contribution. External priority confirmation and formal peer review remain
pending.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
