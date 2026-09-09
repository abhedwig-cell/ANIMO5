# ANIMO-STATEQ01 supplied-testbank restricted-core suitability scan

Status: `DIAGNOSTIC_TESTBANK_COVERAGE_EVIDENCE_NO_STATE_ADMISSION`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Purpose

This diagnostic scan asks whether the supplied frozen ANIMO testbank already contains a natural full-run case suitable for the first `CORE_CNP_SUBSURFACE_ONLY` split-run campaign.

The scan is deliberately narrower than model qualification. It checks the source-qualified zero-surface application envelope and the configured crop ownership route. It does not change any physical input, repair any restart defect, or promote the GNU diagnostic executable to historical-reference evidence.

## Frozen identities and observer build

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The deterministic GNU diagnostic executable rebuilt from that source has SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This matches the PREP01 reproducible diagnostic build identity. The build remains `DIAGNOSTIC_NOT_REFERENCE`.

For this scan an execution-copy-only observer was inserted immediately after the source `Flpn` decision in `Hydro_detailed.for`. The observer writes only:

`Tito, Pn, Snla, Pnt, Snt, Flpn`

and does not assign any model state. The original execution-copy `Hydro_detailed.for` SHA-256 was:

`f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`

The observer-instrumented copy SHA-256 was:

`faa0a17ff2a42a9a082474cd7a4d2bc986c227ab9216f40eac819aec6aca3872`

The observer executable SHA-256 was:

`faa0d2349615e7bf2de3871bcf75b93277faf3746b28bb973d8e8698a16dec6d`

No frozen source or frozen testcase bytes were modified.

## Envelope criterion

All supplied runnable cases use detailed hydrology (`HydrologicInput=2`). STATEQ01 therefore applies the deliberately strict restricted-core invariant at every observed interval:

```text
Pn + Snla == 0
Pnt + Snt  == 0
```

This is stricter than the legacy `Flpn` threshold. Positive surface storage below `1e-4` still violates the restricted profile.

## Result

Eight source-compatible supplied cases reached normal diagnostic simulation completion and produced observer records. `GHGMais` still fails before the hydrology observer because of the previously known source/testcase contract mismatch.

Only one complete successful case, `RuurloGrass`, satisfies the strict zero-surface invariant for every observed interval:

- observer records: `1947`;
- maximum `Pn + Snla`: `0.0 m`;
- maximum `Pnt + Snt`: `0.0 m`;
- nonzero strict-envelope records: `0`;
- legacy `Flpn=1` records: `0`.

The other successful cases all contain physically positive surface storage at least once. Some violations occur below the legacy activation threshold. For example, the first observed nonzero surface state in `CranGrass` has candidate surface storage `1.401081e-08 m` while `Flpn=0`. This directly confirms why the restricted-core guard cannot be weakened to `Flpn==0`.

## Crop-route consequence

The testbank does not provide a clean full-run realization of the architectural `crop_mode=none` candidate.

Source control flow distinguishes `CropUptakeModel=1` as the external crop route. When `CropUptakeModel=0`, the main program selects an internal plant or grass route from the current crop code. The supplied cases use one of those two ownership routes rather than a demonstrated no-crop runtime topology.

`RuurloGrass`, the only full-run zero-surface witness, uses `CropUptakeModel=0` and therefore an internal ANIMO crop route. It is not a clean natural runtime witness for `CORE_CNP_SUBSURFACE_ONLY` with crop excluded. Using it as if crop continuation did not exist would bypass the PREP12 crop restart findings and is not admitted.

The successful external-crop cases observed in this scan (`GrassPeat`, `LWKM_gras_1040.2021.2045`, `STONE_akk_0006.2001.2015`) all leave the strict zero-surface envelope somewhere in the full run. `GHGMais` is additionally blocked by its source/testcase contract and GHG scope.

## Admission consequence

The scan improves the test strategy but does not strengthen STATE admission.

It establishes:

1. the strict surface guard is naturally relevant in the supplied corpus;
2. `RuurloGrass` is a natural full-run zero-surface witness for guard and upper-boundary-reservoir diagnostics;
3. the supplied testbank does not currently provide an uncontaminated full-run `CORE_CNP_SUBSURFACE_ONLY` split-run qualification case with crop ownership absent;
4. therefore RC-R1 cannot honestly be claimed as a natural supplied-core-only split-run test merely by selecting `RuurloGrass`;
5. a later campaign must either use a separately qualified synthetic core-only fixture or qualify a broader profile whose crop/external-crop continuation contract is closed.

This is an evidence-coverage gap, not a new theory/code discrepancy and no TCD number is allocated.

Machine-readable results are in:

`integration/animo-state/RESTRICTED_CORE_TESTBANK_SUITABILITY.csv`

Final classification:

`SUPPLIED_TESTBANK_HAS_ZERO_SURFACE_WITNESS_BUT_NO_CLEAN_FULL_RUN_CORE_ONLY_PROFILE_WITNESS`
