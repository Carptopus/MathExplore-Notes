# Verification materials

This directory contains the public, offline verification programs accompanying
*A recursive non-symmetric strong spectral criterion for root-loop tree
matrices*.

They require Python 3.11 or newer, use only the standard library, and do not
need network access or a computer algebra system.

## Run

From the manuscript entry directory:

    python -X utf8 verification/verify_recursive_tree_criterion.py --max-vertices 7 --samples 2
    python -X utf8 verification/verify_collision_witness.py
    python -X utf8 verification/verify_minimal_counterexample.py

## Programs

- **verify_recursive_tree_criterion.py** compares the recursive
  sibling-coprimality condition with the full nSSP verification-matrix rank on
  1746 rooted-tree cases through seven vertices. Six targeted cases also use
  exact rational rank and an independent Newton--trace polynomial
  implementation.
- **verify_collision_witness.py** constructs exact rational pattern-zero
  centralizers at a deepest shared zero root and a deepest shared factor
  $x^2-1$, then checks commutation and every prescribed zero.
- **verify_minimal_counterexample.py** checks the three-vertex
  arbitrary-diagonal boundary certificate from Remark 8.6, its exact rank
  $2/3$, and two destructive controls of rank $3/3$.

The witness program imports exact matrix and rooted-tree helpers from
verify_recursive_tree_criterion.py; it is not an implementation-independent
copy of the entire calibration program. The boundary program is
dependency-free and hard-codes its exact certificate.

## Expected results

The standard calibration reports:

- 366 recursively coprime cases, all with full rank modulo 1000003;
- 1380 recursively noncoprime cases, none with modular full rank;
- zero coprime modular-rank-loss candidates;
- zero noncoprime modular-full-rank counterexamples.

The witness program reports two cases with exact commutation, pattern-zero
support, and nonzero witnesses. The boundary program prints PASS, rank
2/3 for the counterexample, and rank 3/3 for both controls.

## Interpretation

Full rank modulo the chosen prime certifies full rank over the rationals and
reals for that integer matrix. Modular rank deficiency is only a
counterexample screen and is not treated as a rational-rank proof. The general
theorem is established by the written mathematical argument, not by finite
enumeration.

## Authorship and license

Carptopus is responsible for the public research output. OpenAI Codex was used
as an AI-assisted research and verification tool and is not an author.

This documentation is distributed under the entry's [CC BY 4.0
license](../LICENSE.md). The Python files are distributed under the [MIT
License](LICENSE-CODE-MIT.txt).
