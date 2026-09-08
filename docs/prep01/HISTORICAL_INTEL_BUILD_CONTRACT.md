# Historical Intel build contract reconstruction

Status: `CONCRETE_HYPOTHESIS_NOT_HISTORICALLY_PROVEN`.

This record separates three evidence classes:

1. **source-bound facts** from the supplied ANIMO 4.1.5 revision-53 source archive;
2. **runtime-bound facts** from the supplied testbank and controlled GNU diagnostic execution;
3. **vendor-semantic cross-checks** from Intel Fortran documentation.

Vendor documentation is used only to identify plausible Intel compiler settings that reproduce already observed source/runtime semantics. It is **not** proof that those options were present in the historical revision-53 project.

## 1. Frozen source identity

Supplied archive:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

`Version.inc` identifies:

- tag: `file:///V:/svn_Animo/tags/animo4.1.5`;
- revision: `53`;
- build string: `Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`.

The archive contains 65 files: 58 `.for`, 5 `.inc` and 2 `.f90`. No `.vfproj`, `.vcxproj`, `.sln`, makefile, batch/cmd file, property sheet or other build-project artifact is present.

A source-wide text scan finds no occurrence of `/4R8`, `/Qautodouble`, `/fpscomp`, `/Qsave`, `/Qauto`, `real-size`, `autodouble`, `fpscomp`, `qsave` or `qauto`.

Therefore the exact historical command line and project settings are not recoverable from the supplied archive alone.

## 2. Default REAL kind

### Source/runtime evidence

The source uses default `REAL` extensively while also containing explicit `REAL(8)` declarations. A four-byte-default-REAL GNU build creates incompatible implicit function-result behaviour around `Dble_trunc` and produces unstable numerical execution. An eight-byte-default-REAL diagnostic build is internally coherent for eight supplied cases and removes the earlier `Dble_trunc`/OXYDEM failure pattern.

This establishes that **default REAL kind is material to the legacy build contract**.

It does not by itself prove which Intel project option was used historically.

### Intel semantic cross-check

Intel Fortran documentation states that Windows `/4R8` and `/Qautodouble` make default REAL/COMPLEX declarations, constants and functions eight bytes long.

That semantic effect matches the build property required by the successful source-consistent diagnostic route.

### PREP01 classification

`BUILD_CONTRACT_HYPOTHESIS_STRONGLY_SUPPORTED`

Candidate historical setting:

`/4R8` or equivalent `/Qautodouble`

Confidence is **not** raised to `HISTORICALLY_PROVEN` until a project file, build log, historical executable comparison or other direct release evidence confirms it.

## 3. PowerStation-compatible unformatted I/O

### Testbank/runtime evidence

All nine supplied hydrology files use the Microsoft/Intel Fortran PowerStation-compatible sequential-unformatted framing recovered in PREP01:

- file header `0x4b`;
- physical record blocks with matching leading/trailing one-byte markers;
- `0x81` continuation blocks for 128-byte chunks;
- file trailer `0x82`.

The payload-preserving PREP01 adapter can parse all nine files and convert record framing for GNU Fortran without modifying logical payload bytes.

### Intel semantic cross-check

Intel documents `/fpscomp:ioformat` as selecting Fortran PowerStation semantic conventions and record formats for list-directed formatted and unformatted I/O.

This is a direct semantic match to the recovered testbank file framing.

### PREP01 classification

`BUILD_CONTRACT_HYPOTHESIS_VERY_STRONGLY_SUPPORTED`

Candidate historical setting:

`/fpscomp:ioformat`

The record-format match is strong evidence for the required Intel runtime semantics, but the exact historical compiler invocation is still not present in the supplied evidence.

## 4. Local variable storage and `Outbal_write`

`Outbal_write` creates local CHARACTER format buffers such as `LineWA`, `LineOM`, `LineNH`, `LineNI`, `LineNO`, `LinePO` and `LinePP` in the `Itask=1` path and later reuses them in the `Itask=3` path without explicit `SAVE`.

An early GNU diagnostic build with automatic local storage lost this state. A GNU `-fno-automatic` build retained it and completed.

That GNU workaround is broader than the historical Intel behaviour that needs to be explained.

Intel documents default `/Qauto-scalar` behaviour as placing only non-SAVEd scalar INTEGER, REAL, COMPLEX and LOGICAL variables on the stack. The `Outbal_write` problem variables are CHARACTER scalars, so their persistence can be compatible with Intel default storage semantics without requiring global `/Qsave`.

### PREP01 classification

`BUILD_CONTRACT_DEPENDENCY_WITH_DEFAULT_INTEL_EXPLANATION`

Current baseline hypothesis:

- **do not assume `/Qsave`** in the historical reference build;
- use Intel default local-storage behaviour as the first reference candidate;
- treat `/Qsave` as a sensitivity variant only if native reproduction requires it.

This distinction matters because GNU `-fno-automatic` should not be read as evidence that the historical Intel project used `/Qsave`.

## 5. Current candidate native build contract

The smallest evidence-consistent candidate is:

```text
Compiler:
  Intel Visual Fortran Composer XE 12.1.0.233, Intel 64

Strongly supported candidate semantics:
  default REAL = 8
    likely /4R8 or equivalent /Qautodouble

Very strongly supported I/O compatibility:
  /fpscomp:ioformat

Local storage:
  start from Intel default storage semantics
  do not add /Qsave to the baseline without evidence
```

Still unknown:

- optimization level;
- floating-point model;
- integer-size options;
- alignment and calling-convention options;
- exception/underflow handling;
- preprocessing and include-search settings;
- debug/runtime-check settings;
- exact source-unit selection provenance;
- linker options and runtime libraries;
- whether other `/fpscomp` suboptions were enabled;
- whether the build was made from the exact supplied archive or a neighbouring revision with the same `Version.inc` identity.

## 6. Qualification experiment matrix

When a compatible Intel 12.1 environment or historically equivalent executable becomes available, run the following serially.

### I12-A: minimal source-declared compiler defaults

Intel 12.1 Intel64 with source-selected units and no hypothesized compatibility options beyond what is strictly required to compile.

Purpose: establish the raw default behaviour and fail points.

### I12-B: eight-byte default REAL

I12-A plus `/4R8` or the directly equivalent project setting.

Purpose: test whether the source's implicit-kind dependencies align with the historical source behaviour inferred from successful diagnostic execution.

### I12-C: PowerStation I/O reference candidate

I12-B plus `/fpscomp:ioformat`.

Purpose: read the frozen hydrology files **directly**, without PREP01 record conversion.

This is the current leading reference-build candidate.

### I12-D: storage sensitivity only

Only if I12-C exposes state-retention differences, compare Intel default storage with `/Qsave`.

`/Qsave` must not be silently folded into the reference baseline merely because GNU required `-fno-automatic`.

## 7. Admission rule

A successful Intel build is not automatically a qualified reference.

Reference admission requires at minimum:

1. exact source/archive provenance;
2. exact compiler version and complete command/project settings;
3. direct reading of frozen legacy hydrology bytes or a separately qualified equivalent exchange path;
4. deterministic repeated execution;
5. capture of unrounded generated outputs;
6. reconciliation of runtime warnings and mass-balance diagnostics;
7. independent comparison against a trusted historical executable or other accepted release evidence, unless an explicit governance decision qualifies the reconstructed Intel build as the canonical frozen legacy reference.

Until then, PREP01 status remains fail-closed and all GNU outputs remain `DIAGNOSTIC_NOT_REFERENCE`.

## 8. Vendor references used only as semantic cross-checks

Intel Fortran Classic documentation consulted during PREP01:

- `real-size`: Windows `/4R8` and `/Qautodouble` produce eight-byte default REAL semantics;
- `fpscomp`: `/fpscomp:ioformat` selects Fortran PowerStation I/O semantics and record formats;
- `auto-scalar, Qauto-scalar`: default stack allocation is limited to scalar INTEGER, REAL, COMPLEX and LOGICAL variables without SAVE;
- `auto` / `save`: `/Qauto` and `/Qsave` are broader storage-policy switches.

These references describe Intel compiler semantics but do not establish the actual revision-53 project settings. Historical invocation remains a qualification target.
