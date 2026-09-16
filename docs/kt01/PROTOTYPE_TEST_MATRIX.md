# ANIMO-KT01 Prototype Verification Matrix

The executable Fortran suite covers requirements 1 through 23. The structural Python suite covers requirements 24 and 25 plus additional guards.

| ID | Property | Test surface |
| --- | --- | --- |
| 01 | rejected trial leaves accepted physical state unchanged | Fortran |
| 02 | retry starts from same accepted physical origin | Fortran runtime trace |
| 03 | commit publishes candidate atomically | Fortran |
| 04 | generation advances exactly once per commit | Fortran |
| 05 | stale origin generation rejects | Fortran |
| 06 | lineage mismatch rejects | Fortran |
| 07 | wrong origin time rejects | Fortran |
| 08 | rejected transfer events do not commit | Fortran |
| 09 | scratch/diagnostics do not alter accepted state | Fortran |
| 10 | checkpoint represents accepted state only | Fortran |
| 11 | restore preserves continuation identity | Fortran |
| 12 | incompatible checkpoint identity fails closed | Fortran |
| 13 | exact time equality without epsilon | Fortran |
| 14 | rational normalization is canonical | Fortran |
| 15 | time serialization round-trips exactly | Fortran |
| 16 | exact rationals remain distinct when REAL projection collapses | Fortran, REAL only in adversarial test |
| 17 | invalid/overflowing time arithmetic fails closed | Fortran |
| 18 | interval success requires exact requested target | Fortran |
| 19 | no-progress retry fails closed | Fortran |
| 20 | worker reuse cannot leak scratch across logical models | Fortran |
| 21 | multiple conserved quantities fit the acceptance interface | Fortran |
| 22 | incomplete conservation evidence rejects | Fortran |
| 23 | runtime creates no balancing event | Fortran |
| 24 | no direct SWAP5 module dependency | structural Python |
| 25 | no ANIMO `src/` production modification from GOV06 base | structural Python plus Git diff |

Additional structural guards assert no REAL in the TIME02 prototype module, no epsilon/ULP policy, no unchecked rational cross multiplication, no file I/O in transaction/persistence/interval kernels, no mutable `SAVE` state, no excluded hydraulic/process payload and complete exact SWAP source blob provenance.

Additional fail-closed runtime coverage:

| ID | Property | Test surface |
| --- | --- | --- |
| 26 | failed acceptance with retry disallowed fails closed | Fortran |
| 27 | attempt-budget exhaustion causes no partial external publication | Fortran |
| 28 | endpoint beyond exact target fails closed | Fortran |
| 29 | unrepresentable synthetic state arithmetic fails closed | Fortran |
