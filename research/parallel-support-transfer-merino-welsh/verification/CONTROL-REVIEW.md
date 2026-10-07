# Finite control review

2026-10-07, case MERINO-WELSH-PARALLEL-SUPPORT-UPGRADE-0001.

The independent read-only guard `transfer_fixed_guard` verified the original input script SHA256 `8E0719EDF36E591ADAAE0243DDCF5F298D9DEF3A74BC2DF50C2E7F6463B77B86` and result fixture SHA256 `2097549F758AFC4FB87EAD61136CB0BAF55293400A15E26E31D7645B68F83364`.

It independently executed the seven fixed calls from the script in memory, without invoking the writing `main()`. All returned fields matched the fixture: 19,013 subsets, maximum 13 elements. With the extra negative-control run it inspected 20,293 subsets; runtime was 0.061 seconds, no resource anomaly. Forcing theta c=4, multiplicity=2 into the accepted class raised the expected premise error. Altering a stored T02 value in memory was detected.

The public runner `run_control_checks.py` additionally passed normal and optimized Python execution. These are explicit exception-based checks, not removable Python assertions.

Verdict: VERIFIED for these finite controls only. They check the earlier s/2 sufficient budget and do not independently certify the general girth theorem, the corank-two structural proof, or the all-parameter sparse paving application. They are not an independent proof or novelty judgment.
