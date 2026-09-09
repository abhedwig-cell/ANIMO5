# TCD-018 independent second-line review handoff

Work unit source: `ANIMO-B3A03R`

Target: `TCD-018`

Candidate readiness branch: `work/animo-b3a03-tcd018-class-a-admission-readiness`

Technical review branch: `work/animo-b3a03r-tcd018-second-line-review`

Technical review head: `36a84680daba259b22d92e61fc33a9a80f8b8323`

## Purpose

This handoff is intended for a genuinely independent second-line reviewer or review workunit. It must not be self-certified by the authoring context that prepared ANIMO-B3A03 or ANIMO-B3A03R.

The technical review already strengthened the evidence with an isolated TCD-018-only eight-case executable non-interference run. The remaining second-line task is to independently verify the evidence and record PASS/FAIL without relying on the authoring conclusion.

## Atomic claim under review

The existing detailed-hydrology interception storage state `Sic/Sict` must be observed in the top-profile water ledger. The correction is accounting/reporting only and must not alter SWAP hydrology, interception physics, water-state representation, state promotion, process fluxes or forcing.

Do not broaden this claim to global water closure.

## Required starting refs

Review these exact branches/heads before accepting any prior result:

- B3A03 candidate: `work/animo-b3a03-tcd018-class-a-admission-readiness` at `8eaaca34e4f0d906c2d8245f0df232586efe8ff3`
- B3A03R technical review: `work/animo-b3a03r-tcd018-second-line-review` at `36a84680daba259b22d92e61fc33a9a80f8b8323`
- GOV02: `work/animo-gov02-evidence-dag-reconciliation` at `db7add6f9561730bbf352aa7fd3f3968405cfaa3`
- PREP02R: `work/animo-prep02r-historical-reference-recovery` at `e29aa75f782a17e1cca6b0c2791ba04077e8bde7`, unless live recheck shows a newer head

## Frozen B0 identities to independently verify

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Relevant source file identities already recorded by the authoring side:

- `Hydro_detailed.for`: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`
- `Outbal_calc.for`: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`

The reviewer must independently recheck, not merely copy these values.

## Source seam to verify

Verify directly from frozen B0 source that:

1. `Hydro_detailed.for` receives `Sic` and `Sict` and includes `-(Sict-Sic)` in detailed whole-profile `Badev` for the applicable detailed-hydrology path.
2. `Outbal_calc.for` does not receive or otherwise observe `Sic/Sict` and its public Bawa finalization includes interception evaporation but not interception storage change.
3. `Init.for` retains the existing conditional `Sic = Sict` lifecycle and the proposed accounting correction does not change it.
4. The causal seam is therefore a ledger-interface omission rather than missing physical state or hydrology physics.

## Natural activation and conservation

Recheck the PREP01 natural case `LWKM_gras_1040.2021.2045`, including the 2008 example:

- legacy total-profile Bawa approximately `-0.0601 mm`;
- interception storage change approximately `-0.060000000000000005 mm`;
- accumulated detailed-hydrology `Badev` approximately `-5.2640587582358e-5 mm`.

The raw `0.0601 mm` value is causal evidence only and must not be used as a tolerance.

Recheck PREP06 detailed-profile water identity:

`external water in - external water out - Δ(matrix water + snow + ponding + interception) = 0`

Recheck SYNQ01 oracle `SYNQ-O003` as an independent conservation cross-check. It is not B2 historical evidence.

## Isolated TCD-018 executable evidence to verify

ANIMO-B3A03R records a temporary execution-copy candidate that changes only the reporting interface and period accumulator. Frozen source/testbank were not changed.

Recorded eight-case comparison:

- cases completed: `8/8`;
- outputs compared: `376`;
- equal after declared volatile normalization: `370`;
- whitelisted differences: `6`;
- unexpected differences: `0`;
- missing/extra: `0`;
- no scientific numeric tolerance.

Declared whitelist:

- `ani_waGP.Bal`
- `ani_waRP.Bal`
- `ani_waTP.Bal`
- `bawaGP.Out`
- `bawaRP.Out`
- `bawaTP.Out`

Only LWKM activated the correction in that eight-case set.

The reviewer should independently inspect the recorded method/results and may rerun the qualification if needed. If the evidence cannot be independently reproduced or trusted, record FAIL rather than inheriting PASS.

## Residual uncertainty that must remain visible

MASSQ01 retains unrelated unexplained water residuals, including:

`CranGrass TITO=724: -0.0030198960466805147 mm`

TCD-018 must not explain, mask or tolerance-absorb this or other unrelated residuals. No global water-closure claim is allowed.

## Live route gate

Before final reviewer disposition, re-read live GOV02 and PREP02R.

At handoff creation PREP02R still recorded:

- `BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`;
- `external_request_sent=false`;
- `historical_reference_artifact_obtained=false`;
- `reference_qualified=false`.

Therefore neither `NORMAL_B2_AVAILABLE` nor `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` was eligible at that point.

A reviewer may PASS the independent technical/scientific second-line review while route remains pending. That does not admit TCD-018.

## Required reviewer output

Create a separate authoritative reviewer record that includes at least:

- reviewer or workunit identity;
- statement that reviewer is independent from B3A03/B3A03R correction authoring;
- exact reviewed branch/head;
- B0 identity PASS/FAIL;
- source seam PASS/FAIL;
- Class-A atomicity PASS/FAIL;
- natural activation PASS/FAIL;
- conservation PASS/FAIL;
- isolated non-interference PASS/FAIL;
- output whitelist PASS/FAIL;
- residual uncertainty PASS/FAIL;
- live admission-route result PASS/FAIL/PENDING;
- overall independent second-line result PASS/FAIL;
- explicit `admitted=false` unless a separate B3 admission authority later records all mandatory gates PASS.

## Fail-closed conditions

Return FAIL or PENDING if any of the following occurs:

- any candidate-attributable physical state or process-flux difference;
- any need to alter SWAP hydrology or interception physics;
- any non-whitelisted output difference without separate causal qualification;
- use of `0.0601 mm`, `0.000207 mm`, or another observed residual as an acceptance tolerance;
- use of GNU B1 or SYNQ01 as historical B2 truth;
- unresolved reviewer independence;
- attempt to admit while the selected GOV02 route is invalid;
- masking of unrelated MASSQ01 residuals.

## Expected independent technical outcome if evidence reproduces

The authoring-side technical result is:

`PASS_TCD018_CLASS_A_SCIENTIFIC_READINESS_TECHNICALLY_STRENGTHENED_BY_ISOLATED_NONINTERFERENCE_RUN`

This is provided only as a result to challenge, not as an expected answer to copy.

The current governance disposition remains:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_AND_VALID_ROUTE_STILL_REQUIRED`
