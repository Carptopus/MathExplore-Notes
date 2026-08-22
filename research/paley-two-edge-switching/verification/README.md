# Verification materials

This directory contains the public, offline verification materials accompanying
*Paley two-edge switching for proper transposed sesqui arrays*.

The six programs check the symbolic switching identities, the
exact quadratic-character count, frozen prime-field cases, an extension-field
case over $GF(27)$, and a generic finite-field implementation with controlled
mutation tests. An implementation-separated verifier also checks the frozen
$q=11$ Youden-completion certificate, its deletion roundtrip, and a destructive
negative control. They use only the Python standard library and require no
network access or computer algebra system.

## Run

From this directory, with Python 3.11 or newer:

```powershell
python -X utf8 run_reproduction.py
```

The generic finite-field audit is the longest step and may take about one
minute. The expected final status is:

```text
PASS_PUBLIC_REPRODUCTION_EXTERNAL_REVIEW_PENDING
```

Generated JSON files are written to `results/`. `MANIFEST.json` records the
SHA-256 digest of every distributed verification source, two frozen completion
inputs, and six mathematical result files (excluding the manifest and reproduction report to
avoid self-referential hashes).

## Programs

- `verify_general_paley_switch_symbolic.py`: exact symbolic switch identities;
- `verify_general_paley_switch_character_count.py`: character-count formula;
- `verify_general_paley_switch_prime_fields.py`: all admissible pairs in frozen prime fields;
- `verify_general_paley_switch_gf27_independent.py`: independent $GF(27)$ complete-array audit;
- `audit_general_paley_switch_generic_fields.py`: implementation-separated generic-field audit.
- `audit_q11_youden_certificate_independent.py`: independent check of one frozen $q=11$ Youden completion and deletion roundtrip.

## Interpretation

A successful run shows that the distributed programs reproduce the stated
exact calculations and reject the included controlled mutation. It does not by
itself prove the written mathematical arguments, establish global priority, or
replace independent expert and peer review.

## Authorship and AI disclosure

Carptopus is the author responsible for the public research output. OpenAI
Codex was used extensively as an AI-assisted research, verification, and
writing tool; it is not an author. The full disclosure appears in the
manuscript.

## Licenses

- Documentation: [CC BY 4.0](LICENSE-DOCS-CC-BY-4.0.md)
- Python code: [MIT License](LICENSE-CODE-MIT.txt)
- JSON manifests and generated results: [CC0 1.0](LICENSE-DATA-CC0.md)
