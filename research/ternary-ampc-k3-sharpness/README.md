# A ternary word attaining the Abelian maximal pattern complexity bound at pattern size three

## Manuscript

- [Read or download the PDF](ternary-ampc-k3-sharpness.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22093018](https://doi.org/10.5281/zenodo.22093018)
- [LaTeX source](ternary-ampc-k3-sharpness.tex)
- [Verification code](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (25 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Define the length-three substitution on the alphabet `{0,1,2}` by

```text
0 -> 001,  1 -> 020,  2 -> 000.
```

Let `alpha` be its one-sided fixed point beginning with `0`. The manuscript
proves that `alpha` is recurrent and aperiodic by projection and that its
Abelian maximal pattern complexity at pattern size three is exactly

$$
p_{\alpha}^{*\mathrm{ab}}(3)=7.
$$

This attains the general lower bound `(r-1)k+1` at the first parameter pair
`r=3`, `k=3` not covered by the previously known equality cases.

## Proof and verification structure

- Primitivity of the substitution gives uniform recurrence.
- Three explicit binary projections prove aperiodicity by projection.
- An exact base-three sparse-language recursion reduces all offset pairs to a
  finite nine-cell patch automaton.
- The closed automaton has 938 states and 8,442 labelled transitions; every
  state has at most seven central Parikh vectors.
- The pattern `{0,2,9}` realizes seven different Parikh vectors, proving
  sharpness.

The supplied Python program reconstructs the complete closure, checks the
transition identities and frozen SHA-256 certificate, and verifies the sharp
pattern. It uses only the Python standard library and no random search,
external solver, or network access.

## Scope and prior-work boundary

Kamae, Widmer and Zamboni proved the lower bound for recurrent words that are
aperiodic by projection. The candidate new contribution is the explicit
ternary substitution and the all-pattern proof that equality is attained for
`r=3`, `k=3`.

The result does not settle equality for arbitrary `r>=3`, `k>=3`, and it does
not answer the stronger question of whether one word can attain the bound for
every pattern size. Absolute priority remains qualified pending broader public
and expert review.

## Reproduction

Using Python 3.11 or newer, run from this entry directory:

```powershell
python -X utf8 verification/verify_ternary_ampc_k3.py
```

The expected state count, transition count, closure hash, Parikh-size
distribution and sharp pattern are recorded in
[`verification/README.md`](verification/README.md).

## AI-assisted research disclosure

OpenAI Codex was used extensively for literature triage, symbolic
experimentation, proof stress-testing, adversarial auditing, verification and
manuscript preparation. Carptopus reviewed the final text and assumes
responsibility for the mathematical claims.

## Keywords

Abelian maximal pattern complexity; combinatorics on words; recurrent word;
aperiodic by projection; primitive substitution; automatic sequence; Parikh
vector; sparse factors; computer-assisted proof; exact finite-state
verification.
