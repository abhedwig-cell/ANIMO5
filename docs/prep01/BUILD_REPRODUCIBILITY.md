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

## Reproducible diagnostic build tool

`tools/build_gnu_diagnostic.py` reconstructs the diagnostic build directly from the original supplied source ZIP. The tool:

1. verifies the exact source archive SHA-256 before extracting;
2. modifies only a temporary execution copy;
3. creates case aliases for include names required on a case-sensitive filesystem;
4. supplies minimal `dfport/secnds` and `KINT/KIDNNT` compatibility shims;
5. creates a GNU-only syntax-equivalent copy of the rejected `Outsel.for` nested implied-do output list and requires exactly 14 known substitutions;
6. requires exactly 58 selected legacy compilation units and explicitly excludes the alternate `input1_1.for` and `Outselorg.for` units;
7. builds from relative paths and disables the linker build ID to remove path/build-instance volatility;
8. records compiler, flags, adaptation count and executable SHA-256 as machine-readable metadata.

GNU Fortran 14.2.0 compile flags:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Link flag:

```text
-Wl,--build-id=none
```

Two completely fresh invocations in separate output directories produced byte-identical executables:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This establishes a deterministic GNU diagnostic build recipe for the supplied archive in the investigated environment. It does **not** establish equivalence to the historical Intel executable.

## Behavioural repeatability of the deterministic build

The deterministic build was run through the same execution-copy harness used for the prior independent GNU build.

Results:

- eight compatible cases again reached `Successful completion of simulation`;
- all eight again contained zero `NaN` mentions;
- `GHGMais` again stopped at the known textual source/testcase contract mismatch;
- after normalizing only legacy run-start/run-end timestamps and elapsed CPU seconds, the complete copied execution trees for all eight successful cases were byte-identical to the previous independently rebuilt execution trees.

Therefore the changed executable binary identity caused by the now-controlled link recipe does not change the observed diagnostic model behaviour for the eight admitted diagnostic cases.

The existing normalized scientific/output bundle hashes in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json` remain unchanged.

## Hydrology exchange

The binary testbank hydrology uses Microsoft/Intel Fortran PowerStation-compatible sequential-unformatted record framing. A fail-closed adapter converts framing while preserving every logical-record payload byte. Both single-block and continued multiblock records are supported and all nine hydrology files parse structurally.

Binary hydrology record framing is therefore no longer a build blocker.

## GHGMais

`GHGMais` passes binary hydrology conversion but is not contract-compatible with the supplied revision-53 source. The mismatch is broader than the previously observed missing `>outGHG:` label:

- revision-53 expects `>outGHG:` in `GENERAL.INP`;
- the testcase instead stores equivalent-looking GHG constants under `>defGHG:` in `MATERIAL.INP`;
- revision-53 requires `>orgcom:` in `MATERIAL.INP`, which the testcase lacks;
- revision-53 reads a narrower positional `>deffra:` record, while the testcase includes additional `RQ` and `cbfr` columns.

A controlled input-only probe confirmed that inserting only `>outGHG:` merely advances to the next contract mismatch. No translated GHGMais testcase is admitted. See `docs/prep01/GHG_TESTCASE_PROVENANCE.md`.

## Current result

- native historical Intel/Windows build: `NOT_REPRODUCED`;
- deterministic GNU diagnostic build recipe: `PASS`;
- byte-identical clean diagnostic rebuilds: `2/2` in the recorded reproducibility probe;
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
