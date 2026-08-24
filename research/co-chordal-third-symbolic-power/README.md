# The third symbolic power of a co-chordal edge ideal is componentwise linear

## Manuscript

- [Read or download the PDF](co-chordal-third-symbolic-power.pdf)
- [LaTeX source](co-chordal-third-symbolic-power.tex)
- [BibTeX citation](CITATION.bib)
- DOI: pending Zenodo deposit
- [Finite proof-identity calibration](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (25 August 2026)
- Licenses: manuscript and documentation under CC BY 4.0; Python verification code under MIT; JSON result under CC0 1.0
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let $G$ be a finite co-chordal graph and let $I(G)$ be its edge ideal over an arbitrary field. The manuscript proves that

$$
I(G)^{(3)}
$$

is componentwise linear.

Earlier work proves the second symbolic power for every co-chordal graph and gives counterexamples from the fourth symbolic power onward. For the third symbolic power, the available degree bounds leave only the component generated in degree five. This manuscript proves that the remaining component always has a five-linear resolution.

## Proof mechanism

The proof establishes a more general theorem for fixed-degree monomial ideals on a chordal graph. Every maximal clique has capacity two, while at most $5-d$ marked cliques have capacity one. A simplicial-vertex split produces two smaller ideals in the same class and an exact intersection identity. A two-level induction and polarization then give a $d$-linear resolution for every $2\leq d\leq5$.

## Verification boundary

The proof is theoretical. The Python program in `verification/` exhaustively checks 21,023 finite recurrence states on noncomplete nonisomorphic chordal graphs with at most six vertices. It verifies the split identities and inclusion used by the proof, but it does not replace the general argument.

## Prior-work and review status

Ficarra, Moradi, and Römer proved the second-power case and formulated the original all-powers conjecture. Ahmed and Namiq determined the regularity of all symbolic powers, supplied counterexamples for every power at least four, and left exactly the degree-five component undecided when $s=3$. The public-source comparison found no direct statement of the result proved here; this is not a claim of absolute global priority.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature triage, symbolic experimentation, proof stress-testing, adversarial auditing, and manuscript preparation. The paper contains the complete disclosure and responsibility statement.

## Keywords

co-chordal graph; chordal graph; edge ideal; symbolic power; componentwise linear ideal; monomial ideal; linear resolution; commutative algebra; combinatorial commutative algebra.
