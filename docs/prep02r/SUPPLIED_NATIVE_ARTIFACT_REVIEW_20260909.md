# ANIMO-PREP02R supplied native artifact review, 2026-09-09

Status: `PARTIAL_RECOVERY_BUILD_CONTRACT_STRONGLY_IMPROVED_MODERN_NATIVE_REBUILD_IDENTIFIED_HISTORICAL_REFERENCE_STILL_BLOCKED`.

## Scope

Three additional files were supplied to PREP02R after the earlier fail-closed historical-reference search:

- `animo41.exe`;
- `animo41.sln`;
- `animo41.vfproj`.

The received bytes were hashed before any execution attempt. The binary itself is not copied into the repository. Only hashes and provenance observations are persisted.

## Receipt identities

| artifact | SHA-256 | size |
| --- | --- | ---: |
| `animo41.exe` | `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d` | 6,778,368 B |
| `animo41.sln` | `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2` | 1,233 B |
| `animo41.vfproj` | `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a` | 9,829 B |

Receipt is not reference admission.

## Intel project contract

The solution identifies Visual Studio 2010, solution format 11.00. The project identifies `Intel Fortran`, version 11.0, and `Console Application - Converted from CVF`.

Four project configurations exist: Debug and Release for Win32 and x64.

The following compiler properties are explicit across all four configurations:

- free-form source;
- `FPS4IOFormat=true`;
- `FPS4LDIOSpacing=true`;
- `FPS4General=true`;
- `RealKIND=realKIND8`;
- `LocalVariableStorage=localStorageSave`;
- `FloatingPointExceptionHandling=fpe0`;
- `FloatingPointModel=source`;
- `CallingConvention=callConventionCVF`;
- traceback enabled;
- bounds checking enabled.

`Debug|x64` additionally sets `LocalSavedScalarsZero=true`, disables optimization, enables debug information, and selects the multithreaded debug runtime. `Release|Win32` uniquely sets `FPS4Logicals=true`.

This is important because PREP02 had inferred some runtime semantics from GNU sensitivity tests. The supplied project now directly corroborates the two most behaviourally material hypotheses:

1. default REAL is configured as 8-byte;
2. local variables are configured with SAVE/static lifetime.

The project also exposes several Intel/CVF compatibility semantics that the GNU diagnostic contract cannot be assumed to reproduce exactly.

The project contains 58 Fortran source units. Every one is present in frozen B0. Frozen B0 contains exactly two additional alternate Fortran units not selected by the Intel project:

- `input1_1.for`;
- `Outselorg.for`.

This independently matches PREP01's 58-unit GNU source selection.

The exact treatment of `DOUBLE PRECISION` is not inferred from `RealKIND=realKIND8` alone; that remains a toolchain-semantics question.

## Executable classification

The received executable is a PE32+ x86-64 Windows console program with SHA-256 shown above.

Static inspection gives:

- PE timestamp `2026-05-27T13:41:28Z`;
- linker version `14.35`;
- image version `4.0`;
- CodeView/RSDS PDB path `D:\USR\5200048928_SWAP_ANIMO\ANIMO\x64\Debug\animo41.pdb`;
- embedded source root `D:\USR\5200048928_SWAP_ANIMO\ANIMO\src_develop_for_20260519\`;
- embedded Intel Fortran RTL message catalog `V20.0-001 Jan 10 2019`;
- no PE security-directory entry;
- imported DLLs observed: `imagehlp.dll` and `KERNEL32.dll`.

The binary also contains the lineage string:

`file:///V:/svn_Animo/tags/animo4.1.5`

and ANIMO 4.1 runtime strings including the normal successful-completion message.

The embedded source/debug paths contain all 58 Fortran source names selected by the supplied `.vfproj`, plus `Version.inc`. Neither `input1_1.for` nor `Outselorg.for` is observed in those embedded source paths.

This is strong source-selection consistency, but it is not byte-level source provenance.

### Why this is not the missing historical executable

The executable cannot be classified as a historical revision-53 release artifact:

- its PE timestamp is in 2026;
- its source directory explicitly names `src_develop_for_20260519`;
- its PDB path identifies an x64 Debug build;
- its embedded runtime library catalog postdates the 2011-era compiler string preserved in frozen `Version.inc`;
- its linker version is a modern toolchain signature.

The correct classification is therefore:

`MODERN_NATIVE_REBUILD_NOT_HISTORICAL_EXECUTABLE`.

This does not make the binary unimportant. It is a useful native Intel-family runtime candidate for cross-runtime comparison and it substantially strengthens the recovered build contract. It simply cannot replace independent historical behavioural truth.

## Relation to frozen B0

The new evidence establishes all of the following:

- same ANIMO 4.1.5 tag-family string is embedded;
- same 58-unit source selection is observed;
- all project-selected units exist in frozen B0;
- the two B0 alternates are excluded by the project and are absent from the binary's embedded source paths.

It does **not** establish that the 2026 build used byte-identical source files to the frozen B0 archive. There is no source-content manifest or PDB/source archive linking the executable to exact B0 file hashes.

## Native execution

No executable run is claimed in this workunit. The current controlled execution environment is Linux and has no Windows/Wine runtime. PREP02R does not silently translate or emulate the supplied binary and testcase to create a pseudo-native result.

A future Windows-native capture should use the already prepared Ruurlo contract, record the executable hash above before launch, avoid scientific input transformations, retain raw output bytes, and compare the complete output tree before any observer instrumentation.

## Admission consequence

The previous status `BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED` is now too coarse because useful native/project artifacts have been obtained. However the decisive historical-evidence gate remains closed.

Current disposition:

`PARTIAL_RECOVERY_BUILD_CONTRACT_STRONGLY_IMPROVED_MODERN_NATIVE_REBUILD_IDENTIFIED_HISTORICAL_REFERENCE_STILL_BLOCKED`.

Specifically:

- `project_build_metadata_obtained = true`;
- `native_candidate_executable_obtained = true`;
- `historical_reference_artifact_obtained = false`;
- `native_reference_run_completed = false`;
- `reference_qualified = false`;
- `equivalent_reference_build_qualified = false`;
- `production_migration_admitted = false`.

The WUR archival request remains useful, but its purpose narrows: historical executable/output provenance is still missing; compiler/project-option recovery is no longer the primary unknown.
