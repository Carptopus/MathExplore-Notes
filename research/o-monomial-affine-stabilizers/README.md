# Affine stabilizers of two o-monomial value sets

This directory contains an internally audited manuscript proving trivial affine stabilizers for
the two known nontranslation o-monomial families left untreated in Ding--Tang's source paper.

- [PDF manuscript](o-monomial-affine-stabilizers.pdf)
- [LaTeX source](o-monomial-affine-stabilizers.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22297838](https://doi.org/10.5281/zenodo.22297838)
- Concept DOI: [10.5281/zenodo.22297837](https://doi.org/10.5281/zenodo.22297837)
- [Verification programs](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (4 September 2026)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/o-monomial-affine-stabilizers)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified public Beta; external mathematical review pending.

## Main result

Let $q=2^m$, where $m\ge5$ is odd, and let

$$
J_e=\{x^e+x:x\in\mathbb F_q\}.
$$

The manuscript proves that the stabilizer of $J_e$ in the one-dimensional general affine group is
trivial for both remaining known families:

- the $\overline{\mathrm{Segre}}$ family $e=q-6$;
- the Glynn I family $e=3\cdot2^{(m+1)/2}+4$.

Together with Ding--Tang's earlier cases, this covers every currently known nontranslation
o-monomial family. It does not classify hypothetical unknown o-monomials and therefore does not
claim the unrestricted logical form of Ding--Tang Conjecture 2.

## Proof mechanism

For the $\overline{\mathrm{Segre}}$ family, the proof gives a general low-coefficient criterion for
the value-set polynomial and computes $(c_1,c_2,c_3)=(0,0,1)$. For Glynn I, it locates the first
nonzero coefficient through a parity count of directed cycle covers, then combines coefficient
gaps, Kummer's theorem, and Lucas' theorem to eliminate every nonidentity affine stabilizer.

## Reproduction

The checkers use only the Python standard library. From the repository root, run:

```powershell
pwsh -NoProfile -File .\research\o-monomial-affine-stabilizers\verification\run_all.ps1
```

The runner executes both verifiers in ordinary and optimized (`-O`) modes and requires every
output to match the frozen results. The finite checks test formula implementations and selected
admissible parameters; they do not replace the general proofs.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof exploration and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Finite geometry; finite fields; o-polynomials; o-monomials; hyperovals; affine stabilizers;
value-set polynomials; cycle covers; 3-designs; exact verification; AI-assisted mathematics.
