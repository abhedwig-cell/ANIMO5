# ANIMO-B3A03R2 - TCD-018 Independent Second-Line R2 Review

Result: `PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW`

This re-review was executed in a new ChatGPT context that is separate from the B3A03, B3A03E and B3D05 authoring contexts. This is context separation only. No organizational or human independence is claimed.

The previous result `FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW` remains historically valid for the earlier evidence packet. R2 does not rewrite that result. It evaluates the remediated packet independently.

A PASS here is review evidence only. It is not B3 admission and does not authorize B4 or production migration.

## Review object and pinned authorities

The clean R2 branch was rechecked immediately before the first review write and still pointed exactly to:

`review/animo-b3a03r2-tcd018-independent-second-line@4c92b27ed5bbcaadb0e703e622e8c3f690458fa8`

The following authority heads were rechecked live:

- `ANIMO-B3A03@8eaaca34e4f0d906c2d8245f0df232586efe8ff3`
- `ANIMO-B3A03R@0876e6e1b6ce33ee5e7b812ab4107f54760d6b27`, evidence input only
- `ANIMO-B3D05@2f06cc86225637f8dadfdd969fe48dcf851b9ee2`
- previous independent review `review/animo-b3a03r-tcd018-independent-second-line@57cfdfb3a7fb982f6692b0b32f8c8aa044c57fd7`
- `ANIMO-B3A03E@4c92b27ed5bbcaadb0e703e622e8c3f690458fa8`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-RG05B@c353c3179f213c1bf24c48b3c06f8065c760d3e2`
- `ANIMO-PREP06@9b1f1ea51c24fb82823290193651830dc61ea3c8`
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- `ANIMO-MASSQ01@6ccddd631a8dcc21f06b1384baf2561e81179e75`

GitHub issue #27 and all three comments present immediately before writing were read. The issue and comments are handoff/context evidence, not scientific proof.

## Atomic claim

R2 reviews only the Class-A claim that the already-existing interception-storage state change `Sict-Sic` must be observed in the selected Bawa water ledger:

`Bawa_Ddev_corrected = Bawa_Ddev_legacy - sum((Sict-Sic)*1000)`

over the active reporting period and control volume.

Classification: `A_ACCOUNTING_REPORTING_ONLY`.

No hydrology state, hydrology flux, forcing, interception physics, state-promotion semantics, SWAP/SWATRE payload or testcase scientific input may change under this claim.

## Independent scientific recheck

Frozen identity is unchanged. The source and testbank SHA-256 pins are respectively:

- `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

PREP06 independently reverified those identities. Its conserved-state inventory identifies `Sic,Sict` as canopy-interception water state, with `Sic` as begin state, `Sict` as end state and the existing promotion `Sic=Sict` in `Init`. The source-seam pin gives the exact lifecycle condition `If(Iopthyvs .Eq. 1 .and. Hlpimp==11) Sic = Sict`. R2 does not broaden or modify this condition.

The frozen-source seam is internally coherent. `Hydro_detailed.for` receives `Sic,Sict` and, for the detailed whole-profile path, subtracts `(Sict-Sic)` in `Badev`. `Outbal_calc.for` has no `Sic` or `Sict` token in the frozen interface/body. Its Bawa finalization observes interception evaporation and ponding, snow and matrix-water storage changes, but not interception storage. This is an observer/interface omission in the selected ledger, not absent hydrological state.

PREP06 states the detailed-profile control-volume identity as:

`external water in - external water out - delta(matrix water + snow + ponding + interception) = 0`

SYNQ-O003 independently reconstructs the interception control-volume identity as `S0 + precipitation - evaporation - throughfall - S1 = 0`. It is used here only as a conservation oracle. Its own boundary explicitly says it does not create B2, establish historical execution, qualify SWAP hydrology or admit a production ledger.

The LWKM natural case activates the seam. The approximately `0.0601 mm` legacy residual is causal evidence only. It is not an acceptance tolerance. MASSQ01 separately retains CranGrass `TITO=724` water residual `-0.0030198960466805147 mm` as `UNEXPLAINED_RESIDUAL`; it remains outside TCD-018. No global water-closure claim is made.

## Former gate 8: 25-period reconciliation

`integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv` is now sufficiently granular for independent audit. R2 derives, from the rows rather than the B3A03E summary:

- 25 rows;
- years exactly 1991 through 2015;
- contiguous reporting periods from `TITO 0` through `TITO 9131`;
- 36 fresh detailed-hydrology probe records in every period;
- 900 probe records total;
- final `TITO = 9131`.

For every row, the stored raw reconstruction is checked from the row values as `hydro_badev_sum_raw_mm + interception_storage_change_sum_raw_mm`. The stored reconstruction-minus-formatted and candidate-minus-raw columns are likewise recomputed from the row values. These are serialization/arithmetic consistency checks, not scientific acceptance tolerances.

The 2008 discriminator independently reads:

- period `6209 -> 6575`;
- legacy formatted Bawa deviation `-0.060100000000000001 mm`;
- raw Hydro_detailed `Badev` sum `-5.2640587582358024e-05 mm`;
- raw interception storage change `-0.059999999999999984 mm`;
- reconstructed legacy value `-0.060052640587582341 mm`;
- fresh candidate Bawa deviation `-5.2599999999999998e-05 mm`.

The residual between raw reconstruction and formatted legacy output is therefore evidence of formatting granularity, not an acceptance criterion. Former gate 8 is `PASS`.

## Former gates 10 and 11: run provenance and independently derived totals

The remediated packet contains exactly 16 run-completion records in `TCD018_EIGHT_CASE_RUN_LEDGER.json`: baseline and candidate for each of eight natural cases. Every record declares successful completion evidence via the message output, and baseline/candidate runner-stdout digests are paired per case.

R2 audits all four files under `integration/animo-b3/tcd018_output_digest_ledger/` directly and derives the totals from their rows. The expected B3A03E summary is not used as the derivation source. The derived result is:

- 376 unique `(case,path)` rows;
- `270 EQUAL_RAW`;
- `100 EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY`;
- `6 DIFFERENT_WHITELISTED`;
- `0` unexpected classifications;
- no duplicate `(case,path)` rows.

The independently derived per-case row counts are:

- CranGrass 31;
- CranMais 23;
- GrassPeat 60;
- LWKM_gras_1040.2021.2045 53;
- Puitmijn_Cranendonck_60 77;
- RuurloGrass 72;
- STONE_akk_0006.2001.2015 44;
- Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA 16.

Digest semantics are checked by classification. Raw-equal rows carry a common raw-byte digest. Volatile-normalized rows carry a common normalized-byte digest. Whitelisted-different rows carry separate unequal reference and candidate normalized-byte digests. No numeric epsilon is part of this classification.

The comparison implementation independently inspected by R2 normalizes only five explicitly anchored complete metadata-line forms: file creation timestamp, output run-start timestamp, message run-start timestamp, message run-end timestamp and elapsed CPU seconds. Scientific numeric tokens are never tolerance-filtered for equality. A numerical-difference summary, where produced, is diagnostic only.

The six different rows occur only in `LWKM_gras_1040.2021.2045` and form exactly this surface:

- `ani_waGP.Bal`
- `ani_waRP.Bal`
- `ani_waTP.Bal`
- `bawaGP.Out`
- `bawaRP.Out`
- `bawaTP.Out`

The qualification-only candidate builder is also independently inspected. It fails if the frozen source archive SHA is wrong; requires exact one-occurrence patch seams; modifies only the execution-copy `Animo.for` call surface and execution-copy `Outbal_calc.for`; passes existing `Sic,Sict` into the reporting routine; creates only a TCD-018 reporting accumulator; subtracts that accumulator from `Bawa(Ddev)` at reporting finalization; resets only that reporting accumulator; and fails unless the resulting executable has exact SHA-256 `c1e281d5ceaa45952dc7ee21041454fbfab5bee34aa8aee09d59604b75826bbe`.

This establishes an auditable persisted provenance chain for the comparison. It does not turn the current-GNU diagnostic executable into B2. Former gates 10 and 11 are `PASS`.

## Former gates 13 and 14: physical state and process-flux non-interference

R2 does not infer internal state or process-flux trajectory equality merely from equality of output files.

The primary basis is the candidate-builder write set. The TCD-018 patch reads existing `Sic,Sict` and introduces writes only to the reporting accumulator `Tcd018IcCu` and the reporting deviation `Bawa(Ddev)`. It contains no assignment to `Sic`, `Sict`, hydrology state, forcing or process/hydrology flux variables, and does not modify the existing state-promotion path. The per-output digest ledger is corroborating evidence that this narrow static write set has no observed spillover across the eight natural cases; it is not the logical basis for claiming internal trajectory identity.

Within the bounded Class-A candidate and eight-case qualification scope, physical-state non-interference and process/hydrology-flux non-interference are therefore `PASS`. This is not a claim about arbitrary future implementations that might use a different write set.

## Former gate 15: non-water reporting

The complete 376-row comparison ledger contains only six scientific differences, all on the predeclared LWKM water-ledger surface above. Every other output row is either byte-identical or identical after only the declared volatile metadata normalization. Thus non-water reporting lies outside the expected-difference surface and former gate 15 is `PASS`.

## Route and historical boundary

GOV03 remains live with `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and `G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`. B3D05 remains the formal TCD-018 route reconciliation. No qualified B2 exists, so historical revision-53 behaviour remains `UNKNOWN`.

RG05B does not admit TCD-018. This R2 review does not perform admission.

## Per-gate disposition

1. Frozen B0 source/testbank identity: `PASS`.
2. Exact physical ownership and lifecycle of `Sic/Sict`: `PASS`.
3. Hydro_detailed interception-storage observation: `PASS`.
4. Outbal_calc/Bawa omission: `PASS`.
5. Atomic `A_ACCOUNTING_REPORTING_ONLY` classification: `PASS`.
6. Natural LWKM activation: `PASS`.
7. PREP06 conservation identity: `PASS`.
8. SYNQ-O003 restricted to independent conservation-oracle role, never B2: `PASS`.
9. `0.0601 mm` used only as causal evidence, never tolerance: `PASS`.
10. MASSQ01 CranGrass `TITO=724` residual retained as unrelated `UNEXPLAINED_RESIDUAL`: `PASS`.
11. No global water-closure claim: `PASS`.
12. Historical revision-53 behaviour remains `UNKNOWN`: `PASS`.
13. GOV03/B3D05 historical-uncertainty route remains live: `PASS`.
14. Former gate 8, full 25-period reconciliation: `PASS`.
15. Former gate 10, isolated eight-case provenance and granular digest evidence: `PASS`.
16. Former gate 11, run/output totals independently audit-derived: `PASS`.
17. Former gate 13, physical-state trajectory non-interference: `PASS`, based primarily on bounded static write-set analysis, not output equality alone.
18. Former gate 14, hydrology/process-flux trajectory non-interference: `PASS`, on the same bounded write-set basis.
19. Former gate 15, non-water reporting outside expected-difference surface: `PASS`.

No mandatory gate remains unresolved in the bounded readiness-review object.

## Exact evidence artifact pins

Reviewed Git blob SHAs include:

- `integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv`: `a8513296e856c716ee1c53d839920d089f92492f`
- `integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json`: `49e0fb498a1e6324290c533aad20485be07d27d5`
- `integration/animo-b3/tcd018_output_digest_ledger/CranGrass.csv`: `52b99da183c20b517a26bd9059da8bc4bc10bd5a`
- `integration/animo-b3/tcd018_output_digest_ledger/part2.csv`: `bd238a6c8c3d20c607535d959be4849d860bcfa3`
- `integration/animo-b3/tcd018_output_digest_ledger/part3.csv`: `749c9a2ad62325702a1578da1db602cf2e554a2a`
- `integration/animo-b3/tcd018_output_digest_ledger/part4.csv`: `59450584b6339c4c001f6d39f98f6f2a7fa3604d`
- `integration/animo-b3/TCD018_EVIDENCE_REMEDIATION_MANIFEST.json`: `e2500475578f6bbd6034c268774ac5f606a91bbd`
- `integration/animo-b3/ANIMO-B3A03E_STATUS.json`: `e931dacc6d22c4dc2eb3478f739b92a041c8b81a`
- `tools/build_tcd018_reporting_candidate.py`: `e52cb88299236aa06ba4b7fd7d8f20705cf7ec14`
- `integration/animo-b3/TCD018_SOURCE_SEAM_PIN.json`: `cbc68024db6b649370ffe55a55b2a2de346ac2d2`
- `docs/prep06/CONSERVED_STATE_INVENTORY.csv`: `838f224fc67a72371437c6d5b6e75cd03f5c8d51`
- `docs/prep06/PROCESS_CONSERVATION_IDENTITIES.md`: `f0e9bfe0432cc7651f3421eccaef472111f36721`
- `integration/animo-synthetic/SYNTHETIC_ORACLE_REGISTER.json`: `4c215d19844614de8868380fb03f93268ea4c5d8`
- `integration/animo-mass/MASSLEDGER_RESIDUAL_REGISTER.csv`: `356cea3db7818905a8fb173af7df6fb0d42fa494`
- `tools/compare_legacy_output_trees.py`: `0b5928184ffef38caf1f8040f47fa4ea5366c62f`
- previous R1 `integration/animo-b3/TCD018_INDEPENDENT_REVIEW_RESULT.json`: `a98b2d094890f9f88587b0b6c196d850ed5fe88f`

## Disposition

`PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW`

This PASS closes the independent R2 readiness-review gate for the bounded evidence object only. The prior R1 FAIL remains historically valid. Historical behaviour remains `UNKNOWN`. TCD-018 is not admitted by this review. No production source, canonical TCD register, B4 state or production migration is modified or authorized.