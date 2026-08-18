# Verification materials

This directory contains the public, offline verification materials accompanying
*Proper transposed sesqui arrays at all Sylvester--Hadamard powers*.

The programs check the exact finite-field identities, resultants, finite-basis
certificates, parameter regressions, and implementation-separated proof-chain
calculations used by the manuscript. They use only the Python standard library
and do not require network access, SageMath, SymPy, NumPy, or a computer algebra
system.

## Run

From this directory, with Python 3.11 or newer:

```powershell
python -X utf8 run_reproduction.py
```

The expected final status is:

```text
PASS_PUBLIC_REPRODUCTION_EXTERNAL_REVIEW_PENDING
```

Generated JSON files are written to `results/`. `MANIFEST.json` records the
SHA-256 digest of every distributed source, input certificate, and generated
verification artifact.

## Layout

- `run_reproduction.py`: one-entry offline runner;
- `src/`: verification and construction programs;
- `data/`: frozen input certificates;
- `results/`: independently regenerated outputs;
- `MANIFEST.json`: generated file and hash inventory.

## Interpretation

A successful run shows that the distributed programs reproduce the frozen exact
calculations and reject detected inconsistencies. It does not by itself prove
the human mathematical arguments, establish global priority, or replace expert
and peer review.

## Authorship and AI disclosure

Carptopus is the author responsible for the public research output. OpenAI Codex
was used extensively as an AI-assisted research, verification, and writing tool;
it is not an author. The full disclosure appears in the manuscript.

## Licenses

- Documentation: [CC BY 4.0](LICENSE-DOCS-CC-BY-4.0.md)
- Python code: [MIT License](LICENSE-CODE-MIT.txt)
- JSON data, certificates, manifests, and generated results: [CC0 1.0](LICENSE-DATA-CC0.md)
