# Legacy build and reproducibility assessment

Status: `DIAGNOSTIC_BUILD_REPRODUCIBLE_REFERENCE_BUILD_NOT_QUALIFIED`.

## Observed environment

- GNU Fortran 14.2.0 available;
- CMake 3.31.6 available;
- GNU Make 4.4.1 available;
- Intel `ifort`/`ifx` not observed;
- Wine not observed.

## Historical/source-declared toolchain

The supplied `Version.inc` identifies:

`Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`

No Visual Studio project, makefile, compiler command line, link script or historical executable was present in the supplied source archive. Exact historical flags and source selection remain unproven.

## Fortran and build-semantics findings

The source is mixed legacy/modern Fortran. The `.for` files contain free-form constructs and are compiled as free form in the GNU investigation. External textual includes, implicit interfaces and compiler-default data semantics are material parts of the legacy build contract.

Confirmed portability dependencies include:

- case-insensitive include-file naming;
- Intel `dfport/secnds` functionality;
- `KINT`/`KIDNNT` behaviour;
- one GNU-incompatible `Outsel.for` output-list construct;
- widespread implicit external procedure interfaces;
- sensitivity to default `REAL` kind;
- sensitivity to automatic versus static local storage.

The last two findings are especially important. A four-byte-default-REAL GNU build produces unstable interface behaviour and NaNs. A build with eight-byte default `REAL` plus static local storage is internally coherent for the investigated cases. This is evidence about a missing build contract, not proof of the exact historical Intel options.

## Reproducible diagnostic build

A fresh extraction of the supplied source was compiled from 58 selected units with GNU Fortran 14.2.0 and:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Excluded alternate units:

- `input1_1.for`;
- `Outselorg.for`.

Execution-only compatibility material outside the frozen source:

- include-name case aliases;
- minimal `dfport/secnds` shim;
- minimal `KINT/KIDNNT` shim;
- GNU-equivalent rewrite of one rejected nested implied-do output list in `Outsel.for`.

Frozen scientific source files were not modified.

Fresh diagnostic executable SHA-256:

`0d082a8f59f4c1fd8c083df33ef92b23a2947d1abf69727c12801e3ceea499bd`

This build is reproducible as a diagnostic artifact. It is not yet a qualified behavioural reference.

## Hydrology exchange

The binary testbank hydrology uses Microsoft/Intel Fortran PowerStation-compatible sequential-unformatted record framing. A fail-closed adapter now converts framing while preserving every logical-record payload byte. Both single-block and continued multiblock records are supported and all nine hydrology files parse structurally.

Binary hydrology record framing is therefore no longer a build blocker.

## Testcase execution

Eight cases reach legacy successful completion under the diagnostic build:

- `CranGrass`;
- `CranMais`;
- `GrassPeat`;
- `LWKM_gras_1040.2021.2045`;
- `Puitmijn_Cranendonck_60`;
- `RuurloGrass`;
- `STONE_akk_0006.2001.2015`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

The eight cases contain no `NaN` diagnostics in this build. Repeated runs and an independently rebuilt executable produce byte-identical generated output after normalization of only run timestamp and elapsed CPU seconds. Exact diagnostic bundle hashes are persisted in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

`GHGMais` passes binary hydrology conversion but stops in the text parser because its supplied `general.inp` lacks the `>outGHG:` section required by revision-53 `input1.for` and uses a different GHG output-key contract. This is a testcase/source provenance mismatch and is not repaired inside PREP01.

## Current result

- native historical Intel/Windows build: `NOT_REPRODUCED`;
- reproducible GNU diagnostic build: `PASS`;
- diagnostic successful-completion cases: `8/9`;
- diagnostic deterministic-output cases: `8/9`;
- source/testcase contract blockers: `1/9` (`GHGMais`);
- qualified reference-regression cases: `0/9`;
- qualified qualification-gate cases: `0/9`;
- trusted numerical oracle: `NOT_ESTABLISHED`.

## Remaining reference-build blockers

1. recover exact historical Intel compiler/project semantics or independently qualify an equivalent build contract;
2. establish controlled immutable B0 byte retention for source and documentation;
3. locate the matching source/testcase lineage for `GHGMais`;
4. capture unrounded outputs from a qualified legacy reference;
5. reconcile source 4.1.5 revision 53 with the available 4.0 documentation and missing later theory/change records.

No diagnostic output is promoted to `FROZEN_LEGACY`, `CORRECTED_LEGACY_REFERENCE`, RR or QG evidence at this stage.
