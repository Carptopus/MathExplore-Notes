# Sharp initial thresholds for Abelian-bordered binary infinite words

## Manuscript

- [Read or download the PDF](abelian-border-periodicity-thresholds.pdf)
- [LaTeX source](abelian-border-periodicity-thresholds.tex)
- [BibTeX citation](CITATION.bib)
- [Verification code and certificates](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (26 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data dedication: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main results

For a binary infinite word $x$, let $\mu_{\mathrm{ab}}(x)$ be the maximum
length of an Abelian-unbordered factor, when this maximum is finite. The
manuscript proves:

1. $\mu_{\mathrm{ab}}(x)\leq13$ forces ordinary ultimate periodicity, with
   eventual period at most $13$; both bounds are sharp.
2. The minimum finite value of $\mu_{\mathrm{ab}}$ among binary words that are
   not ordinarily ultimately periodic is exactly $14$.
3. $\mu_{\mathrm{ab}}(x)\leq14$ forces Abelian ultimate periodicity, with
   Abelian period at most $14$; this bound is sharp.
4. If the limiting frequency of $1$ is the reduced fraction $p/q$ and
   $\mu_{\mathrm{ab}}(x)<2q$, then the tail admits consecutive length-$q$
   blocks, each of weight $p$.

## Proof and verification structure

The first two threshold layers are reduced to exact finite overlap graphs.
At threshold $14$, every recurrent component is a directed cycle. At threshold
$15$, four branching recurrent components remain, but each has a closed Parikh
phase whose complement is acyclic. Exact cycle post-processing gives the sharp
ordinary and Abelian period bounds. The frequency-denominator result is a
separate theoretical consequence of the bounded-discrepancy formulation.

The Python package independently checks the Abelian-border predicate, small
controls, both full overlap graphs, all closed phases, all nonbranching cycles,
and the sharp period witnesses. Two C++17 programs independently reconstruct
the threshold graphs and recurrent-component data.

## Scope and prior-work boundary

The result gives the sharp first ordinary-periodicity threshold, the next
Abelian-periodicity layer, and a general sufficient condition. It does not
solve the full open question asking whether every binary word with bounded
Abelian-unbordered factors is Abelian ultimately periodic. A targeted search
of the original paper, the 2022 survey, and indexed follow-up literature found
no directly covering result; this is not an assertion of absolute global
priority.

## Reproduction

Using Python 3.11 or newer and NetworkX 3.6.1, run from this entry directory:

```powershell
python -X utf8 verification\verify.py
python -X utf8 verification\verify_period_bounds.py
```

Both commands must print `"status": "VERIFIED"` and exit with code `0`.
Independent C++17 commands and expected counts are documented in
[`verification/README.md`](verification/README.md).

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature triage, finite-search implementation, exact-certificate
checking, proof stress-testing, adversarial auditing, and manuscript
preparation. The paper contains the complete disclosure and responsibility
statement.

## Keywords

Abelian border; Abelian-unbordered factor; combinatorics on words; binary
infinite word; ultimate periodicity; Abelian periodicity; Parikh vector;
bounded discrepancy; finite overlap graph; computer-assisted proof.
