# Counterexamples to unimodality of the connected set polynomial

## Manuscript

- [Read or download the PDF](connected-set-polynomial-counterexamples.pdf)
- [LaTeX source](connected-set-polynomial-counterexamples.tex)
- [BibTeX citation](CITATION.bib)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Candidate version: v0.1-beta (2 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

Status: Public Beta v0.1; internally verified candidate proof; external mathematical review pending.

## Main result

For every order `n >= 8`, the manuscript constructs four pairwise nonisomorphic connected graphs
with at least as many edges as vertices and with nonunimodal connected set polynomial. It gives a
common closed formula, proves the fixed coefficient pattern `10, 11, 10`, determines that eight is
the minimum counterexample order, and classifies all four minimum-order isomorphism classes.

## Reproduction

The family identities and the boundary through order seven use NetworkX's graph atlas. The complete
order-eight classification additionally requires Brendan McKay's official `graph8c.g6` catalogue.
See [verification/README.md](verification/README.md) for the source URL, frozen SHA-256 digest and
the complete command.

## Scope

The result does not classify all higher-order counterexamples and does not claim that no
counterexample with exactly `n` edges exists. External priority confirmation and formal peer review
remain pending.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
