# TCD-018 second-line technical review

Work unit: `ANIMO-B3A03R`

Target: `TCD-018`

Candidate reviewed: `work/animo-b3a03-tcd018-class-a-admission-readiness` at `8eaaca34e4f0d906c2d8245f0df232586efe8ff3`.

## Disposition

Technical result:

`PASS_TCD018_CLASS_A_SCIENTIFIC_READINESS_TECHNICALLY_STRENGTHENED_BY_ISOLATED_NONINTERFERENCE_RUN`

Governance result:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_AND_VALID_ROUTE_STILL_REQUIRED`

This workunit deliberately does **not** claim the B3Q01 independent-second-line gate. It was executed from the same ChatGPT authoring context that prepared ANIMO-B3A03. The evidence was re-read and source bytes were rechecked independently, but reviewer independence from correction authoring is not genuinely established.

## 1. Frozen B0 identity recheck

The locally supplied frozen archives were hashed again before technical review.

- source ZIP: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank ZIP: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Both match the frozen B0 identities.

Relevant source file hashes also re-match the earlier source manifest:

- `Hydro_detailed.for`: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`
- `Outbal_calc.for`: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`

Result: `PASS`.

## 2. Exact source seam

The source was re-opened from the frozen ZIP rather than relying on the B3A03 summary.

`Hydro_detailed.for`:

- line 14 receives `Sic` and `Sict`;
- lines 241-243 include `-(Sict-Sic)` in detailed whole-profile `Badev` for `Iopthyvs == 1`;
- lines 245-247 then add matrix-water begin-minus-end storage.

`Outbal_calc.for`:

- contains zero `Sic` tokens and zero `Sict` tokens;
- lines 302-310 form top-profile `Bawa(Ddev)`;
- interception evaporation `Bawa(Eint)` is included;
- ponding, snow and matrix-water storage changes are included;
- interception begin/end storage is absent and cannot be observed through the existing interface.

`Init.for` line 348 retains the existing lifecycle:

`If(Iopthyvs .Eq. 1 .and. Hlpimp==11) Sic = Sict`

Nothing in TCD-018 requires changing or broadening that condition.

The causal classification therefore survives direct review: the physical interception state already exists and participates in detailed hydrology closure; the public water-ledger interface is incomplete.

Result: `PASS`.

## 3. Atomic Class-A claim

The reviewed claim is limited to:

> observe the already-existing interception storage change in the top-profile water ledger.

The correction does not require:

- a SWAP hydrology change;
- new interception physics;
- a new water-state representation;
- altered forcing;
- altered state promotion;
- altered process fluxes.

This remains a Class-A accounting/reporting-only correction.

Result: `PASS`.

## 4. Natural causal activation

PREP01 natural evidence was re-read at its source artifact.

Case: `LWKM_gras_1040.2021.2045`.

For the 2008 period:

- legacy total-profile Bawa: `-0.0601 mm`;
- accumulated detailed-hydrology `Badev`: `-5.2640587582358e-5 mm`;
- interception storage change: `-0.060000000000000005 mm`;
- predicted legacy residual from the two terms: `-0.06005264058758236 mm`.

Across the reported annual periods PREP01 attributes the characteristic approximately `0.06 mm` pattern to the omitted interception storage change.

The `0.0601 mm` value is causal evidence. It is not an acceptance epsilon and no such tolerance is introduced here.

Result: `PASS`.

## 5. Conservation authority

PREP06 defines the detailed-profile water identity as:

`external water in - external water out - Δ(matrix water + snow + ponding + interception) = 0`

and explicitly marks the public Bawa interception-storage omission as TCD-018.

SYNQ01 `SYNQ-O003` independently checks the interception control volume:

`S0 + precipitation - evaporation - throughfall - S1 = 0`

with an exact zero residual under its synthetic microcase. The oracle is strongly independent from ANIMO code and confirms that interception begin/end storage belongs in the selected water control volume. It is not B2 historical evidence.

Result: `PASS`.

## 6. New isolated TCD-018 executable check

The largest open technical limitation in B3A03 was that PREP02's eight-case Class-A probe combined TCD-017 and TCD-018. ANIMO-B3A03R therefore ran a new isolated TCD-018 diagnostic execution copy.

The frozen source archive itself remained unchanged.

### Build identity

The baseline GNU diagnostic was rebuilt using the PREP01 contract:

- GNU Fortran 14.2.0;
- `-ffree-form`;
- `-ffree-line-length-none`;
- `-fallow-argument-mismatch`;
- `-std=legacy`;
- `-fdefault-real-8`;
- `-fdefault-double-8`;
- `-fno-automatic`;
- link `-Wl,--build-id=none`.

The rebuilt baseline executable SHA-256 was:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This is byte-identical to the PREP01 diagnostic executable identity.

The isolated TCD-018 execution-copy executable SHA-256 was:

`2ef9347fab024fe932304754811287c7a05e9722c11f6e1fb070afe8de73c1e7`

### Temporary reporting-only correction

Only the temporary execution copy was changed:

1. pass existing `Sic` and `Sict` to `Outbal_calc`;
2. accumulate `(Sict-Sic)*1000` for top-profile balance periods;
3. subtract that reporting accumulator from `Bawa(Ddev)` at `Optout` finalization;
4. reset only that reporting accumulator after finalization.

No physical state or hydrology/process equation was changed.

### Eight-case execution

The eight PREP01/PREP02 compatible natural cases were executed for baseline and isolated candidate. Both executions reached the legacy `Successful completion of simulation` path for all eight cases.

The comparison considered generated `.Out/.out/.Bal/.bal` artifacts outside testcase input directories. Only known timestamp and elapsed-time text lines were normalized. No scientific numeric tolerance was used.

| case | compared | equal | whitelisted differences | unexpected | missing/extra |
| --- | ---: | ---: | ---: | ---: | ---: |
| CranGrass | 31 | 31 | 0 | 0 | 0 |
| CranMais | 23 | 23 | 0 | 0 | 0 |
| GrassPeat | 60 | 60 | 0 | 0 | 0 |
| LWKM_gras_1040.2021.2045 | 53 | 47 | 6 | 0 | 0 |
| Puitmijn_Cranendonck_60 | 77 | 77 | 0 | 0 | 0 |
| RuurloGrass | 72 | 72 | 0 | 0 | 0 |
| STONE_akk_0006.2001.2015 | 44 | 44 | 0 | 0 | 0 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 16 | 16 | 0 | 0 | 0 |

Totals:

- outputs compared: `376`;
- equal after declared volatile normalization: `370`;
- intended differences: `6`;
- unexpected differences: `0`;
- missing/extra: `0`.

The six differences are exactly the predeclared water-ledger whitelist:

- `ani_waGP.Bal`;
- `ani_waRP.Bal`;
- `ani_waTP.Bal`;
- `bawaGP.Out`;
- `bawaRP.Out`;
- `bawaTP.Out`.

No non-water balance output or ordinary physical/process output differs after the declared volatile normalization.

Result: `PASS_TECHNICAL`.

## 7. Isolated water-balance effect

For LWKM, maximum absolute `BAWADV` values changed as follows:

| file | baseline max abs | isolated TCD-018 max abs |
| --- | ---: | ---: |
| `bawaGP.Out` | `0.06 mm` | `4.65e-5 mm` |
| `bawaRP.Out` | `0.06 mm` | `4.93e-5 mm` |
| `bawaTP.Out` | `0.0601 mm` | `2.07e-4 mm` |

The largest corrected total-profile period is `0.000207 mm` in 2005. This matches the previously observed detailed-hydrology closure scale and is not used as a newly invented tolerance.

The new isolated run removes the main technical ambiguity left by the combined TCD-017/TCD-018 PREP02 probe.

## 8. Residual uncertainty remains visible

MASSQ01 still retains unrelated unexplained water residuals. In particular:

`CranGrass TITO=724: -0.0030198960466805147 mm`

remains an `UNEXPLAINED_RESIDUAL`.

TCD-018 does not explain, correct, absorb or tolerance-mask that residual. No global exact-water-closure claim follows from this review.

Result: `PASS_RETAINED`.

## 9. Live admission-route recheck

GOV02 remains at:

`db7add6f9561730bbf352aa7fd3f3968405cfaa3`

Its policy allows a Class-A no-B2 route only after documented B2 acquisition closure plus the Class-A scientific burden and independent second-line review.

PREP02R remains at:

`e29aa75f782a17e1cca6b0c2791ba04077e8bde7`

with status:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`

and still records:

- `external_request_sent=false`;
- `historical_reference_artifact_obtained=false`;
- `reference_qualified=false`.

Therefore neither `NORMAL_B2_AVAILABLE` nor the historical-uncertainty route is currently valid.

Result: `FAIL_PENDING_NO_VALID_ROUTE`.

## 10. Reviewer-independence gate

Although this workunit deliberately re-fetched the authoritative evidence, independently rehashed B0 and reran an isolated executable qualification, it was executed by the same ChatGPT authoring context that prepared ANIMO-B3A03.

The B3Q01 requirement is stronger than methodological rechecking: second-line review must be separate from correction authoring. That condition cannot be honestly certified here.

Result:

`FAIL_NOT_INDEPENDENT`

This is a governance failure only. It does not reverse the technical PASS results above.

## Final decision

The technical Class-A readiness case for TCD-018 is now stronger than at B3A03 closeout because an isolated eight-case TCD-018 executable non-interference run has been added and passes its predeclared whitelist exactly.

However, B3 admission remains fail-closed for two independent reasons:

1. no GOV02-valid admission route is currently open;
2. genuinely independent second-line review is still missing.

Final workunit disposition:

`TECHNICAL_REVIEW_PASS_BUT_INDEPENDENT_SECOND_LINE_AND_ROUTE_GATES_NOT_SATISFIED_TCD018_NOT_ADMITTED`
