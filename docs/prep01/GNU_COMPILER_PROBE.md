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

The source-consistent diagnostic hypothesis uses:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Fifty-eight Fortran compilation units are selected. `input1_1.for` and `Outselorg.for` are excluded as alternate units because the main-program signatures bind to `input1.for` and `Outsel.for` in this diagnostic lineage.

Execution-only compatibility material outside the frozen source consists of:

- case aliases for include names on a case-sensitive filesystem;
- a minimal `dfport/secnds` shim;
- a minimal `KINT`/`KIDNNT` shim;
- a GNU-equivalent rewrite of the rejected nested implied-do output list in `Outsel.for`.

No frozen source file is edited.

## Deterministic build recipe

`tools/build_gnu_diagnostic.py` makes the above probe repeatable from the original source ZIP. It verifies the exact archive hash and fails closed if the expected source-unit count or known `Outsel` compatibility pattern changes.

The link step uses:

```text
-Wl,--build-id=none
```

and compiles from relative paths so that build-directory identity is not embedded as accidental volatility.

Two completely fresh builds in separate output directories produced byte-identical executables with SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This replaces the earlier manually assembled diagnostic executable as the preferred reproducibility artifact. It does not change the scientific qualification status.

## Hydrology binary exchange

The supplied hydrology files use Microsoft/Intel Fortran PowerStation-compatible sequential-unformatted framing. The repository adapter `tools/convert_legacy_unformatted.py` converts only physical/logical record framing. Logical-record payload bytes are unchanged.

The parser supports both:

- one-block logical records;
- multiblock logical records using PowerStation continuation blocks.

All nine testbank hydrology files can be structurally parsed. Binary hydrology framing is therefore no longer the PREP01 execution blocker.

## Diagnostic testcase execution

Eight of nine supplied cases reach legacy `Successful completion of simulation` under the deterministic diagnostic build:

- `CranGrass`;
- `CranMais`;
- `GrassPeat`;
- `LWKM_gras_1040.2021.2045`;
- `Puitmijn_Cranendonck_60`;
- `RuurloGrass`;
- `STONE_akk_0006.2001.2015`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

No `NaN` diagnostics occur in those eight runs. Some runs emit GNU IEEE underflow/denormal notes; these have not been promoted to scientific findings.

The deterministic-build executions were compared against the earlier independently rebuilt execution trees. After normalizing only run-start/run-end/file-creation timestamps and elapsed CPU seconds, all eight complete execution trees match byte-for-byte. Exact diagnostic scientific/output bundle hashes remain persisted in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

## GHGMais

`GHGMais` passes binary hydrology but is not input-contract compatible with the supplied revision-53 source.

The first visible mismatch is the absent `>outGHG:` section in `GENERAL.INP`. Deeper inspection establishes independent schema differences in `MATERIAL.INP`: supplied GHGMais uses `>defGHG:`, lacks source-required `>orgcom:`, and has extra positional `RQ` and `cbfr` fields in `>deffra:`.

A controlled input-only probe showed that inserting only the already-available GHG constants under the revision-53 label merely advances to the next mismatch. No translated testcase is admitted. See `docs/prep01/GHG_TESTCASE_PROVENANCE.md`.

## Interpretation of earlier GNU failures

An earlier diagnostic build using four-byte default `REAL` produced a `Dble_trunc` return-kind mismatch and subsequent aeration `NaN` values. Those observations are not stable under the more source-consistent eight-byte default-real/static-storage build described above.

Accordingly:

- default-real dependence around `Dble_trunc` is classified as `BUILD_CONTRACT_DEPENDENCY`, not as a demonstrated historical defect;
- the earlier `OXYDEM` NaNs are classified as `DIAGNOSTIC_BUILD_ARTIFACT` unless independent qualified evidence reproduces them;
- local-state retention in `Outbal_write` is classified as `BUILD_CONTRACT_DEPENDENCY` because the historical Intel project flags are still unavailable.

## Gate

Current evidence supports:

- deterministic modern diagnostic build: `DEMONSTRATED`;
- PowerStation hydrology framing recovery: `DEMONSTRATED`;
- deterministic diagnostic execution for eight testcases: `DEMONSTRATED`;
- native historical build reproduction: `NOT_REPRODUCED`;
- behavioural equivalence with historical ANIMO 4.1.5 revision 53: `NOT_QUALIFIED`;
- RR/QG oracle admission: `NOT_ADMITTED`.

A reproducible diagnostic program is useful archaeology evidence, but it is not yet the frozen behavioural reference.
