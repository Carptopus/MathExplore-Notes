# Finite calibration

`verify_f7star_group_propagation.py` uses only the Python standard library.
From the repository root, run:

```powershell
python .\research\dual-fano-partition-degrees\verification\verify_f7star_group_propagation.py
```

The script checks:

- the normalized $M(K_4)$ slice identities over their full finite domains;
- the full $F_7^*$ variable-strength orthogonal-array conditions for
  $C_2$, $C_2^2$, and $C_2^3$;
- a concrete last-circuit failure for $C_4$, $C_6$, $S_3$, and $D_8$.

Every run should finish with seven result lines and no assertion failure. These
finite checks detect multiplication-order errors; they do not prove the group
normal form or the universal theorem.
