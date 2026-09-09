# Legacy execution recovery evidence

Status: `DIAGNOSTIC_EXECUTION_RECOVERED_REFERENCE_NOT_QUALIFIED`.

This record describes execution archaeology against the supplied ANIMO 4.1.5 revision-53 source and frozen testbank. No frozen scientific source file is modified by this work.

## 1. PowerStation hydrology framing recovered

The supplied binary hydrology files are not directly readable by GNU Fortran's default sequential-unformatted runtime because their record framing follows a Microsoft/Intel Fortran PowerStation-compatible convention.

The observed framing consists of:

- file header `0x4b`;
- one or more physical blocks per logical record;
- physical-block marker `0..128` for a terminating block of that payload length;
- marker `0x81` for a 128-byte continuation block;
- identical leading/trailing marker for every physical block;
- file trailer `0x82`.

`tools/convert_legacy_unformatted.py` joins physical blocks into logical records and rewrites framing to GNU's default four-byte record markers. Logical payload bytes are copied unchanged. The parser fails closed on malformed marker pairs, truncation, continuation at EOF or bytes after the file trailer.

### RuurloGrass

- source hydrology SHA-256: `36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13`;
- source size: 888148 bytes;
- logical records: 11691;
- physical blocks: 11691;
- logical payload lengths: 8, 12, 20, 24, 40, 80 and 84 bytes;
- first logical payload decodes as `(1980, 1985, 1.0, 120.0, 1.0)`, matching the old-SWAP header contract in `input1.for`;
- GNU-framed target SHA-256: `b5fc15f51074ba9e4131e0616b4348e31d523d0a8e874be6055bcd614de4de5c`.

### GHGMais

The earlier assumption that `result.bun` used an unresolved extended record format was wrong. Marker `0x80` is a valid terminating 128-byte block and marker `0x81` is the continuation form.

For `GHGMais/Input/result.bun`:

- source SHA-256: `cd4202745ee8a9ccd890e6aa6d3f551ff3bb80041efd178aedb3f5f4bbe002e2`;
- source size: 4178832 bytes;
- logical records: 40189;
- physical blocks: 43841;
- logical payload lengths: 4, 8, 12, 16, 20, 72, 80, 128 and 132 bytes;
- GNU-framed target SHA-256: `c6cc86dfa7855d02e0ff13b909317460ee478008c6f284bd1cb902d2215e7537`.

All nine testbank hydrology files are now structurally parseable by the qualification adapter. Binary record framing is no longer a PREP01 blocker.

## 2. Default-real and local-storage semantics

An earlier GNU probe used four-byte default `REAL`. In that build `Function.for` returned `REAL(8)` from `Dble_trunc` while callers declared default `REAL`, resulting in a return-kind mismatch. The corrupted hydrology end time caused `STOP 1111`, and later diagnostic adaptations exposed `OXYDEM` NaNs.

A fresh diagnostic build using:

```text
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

in addition to the legacy/free-form compatibility flags gives a materially different and internally more coherent result:

- caller-side default `REAL` is eight bytes, consistent with the explicit `REAL(8)` `Dble_trunc` result;
- local data in routines such as `Outbal_write` have static storage, preserving values across the split `Itask` calls;
- eight testcases complete without `NaN` diagnostics.

This does **not** establish that these were the exact historical Intel project options. It does establish that the earlier GNU failures cannot be promoted to legacy model defects without first resolving compiler semantics.

Current classifications:

- default-real dependence around `Dble_trunc` and related implicit interfaces: `BUILD_CONTRACT_DEPENDENCY`, not a demonstrated legacy scientific defect;
- `Outbal_write` local retention: `BUILD_CONTRACT_DEPENDENCY`, because persistence depends on compiler storage semantics not expressed in the routine;
- earlier `OXYDEM` NaNs: `DIAGNOSTIC_BUILD_ARTIFACT` for PREP01 purposes, not a demonstrated legacy aeration defect.

## 3. Deterministic diagnostic build recipe

`tools/build_gnu_diagnostic.py` now reconstructs the diagnostic executable directly from the exact supplied source ZIP and fails closed on source hash, expected source-unit count and expected GNU-only syntax adaptation count.

The controlled recipe uses GNU Fortran 14.2.0 with:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

and linker option:

```text
-Wl,--build-id=none
```

Execution-only compatibility material consists of include-case aliases, minimal `dfport/secnds` and `KINT/KIDNNT` shims, and a GNU-equivalent rewrite of one rejected `Outsel.for` output-list construct. The original archive remains unchanged.

Two clean builds in separate directories produced byte-identical executables:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This improves reproducibility of the diagnostic toolchain. It does not convert the GNU executable into a qualified historical reference.

## 4. Eight deterministic diagnostic cases

The following cases reach the legacy successful-completion path:

1. `CranGrass`;
2. `CranMais`;
3. `GrassPeat`;
4. `LWKM_gras_1040.2021.2045`;
5. `Puitmijn_Cranendonck_60`;
6. `RuurloGrass`;
7. `STONE_akk_0006.2001.2015`;
8. `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

Repeated executions, an independently rebuilt earlier executable and the new deterministic build recipe were compared. After normalizing only volatile legacy run-start/run-end timestamps and elapsed CPU seconds, the complete execution trees for all eight successful cases are byte-identical. Exact generated-output counts and normalized scientific/output bundle hashes remain recorded in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

This establishes deterministic diagnostic behaviour for the investigated GNU build contract. It does not establish equivalence to the historical Intel executable and the bundle hashes are not admitted as `FROZEN_LEGACY` or `QUALIFIED_GOLDEN_CASE` expected values.

## 5. GHGMais is a structural source/testcase contract blocker

`GHGMais` passes hydrology conversion but stops in text-input parsing with `STOP 1995` because the supplied `GENERAL.INP` lacks `>outGHG:` required by revision-53 `input1.for`.

Further source-bound inspection shows that this is not a single missing-label packaging error:

- the testcase stores `CH4_CO2e`, `N2O_CO2e`, `NuCO2fr` and `CO2frno` under `>defGHG:` in `MATERIAL.INP`;
- revision-53 instead reads equivalent GHG controls from `>outGHG:` in `GENERAL.INP`;
- revision-53 requires `>orgcom:` and `Cfracom` in `MATERIAL.INP`, which supplied GHGMais lacks;
- revision-53 `>deffra:` consumes `frno recfav hufros Ratio_rd_st asfa nifr [pofr]`;
- supplied GHGMais `>deffra:` contains additional positional `RQ` and `cbfr` fields before `nifr` and `pofr`.

A controlled input-only diagnostic probe reused the already-present `>defGHG:` values in a temporary `>outGHG:` block only to test whether the mismatch ended there. It advanced to the missing `>orgcom:` contract and was abandoned. No translated testcase is admitted.

Therefore GHGMais belongs to a different or incomplete source/input-contract lineage. Blindly inserting labels or dropping positional columns could alter scientific semantics. See `docs/prep01/GHG_TESTCASE_PROVENANCE.md`.

## 6. Current interpretation

Execution recovery has moved beyond the original build and binary-I/O blockers. We now have:

- source-bound build-semantics hypotheses;
- a payload-preserving PowerStation-to-GNU record adapter;
- a deterministic source-hash-bound diagnostic build recipe;
- eight reproducibly completing and NaN-free diagnostic testcases;
- one explicit structural source/testcase provenance blocker.

Still unresolved:

- exact historical Intel compiler flags/project configuration;
- equivalence of the GNU diagnostic results to a trusted native ANIMO 4.1.5 revision-53 executable;
- controlled immutable retention of the raw source and documentation bytes;
- provenance of the `GHGMais` testcase and the matching ANIMO revision;
- trusted unrounded numerical outputs from a qualified legacy reference;
- complete 4.1.5 theory documentation and balance-term reconciliation.

## Gate

`DIAGNOSTIC_EXECUTION_RECOVERED_REFERENCE_NOT_QUALIFIED`

PREP01 must remain fail-closed. Deterministic diagnostic execution is evidence for archaeology and later qualification, not yet a behavioural oracle.
