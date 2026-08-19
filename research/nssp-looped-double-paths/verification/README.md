# Verification materials

This directory contains the public, offline verification programs accompanying
*Spectral separation and the non-symmetric strong spectral property for looped
double paths*.

They require Python 3.11 or newer, use only the standard library, and do not
need network access or a computer algebra system.

## Run

From the manuscript entry directory:

```powershell
python -X utf8 verification/verify_nssp_weighted_paths.py --max-n 32
python -X utf8 verification/verify_nssp_spectral_separation.py
python -X utf8 verification/audit_nssp_spectral_jacobian.py
```

## Programs

- `verify_nssp_weighted_paths.py`: checks 272 naturally labelled single-loop
  positions at even orders through 32 by exact modular rank;
- `verify_nssp_spectral_separation.py`: compares polynomial coprimality,
  modular-rank calibration, and the parity classification on 119 positions;
- `audit_nssp_spectral_jacobian.py`: compares characteristic-coefficient,
  moment, and verification-matrix ranks on 77 cases and constructs two exact
  obstruction witnesses.

The second and third programs reuse the weighted-path and modular-rank routines
from `verify_nssp_weighted_paths.py`. They test complementary identities and
controlled examples, but are not three implementation-independent verifiers.

## Interpretation

A successful run reproduces the stated finite checks. Full rank modulo the
chosen prime certifies full rank over the rationals and reals. Modular rank
deficiency is used only for calibration and is not treated as a real-rank
proof. The general theorem is established by the written mathematical
argument, not by finite enumeration.

## Authorship and license

Carptopus is responsible for the public research output. OpenAI Codex was used
as an AI-assisted research and verification tool and is not an author.

This documentation is distributed under the entry's [CC BY 4.0
license](../LICENSE.md). The Python files are distributed under the [MIT
License](LICENSE-CODE-MIT.txt).
