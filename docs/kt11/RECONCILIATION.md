# ANIMO-KT11 Reconciliation

## Consumed runtime authority

ANIMO-KT06 Tier C admission:

`ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`

Admitted frozen implementation:

`fc818917a46408d55cd7f03e2fa8257534683907`

Frozen implementation blob:

`9a24ea833291f761d2fa76ca4cc9fee28436c614`

The KT11 branch is based on the KT06-A1 admission head. KT02, KT05 and KT06
files are not modified by KT11.

## Central regie

ANIMO-RG05P is being qualified in parallel as a disjoint governance-only
attachment of KT06-A1 to central regie. KT11 may not claim central-regie
completion until RG05P exact-final validation is green.

## Supplemental producer evidence

KT08 closeout:

`ANIMO-KT08@281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`

Imported KT08 summary blob:

`6ba7fe07ca47a6f8d45f18d09b7276dc4ece66f3`

KT09 closeout:

`ANIMO-KT09@249066b7c07d505ba9a72a5aa199401a4349b0da`

Imported representative packet fixture blob:

`8aa4f5dcc8041979d9dc2e2b4fc8cc7f1c88de84`

Imported fixture-to-Fortran tool blob:

`cfcebbe2f4c0635007788fac0b1d5bfcd5c6f704`

These imports are exact evidence transplants. They do not promote KT08 or KT09
to runtime authority.

## Scope decision

KT11 deliberately does not require provider storage to be contiguous or sorted.
The provider contract is a deterministic immutable interval-key lookup. This
allows bounded sparse evidence and makes missing coverage explicit and
fail-closed.

Complete-sequence materialization is a separate later composition claim.
