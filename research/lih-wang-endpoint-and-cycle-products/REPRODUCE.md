# Reproduction and frozen-source boundary

Run commands from this entry directory, not the collection root. Use Python 3.13 on Windows for the frozen resource guards. The endpoint checker uses Windows process-memory monitoring; the bounded small-shape runner uses Windows Job Objects. `verify_star_certificate.py` additionally requires SymPy (tested with 1.14.0). No discovery code or internal research state is required.

Create your own virtual environment and install the declared dependency before running; the repository does not ship an environment. Substitute your Python executable for `python` below. Create `tmp` before the small-shape run. Do not run the guards concurrently.

```powershell
python -X utf8 loops/LIH-WANG-DIRECT-SUM-GATE-0001/verification/endpoint_threshold_guard.py
python -X utf8 loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/coupled_small_mean_guard.py
python -X utf8 loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/poisson_boundary_window_guard.py
python -X utf8 loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/verify_star_certificate.py --certificate loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/results/star_low_degree_certificates.json --output tmp/star-check.json
New-Item -ItemType Directory -Path tmp -Force
python -X utf8 loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/run_small_shape_independent_window.py --packet loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/results/small_shape_window_s32_v1.json --output loops/LIH-WANG-NONCUBICAL-FACES-0001/verification/results/reproduced-small-shape.json
```

Important correction to the frozen supplement's example command: the small-shape runner deliberately requires a NEW output directly under its `verification/results` directory, not under `tmp`. Its per-case intermediate outputs go under `tmp`. Existing evidence files cannot be overwritten. This clarification changes no mathematical formula or verifier.

Expected scalar certificate digests and exact scopes are in [the supplement](supplement.md). The small-shape run is serial, with a 50-second / 128-MiB process-tree guard per case and an internal 44-second deadline. Stop on failure; do not automatically retry. The frozen certificate covers 32 structures and 318 rational boxes, not arbitrary cycle forests. Finite verification is not a replacement for the analytic proof or external review.

## PDFs and semantic sources

The accepted PDFs have SHA-256 values:

- main.pdf: `288239D57D3644F8EA01222D04F0EB00CBD78B2B931474E7A619A0E2EE1D88ED`
- supplement.pdf: `F78CAE61842D8580A0F3F796BD692670875EA3A4066E5A3B15E242B8D694A4FF`

Compile the supplied TeX from `paper` using Tectonic (`tectonic -X compile --untrusted main.tex` and the same command for `supplement.tex`). Keep `audit-packet-cjk.png` beside the TeX; it is a rendered Chinese path label, not a proof figure. No internal absolute path or private paper PDF is needed. Regenerated PDFs may differ bytewise by compiler version.

The optional `paper/build_tex.py` converter reconstructs the TeX from the hash-frozen Markdown sources. It requires Pillow and the Windows font `C:/Windows/Fonts/msyh.ttc`; it rejects any source hash change. Run `python paper/build_tex.py` from this entry. The public compile entry uses a Tectonic executable already installed by the user; no runtime is downloaded automatically.

The supplement's A1 reference names an internal prewrite dependency register, not an additional public proof obligation. All analytic proofs are stated in the manuscript. The public package includes only the exact verifier/certificate subset of that closure, plus its required resource guard, and `SHA256SUMS.txt` binds every shipped file. Internal exploration notes and audit instructions are intentionally not mirrored.
