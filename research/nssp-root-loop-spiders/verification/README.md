# Verification materials

This directory contains the public, offline verification program accompanying
*An exact non-symmetric strong spectral criterion for root-loop spider
matrices*.

It requires Python 3.11 or newer, uses only the standard library, and does not
need network access or a computer algebra system.

## Run

From the manuscript entry directory:

```powershell
python -X utf8 verification/verify_directed_spider_criterion.py --max-vertices 11 --samples 10
```

## Program

`verify_directed_spider_criterion.py` compares pairwise coprimality of the arm
characteristic polynomials with the full nSSP verification-matrix rank. The
standard run produces 585 signed, genuinely non-symmetric integer-weight
cases, together with five integrated destructive controls:

- a repeated nonreal root within one arm while different arms remain coprime;
- a different directed splitting with the same two-way edge products;
- two arms sharing a nonzero real factor;
- two arms sharing the nonreal factor $x^2+1$;
- two odd arms sharing the zero factor $x$.

## Interpretation

The expected standard-run counts are:

- 145 pairwise-coprime cases, all with full rank modulo 1000003;
- 440 noncoprime cases, none with full rank modulo 1000003;
- zero coprime modular-rank-loss candidates;
- zero noncoprime modular-full-rank counterexamples.

Full rank modulo the chosen prime certifies full rank over the rationals and
reals for that integer matrix. Modular rank deficiency alone does not prove
rank deficiency over the rationals; the shared-factor destructive controls are
therefore also checked by exact rational elimination. The general theorem is
established by the written proof, not by finite enumeration.

## Authorship and license

Carptopus is responsible for the public research output. OpenAI Codex was used
as an AI-assisted research and verification tool and is not an author.

This documentation is distributed under the entry's [CC BY 4.0
license](../LICENSE.md). The Python file is distributed under the [MIT
License](LICENSE-CODE-MIT.txt).
