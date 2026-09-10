# ANIMO-B3D12 — TCD-015 B3 admission closeout

## Result

TCD-015 is admitted as one **atomic Class-B scientific correction** through the B3 historical-uncertainty route:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

Admission decision:

`ADMIT_TCD015_ATOMIC_CLASS_B_SCIENTIFIC_NITRATE_TRANSPORT_ALGEBRA_CORRECTION_WITH_HISTORICAL_UNCERTAINTY`

This admission is deliberately narrower than a generic `Transsub` correction. It applies only to the NITRATE-bound second negative-concentration `Reko` reconstruction in the qualified `GreenHouseGasOption=0` core scope.

## Authorities reconciled

- readiness: `ANIMO-B3B01@b982242949aecab32b9067cf7910ad75abfc2b19`;
- formal GOV03 disposition: scientific object `ANIMO-B3D09@2a5abc00a779baaa3fb3fa28b3c051231c286132`, administrative closeout `cf3e2746351c5c75d236e1b63fb0623daa8e7372`;
- independent second-line review: `ANIMO-B3B01R@a6880282e9ed743f97a3435b55e4fb54f7d55a44`;
- successful independent-review workflow: `34455556365`;
- historical-route authority: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- independent synthetic conservation oracle: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`;
- central admission inventory at workunit start: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`.

The independent review returned semantic `PASS` with disposition `PASS_TCD015_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION`. That review was separate-context only. No organizational, institutional or human independence is claimed.

## Exact atomic correction

Frozen revision-53 defines:

```fortran
Hv = (Mt-Mto)/st
Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv
```

The legacy second post-clipping reconstruction is:

```fortran
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*Hv1
     + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)
```

The admitted nitrate-scoped scientific correction is:

```fortran
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*(Hv1-Hv)
     + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)
```

Therefore:

```text
candidate - legacy = -Avc*Hv
```

and the duplicated local mass contribution is:

```text
Avc*Hv*St*Ld
```

The exact atomic claim is that `Hv` is already included in `Hv1`, while the explicit storage term already represents the complete moisture-storage change. Retaining both contributions in this reconstruction double-counts the same storage derivative.

## Causal and conservation evidence

The natural LWKM event activates the target at year 1997, TITO 2312, layer 1, `NITRATE`, `Iflsol=1`. The independently reviewed event gives:

```text
BAPD - BATR = 0.00005787119019887 kg/m2
              = 0.5787119019887 kg/ha
```

which matches the local duplicated-storage identity `Avc*Hv*St*Ld` from the persisted event values. The execution-only corrected reconstruction closes the local target residual to printed floating-point precision and reduces the annual LWKM NO3 residual from `0.5760503022407 kg/ha N` to approximately `2.28e-7 kg/ha N`; nitrate transport warnings change from 3 to 0. These are causal diagnostics, not acceptance tolerances and not historical truth.

`SYNQ-O001` independently encodes the same conservation discriminator. With `Avc=0.2`, `Hv=0.1`, `St=2`, `Ld=0.1`, the duplicated term is exactly `0.004 kg/m2` while the conservative residual is exactly zero. The synthetic oracle is not B2 and is not evidence of historical prevalence.

## Coverage and non-interference

Natural branch instrumentation records 508 target entries, all NITRATE: 486 with `Iflsol=1` and 22 with `Iflsol=3`. `Iflsol=3` is an exact zero-delta control because `Hv=0`. An isolated frozen-source harness covers reachable `Iflsol=4`. The independent review also confirms source-level structural unreachability of the target second reconstruction for `Iflsol=2` and `Iflsol=5` under valid positive storage denominators. No hidden reachable target analytical mode was found.

The eight-case B1 comparison covers 550 files excluding stdout: 430 are raw-equal, 99 become equal only after the predeclared volatile-metadata normalization, and 21 are scientifically different. All 21 scientific differences stay within the declared nitrate/N-balance or warning surface. No numerical acceptance tolerance is used.

The admitted expected-difference surface includes only the target NITRATE `Reko` reconstruction and causally derived nitrate bookkeeping, balance and warning consequences. Existing `Rekonide`/`CORRECTION(2)` bookkeeping may differ only where the corrected nitrate accounting already propagates through that legacy path.

## Scope boundaries

`Transsub` is a shared generic routine. The evidence does not qualify the same algebraic edit for ammonium, dissolved organic matter/nitrogen/phosphorus, phosphorus or any other substance. A natural diagnostic observation that an unguarded generic probe happened to match the nitrate-scoped probe in the eight supplied cases is non-interference evidence only.

This admission also retains the following boundaries:

- `GreenHouseGasOption=0` only;
- GHG-enabled downstream consequences remain unqualified;
- optional macropore interaction outside the qualified natural matrix remains unqualified;
- no change to the existing negative-concentration trigger, `Optneg`, `Vsmall`, `Ttry`, analytical branch selection, solver/convergence tolerances, hydrology, boundary data or other transport physics.

## Historical uncertainty

No provenance-qualified historical B2 behavioural reference was recovered. GOV03 therefore supplies the qualified route state:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

with:

`G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

Historical revision-53 behaviour and prevalence remain **UNKNOWN**. This admission does not claim historical fidelity or whole-model historical equivalence. Controlled immutable external B0 storage proof remains pending; the source archive, testbank archive and exact `Transsub.for` member identities are nevertheless hash-pinned.

## Admission gate reconciliation

All mandatory Class-B and historical-uncertainty-route gates are explicitly PASS after combining B3B01, B3D09, GOV03, B3Q01, SYNQ-O001 and the completed independent B3B01R review. This includes B0 identity, causal evidence, B2 route, exact local identity, conservation, expected difference, non-interference, branch coverage, independent review, class-specific evidence and explicit residual uncertainty. Composition is not applicable because this is one atomic TCD-015 claim.

## Hard boundary

This B3 admission **does not authorize** a production patch, production migration, B4, generic `Transsub` modification, clipping-policy redesign, tolerance change, solver change, canonical TCD register modification, composition with another correction or central RG05D modification in this workunit.

The next project step after validated B3D12 closeout is a separate central-regie admission integration, expected to become the fifth atomic B3 admission if no newer central admission authority supersedes RG05D. Production remains closed.
