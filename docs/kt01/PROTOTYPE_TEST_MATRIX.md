# ANIMO-KT01 Prototype Verification Matrix

The executable Fortran suites cover requirements 1 through 23 and the bounded fail-closed controls below. The structural Python suite covers requirements 24 and 25 plus ownership/provenance guards.

| ID | Property | Test surface |
| --- | --- | --- |
| 01 | rejected trial leaves accepted physical state unchanged | Fortran |
| 02 | retry starts from same accepted physical origin | Fortran runtime trace |
| 03 | commit publishes accepted physical state and separate event ledger only after all checks pass | Fortran |
| 04 | generation advances exactly once per commit | Fortran |
| 05 | stale origin generation rejects | Fortran |
| 06 | lineage mismatch rejects | Fortran |
| 07 | wrong origin time rejects | Fortran |
| 08 | rejected transfer events do not enter the committed event ledger | Fortran |
| 09 | scratch/diagnostics do not alter accepted physical state | Fortran |
| 10 | checkpoint represents accepted physical state only | Fortran plus structural checkpoint guard |
| 11 | restore preserves continuation identity | Fortran |
| 12 | incompatible checkpoint identity fails closed | Fortran |
| 13 | exact time equality without epsilon | Fortran |
| 14 | rational normalization is canonical within the bounded backend | Fortran |
| 15 | prototype time serialization round-trips exactly | Fortran |
| 16 | exact rationals remain distinct when REAL projection collapses | Fortran, REAL only in adversarial test |
| 17 | invalid/overflowing time arithmetic fails closed | Fortran |
| 18 | interval success requires exact requested target and incomplete progress is not published | Fortran |
| 19 | no-progress retry fails closed | Fortran |
| 20 | worker reuse cannot leak scratch across logical models | Fortran |
| 21 | multiple conserved quantities fit the acceptance interface | Fortran |
| 22 | incomplete conservation evidence rejects | Fortran |
| 23 | runtime creates no balancing event | Fortran |
| 24 | no direct SWAP5 module dependency | structural Python |
| 25 | no ANIMO `src/` production modification from GOV06 base | structural Python plus Git diff |

Additional structural guards assert no REAL in the TIME02 prototype module, no epsilon/ULP policy, no unchecked rational cross multiplication, no file I/O in transaction/persistence/interval kernels, no mutable `SAVE` state, no excluded hydraulic/process payload, complete exact SWAP source blob provenance, no committed event history in physical `AcceptedState`, no event journal/ledger in physical checkpoint state, and private checkpoint components.

Additional fail-closed and adversarial runtime coverage:

| ID | Property | Test surface |
| --- | --- | --- |
| 26 | failed acceptance with retry disallowed fails closed | Fortran |
| 27 | attempt-budget exhaustion causes no partial physical or event publication | Fortran |
| 28 | endpoint beyond exact target fails closed | Fortran |
| 29 | unrepresentable synthetic state arithmetic fails closed | Fortran |
| 30 | overlength calendar identity is rejected rather than truncated | Fortran identity-envelope suite |
| 31 | delimiter-ambiguous prototype calendar identity is rejected | Fortran identity-envelope suite |
| 32 | overlength checkpoint compatibility identity is rejected rather than truncated | Fortran identity-envelope suite |
| 33 | overlength worker identity is rejected rather than truncated | Fortran identity-envelope suite |
| 34 | a candidate without explicit trial provenance cannot commit | Fortran identity-envelope suite |
| 35 | a negative directed transfer amount is rejected without journal mutation | Fortran identity-envelope suite |
| 36 | an outer interval that fails after private accepted progress publishes neither physical state nor events | Fortran |
| 37 | accepted substep events accumulate in the private ledger and publish together at exact interval completion | Fortran |
| 38 | uninterrupted and checkpoint-split synthetic continuations reach identical exact final physical state and separately retained event history | Fortran |
