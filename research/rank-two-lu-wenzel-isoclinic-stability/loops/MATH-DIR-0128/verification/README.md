# Exact verification

The five scripts listed in Section 7 of the manuscript and the fixed guard JSON
are the complete public verification subset for the theorem package. They use
exact SymPy polynomial arithmetic for theorem-facing identities and Bernstein
coefficients. NumPy floating-point computations are controls only.

Run from the entry root with Python 3.11 or newer after installing
`requirements.txt`:

```powershell
python -m pip install -r loops\MATH-DIR-0128\verification\requirements.txt

python -X utf8 loops\MATH-DIR-0128\verification\mi14_isoclinic_pair_sum_certificate.py
python -X utf8 loops\MATH-DIR-0128\verification\mi14_general_b0_reduction.py --stage b0
python -X utf8 loops\MATH-DIR-0128\verification\mi14_b0_parts_certificate.py --part both
python -X utf8 loops\MATH-DIR-0128\verification\mi14_isoclinic_b0_zero_faces.py
python -X utf8 loops\MATH-DIR-0128\verification\mi14_rank_one_b0_factor.py
```

The scripts exit nonzero on a failed hard assertion. Their printed JSON is the
reproducible run record. The committed
`results/isoclinic_b0_zero_faces_guard_v1.json` is the accepted fixed guard; its
recorded source hashes must match the supplied scripts. A successful script
exit is an implementation check and does not replace the proof in the
manuscript.
