# ANIMO-B3D06 — TCD-018 B3 Admission Closeout

## Decision

TCD-018 is admitted as one atomic Class-A scientific accounting correction under the qualified GOV03 historical-uncertainty route.

Decision string:

`ADMIT_TCD018_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY`

Canonical disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

## Atomic scope

The admitted claim is limited to the selected Bawa water-ledger interface for canopy interception storage. The already-existing physical state change `Sict-Sic` must be observed in that reporting control volume:

`Bawa_Ddev_corrected = Bawa_Ddev_legacy - sum((Sict-Sic)*1000)`

over the active reporting period/control volume.

This is `A_ACCOUNTING_REPORTING_ONLY`. The admission does not change hydrology state, hydrology/process fluxes, forcing, interception physics, state-promotion semantics, SWAP/SWATRE payload, or testcase scientific inputs.

## Admission authorities

Formal route reconciliation remains `ANIMO-B3D05@2f06cc86225637f8dadfdd969fe48dcf851b9ee2`.

The evidence-remediation workunit is `ANIMO-B3A03E@4c92b27ed5bbcaadb0e703e622e8c3f690458fa8`.

The genuinely separate R2 second-line review is `ANIMO-B3A03R2@fc4a53c2e2e32dee27062959c7ecba7b605cf398`, with result:

`PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW`

Final R2 GitHub Actions run `34443743545` passed on that exact head. The earlier independent FAIL at `57cfdfb3a7fb982f6692b0b32f8c8aa044c57fd7` remains historically valid for the earlier, less granular evidence packet and is not overwritten.

## Evidence reconciled for admission

The R2 review independently re-audited the remediated packet. The 25-period LWKM reconciliation contains exactly 25 contiguous annual rows for 1991–2015, 36 detailed-hydrology probe records per period, 900 total records, and final TITO 9131. The 2008 discriminator retains the legacy Bawa deviation near `-0.0601 mm` while the independently reconstructed detailed-hydrology residual remains near the much smaller detailed closure scale. `0.0601 mm` is causal evidence only and is not an acceptance tolerance.

The eight-case non-interference package contains 16 successful baseline/candidate run records and 376 unique `(case,path)` output rows. R2 independently re-derived 270 raw-equal outputs, 100 equal after only declared volatile metadata normalization, six whitelisted differences, zero unexpected differences, and zero missing/extra outputs. The six differences occur only in LWKM and only on `ani_waGP.Bal`, `ani_waRP.Bal`, `ani_waTP.Bal`, `bawaGP.Out`, `bawaRP.Out`, and `bawaTP.Out`.

Physical-state and process-flux non-interference are not inferred from output equality alone. Their primary basis is the independently reviewed bounded write set: the qualification candidate reads existing `Sic/Sict`, adds only a reporting accumulator and a `Bawa(Ddev)` reporting write, does not assign `Sic/Sict`, and does not modify hydrology or process-flux assignments. The output digest ledger is corroborating evidence.

## Historical uncertainty and residual boundaries

No qualified B2 behavioural reference exists. Historical revision-53 behaviour therefore remains `UNKNOWN`; historical fidelity is not claimed.

The MASSQ01 CranGrass residual at `TITO=724`, `-0.0030198960466805147 mm`, remains `UNEXPLAINED_RESIDUAL` outside TCD-018. This admission does not convert that residual into TCD-018 evidence and makes no global water-closure claim.

## What this admission does not authorize

This admission does **not** authorize a production-source patch, B4 migration, production migration, whole-model equivalence, historical equivalence, hydrology changes, canonical-TCD-register changes, or composition with any unrelated TCD.

The next project-level action is to integrate this third atomic scientific admission into the central admission inventory while retaining B3 as incomplete and production migration as closed.
