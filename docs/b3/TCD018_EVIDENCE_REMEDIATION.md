# TCD-018 independent-review evidence remediation

Work unit: `ANIMO-B3A03E`

Target: `TCD-018`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Branch: `work/animo-b3a03e-tcd018-independent-review-evidence-remediation`

## Purpose

The genuinely separate TCD-018 review at `review/animo-b3a03r-tcd018-independent-second-line@57cfdfb3a7fb982f6692b0b32f8c8aa044c57fd7` returned:

`FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW`

The review did not refute the source seam or the Class-A causal claim. It failed closed because two mandatory evidence surfaces were not persisted at sufficient audit granularity:

1. the complete 25-period LWKM reconciliation was asserted but no full 25-row period ledger existed;
2. the isolated eight-case run was summarized, but the reviewer had no raw comparison tree, per-output digest ledger, or equivalent independently auditable run artifact.

B3A03E remediates only those evidence gaps. It does not alter the TCD-018 scientific claim, does not re-review it, and does not perform admission.

## Frozen evidence identity

The remediation execution used the same frozen B0 archives:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The archives themselves were not modified.

GNU qualification execution used GNU Fortran 14.2.0 with the existing frozen diagnostic portability contract. The rebuilt baseline executable is:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

The fresh TCD-018 reporting-only qualification candidate is:

`c1e281d5ceaa45952dc7ee21041454fbfab5bee34aa8aee09d59604b75826bbe`

The exact candidate builder is persisted at `tools/build_tcd018_reporting_candidate.py`. It fails closed on source identity and patch-seam counts and is qualification tooling only, not a production patch.

## Remediation 1: complete 25-period ledger

`integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv` now persists all 25 annual total-profile balance periods from 1991 through 2015.

For every period it records:

- period bounds and reported duration;
- number of fresh detailed-hydrology probe records;
- legacy formatted Bawa deviation;
- raw summed `Hydro_detailed` `Badev`;
- raw summed `(Sict-Sic)*1000` interception-storage change;
- reconstructed legacy value;
- reconstruction-minus-formatted-legacy difference;
- fresh candidate Bawa deviation;
- fresh-candidate-minus-raw-hydrology difference.

The fresh probe produced 900 detailed-hydrology records, exactly 36 records for each of the 25 periods, ending at `Tito=9131`.

This is an audit ledger, not a tolerance definition. In particular, the historical approximately `0.0601 mm` LWKM residual remains causal evidence only. The formatting-scale differences between raw sums and formatted Bawa output are not converted into scientific acceptance epsilons.

## Remediation 2: per-output eight-case digest ledger

The fresh baseline and TCD-018 candidate were executed on the same eight natural cases used by the isolated Class-A diagnostic:

- `CranGrass`;
- `CranMais`;
- `GrassPeat`;
- `LWKM_gras_1040.2021.2045`;
- `Puitmijn_Cranendonck_60`;
- `RuurloGrass`;
- `STONE_akk_0006.2001.2015`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

`integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json` contains separate baseline/candidate completion records for all 16 executions.

The per-output digest ledger is persisted in four CSV partitions under:

`integration/animo-b3/tcd018_output_digest_ledger/`

Together they contain exactly 376 `(case,path)` records. Each row records whether the output is byte-identical, equal after only the declared volatile metadata normalization, or different on the predeclared whitelist. Digest fields permit the reviewer to audit every output identity rather than inherit a summary count.

The complete classification is:

- 270 `EQUAL_RAW`;
- 100 `EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY`;
- 6 `DIFFERENT_WHITELISTED`;
- 0 unexpected differences;
- 0 missing/extra outputs.

All six differences occur only for `LWKM_gras_1040.2021.2045` and are exactly:

- `ani_waGP.Bal`;
- `ani_waRP.Bal`;
- `ani_waTP.Bal`;
- `bawaGP.Out`;
- `bawaRP.Out`;
- `bawaTP.Out`.

No scientific numeric tolerance was used in the comparison.

## Scientific boundary

The qualification candidate changes only the reporting interface and reporting accumulator needed to observe the already-existing `Sic/Sict` storage change in the top-profile water ledger. It does not change hydrology state, hydrology fluxes, forcing, interception physics, state promotion, SWAP/SWATRE payload, or testcase scientific inputs.

The unrelated MASSQ01 CranGrass `TITO=724` residual of `-0.0030198960466805147 mm` remains `UNEXPLAINED_RESIDUAL` outside TCD-018. No global water-closure claim is made.

Qualified historical B2 evidence still does not exist. Historical revision-53 behaviour therefore remains `UNKNOWN`. GOV03 only opens the bounded historical-uncertainty route; it does not create historical truth.

## Relationship to the failed review

B3A03E does **not** change the previous review result. `FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW` remains the correct result for the evidence packet that was reviewed at that time.

B3A03E makes new evidence available for a new review attempt:

- former gate 8 now has a persisted 25-row period-by-period ledger;
- former gate 10 now has a persisted 376-row per-output digest ledger, 16 run-completion records and a pinned candidate builder;
- former dependent gates 11, 13, 14 and 15 therefore have evidence that a new independent reviewer can assess directly.

Those gates are **not self-certified as PASS by this authoring workunit**. A new genuinely separate ChatGPT review context must independently re-evaluate them and may still return FAIL.

## Hard boundaries

B3A03E does not:

- claim independent second-line PASS;
- admit TCD-018;
- claim historical fidelity;
- promote GNU B1 evidence to B2;
- modify production source;
- modify the canonical TCD register;
- admit B4;
- authorize production migration.

The next valid step after B3A03E qualification is a new independent second-line re-review of TCD-018 against the remediated packet.
