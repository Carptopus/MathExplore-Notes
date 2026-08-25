# Verification

`verify_ternary_ampc_k3.py` is the fail-closed exact finite-state certificate
for the manuscript's global upper bound.

## Environment

- Python 3.11 or newer;
- standard library only;
- no random seed, network access or external solver.

## Run

From the project entry directory:

```powershell
python -X utf8 verification/verify_ternary_ampc_k3.py
```

The final output must contain:

```text
PATCH_STATES 938
PATCH_TRANSITIONS 8442
CLOSURE_SHA256 BBF0CBF7D6E5E23CCEECC71A59644AD4F5DA0D48A1A2A0A219BB292A127CDAAA
CENTER_PARIKH_SIZE_DISTRIBUTION {3: 3, 4: 246, 5: 223, 6: 285, 7: 181}
MAX_CENTER_PARIKH_SIZE 7
PASS: exact finite patch closure covers all base-3 offset pairs
```

## Evidence boundary

The program does not infer an infinite theorem from a bounded offset scan.
It closes a finite family of nine-cell language patches under all nine paired
base-three digit transitions. The proof in the manuscript shows that this
closure covers every nonnegative offset pair. Prefix and bounded-box checks
are implementation cross-checks only.

The program is licensed under the MIT License; see
[`LICENSE-CODE-MIT.txt`](LICENSE-CODE-MIT.txt).

