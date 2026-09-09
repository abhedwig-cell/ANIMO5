# ANIMO-PREP02 GNU runtime-contract probe

Status: `DIAGNOSTIC_GNU_RUNTIME_CONTRACT_NARROWED_REFERENCE_NOT_QUALIFIED`.

## Purpose

PREP02 needs to distinguish scientific behaviour from compiler/runtime compatibility. The frozen revision-53 source and supplied Windows-era testcase material do not execute byte-for-byte on a case-sensitive GNU/Linux runtime without explicit compatibility handling.

This probe makes that compatibility surface explicit and tests several build-semantics hypotheses. It does not qualify GNU as the ANIMO behavioural reference.

## Frozen evidence

Source archive:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank:

`ANIMO_testbank.zip`

SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Diagnostic GNU executable:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Compiler observed in the controlled probe:

`GNU Fortran 14.2.0`

The source archive and testbank ZIP remained unchanged.

## Runtime compatibility findings

### 1. Direct-file paths carry Windows filesystem assumptions

The supplied `animo.ini` files use backslash separators. File-name spelling also assumes case-insensitive resolution, for example a direct-file request can use `Input/general.inp` while the frozen testcase member is `Input/GENERAL.INP`.

This is not a scientific input difference. It is a host-filesystem contract inherited from the historical Windows execution environment.

### 2. `PrintBalLabel` exposes an Intel/GNU list-directed input difference

Revision-53 `input1.for` reads each `PrintBalLabel` line into a character buffer and then performs a list-directed internal `READ` on the substring after `=`.

The supplied inputs use forms such as:

```text
PrintBalLabel=      'RP'! 2-character identifier
```

GNU Fortran 14.2 rejects the quoted character value followed immediately by `!` in that internal list-directed record with:

```text
Fortran runtime error: Invalid string input in item 1
```

The execution-copy adapter therefore changes only the lexical representation to:

```text
PrintBalLabel=      RP! 2-character identifier
```

The two-character payload is unchanged. No balance-profile identifier changes.

This adaptation is now explicit in `tools/prepare_gnu_case.py`; it must no longer be an undocumented part of diagnostic execution.

### 3. PowerStation record framing remains a runtime adaptation

The hydrology input is converted from the observed Microsoft/Intel Fortran PowerStation-compatible physical-block framing to GNU sequential-unformatted framing. Logical-record payload bytes remain unchanged.

The new testcase adapter records source/target hashes, logical-record count, physical-block count and a payload hash for each prepared case.

## Explicit testcase adapter

`tools/prepare_gnu_case.py` now performs, on an extracted execution copy only:

1. frozen testbank SHA verification;
2. path-separator adaptation in the direct file;
3. exact-path aliases for case-insensitive Windows filename resolution;
4. `PrintBalLabel` lexical adaptation with unchanged character payload;
5. PowerStation-to-GNU hydrology record framing conversion;
6. machine-readable recording of every adaptation.

Unit tests cover:

- case-insensitive path resolution;
- `PrintBalLabel` payload preservation;
- multi-block PowerStation logical-record reconstruction.

Local controlled result:

```text
3 tests passed
```

## Re-execution of the supplied cases

Using the pinned diagnostic executable and the explicit testcase adapter, the following cases again reached the legacy successful-completion path:

1. `CranGrass`;
2. `CranMais`;
3. `GrassPeat`;
4. `LWKM_gras_1040.2021.2045`;
5. `Puitmijn_Cranendonck_60`;
6. `RuurloGrass`;
7. `STONE_akk_0006.2001.2015`;
8. `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

`GHGMais` still stops independently at the already known source/testcase contract mismatch:

```text
STOP 1995
Error: label ">outGHG:" not found in file "Input/general.inp"
```

The explicit compatibility adapter therefore does not remove or hide the GHGMais provenance blocker.

## Ruurlo build-semantics sensitivity matrix

The first PREP02 native-equivalence case is intended to be `RuurloGrass`. Controlled GNU variants were therefore used to test whether the current build semantics are arbitrary conveniences or behaviourally material.

### Contract G0: current diagnostic contract

Flags relevant to this probe:

```text
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Result:

- successful completion;
- no `NaN` in `message.out`;
- no OXYDEM convergence warning in `message.out`;
- `message.out` has 48 lines in the controlled run.

### Contract G1: automatic local storage

Removed:

```text
-fno-automatic
```

Result:

- simulation advances through the final simulated day;
- final balance writing fails in `Outbal_write.for` at the dynamic format `LineWA`;
- GNU reports `Missing initial left parenthesis in format`;
- no successful completion is obtained.

Interpretation:

Static retention of legacy local state is behaviourally required for this source as written. This supports the existing classification of local-storage duration as part of the historical build contract.

### Contract G2: four-byte default REAL

Removed the default-real promotion while retaining static locals.

Result:

```text
STOP 1111
```

This reproduces the known default-real build-contract sensitivity. Four-byte default `REAL` is not a viable equivalent-reference candidate for revision 53 as currently reconstructed.

### Contract G3: eight-byte default REAL but promoted DOUBLE PRECISION

Used:

```text
-fdefault-real-8
-fno-automatic
```

without:

```text
-fdefault-double-8
```

Under GNU this promotes `DOUBLE PRECISION` beyond eight bytes.

Result:

- the run reaches the nominal successful-completion path;
- `message.out` grows to 15,624 lines;
- 1,947 OXYDEM non-convergence warnings are emitted;
- `NaN` values occur throughout those diagnostics;
- after normalization of volatile run timestamps/CPU metadata, 59 of 74 compared non-input files differ from the current diagnostic contract in the controlled comparison.

Interpretation:

`-fdefault-double-8` is not a cosmetic flag. The eight-byte default-REAL hypothesis is insufficient by itself; the treatment of `DOUBLE PRECISION` materially affects model behaviour.

## Consequence for historical reconstruction

The acceptable native/reference candidate cannot be defined merely as "an Intel build that runs". PREP02 must establish at least:

- default `REAL` semantics;
- `DOUBLE PRECISION` semantics;
- local-storage duration;
- PowerStation/unformatted-I/O semantics;
- Windows filename/path semantics;
- source-unit selection.

The source metadata still names:

`Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`

but no historical project file or native executable is present in the supplied source or testbank archives. The testbank runner files reference `animo41.exe`, but the executable itself is absent.

## Gate

The probe narrows the equivalent-reference search space but cannot provide independent behavioural truth.

Current gate:

`BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`

A modern GNU run remains:

`DIAGNOSTIC_NOT_REFERENCE`.

ANIMO5 production process migration remains `NOT_ADMITTED`.
