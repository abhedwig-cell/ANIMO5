# ANIMO-PREP02R-I5 — Native Intel Project/Executable Artifact Intake & Lineage Classification

## Decision scope

This workunit receives and classifies three user-supplied artifacts without executing the binary and without admitting a historical reference:

- `animo41.sln`;
- `animo41.vfproj`;
- `animo41.exe`.

The governing rule remains `REFERENCE_ARTIFACT_RECEIPT_PROTOCOL.md`: received bytes are evidence, not reference admission.

## Receipt identity

The bytes were hashed before any executable run.

| artifact | size | SHA-256 |
| --- | ---: | --- |
| `animo41.sln` | 1,233 B | `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2` |
| `animo41.vfproj` | 9,829 B | `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a` |
| `animo41.exe` | 6,778,368 B | `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d` |

The two-file project metadata content-set hash is `3dc760141d9047d86e07f9490c5e591ac1d6298b3c47882177d8ed9dec53e2b6`.

The original sender/archive provenance is not independently established. The public repository therefore stores receipt hashes and derived observations, not the received executable bytes.

## Solution and project evidence

`animo41.sln` is a Visual Studio solution format 11.00 and labels itself `Visual Studio 2010`. It points to one project named `animo41` using `animo41.vfproj`, with Win32 and x64 Debug/Release configurations.

`animo41.vfproj` identifies its creator as `Intel Fortran`, keyword `Console Application - Converted from CVF`, project version `11.0`.

The important compiler configuration is explicit, not inferred. All four configurations set:

- `RealKIND="realKIND8"`;
- `LocalVariableStorage="localStorageSave"`;
- `FloatingPointModel="source"`;
- `CallingConvention="callConventionCVF"`;
- `FPS4IOFormat="true"`;
- `FPS4LDIOSpacing="true"`;
- `FloatingPointExceptionHandling="fpe0"`;
- `BoundsCheck="true"`.

`Release|Win32` additionally sets `FPS4Logicals="true"`. `Debug|x64` additionally sets `LocalSavedScalarsZero="true"` and the multithreaded debug runtime.

This materially changes the PREP02R build-contract evidence. In particular, the previously inferred eight-byte default-real and SAVE-style local-storage hypotheses now have a direct project-file basis for this received project artifact.

## Project/source-set relation

The received project contains 63 file members. The frozen supplied source directory contains 65 top-level files. Case-normalized comparison gives:

- no project member absent from the frozen source directory;
- `input1_1.for` and `Outselorg.for` are present in the frozen source directory but absent from the project;
- no source reference to either filename was found in the frozen source scan used for this intake.

Therefore presence in the ZIP cannot be treated as proof that those two files belonged to the compiled executable. The project file gives a narrower candidate compilation set.

This is compilation-set evidence only. It does not prove that the received project is the original project used for revision 53, nor that the frozen source bytes exactly generated the received executable.

## Executable lineage evidence

Static PE/debug inspection of the received executable gives:

- PE32+ x86-64 console executable;
- PE timestamp: `2026-05-27 13:41:28 UTC`;
- linker version `14.35`;
- RSDS CodeView record with PDB path `D:\USR\5200048928_SWAP_ANIMO\ANIMO\x64\Debug\animo41.pdb`;
- embedded Intel Fortran runtime catalog string `V20.0-001 Jan 10 2019`;
- embedded compiler/debug source paths rooted at `D:\USR\5200048928_SWAP_ANIMO\ANIMO\src_develop_for_20260519\`;
- embedded ANIMO SVN tag string `file:///V:/svn_Animo/tags/animo4.1.5`.

The frozen `Version.inc` contains the static string `Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`. That string is also available to the built program as source metadata, but it is not reliable evidence of the compiler that actually produced this executable. The 2026 PE timestamp, `src_develop_for_20260519` debug path, linker 14.35 and 2019 Intel RTL catalog jointly contradict treating the static 2011 compiler string as actual build provenance.

The executable is therefore classified as:

`RECENT_2026_NATIVE_REBUILD_CANDIDATE_NOT_HISTORICAL_REFERENCE`

This is a positive lineage result, not merely absence of evidence. The executable has direct evidence of a 2026 build.

## Configuration match

The executable is strongly consistent with the received project's `Debug|x64` configuration because:

1. the PE machine is x86-64;
2. its CodeView path contains `x64\Debug`;
3. debug information and a PDB reference are present.

This does not prove that these exact `vfproj` bytes generated the executable. The PDB and build log are absent, and executable inspection cannot establish identity of every compiled source byte.

## Consequence for existing build-contract gaps

### TCD-010 default REAL kind

The received project sets `RealKIND=realKIND8` in all configurations. This is direct build-configuration evidence and is consistent with the existing successful eight-byte GNU diagnostic contract. It substantially narrows the TCD-010 build-contract uncertainty.

It does **not** create B2. Original historical project provenance remains unqualified.

### TCD-011 local storage duration

The received project sets `LocalVariableStorage=localStorageSave` in all configurations. `Debug|x64` additionally zero-initializes saved scalars. This is stronger than the earlier inference that Intel local retention might explain `Outbal_write` CHARACTER reuse. SAVE-style storage is explicitly configured in this project artifact.

Again, this does not establish historical fidelity by itself.

### TCD-004 build environment

The missing-project question is materially narrowed: a Visual Studio 2010-format Intel Fortran/CVF-compatible project has now been received. However, the paired executable demonstrates that old-format project metadata can participate in a much later rebuild. Project format and static `Version.inc` strings therefore cannot substitute for exact build provenance.

## Reference and execution disposition

This intake does not admit:

- a historical revision-53 executable;
- a B2 reference;
- a native historical comparison;
- an equivalent reference build;
- any corrected-legacy behaviour;
- production migration.

The received executable may be useful in a later, separately approved native-reconstruction experiment. If such execution is opened, `RuurloGrass` remains the preferred first frozen case and no silent input translation is allowed. Its outputs would be reconstruction evidence, not independent historical truth.

Historical B2 recovery therefore remains open. A provenance-qualified historical 4.1.x executable, original build/archive evidence, or executable-linked historical outputs would still materially improve the evidence base.
