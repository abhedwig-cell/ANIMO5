# TCD-018 independent second-line review packet

Work unit: `ANIMO-B3A03`

Target: `TCD-018`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Review status: `REQUEST_PREPARED_NOT_COMPLETED`

This packet exists to make the B3Q01 independent-review gate executable without allowing the authoring activity to mark its own work as independently reviewed. It is not an admission record.

## Review claim

Review only this atomic claim:

> The detailed-profile water ledger must observe the already-existing interception storage change `Sict-Sic`. The correction is a reporting/ledger-interface correction and must not change hydrology state, hydrology fluxes, water-state representation, SWAP input or interception physics.

Do not broaden the review to global water closure or to other hydrology/interface defects.

## Source identity and exact seam

Recheck the frozen source archive and testbank hashes independently:

- source: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The authoring-side local hash recheck matched both values. The reviewer must not rely only on that statement.

The exact source seam to verify is pinned in `integration/animo-b3/TCD018_SOURCE_SEAM_PIN.json`:

1. `Hydro_detailed.for` lines 10-19 expose `Sic` and `Sict` as routine arguments.
2. For `Iopthyvs == 1`, lines 241-243 include `-(Sict-Sic)` in the whole-profile `Badev` expression.
3. Lines 245-247 then add matrix-water begin-minus-end storage.
4. `Outbal_calc.for` has no `Sic` or `Sict` token in its interface or body.
5. Its Bawa finalization at lines 302-310 includes interception evaporation `Bawa(Eint)` and storage changes for ponding, snow and matrix water, but no interception storage term.
6. `Init.for` line 348 promotes `Sic = Sict` only under its existing `Iopthyvs == 1` and `Hlpimp == 11` condition. TCD-018 must not alter or broaden that lifecycle condition.

The required review result is not merely that a term is absent. The reviewer must confirm the causal classification: existing physical state is complete enough for this narrow store, while the reporting interface is incomplete.

## Natural B1 activation

Recheck the PREP01 LWKM evidence rather than relying on the readiness summary.

The key natural case is `LWKM_gras_1040.2021.2045`. PREP01 reports that all 25 annual total-profile Bawa periods satisfy, to formatted-output precision:

`legacy BAWADV = sum(Hydro_detailed Badev) + final interception storage - initial interception storage`

For the 2008 period:

- legacy Bawa: `-0.0601 mm`
- interception change: `-0.060000000000000005 mm`
- accumulated `Hydro_detailed Badev`: `-5.2640587582358e-5 mm`
- predicted legacy value: `-0.06005264058758236 mm`
- accounting-only probe value: approximately `-5.26e-5 mm`

The reviewer must verify that the approximately `0.0601 mm` residual is causal evidence only. Any attempt to convert it into a water-balance tolerance is a review failure.

## Conservation cross-check

Review SYNQ01 `SYNQ-O003` independently from the B1 diagnostic evidence. Its exact control-volume identity is:

`S0 + precipitation - evaporation - throughfall - S1 = 0`

The oracle is useful because it establishes the role of begin/end interception storage without sharing ANIMO code or control flow. It is not historical B2 evidence and must not be treated as such.

## Non-interference review

For Class A, B3Q01 requires physical state trajectory unchanged, process flux trajectory unchanged, intended ledger/report-only difference, restored identity and non-interference.

The reviewer must examine all three evidence layers:

- PREP01 TCD-specific probe: `changed_hydrology_state=false` and `changed_hydrology_fluxes=false`.
- PREP02 combined Class-A probe: eight natural cases, 379 compared outputs, zero unintended differences, but the candidate contains both TCD-017 and TCD-018.
- MASSQ01 observer: read-only observer, 379 physical outputs compared, zero physical differences after declared volatile normalization, no scientific numeric tolerance.

A critical limitation must remain visible: ANIMO-B3A03 did not run a new isolated eight-case TCD-018 patched executable. The water-only whitelist is derived from the TCD-specific source seam, the PREP01 TCD-specific probe and separation of the combined PREP02 reporting differences. The reviewer must decide whether that is sufficient for the selected route. If not, request a dedicated isolated non-interference run. Do not silently upgrade the evidence.

## Expected difference whitelist

The only predeclared legacy output files allowed to differ are:

- `bawaGP.Out`
- `bawaRP.Out`
- `bawaTP.Out`
- `ani_waGP.Bal`
- `ani_waRP.Bal`
- `ani_waTP.Bal`

Differences are allowed only where the selected reporting period/control volume has nonzero net interception storage change.

No physical output, state trajectory or non-water balance family is whitelisted.

## Residual uncertainty

The review must preserve unrelated water findings. MASSQ01 still contains an unexplained natural water residual, for example CranGrass `TITO=724` at `-0.0030198960466805147 mm`.

TCD-018 must not be used to explain, absorb or mask that residual. The only scientifically supported claim here is the interception-store omission from the Bawa reporting interface.

## Route review

Before review closeout, re-read live GOV02 and PREP02R.

At packet creation PREP02R remained:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`

with no historical artifact obtained, no qualified B2 reference and no external archival request sent. Therefore:

- `NORMAL_B2_AVAILABLE` is not currently valid;
- `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` is also not currently valid because the acquisition effort has not been closed with a stopping rationale.

A second-line reviewer may complete the scientific/readiness review while the route remains pending, but must not mark B3 admission complete.

## Required reviewer record

The reviewer or second-line workunit must record at least:

| field | required result |
| --- | --- |
| independent from correction authoring | `true` |
| reviewed branch/head | exact SHA |
| B0 identity | PASS/FAIL |
| source seam | PASS/FAIL |
| Class-A atomicity | PASS/FAIL |
| natural activation | PASS/FAIL |
| conservation identity | PASS/FAIL |
| non-interference | PASS/FAIL |
| output whitelist | PASS/FAIL |
| residual uncertainty | PASS/FAIL |
| live route state | PASS/FAIL |
| overall second-line result | PASS/FAIL |

Any failed mandatory scientific gate keeps the disposition `UNRESOLVED_NOT_ADMITTED`. A passing second-line review still does not admit TCD-018 until the route gate is valid and a separate B3 disposition record explicitly admits it.
