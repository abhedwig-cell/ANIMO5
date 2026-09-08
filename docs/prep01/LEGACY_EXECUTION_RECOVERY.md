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

- `Dble_trunc`: `SUSPICIOUS_LEGACY_CONSTRUCT`, dangerous because correctness depends on default-real compiler policy and an implicit procedure interface;
- `Outbal_write` local retention: `SUSPICIOUS_LEGACY_CONSTRUCT`, because persistence depends on compiler storage semantics not expressed in the routine;
- earlier `OXYDEM` NaNs: `DIAGNOSTIC_BUILD_ARTIFACT` for PREP01 purposes, not a demonstrated legacy aeration defect.

## 3. Independently rebuilt diagnostic executable

A fresh source extraction, with no edits to frozen scientific source, was compiled from 58 selected units under GNU Fortran 14.2.0 using:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Execution-only compatibility material consisted of include-case aliases, minimal `dfport/secnds` and `KINT/KIDNNT` shims, and a GNU-equivalent rewrite of one rejected `Outsel.for` output-list construct.

Fresh diagnostic executable SHA-256:

`0d082a8f59f4c1fd8c083df33ef92b23a2947d1abf69727c12801e3ceea499bd`

This executable is a research artifact, not an admitted legacy reference.

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

Two repeated execution sets and an independently rebuilt executable were compared. After normalizing only volatile run timestamps and elapsed CPU seconds, the generated output bundles are byte-identical for all eight cases. Exact file counts and bundle hashes are recorded in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

This establishes deterministic diagnostic behaviour for the investigated GNU build. It does not establish equivalence to the historical Intel executable and the bundle hashes are not admitted as `FROZEN_LEGACY` or `QUALIFIED_GOLDEN_CASE` expected values.

## 5. GHGMais is a source/testcase contract blocker

`GHGMais` passes hydrology conversion but stops in text-input parsing with `STOP 1995` and the message:

`label ">outGHG:" not found in file "Input/general.inp"`

The supplied revision-53 `input1.for` requires `>outGHG:` when `IoptGHG >= 1` and then reads GHG-control variables from that section. The supplied `GHGMais/Input/general.inp` instead contains a different set of GHG output keys and no `>outGHG:` section.

This is evidence that the GHG testcase and supplied source do not share exactly the same input contract, or that required testcase material is missing. PREP01 does not insert the missing section or translate the newer keys because that would manufacture a reference case.

## 6. Current interpretation

Execution recovery has moved beyond the original build and binary-I/O blockers. We now have:

- source-bound build semantics hypotheses;
- a payload-preserving PowerStation-to-GNU record adapter;
- a fresh deterministic diagnostic build;
- eight reproducibly completing testcases;
- one explicit source/testcase provenance blocker.

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
