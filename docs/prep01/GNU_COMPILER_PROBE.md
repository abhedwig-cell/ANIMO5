# GNU Fortran compatibility and execution probe

Evidence class: `DIAGNOSTIC_NOT_REFERENCE`.

This experiment investigates whether the supplied ANIMO 4.1.5 revision-53 source can be executed reproducibly with a modern compiler without changing the frozen scientific source. It is not evidence that GNU output equals the historical Intel executable.

## Environment and provenance

- GNU Fortran 14.2.0;
- supplied source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- embedded source identity: `animo4.1.5`, revision `53`;
- historical toolchain string in `Version.inc`: `Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`.

## Source form and platform dependencies

The `.for` suffix does not describe the actual syntax sufficiently. The source uses free-form continuation and declarations. The diagnostic build therefore uses `-ffree-form -ffree-line-length-none`.

Observed platform/toolchain dependencies include:

1. case-insensitive include-name assumptions;
2. Intel `dfport/secnds` timing functionality;
3. Intel-compatible `KINT`/`KIDNNT` behaviour;
4. a nested implied-do output-list construct in `Outsel.for` rejected by GNU Fortran 14.2;
5. implicit procedure interfaces and compiler-dependent default-kind/local-storage semantics.

These are compatibility observations, not automatically scientific defects.

## Diagnostic build semantics

A fresh source extraction was compiled with:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Fifty-eight Fortran compilation units were selected. `input1_1.for` and `Outselorg.for` were excluded as alternate units because the main-program signatures bind to `input1.for` and `Outsel.for` in this diagnostic lineage.

Execution-only compatibility material outside the frozen source consisted of:

- case aliases for include names on a case-sensitive filesystem;
- a minimal `dfport/secnds` shim;
- a minimal `KINT`/`KIDNNT` shim;
- a GNU-equivalent rewrite of the rejected nested implied-do output list in `Outsel.for`.

No frozen source file was edited. The independently rebuilt diagnostic executable has SHA-256:

`0d082a8f59f4c1fd8c083df33ef92b23a2947d1abf69727c12801e3ceea499bd`

Object inspection confirms that default local `REAL` data are eight bytes under this probe and that `-fno-automatic` gives static local storage for the legacy local format variables used across calls.

## Hydrology binary exchange

The supplied hydrology files use Microsoft/Intel Fortran PowerStation-compatible sequential-unformatted framing. The repository adapter `tools/convert_legacy_unformatted.py` converts only physical/logical record framing. Logical-record payload bytes are unchanged.

The parser now supports both:

- one-block logical records;
- multiblock logical records using PowerStation continuation blocks.

All nine testbank hydrology files can be structurally parsed. Binary hydrology framing is therefore no longer the PREP01 execution blocker.

## Diagnostic testcase execution

Eight of nine supplied cases reach legacy `Successful completion of simulation` under the diagnostic build:

- `CranGrass`;
- `CranMais`;
- `GrassPeat`;
- `LWKM_gras_1040.2021.2045`;
- `Puitmijn_Cranendonck_60`;
- `RuurloGrass`;
- `STONE_akk_0006.2001.2015`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

No `NaN` diagnostics occur in those eight runs. Some runs emit GNU IEEE underflow/denormal notes; these have not been promoted to scientific findings.

The eight successful cases were run again and also compared with an independently rebuilt diagnostic executable. After normalizing only volatile run timestamps and elapsed CPU seconds, generated outputs matched exactly in all eight cases. Exact diagnostic bundle hashes are persisted in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

`GHGMais` now passes the binary hydrology stage but stops during text input parsing. The supplied `general.inp` lacks the `>outGHG:` section required by the supplied 4.1.5 revision-53 `input1.for` when `IoptGHG >= 1` and uses a different set of GHG output keys. This is treated as a source/testcase contract-provenance mismatch, not repaired silently.

## Interpretation of earlier GNU failures

An earlier diagnostic build using four-byte default `REAL` produced a `Dble_trunc` return-kind mismatch and subsequent aeration `NaN` values. Those observations are not stable under the more source-consistent eight-byte default-real/static-storage build described above.

Accordingly:

- the `Dble_trunc` declaration pattern remains a dangerous implicit-interface/build-semantics dependency, but is not currently qualified as a legacy scientific defect;
- the earlier `OXYDEM` NaNs are classified as a diagnostic build-semantics artifact unless independent native reference evidence shows otherwise;
- local-state retention in `Outbal_write` remains an explicit compiler-semantics dependency because the historical Intel project flags are still unavailable.

## Gate

Current evidence supports:

- modern diagnostic build feasibility: `DEMONSTRATED`;
- PowerStation hydrology framing recovery: `DEMONSTRATED`;
- deterministic diagnostic execution for eight testcases: `DEMONSTRATED`;
- native historical build reproduction: `NOT_REPRODUCED`;
- behavioural equivalence with historical ANIMO 4.1.5 revision 53: `NOT_QUALIFIED`;
- RR/QG oracle admission: `NOT_ADMITTED`.

A reproducible diagnostic program is useful archaeology evidence, but it is not yet the frozen behavioural reference.
