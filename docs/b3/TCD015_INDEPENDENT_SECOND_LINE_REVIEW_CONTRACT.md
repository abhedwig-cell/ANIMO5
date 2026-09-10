# ANIMO-B3B01R — TCD-015 independent second-line review contract

## Purpose

This branch is a handoff for a genuinely separate second-line review of TCD-015. It contains no review result and performs no admission.

Review candidate readiness:

`ANIMO-B3B01@b982242949aecab32b9067cf7910ad75abfc2b19`

Formal GOV03 disposition:

`ANIMO-B3D09@2a5abc00a779baaa3fb3fa28b3c051231c286132`

Historical-route authority:

`ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`

B3 framework:

`ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

## Atomic review object

Review only the nitrate-scoped TCD-015 claim at the second negative-concentration `Reko` reconstruction in frozen revision-53 `Transsub.for`.

Frozen definitions:

```fortran
Hv = (Mt-Mto)/st
Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv
```

Legacy target expression:

```fortran
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*Hv1 + Flo*Con/ld + &
       Flb*Cb/ld + Fid*Coid/ld)
```

Candidate atomic nitrate algebra:

```fortran
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*(Hv1-Hv) + Flo*Con/ld + &
       Flb*Cb/ld + Fid*Coid/ld)
```

Candidate minus legacy is `-Avc*Hv` only at this seam.

`Transsub` is a shared generic routine. TCD-015 does not authorize applying this change generically to ammonium, dissolved organic matter/nitrogen/phosphorus, phosphorus or any other substance.

## Required independent checks

The reviewer must independently re-open the relevant source and evidence and fail closed on every item below.

1. Recheck frozen B0 source/testbank identities and the exact `Transsub.for` member identity.
2. Recheck the exact `Hv`, `Hv1`, target `Reko` source lines, control-flow location and nitrate call binding. Do not rely on B3D09 prose alone.
3. Recheck the natural LWKM activation at TITO 2312, layer 1, `NITRATE`, `Iflsol=1` and the source-bound `Avc*Hv*St*Ld` local mass identity.
4. Recheck that the execution-only candidate closes the target local residual without treating the remaining floating-point magnitude as a scientific tolerance.
5. Recheck `SYNQ-O001` independence, exact `0.004 kg/m2` duplicated-storage discriminator and its strict scope as conservation evidence, never B2 or historical prevalence evidence.
6. Recheck the predeclared changed and unchanged surfaces before accepting the eight-case B1 matrix.
7. Recheck the eight revision-53-compatible natural cases, 550 compared files, 430 raw-equal, 99 volatile-metadata-only equal and 21 scientific differences, including that all scientific differences remain inside the declared nitrate/N-balance or warning surface and no numerical tolerance was used.
8. Recheck the IFLSOL supplement: 508 natural target entries, all nitrate; 486 `Iflsol=1`; 22 `Iflsol=3`; exact zero-delta role of `Iflsol=3`; isolated reachable `Iflsol=4`; and the derivation that `Iflsol=2` and `Iflsol=5` cannot reach this second reconstruction for valid positive storage denominators after the frozen pre-adjustment.
9. Recheck that the admission claim is nitrate-only even though the underlying `Transsub` expression is shared. The natural observation that a generic diagnostic probe happened to match the nitrate-scoped probe is not authority for a generic correction.
10. Recheck the qualified feature boundary `GreenHouseGasOption=0`. Do not infer GHG-enabled equivalence or admission from core nitrate evidence.
11. Verify that no clipping-policy redesign, `Optneg`/`Vsmall` change, tolerance change, solver change, analytical-branch change or unrelated transport-physics change is bundled into the candidate.
12. Recheck the live GOV03 route state. B2 remains unavailable; G6U is eligible only through documented historical uncertainty; historical behaviour remains `UNKNOWN` and no historical fidelity may be claimed.
13. Treat the existing same-account `COMMENTED` review on B3B01 PR #21 as handoff prose only, not independent second-line evidence.
14. Verify that the review itself performs no production patch, B4 step, central RG05 update, composition or B3 admission.

Any unresolved item must produce a fail-closed result rather than a qualified PASS.

## Independence boundary

Execute this review in a separate ChatGPT context from the B3B01 and B3D09 authoring contexts. The review must derive its conclusions from re-opened source/evidence rather than copying the authoring disposition.

The reviewer may record separate-context independence. Do not claim organizational, institutional or human independence unless that is actually established.

## Historical uncertainty boundary

ANIMO-GOV03 qualifies acquisition closure and route eligibility, not historical behavioural truth. The frozen-source Intel rebuild, GNU B1 executions and SYNQ-O001 must not be promoted to historical B2.

A review PASS must retain:

`historical_behaviour = UNKNOWN`

and:

`historical_fidelity_claimed = false`.

## Result boundary

Persist a machine-readable review result and a human-readable review report on this review branch. The semantic outcome must be fail-closed and clearly distinguish `PASS`, `FAIL` and `INCOMPLETE` or the exact equivalent already required by current repository review tooling.

A PASS is independent-review evidence only. It is not TCD-015 admission. If the independent review passes, stop before admission and hand off to a later separate admission-closeout workunit.

No production source, frozen legacy source, frozen testcase, clipping policy, numerical tolerance, solver policy or canonical TCD row may be modified by ANIMO-B3B01R.
