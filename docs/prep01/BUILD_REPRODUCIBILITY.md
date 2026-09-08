# Legacy build and reproducibility assessment

Status: `PARTIALLY_ASSESSED_BUILD_NOT_YET_REFERENCE_REPRODUCIBLE`.

## Observed environment

- GNU Fortran 14.2.0 available
- CMake 3.31.6 available
- GNU Make 4.4.1 available
- Intel `ifort`/`ifx` not observed
- Wine not observed

## Historical/source-declared toolchain

The supplied `Version.inc` identifies:

`Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`

No Visual Studio project, makefile, compiler command line, link script or historical binary was present in the supplied source archive. The exact historical build flags and selected source-file list are therefore not yet reproduced.

## Fortran/source-form assessment

The source is a mixed legacy/modern Fortran code base. Although 58 files use a `.for` suffix, they contain free-form continuation and constructs that require free-form interpretation in the GNU investigation. Two additional files use `.f90`. Include files are external textual includes rather than a module-based interface layer.

A modern-compiler probe establishes several portability dependencies:

- case-insensitive include-file naming assumptions;
- Intel `dfport/secnds` dependency;
- `KINT`/`KIDNNT` toolchain-specific behaviour;
- one `Outsel.for` WRITE-list construct rejected by GNU Fortran 14.2;
- large numbers of implicit external interfaces and legacy calling conventions.

See `docs/prep01/GNU_COMPILER_PROBE.md`.

## Probe result

In a disposable working copy only, with explicit compatibility shims and one targeted GNU syntax adaptation, a selected 58-unit build compiles and links under GNU Fortran 14.2. Those adaptations are not part of the frozen source and the resulting executable is not a behavioural oracle.

This demonstrates that a modern-portability route appears feasible, but it does **not** establish a reproducible legacy reference build.

## Testcase execution

The nine testcases identify themselves as `Animo41`. Source parsing accepts `Animo40` and `Animo41`, supporting format continuity but not proving numerical compatibility.

A GNU probe run required nonreference path/case normalization for Windows-style testcase paths. It then reached hydrological input reading and failed on the supplied binary `SWATRE.UNF` under GNU sequential-unformatted runtime semantics.

Current result:

- native historical Intel/Windows build: `NOT_REPRODUCED`
- GNU portability build: `PROBE_ONLY_WITH_SHIMS`
- testcases executed to successful completion: `0/9`
- qualified reference-regression cases: `0/9`
- trusted numerical oracle: `NOT_ESTABLISHED`

## Build blockers

1. historical Intel compiler/runtime or an evidenced byte-compatible alternative;
2. exact compile/link source selection and flags;
3. binary hydrology record-format/runtime compatibility;
4. controlled capture of unrounded legacy output;
5. a qualified relation between source 4.1.5 revision 53 and the supplied testbank.

No legacy source is modified in PREP01 to make this gate pass.
