# A sparse-defect counterexample to Abelian-border periodicity

## Manuscript

- [Read or download the PDF](abelian-border-problem42-counterexample.pdf)
- [LaTeX source](abelian-border-problem42-counterexample.tex)
- [BibTeX citation](CITATION.bib)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (28 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

The manuscript constructs a binary infinite word that is not Abelian
ultimately periodic but whose every factor of length at least 141 is Abelian
bordered. Consequently, it gives a negative answer to Question 1 of Charlier,
Harju, Puzynina and Zamboni and to Problem 42 of the Fici--Puzynina survey.

The constants 28 and 141 are explicit parameters of one construction; the
paper does not claim that the threshold, period or height range is minimal.

## Construction mechanism

A periodic nearest-neighbor path on four heights supplies the full
parity-compatible endpoint-sum palette at every anti-diagonal. Widely separated
finite replacement walks then alter every arithmetic progression infinitely
often. Five translated witnesses for each center and sum ensure that a single
replacement interval cannot destroy all local certificates. The resulting
sparse defect set has density zero but rules out every constant arithmetic-
progression tail, which is equivalent to ruling out Abelian ultimate
periodicity of the associated binary word.

## Relation to the preceding Abelian-border entry

The earlier [threshold paper](../abelian-border-periodicity-thresholds/README.md)
proves sharp periodicity results in the first two finite layers and a
frequency-denominator sufficient condition. Those theorems remain valid and
independent. The present paper addresses the unrestricted open problem and
shows that a sufficiently large finite threshold does not force Abelian
ultimate periodicity.

A targeted public search completed on 28 August 2026 found no paper, preprint,
author update or indexed archive directly covering this counterexample. This
records the search boundary and is not an absolute worldwide-priority claim.

## Reproduction

The proof of the infinite sparse construction is mathematical. The bundled
Python program independently checks the 28-periodic palette, all 28 replacement
certificates, the four-of-five contamination bound and an 80-interval finite
positive control.

From this entry directory:

```powershell
python -X utf8 .\verification\verify_sparse_palette_counterexample.py
```

The first seven output lines must end with
`finite_sparse_full_local_palette=PASS`. The finite program does not replace
the infinite sparse-set and arithmetic-progression arguments in the paper.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for computational exploration, proof development and organization,
adversarial checking, literature search, verification and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Combinatorics on words; Abelian borders; Abelian periodicity; infinite words;
counterexamples; sparse defects; Parikh vectors; exact verification;
AI-assisted mathematics.
